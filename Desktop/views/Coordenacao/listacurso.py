import customtkinter as ctk
from tkinter import messagebox
from Desktop.views.Coordenacao.sidebar_C import sidebar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CursosView:
    def __init__(self, master):
        self.master = master

        # ───────────── DADOS DOS CURSOS ─────────────
        self.cursos = [
            ("Desenvolvimento de Sistemas", "Manhã", "2025", "💻", 32),
            ("Banco de Dados", "Tarde", "2025", "🗄️", 28),
            ("Redes de Computadores", "Noite", "2024", "🌐", 25),
            ("Programação Web", "Manhã", "2025", "🕸️", 30),
        ]

        # VARIÁVEIS DA BUSCA E FILTRO
        self.busca_var = ctk.StringVar()
        self.filtro_turno = ctk.StringVar(value="Todos")

        self.montar_tela()

    # ───────────── TELA ─────────────
    def montar_tela(self):
        self.container = ctk.CTkFrame(self.master)
        self.container.pack(fill="both", expand=True)

        sidebar_frame, _ = sidebar(self.container)

        self.conteudo = ctk.CTkFrame(self.container, fg_color="#f5f6fa")
        self.conteudo.pack(side="left", fill="both", expand=True)

        # TOPO
        topo = ctk.CTkFrame(self.conteudo, height=60, fg_color="#004a8f", corner_radius=0)
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo,
            text="📚  LISTA DE CURSOS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        # ───────────── BARRA DE AÇÕES ─────────────
        acoes = ctk.CTkFrame(self.conteudo, fg_color="#f5f6fa")
        acoes.pack(fill="x", padx=20, pady=(15, 0))

        acoes.grid_columnconfigure(0, weight=1)
        acoes.grid_columnconfigure(1, weight=1)

        # BUSCA (ESQUERDA)
        busca = ctk.CTkEntry(
            acoes,
            placeholder_text="Buscar curso...",
            width=250,
            textvariable=self.busca_var
        )
        busca.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        busca.bind("<KeyRelease>", self.aplicar_filtro)

        # FILTRO (DIREITA)
        filtro_frame = ctk.CTkFrame(acoes, fg_color="transparent")
        filtro_frame.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        ctk.CTkLabel(
            filtro_frame,
            text="Turno:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 8))

        for turno in ["Todos", "Manhã", "Tarde", "Noite"]:
            ctk.CTkRadioButton(
                filtro_frame,
                text=turno,
                variable=self.filtro_turno,
                value=turno,
                command=self.aplicar_filtro
            ).pack(side="left", padx=5)

        # ÁREA DOS CARDS
        self.tabela = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)

        self.carregar_tabela(self.cursos)

    # ───────────── CARD (IGUAL AO DA TURMA) ─────────────
    def carregar_tabela(self, lista_cursos):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        for curso in lista_cursos:
            card = ctk.CTkFrame(
                self.tabela,
                fg_color="#ffffff",
                corner_radius=15,
                border_width=1,
                border_color="#e0e0e0"
            )
            card.pack(fill="x", padx=30, pady=12)

            conteudo = ctk.CTkFrame(card, fg_color="transparent")
            conteudo.pack(fill="both", expand=True, padx=20, pady=15)

            # TÍTULO
            ctk.CTkLabel(
                conteudo,
                text=f"{curso[0]}  •  {curso[3]}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#004a8f"
            ).pack(anchor="w", pady=(0, 6))

            info = ctk.CTkFrame(conteudo, fg_color="transparent")
            info.pack(anchor="w")

            ctk.CTkLabel(info, text=f"🕒 Turno: {curso[1]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"📅 Ano: {curso[2]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"👥 Alunos: {curso[4]}").pack(anchor="w")

            ctk.CTkFrame(conteudo, height=1, fg_color="#eeeeee").pack(fill="x", pady=10)

            # AÇÕES
            acoes = ctk.CTkFrame(conteudo, fg_color="transparent")
            acoes.pack(anchor="e")

            ctk.CTkButton(
                acoes,
                text="🔒 Visualizar",
                width=120,
                fg_color="#004a8f",
                hover_color="#003366",
                command=lambda c=curso: self.visualizar_curso(c)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes,
                text="✏️ Editar",
                width=100,
                fg_color="#ffc107",
                hover_color="#e0a800",
                text_color="#212529",
                command=lambda c=curso: self.editar_curso(c)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes,
                text="🗑️ Excluir",
                width=100,
                fg_color="#dc3545",
                hover_color="#b52a37",
                command=lambda c=curso: self.excluir_curso(c)
            ).pack(side="left", padx=5)

    # ───────────── FILTRO ─────────────
    def aplicar_filtro(self, event=None):
        texto = self.busca_var.get().lower()
        turno = self.filtro_turno.get()

        filtrados = []
        for curso in self.cursos:
            bate_texto = texto in curso[0].lower()
            bate_turno = turno == "Todos" or curso[1] == turno

            if bate_texto and bate_turno:
                filtrados.append(curso)

        self.carregar_tabela(filtrados)

    # ───────────── AÇÕES ─────────────
    def visualizar_curso(self, curso):
        messagebox.showinfo("Curso", f"Curso: {curso[0]}")

    def editar_curso(self, curso):
        messagebox.showinfo("Editar", f"Editar curso: {curso[0]}")

    def excluir_curso(self, curso):
        messagebox.showwarning("Excluir", f"Excluir curso: {curso[0]}")


# ───────────── APP ─────────────
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Sistema de Gestão")
    app.attributes("-fullscreen", True)

    CursosView(app)

    app.mainloop()
