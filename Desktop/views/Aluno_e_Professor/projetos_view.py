import customtkinter as ctk
import os
import sys
from tkinter import messagebox

# Ajuste de caminhos para imports (MVC)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *
from controllers.projeto_controller import ProjetoController

class ProjetosDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master, id_turma, nome_turma, tipo_usuario, controller):
        super().__init__(master)
        self.janela = master
        self.id_turma = id_turma
        self.nome_turma = nome_turma
        self.tipo_usuario = str(tipo_usuario).strip().capitalize()
        self.controller = controller
        
        self.configure(fg_color="#f0f2f5") 
        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text=f"Projetos | {self.nome_turma}",
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color=Branco).pack(side="left", padx=30)

        # Apenas Professor pode cadastrar novos projetos
        if self.tipo_usuario == "Professor":
            ctk.CTkButton(header, text="+ Novo Projeto", fg_color="#ffffff", text_color=azulEscuro,
                          hover_color="#e2e8f0", width=140, height=35,
                          font=ctk.CTkFont(size=13, weight="bold"),
                          command=self.abrir_modal_cadastro).pack(side="right", padx=30)

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)
        self.carregar_projetos()

    def carregar_projetos(self):
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        projetos = self.controller.listar_projetos(self.id_turma)
        for p in projetos:
            self.criar_card_projeto(p)

    def criar_card_projeto(self, projeto):
        card = ctk.CTkFrame(self.main_scroll, fg_color=Branco, corner_radius=12, height=100)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(info_frame, text=projeto["nome_projeto"], 
                    font=ctk.CTkFont(size=16, weight="bold"), text_color="#1e293b").pack(anchor="w")
        
        # Botões de Ação
        btn_container = ctk.CTkFrame(card, fg_color="transparent")
        btn_container.pack(side="right", padx=20)

        # Botão Acessar (Para todos)
        ctk.CTkButton(btn_container, text="📂 Repositório", width=100, height=32,
                      command=lambda: print("Acessar Repositório")).pack(side="left", padx=5)

        # Botões Restritos ao Professor
        if self.tipo_usuario == "Professor":
            ctk.CTkButton(btn_container, text="🔐 Permissões", width=100, height=32, fg_color="#3b82f6",
                          command=lambda p=projeto: self.abrir_modal_permissoes(p)).pack(side="left", padx=5)
            
            ctk.CTkButton(btn_container, text="🗑", width=35, height=32, fg_color="#fee2e2", text_color="#ef4444",
                          command=lambda p=projeto: self.excluir(p)).pack(side="left", padx=5)

    def abrir_modal_permissoes(self, projeto):
        # Busca alunos da turma e o status de quem pode editar esse projeto no MySQL
        membros = self.controller.obter_membros_com_status_edicao(projeto['idprojeto'], self.id_turma)
        ModalPermissoes(self, projeto, membros, self.controller)

    def abrir_modal_cadastro(self):
        # Lógica de cadastro (Omitida por brevidade, mas segue o mesmo padrão)
        pass

    def excluir(self, projeto):
        if messagebox.askyesno("Confirmar", f"Excluir {projeto['nome_projeto']}?"):
            self.controller.excluir_projeto(projeto['idprojeto'])
            self.carregar_projetos()

# ==========================================
# MODAL DE CHECKLIST (Permissões MySQL)
# ==========================================
class ModalPermissoes(ctk.CTkToplevel):
    def __init__(self, parent, projeto, membros, controller):
        super().__init__(parent)
        self.projeto = projeto
        self.controller = controller
        self.widgets_checklist = {}

        self.title("Permissões de Edição")
        self.geometry("400x500")
        self.grab_set()

        ctk.CTkLabel(self, text=f"Quem pode editar:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        for m in membros:
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            cb = ctk.CTkCheckBox(row, text=m['nome_usuario'])
            if m['pode_editar']: # Se o MySQL retornou que já tem permissão
                cb.select()
            cb.pack(side="left", padx=10)
            
            self.widgets_checklist[m['id_usuario']] = cb

        ctk.CTkButton(self, text="Salvar Acessos", fg_color="#10b981", 
                      command=self.salvar).pack(pady=20)

    def salvar(self):
        # 1. Pega os IDs de quem está com o checkbox marcado (valor 1 ou True)
        ids_selecionados = [id_usr for id_usr, cb in self.widgets_checklist.items() if cb.get()]
        
        # 2. Envia para o controller
        if self.controller.atualizar_acessos(self.projeto['idprojeto'], ids_selecionados):
            messagebox.showinfo("Sucesso", "Permissões atualizadas no MySQL!")
            self.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar as permissões.")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x700")
    app = ProjetosDesktopDashboard(root, 1, "Dev 2024", "Professor")
    root.mainloop()