import customtkinter as ctk
from tkinter import messagebox
from sidebar_C import sidebar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ListaTurmasApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1300x650")
        self.app.title("Sistema de Gestão")
        # self.app.attributes("-fullscreen", True)

        # GRID PRINCIPAL
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=1)

        # SIDEBAR (estrutura que FUNCIONA)
        self.sidebar_frame, self.botoes_menu = sidebar(self.app)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        # CONTEÚDO
        self.conteudo_frame = ctk.CTkFrame(self.app, fg_color="#ffffff", corner_radius=0)
        self.conteudo_frame.grid(row=0, column=1, sticky="nsew")
        self.conteudo_frame.grid_columnconfigure(0, weight=1)
        self.conteudo_frame.grid_rowconfigure(1, weight=1)

        # TOPO (NÃO ALTERADO)
        self.criar_topo()

        # DADOS
        self.turmas = [
            ("2025.10.111", "Manhã", "2025", "Desenvolvimento de sistemas", "30", "🔒"),
            ("2025.02.001", "Tarde", "2025", "Administrador de Banco de dados", "25", "🔒"),
            ("2025.10.201", "Noite", "2025", "Administrador de Redes", "20", "🔒"),
            ("2025.12.115", "Manhã", "2024", "IT Essentials", "15", "🔒"),
            ("2025.05.210", "Tarde", "2024", "Programação Web", "28", "🔒"),
            ("2024.09.001", "Noite", "2024", "Segurança da Informação", "22", "🔒"),
        ]

        # CARDS ABAIXO DO TOPO
        self.criar_cards()

        self.app.mainloop()

    # ───────────── TOPO (IGUAL AO SEU) ─────────────
    def criar_topo(self):
        topo = ctk.CTkFrame(self.conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
        topo.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            topo,
            text="👥 LISTA DE TURMAS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

    # ───────────── CARDS ─────────────
    def criar_cards(self):
        corpo = ctk.CTkScrollableFrame(self.conteudo_frame, fg_color="#ffffff")
        corpo.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        for turma in self.turmas:
            card = ctk.CTkFrame(
                corpo,
                fg_color="#ffffff",
                corner_radius=12,
                border_width=1,
                border_color="#e0e0e0"
            )
            card.pack(fill="x", pady=10)

            # TÍTULO
            ctk.CTkLabel(
                card,
                text=f"{turma[0]} • {turma[3]}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#004a8f"
            ).pack(anchor="w", padx=20, pady=(15, 5))

            # INFOS
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(anchor="w", padx=20)

            ctk.CTkLabel(info, text=f"🕒 Turno: {turma[1]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"📅 Ano: {turma[2]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"👥 Usuários: {turma[4]}").pack(anchor="w")

            # AÇÕES
            acoes = ctk.CTkFrame(card, fg_color="transparent")
            acoes.pack(anchor="e", padx=20, pady=15)

            ctk.CTkButton(
                acoes,
                text="✏️ Editar",
                width=110,
                fg_color="#ffc107",
                hover_color="#e0a800",
                text_color="#212529",
                command=lambda t=turma: self.editar_turma(t)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes,
                text="🗑️ Excluir",
                width=110,
                fg_color="#dc3545",
                hover_color="#b52a37",
                command=lambda t=turma: self.excluir_turma(t)
            ).pack(side="left", padx=5)

    def editar_turma(self, turma):
        messagebox.showinfo("Editar", f"Editar turma {turma[0]}")

    def excluir_turma(self, turma):
        messagebox.showwarning("Excluir", f"Excluir turma {turma[0]}?")


if __name__ == "__main__":
    ListaTurmasApp()
