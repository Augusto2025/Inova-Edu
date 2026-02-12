import customtkinter as ctk
from tkinter import messagebox
from sidebar_C import sidebar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ListaTurmasApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1300x650")
        self.app.title("Sistema de Gestão de Turmas")
        self.app.attributes("-fullscreen", True)

        # ───────────── DADOS DAS TURMAS ─────────────
        self.turmas = [
            ("2025.10.111", "Manhã", "2025", "Desenvolvimento de sistemas", "📌", "🔒"),
            ("2025.02.001", "Tarde", "0", "Administrador de Banco de dados", "📌", "🔒"),
            ("2025.10.201", "Noite", "0", "Administrador de Redes", "📌", "🔒"),
            ("2025.12.115", "Manhã", "0", "IT Essentials", "📌", "🔒"),
            ("2025.05.210", "Tarde", "0", "Programação Web", "📌", "🔒"),
            ("2024.09.001", "Noite", "0", "Segurança da Informação", "📌", "🔒"),
            ("2025.06.300", "Manhã", "0", "Design Gráfico", "📌", "🔒"),
            ("2025.07.101", "Noite", "0", "Engenharia de Software", "📌", "🔒"),
            ("2025.10.111", "Manhã", "0", "Desenvolvimento de sistemas", "📌", "🔒"),
            ("2025.10.201", "Noite", "0", "Administrador de Redes", "📌", "🔒"),
            ("2025.12.115", "Manhã", "0", "IT Essentials", "📌", "🔒"),
            ("2025.05.210", "Tarde", "0", "Programação Web", "📌", "🔒"),
            ("2024.09.001", "Noite", "0", "Segurança da Informação", "📌", "🔒"),
        ]

        self.montar_layout()
        self.carregar_tabela(self.turmas)

        self.app.mainloop()

    # ───────────── FUNÇÕES ─────────────
    def carregar_tabela(self, lista_turmas):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        for turma in lista_turmas:
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

            ctk.CTkLabel(
                conteudo,
                text=f"{turma[0]}  •  {turma[3]}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#004a8f"
            ).pack(anchor="w", pady=(0, 6))

            info = ctk.CTkFrame(conteudo, fg_color="transparent")
            info.pack(anchor="w")

            ctk.CTkLabel(info, text=f"🕒 Turno: {turma[1]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"📅 Ano: {turma[2]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"👥 Usuários: {turma[4]}").pack(anchor="w")

            ctk.CTkFrame(conteudo, height=1, fg_color="#eeeeee").pack(fill="x", pady=10)

            acoes = ctk.CTkFrame(conteudo, fg_color="transparent")
            acoes.pack(anchor="e")

            ctk.CTkButton(
                acoes,
                text="🔒 Visualizar",
                width=120,
                fg_color="#004a8f",
                hover_color="#003366",
                command=lambda t=turma: self.visualizar_turma(t)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes,
                text="✏️ Editar",
                width=100,
                fg_color="#ffc107",
                hover_color="#e0a800",
                text_color="#212529",
                command=lambda t=turma: self.editar_turma(t)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes,
                text="🗑️ Excluir",
                width=100,
                fg_color="#dc3545",
                hover_color="#b52a37",
                command=lambda t=turma: self.excluir_turma(t)
            ).pack(side="left", padx=5)

    def aplicar_filtro(self, *args):
        texto = self.busca.get().lower()
        turno = self.filtro_turno.get()
        ano = self.filtro_ano.get()

        resultado = []
        for turma in self.turmas:
            bate_texto = texto in "".join(turma).lower()
            bate_turno = turno == "Todos" or turma[1] == turno
            bate_ano = ano == "Todos" or turma[2] == ano

            if bate_texto and bate_turno and bate_ano:
                resultado.append(turma)

        self.carregar_tabela(resultado)

    def visualizar_turma(self, turma):
        messagebox.showinfo(
            "Detalhes da Turma",
            f"🔢 Código: {turma[0]}\n\n"
            f"🕒 Turno: {turma[1]}\n"
            f"📅 Ano: {turma[2]}\n"
            f"📚 Curso: {turma[3]}\n"
            f"👥 Usuários: {turma[4]}\n"
            f"🔒 Status: {turma[5]}"
        )

    def editar_turma(self, turma):
        if messagebox.askyesno(
            "Editar Turma",
            f"Deseja editar a turma '{turma[0]}' - {turma[3]}?"
        ):
            messagebox.showinfo(
                "Em Desenvolvimento",
                "Funcionalidade de edição será implementada em breve!"
            )

    def excluir_turma(self, turma):
        if messagebox.askyesno(
            "Excluir Turma",
            f"Tem certeza que deseja excluir a turma '{turma[0]}'?\n\nCurso: {turma[3]}"
        ):
            messagebox.showinfo(
                "Turma Excluída",
                f"✅ A turma '{turma[0]}' foi marcada para exclusão."
            )

    # ───────────── LAYOUT ─────────────
    def montar_layout(self):
        main_container = ctk.CTkFrame(self.app)
        main_container.pack(fill="both", expand=True)

        sidebar(main_container)

        conteudo_frame = ctk.CTkFrame(main_container, fg_color="#ffffff")
        conteudo_frame.pack(side="left", fill="both", expand=True)
        conteudo_frame.grid_rowconfigure(2, weight=1)
        conteudo_frame.grid_columnconfigure(0, weight=1)

        topo = ctk.CTkFrame(conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
        topo.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            topo,
            text="👥  LISTA DE TURMAS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=20, pady=15)

        acoes = ctk.CTkFrame(conteudo_frame, fg_color="#f5f5f5", height=80)
        acoes.grid(row=1, column=0, sticky="ew", padx=20, pady=15)

        filtros_frame = ctk.CTkFrame(acoes, fg_color="transparent")
        filtros_frame.pack(side="left", padx=15, pady=10)

        self.busca = ctk.CTkEntry(
            filtros_frame,
            placeholder_text="Buscar por código ou curso...",
            width=250
        )
        self.busca.pack(anchor="w")
        self.busca.bind("<KeyRelease>", self.aplicar_filtro)
        

        self.filtro_turno = ctk.StringVar(value="Todos")
        self.filtro_ano = ctk.StringVar(value="Todos")

        corpo = ctk.CTkFrame(conteudo_frame, fg_color="#ffffff")
        corpo.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        corpo.grid_rowconfigure(1, weight=1)
        corpo.grid_columnconfigure(0, weight=1)

        self.tabela = ctk.CTkScrollableFrame(corpo, fg_color="#ffffff")
        self.tabela.grid(row=1, column=0, sticky="nsew")


if __name__ == "__main__":
    ListaTurmasApp()
