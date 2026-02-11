import customtkinter as ctk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *

class TurmasDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.configure(fg_color="#f0f2f5") # Fundo estilo software corporativo
        
        # Dados estruturados com a cor padronizada #3b82f6
        self.turmas_por_ano = {
            "2027": [
                {"cod": "DS1-A", "turno": "Manhã", "alunos": 32, "cor": "#3b82f6"},
                {"cod": "DS1-B", "turno": "Tarde", "alunos": 28, "cor": "#3b82f6"},
            ],
            "2026": [
                {"cod": "DS2-A", "turno": "Manhã", "alunos": 30, "cor": "#3b82f6"},
            ],
            "2025": [
                {"cod": "DS3-A", "turno": "Integral", "alunos": 25, "cor": "#3b82f6"},
            ]
        }
        
        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        # Header Superior fixo
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Gestão de Turmas", 
                     font=ctk.CTkFont(size=24, weight="bold"), 
                     text_color=Branco).pack(side="left", padx=30)

        # Barra de Pesquisa
        self.entry_busca = ctk.CTkEntry(header, placeholder_text="Pesquisar turma...", width=300, height=35)
        self.entry_busca.pack(side="right", padx=30)

        # Área de Conteúdo com Scroll
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        # Gerar Seções por Ano
        for ano, turmas in self.turmas_por_ano.items():
            self.renderizar_secao(ano, turmas)

    def renderizar_secao(self, ano, turmas):
        # Container da Seção (Ano)
        section_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section_container.pack(fill="x", pady=(10, 20))

        # Título da Seção com Linha
        title_frame = ctk.CTkFrame(section_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(title_frame, text=f"Ano Letivo {ano}", font=ctk.CTkFont(size=18, weight="bold"), 
                     text_color="#64748b").pack(side="left", padx=10)
        
        ctk.CTkFrame(title_frame, height=2, fg_color="#e2e8f0").pack(side="left", fill="x", expand=True, padx=10)

        # Grid para os Cards
        grid_container = ctk.CTkFrame(section_container, fg_color="transparent")
        grid_container.pack(fill="x")
        
        for i, turma in enumerate(turmas):
            self.criar_card_turma(grid_container, turma, i)

    def criar_card_turma(self, master, turma, col):
        # Card principal - Aumentei um pouco a altura para caber os botões novos
        card = ctk.CTkFrame(master, fg_color="#ffffff", width=300, height=200, corner_radius=15, 
                            border_width=1, border_color="#e2e8f0")
        card.grid(row=0, column=col, padx=10, pady=10)
        card.pack_propagate(False)

        # Faixa lateral de cor fixa
        accent = ctk.CTkFrame(card, width=6, fg_color=turma["cor"], corner_radius=0)
        accent.pack(side="left", fill="y")

        # Conteúdo do Card
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(content, text=turma["cod"], font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color="#1e293b").pack(anchor="w")
        
        ctk.CTkLabel(content, text=f"Turno: {turma['turno']}", font=ctk.CTkFont(size=13), 
                     text_color="#64748b").pack(anchor="w")

        ctk.CTkLabel(content, text=f"👥 {turma['alunos']} Alunos matriculados", font=ctk.CTkFont(size=12), 
                     text_color="#94a3b8").pack(anchor="w", pady=(10, 0))

        # --- CONTAINER DE BOTÕES (RODAPÉ DO CARD) ---
        button_row = ctk.CTkFrame(content, fg_color="transparent")
        button_row.pack(side="bottom", fill="x", pady=(10, 0))

        # Botão Usuários (Novo)
        btn_usuarios = ctk.CTkButton(button_row, text="Usuários", height=32, width=100,
                                     fg_color="#f1f5f9", text_color="#475569", hover_color="#e2e8f0",
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     command=lambda: print(f"Lista de usuários: {turma['cod']}"))
        btn_usuarios.pack(side="left", expand=True, padx=(0, 5))

        # Botão Gerenciar
        btn_gerenciar = ctk.CTkButton(button_row, text="Projetos", height=32, width=100,
                                      fg_color="#3b82f6", text_color="#ffffff", hover_color="#2563eb",
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      command=lambda: print(f"Gerenciar: {turma['cod']}"))
        btn_gerenciar.pack(side="left", expand=True, padx=(5, 0))

if __name__ == "__main__":
    ctk.set_appearance_mode("light") # Garante o visual claro corporativo
    root = ctk.CTk()
    root.geometry("1150x750")
    root.title("Inova Edu - Desktop Admin")
    app = TurmasDesktopDashboard(root)
    root.mainloop()