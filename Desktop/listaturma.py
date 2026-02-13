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
            ("2025.02.001", "Tarde", "2025", "Administrador de Banco de dados", "📌", "🔒"),
            ("2025.10.201", "Noite", "2025", "Administrador de Redes", "📌", "🔒"),
            ("2025.12.115", "Manhã", "2024", "IT Essentials", "📌", "🔒"),
            ("2025.05.210", "Tarde", "2024", "Programação Web", "📌", "🔒"),
            ("2024.09.001", "Noite", "2024", "Segurança da Informação", "📌", "🔒"),
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

    def aplicar_filtro(self, event=None):
        texto = self.busca.get().lower()
        turno = self.filtro_turno.get()
        ano = self.filtro_ano.get()

        resultado = []
        for turma in self.turmas:
            bate_texto = texto in f"{turma[0]} {turma[3]}".lower()
            bate_turno = turno == "Todos" or turma[1] == turno
            bate_ano = ano == "Todos" or turma[2] == ano

            if bate_texto and bate_turno and bate_ano:
                resultado.append(turma)

        self.carregar_tabela(resultado)

    def visualizar_turma(self, turma):
        messagebox.showinfo("Turma", turma[0])

    def editar_turma(self, turma):
        messagebox.showinfo("Editar", turma[0])

    def excluir_turma(self, turma):
        messagebox.showwarning("Excluir", turma[0])

    # ───────────── LAYOUT ─────────────
    def montar_layout(self):
        main_container = ctk.CTkFrame(self.app)
        main_container.pack(fill="both", expand=True)

        sidebar(main_container)

        conteudo_frame = ctk.CTkFrame(main_container, fg_color="#ffffff")
        conteudo_frame.pack(side="left", fill="both", expand=True)

        topo = ctk.CTkFrame(conteudo_frame, height=60, fg_color="#004a8f",corner_radius=0)
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo,
            text="👥 LISTA DE TURMAS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
      

        # ───────────── AÇÕES ─────────────
        acoes = ctk.CTkFrame(conteudo_frame, fg_color="#f5f5f5", height=80)
        acoes.pack(fill="x", padx=20, pady=15)

        acoes.grid_columnconfigure(0, weight=1)
        acoes.grid_columnconfigure(1, weight=1)

        # BUSCA (ESQUERDA)
        self.busca = ctk.CTkEntry(
            acoes,
            placeholder_text="Buscar por código ou curso...",
            width=260
        )
        self.busca.grid(row=0, column=0, sticky="w", padx=15)
        self.busca.bind("<KeyRelease>", self.aplicar_filtro)

        # FILTROS (DIREITA)
        filtros = ctk.CTkFrame(acoes, fg_color="transparent")
        filtros.grid(row=0, column=1, sticky="e", padx=15)

        ctk.CTkLabel(filtros, text="Filtrar por:").pack(side="left", padx=(0, 10))
        self.filtro_turno = ctk.StringVar(value="Todos")
        self.filtro_ano = ctk.StringVar(value="Todos")

        for turno in ["Todos", "Manhã", "Tarde", "Noite"]:
            ctk.CTkRadioButton(
                filtros,
                text=turno,
                variable=self.filtro_turno,
                value=turno,
                command=self.aplicar_filtro
            ).pack(side="left", padx=5)
            
            
        # TABELA
        self.tabela = ctk.CTkScrollableFrame(conteudo_frame, fg_color="#ffffff")
        self.tabela.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkButton(
                filtros, text="+ Cadastro ",
                width=40, height=20, 
                fg_color="#004a8f",
                hover_color="#003366"
            ).pack(side="left", padx=5)  # Espaço entre os filtros   





if __name__ == "__main__":
    ListaTurmasApp()
