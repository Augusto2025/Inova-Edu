import customtkinter as ctk
import os
import sys
from tkinter import messagebox

# Ajuste de caminhos para imports (MVC)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *
from controllers.projeto_controller import ProjetoController

class ProjetosDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master, id_turma, nome_turma, tipo_usuario):
        super().__init__(master)
        self.janela = master
        self.id_turma = id_turma
        self.nome_turma = nome_turma
        
        # NORMALIZAÇÃO CRÍTICA: Força a comparação correta independente de como vem do banco
        self.tipo_usuario = str(tipo_usuario).strip().capitalize()
        
        self.configure(fg_color="#f0f2f5") 
        
        self.controller = ProjetoController()
        self.projetos = self.controller.listar_projetos(self.id_turma)

        # Garantir Sidebar
        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break
        if not sidebar_existente:
            sidebar(self.janela)

        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text=f"Projetos | {self.nome_turma}",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color=Branco).pack(side="left", padx=30)

        # Botão "+ Novo" - SÓ PROFESSOR
        if self.tipo_usuario == "Professor":
            self.btn_cadastrar = ctk.CTkButton(header, text="+ Novo Projeto", text_color=azulEscuro,
                                               fg_color="#ffffff", hover_color="#e2e8f0",
                                               font=ctk.CTkFont(size=13, weight="bold"),
                                               width=140, height=35,
                                               command=self.abrir_modal_cadastro)
            self.btn_cadastrar.pack(side="right", padx=30)

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)

        self.atualizar_lista_projetos()

    def atualizar_lista_projetos(self):
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        if not self.projetos:
            ctk.CTkLabel(self.main_scroll, text="Nenhum projeto cadastrado nesta turma.", 
                         font=ctk.CTkFont(size=14), text_color="#64748b").pack(pady=50)
            return

        for projeto in self.projetos:
            self.criar_card_projeto(projeto)

    def criar_card_projeto(self, projeto):
        card = ctk.CTkFrame(self.main_scroll, fg_color=Branco, corner_radius=12, 
                            border_width=1, border_color="#e2e8f0", height=100)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)

        ctk.CTkFrame(card, width=6, fg_color="#3b82f6", corner_radius=0).pack(side="left", fill="y")

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(info_frame, text=projeto["nome"], 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#1e293b").pack(anchor="w")
        
        subtexto = f"Ref: {projeto['caminho']}" if projeto.get('caminho') else "Sem descrição"
        ctk.CTkLabel(info_frame, text=subtexto, font=ctk.CTkFont(size=13), text_color="#64748b").pack(anchor="w")

        btn_container = ctk.CTkFrame(card, fg_color="transparent")
        btn_container.pack(side="right", padx=20)

        # ACESSAR (Geral)
        ctk.CTkButton(btn_container, text="📂 Acessar", width=100, height=32,
                      fg_color="#f1f5f9", text_color="#475569", hover_color="#e2e8f0",
                      command=lambda p=projeto: self.abrir_repositorio(p),
                      font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)

        # RESTRITOS (Apenas se for exatamente "Professor")
        if self.tipo_usuario == "Professor":
            ctk.CTkButton(btn_container, text="🔐 Permissões", width=110, height=32,
                          fg_color="#3b82f6", hover_color="#2563eb",
                          font=ctk.CTkFont(size=12, weight="bold"),
                          command=lambda p=projeto: self.abrir_modal_permissoes(p)).pack(side="left", padx=5)

            ctk.CTkButton(btn_container, text="🗑", width=35, height=32,
                          fg_color="#fee2e2", text_color="#ef4444", hover_color="#fecaca",
                          command=lambda p=projeto: self.confirmar_exclusao(p)).pack(side="left", padx=5)

    def abrir_repositorio(self, projeto):
        try:
            from views.Aluno_e_Professor.repositorio_view import RepositorioDashboard
            self.pack_forget()
            tela_repo = RepositorioDashboard(self.janela)
            tela_repo.pack(side="right", fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Repositório indisponível: {e}")

    def confirmar_exclusao(self, projeto):
        if messagebox.askyesno("Confirmar", f"Excluir '{projeto['nome']}'?"):
            if self.controller.excluir_projeto(projeto["id"]):
                self.projetos = self.controller.listar_projetos(self.id_turma)
                self.atualizar_lista_projetos()

    def abrir_modal_permissoes(self, projeto):
        # PROTEÇÃO CONTRA O ERRO DE ATTRIBUTE:
        # Se o seu controller ainda não tem essa função, vamos usar uma lista segura para não travar
        try:
            membros = self.controller.listar_membros_permissao(self.id_turma)
        except AttributeError:
            # Caso a função não exista no controller, exibe aviso e não trava
            messagebox.showwarning("Aviso", "O Controller ainda não possui a função 'listar_membros_permissao'.")
            return
            
        ModalPermissoes(self.janela, projeto, membros)

    def abrir_modal_cadastro(self):
        messagebox.showinfo("Inova Edu", "Modal de cadastro em breve.")

# ==========================================
# MODAL DE PERMISSÕES
# ==========================================
class ModalPermissoes(ctk.CTkToplevel):
    def __init__(self, master, projeto, membros):
        super().__init__(master)
        self.title(f"Permissões - {projeto['nome']}")
        self.geometry("500x550")
        self.configure(fg_color="#ffffff")
        self.grab_set() 
        
        ctk.CTkLabel(self, text="Gerenciar Acessos", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text=f"Projeto: {projeto['nome']}", text_color="#3b82f6").pack(pady=(0, 20))

        table_container = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=10, border_width=1, border_color="#e2e8f0")
        table_container.pack(fill="both", expand=True, padx=25, pady=10)

        # Cabeçalho da lista
        h = ctk.CTkFrame(table_container, fg_color="#f1f5f9", height=40)
        h.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(h, text="Nome do Aluno", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=15)
        ctk.CTkLabel(h, text="Pode Editar?", font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", padx=15)

        self.scroll = ctk.CTkScrollableFrame(table_container, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Popula o checklist com os membros
        for membro in membros:
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(row, text=f"{membro.get('nome', 'Sem Nome')} ({membro.get('cargo', 'Aluno')})", 
                         font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
            
            # Aqui você pode salvar o estado do checkbox se desejar
            ctk.CTkCheckBox(row, text="", width=20, fg_color="#3b82f6").pack(side="right", padx=15)
            
            ctk.CTkFrame(self.scroll, height=1, fg_color="#f1f5f9").pack(fill="x", padx=10)

        ctk.CTkButton(self, text="Salvar Permissões", fg_color="#3b82f6", height=40,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=self.destroy).pack(pady=20)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x700")
    app = ProjetosDesktopDashboard(root, 1, "Dev 2024", "Professor")
    root.mainloop()