import customtkinter as ctk
from tkinter import messagebox
from Desktop.views.Coordenacao.sidebar_C import sidebar

# Configurações de Cores
azulEscuro = "#004A8D"
azulClaro = "#419FFD"
Branco = "#ecf0f1"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ListaTurmasApp:
    def __init__(self, master=None):
        # Se não houver master, cria a janela (para teste isolado)
        if master is None:
            self.app = ctk.CTk()
            self.app.geometry("1300x650")
            self.app.title("Sistema de Gestão de Turmas")
            self.app.attributes("-fullscreen", True)
            self.root = self.app
        else:
            self.root = master

        # ───────────── DADOS DAS TURMAS (Lógica do Código 1) ─────────────
        self.turmas = [
            ("2025.10.111", "Manhã", "2025", "Desenvolvimento de sistemas", "30", "🔒"),
            ("2025.02.001", "Tarde", "2025", "Administrador de Banco de dados", "25", "🔒"),
            ("2025.10.201", "Noite", "2025", "Administrador de Redes", "20", "🔒"),
            ("2025.12.115", "Manhã", "2024", "IT Essentials", "15", "🔒"),
            ("2025.05.210", "Tarde", "2024", "Programação Web", "28", "🔒"),
            ("2024.09.001", "Noite", "2024", "Segurança da Informação", "22", "🔒"),
        ]

        # Variáveis de filtro (Lógica do Código 1)
        self.filtro_turno = ctk.StringVar(value="Todos")
        self.filtro_ano = ctk.StringVar(value="Todos")

        self.montar_layout()
        self.carregar_tabela(self.turmas)

        if master is None:
            self.app.mainloop()

    # ───────────── FUNÇÕES DE LÓGICA ─────────────
    def carregar_tabela(self, lista_turmas):
        # Limpa widgets anteriores da tabela
        for widget in self.tabela.winfo_children():
            widget.destroy()

        for turma in lista_turmas:
            # CARD (Design do Código 2)
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
                text=f"{turma[0]}  •  {turma[3]}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#004a8f"
            ).pack(anchor="w", pady=(0, 6))

            # INFOS
            info = ctk.CTkFrame(conteudo, fg_color="transparent")
            info.pack(anchor="w")

            ctk.CTkLabel(info, text=f"🕒 Turno: {turma[1]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"📅 Ano: {turma[2]}").pack(anchor="w")
            ctk.CTkLabel(info, text=f"👥 Usuários: {turma[4]}").pack(anchor="w")

            # LINHA DIVISORA
            ctk.CTkFrame(conteudo, height=1, fg_color="#eeeeee").pack(fill="x", pady=10)

            # AÇÕES
            acoes_area = ctk.CTkFrame(conteudo, fg_color="transparent")
            acoes_area.pack(anchor="e")

            ctk.CTkButton(
                acoes_area, text="🔒 Visualizar", width=120, fg_color="#004a8f",
                hover_color="#003366", command=lambda t=turma: self.visualizar_turma(t)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes_area, text="✏️ Editar", width=100, fg_color="#ffc107",
                hover_color="#e0a800", text_color="#212529", command=lambda t=turma: self.editar_turma(t)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                acoes_area, text="🗑️ Excluir", width=100, fg_color="#dc3545",
                hover_color="#b52a37", command=lambda t=turma: self.excluir_turma(t)
            ).pack(side="left", padx=5)

    def aplicar_filtro(self, event=None):
        texto = self.busca.get().lower()
        turno = self.filtro_turno.get()
        # Nota: ano está aqui para expansão futura, conforme seu código 1
        
        resultado = []
        for turma in self.turmas:
            bate_texto = texto in f"{turma[0]} {turma[3]}".lower()
            bate_turno = (turno == "Todos" or turma[1] == turno)

            if bate_texto and bate_turno:
                resultado.append(turma)

        self.carregar_tabela(resultado)

    def visualizar_turma(self, turma):
        messagebox.showinfo("Turma", f"Visualizar código: {turma[0]}")

    def editar_turma(self, turma):
        messagebox.showinfo("Editar", f"Editar turma: {turma[0]}")

    def excluir_turma(self, turma):
        messagebox.showwarning("Excluir", f"Deseja excluir a turma: {turma[0]}?")

    # ───────────── LAYOUT (Designer do Código 2) ─────────────
    def montar_layout(self):
        # Container Principal
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # Sidebar (Injetada conforme designer 2)
        sidebar(self.main_container)

        # Área de Conteúdo
        self.conteudo_frame = ctk.CTkFrame(self.main_container, fg_color="#ffffff")
        self.conteudo_frame.pack(side="left", fill="both", expand=True)

        # Cabeçalho Azul (Topo)
        topo = ctk.CTkFrame(self.conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo,
            text="👥 LISTA DE TURMAS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        # Barra de Ações e Filtros
        acoes = ctk.CTkFrame(self.conteudo_frame, fg_color="#f5f5f5", height=80)
        acoes.pack(fill="x", padx=20, pady=15)

        # BUSCA (Esquerda)
        self.busca = ctk.CTkEntry(
            acoes,
            placeholder_text="Buscar por código ou curso...",
            width=260
        )
        self.busca.pack(side="left", padx=15, pady=20)
        self.busca.bind("<KeyRelease>", self.aplicar_filtro)

        # FILTROS (Direita)
        filtros_container = ctk.CTkFrame(acoes, fg_color="transparent")
        filtros_container.pack(side="right", padx=15)

        ctk.CTkLabel(filtros_container, text="Filtrar por:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))

        for turno in ["Todos", "Manhã", "Tarde", "Noite"]:
            ctk.CTkRadioButton(
                filtros_container,
                text=turno,
                variable=self.filtro_turno,
                value=turno,
                command=self.aplicar_filtro,
                radiobutton_width=16,
                radiobutton_height=16
            ).pack(side="left", padx=5)

        # Botão + Cadastro
        ctk.CTkButton(
            filtros_container, 
            text="+ Cadastro",
            width=90, 
            height=30, 
            fg_color="#004a8f",
            hover_color="#003366",
            command=lambda: messagebox.showinfo("Cadastro", "Redirecionar para tela de Cadastro")
        ).pack(side="left", padx=(15, 0))

        # Tabela Scrollable
        self.tabela = ctk.CTkScrollableFrame(self.conteudo_frame, fg_color="#ffffff")
        self.tabela.pack(fill="both", expand=True, padx=20, pady=(0, 20))

if __name__ == "__main__":
    ListaTurmasApp()