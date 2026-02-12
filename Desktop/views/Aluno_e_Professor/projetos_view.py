import customtkinter as ctk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *


class ProjetosDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.configure(fg_color="#f0f2f5") 
        
        # Mock de dados dos projetos
        self.projetos = [
            {"id": 1, "nome": "E-commerce Python", "desc": "Plataforma de vendas com integração Django e Stripe."},
            {"id": 2, "nome": "App de Gestão de Resíduos", "desc": "Sistema mobile para controle de coleta seletiva urbana."},
            {"id": 3, "nome": "Dashboard Logístico", "desc": "Visualização de frotas e rotas em tempo real."},
        ]

        # Simulação da lista de usuários para o modal
        self.usuarios_turma = [
            {"id": 1, "nome": "Ana Silva", "cargo": "Desenvolvedora", "status": True},
            {"id": 2, "nome": "Bruno Souza", "cargo": "Designer", "status": False},
            {"id": 3, "nome": "Carla Lima", "cargo": "PO", "status": True},
        ]

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
        # Header Superior (Seguindo seu padrão)
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Projetos da Turma",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color=Branco).pack(side="left", padx=30)

        # Botão de Cadastrar no Header
        self.btn_cadastrar = ctk.CTkButton(header, text="+ Novo Projeto", text_color=azulEscuro,
                                           fg_color="#ffffff", hover_color="#e2e8f0",
                                           font=ctk.CTkFont(size=13, weight="bold"),
                                           width=140, height=35)
        self.btn_cadastrar.pack(side="right", padx=30)

        # Área de Conteúdo
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)

        # Renderizar lista de projetos (Full Width)
        for projeto in self.projetos:
            self.criar_card_projeto(projeto)

    def criar_card_projeto(self, projeto):
        # Card ocupando a largura total
        card = ctk.CTkFrame(self.main_scroll, fg_color=Branco, corner_radius=12, 
                            border_width=1, border_color="#e2e8f0", height=100)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)

        # Faixa lateral azul (Acentuação)
        accent = ctk.CTkFrame(card, width=6, fg_color="#3b82f6", corner_radius=0)
        accent.pack(side="left", fill="y")

        # Conteúdo Textual
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(info_frame, text=projeto["nome"], 
                    font=ctk.CTkFont(size=18, weight="bold"), 
                    text_color="#1e293b").pack(anchor="w")
        
        ctk.CTkLabel(info_frame, text=projeto["desc"], 
                    font=ctk.CTkFont(size=13), 
                    text_color="#64748b").pack(anchor="w")

        # Container de Botões (Lado Direito)
        btn_container = ctk.CTkFrame(card, fg_color="transparent")
        btn_container.pack(side="right", padx=20)

        # Botão Repositório
        ctk.CTkButton(btn_container, text="📂 Repositório", width=110, height=32,
                      fg_color="#f1f5f9", text_color="#475569", hover_color="#e2e8f0",
                      command=lambda: self.abrir_repositorio(),
                      font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)

        # Botão Permissões (Abre o Modal)
        ctk.CTkButton(btn_container, text="🔐 Permissões", width=110, height=32,
                      fg_color="#3b82f6", hover_color="#2563eb",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=lambda p=projeto: self.abrir_modal_permissoes(p)).pack(side="left", padx=5)

        # Botão Excluir
        ctk.CTkButton(btn_container, text="🗑", width=35, height=32,
                      fg_color="#fee2e2", text_color="#ef4444", hover_color="#fecaca",
                      command=lambda p=projeto: print(f"Deletar {p['nome']}")).pack(side="left", padx=5)
        
    def abrir_repositorio(self, projeto=None):
        try:
            from views.Aluno_e_Professor.repositorio_view import RepositorioDashboard
            
            self.pack_forget()
            
            tela_repositorio = RepositorioDashboard(self.janela)
            tela_repositorio.pack(side="right", fill="both", expand=True)
            
        except ImportError as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Não foi possível carregar a tela de repositório.\n{e}")

    def abrir_modal_permissoes(self, projeto):
        modal = ModalPermissoes(self.janela, projeto)

# ==========================================
# CLASSE DO MODAL (ESTRUTURA DE CHECKLIST)
# ==========================================
class ModalPermissoes(ctk.CTkToplevel):
    def __init__(self, master, projeto):
        super().__init__(master)
        self.title(f"Permissões - {projeto['nome']}")
        self.geometry("500x550")
        self.configure(fg_color="#ffffff")
        self.grab_set() # Foca no modal
        
        # Header do Modal
        ctk.CTkLabel(self, text="Gerenciar Acessos", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text=projeto["nome"], text_color="#3b82f6").pack(pady=(0, 20))

        # Container da Tabela de Checklist
        table_container = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=10, border_width=1, border_color="#e2e8f0")
        table_container.pack(fill="both", expand=True, padx=25, pady=10)

        # Cabeçalho da Tabela
        header_table = ctk.CTkFrame(table_container, fg_color="#f1f5f9", height=40, corner_radius=8)
        header_table.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_table, text="Nome do Membro", font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569").pack(side="left", padx=15)
        ctk.CTkLabel(header_table, text="Autorizar", font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569").pack(side="right", padx=15)

        # Área de Rolagem dos Alunos
        self.scroll_alunos = ctk.CTkScrollableFrame(table_container, fg_color="transparent")
        self.scroll_alunos.pack(fill="both", expand=True, padx=5, pady=5)

        # Simulando os alunos (Aqui você usaria os dados do seu banco)
        alunos_mock = [
            {"nome": "Ana Souza", "cargo": "Líder"},
            {"nome": "Carlos Roberto", "cargo": "Dev"},
            {"nome": "Felipe Neto", "cargo": "Designer"},
            {"nome": "Beatriz Matos", "cargo": "Dev"},
        ]

        for aluno in alunos_mock:
            row = ctk.CTkFrame(self.scroll_alunos, fg_color="transparent")
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(row, text=f"{aluno['nome']} ({aluno['cargo']})", 
                         font=ctk.CTkFont(size=13), text_color="#1e293b").pack(side="left", padx=10)
            
            ctk.CTkCheckBox(row, text="", width=20, border_width=2, fg_color="#3b82f6").pack(side="right", padx=15)
            
            # Linha divisória sutil
            ctk.CTkFrame(self.scroll_alunos, height=1, fg_color="#f1f5f9").pack(fill="x", padx=10)

        # Botão Salvar
        ctk.CTkButton(self, text="Salvar Alterações", fg_color="#3b82f6", hover_color="#2563eb",
                      height=40, font=ctk.CTkFont(size=13, weight="bold"),
                      command=self.destroy).pack(pady=20)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x700")
    root.attributes("-fullscreen", True)
    app = ProjetosDesktopDashboard(root)
    root.mainloop()