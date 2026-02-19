import customtkinter as ctk
import os
import sys
from tkinter import messagebox

# Ajuste de caminhos para imports (MVC)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *
# from controllers.projeto_controller import ProjetoController

class ProjetosDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master, id_turma, nome_turma, tipo_usuario, controller):
        super().__init__(master)
        self.janela = master
        self.id_turma = id_turma
        self.nome_turma = nome_turma
        self.controller = controller
        
        self.configure(fg_color="#f0f2f5") 
        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        # Header simples apenas com o título da turma
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=70, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text=f"Projetos da Turma: {self.nome_turma}",
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=Branco).pack(side="left", padx=30)

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)
        self.carregar_projetos()

    def carregar_projetos(self):
        # Limpa a tela antes de carregar
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        projetos = self.controller.listar_projetos(self.id_turma)
        print(f"DEBUG: Projetos encontrados -> {projetos}")
        
        if not projetos:
            ctk.CTkLabel(self.main_scroll, text="Nenhum projeto encontrado para esta turma.",
                        font=ctk.CTkFont(size=14)).pack(pady=20)
            return

        for p in projetos:
            self.criar_card_projeto(p)

    def criar_card_projeto(self, projeto):
        card = ctk.CTkFrame(self.main_scroll, fg_color=Branco, corner_radius=12, height=100)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)

        # Informações do Projeto (Esquerda)
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(info_frame, text=projeto["nome_projeto"], 
                    font=ctk.CTkFont(size=16, weight="bold"), text_color="#1e293b").pack(anchor="w")
        
        ctk.CTkLabel(info_frame, text=f"Criado em: {projeto['data']}", 
                    font=ctk.CTkFont(size=12), text_color="#64748b").pack(anchor="w")

        # Botão Acessar (Direita)
        ctk.CTkButton(card, text="📂 Abrir Repositório", width=150, height=35,
                      fg_color=azulEscuro, hover_color="#2c3e50",
                      command=lambda p=projeto: self.abrir_repositorio(p)).pack(side="right", padx=20)

    def abrir_repositorio(self, projeto):
        try:
            from views.Aluno_e_Professor.repositorio_view import RepositorioDashboard
            
            self.pack_forget() 
            
            # O erro estava aqui: os nomes devem ser 'turma_id' e 'nome_projeto'
            # conforme definido no __init__ do RepositorioDashboard
            tela_repo = RepositorioDashboard(
                master=self.janela, 
                turma_id=self.id_turma,      # Passando o ID da turma
                pasta_id=None,               # Começa na raiz (None)
                nome_projeto=projeto["nome_projeto"]
            )
            tela_repo.pack(side="right", fill="both", expand=True)
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Erro ao abrir repositório: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x700")
    # app = ProjetosDesktopDashboard(root, 1, "Dev 2024", "Professor")
    root.mainloop()