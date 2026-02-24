import customtkinter as ctk
from tkinter import messagebox
from Desktop.views.Coordenacao.sidebar_C import sidebar
from PIL import Image
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ListaUsuariosApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1300x650")
        self.app.title("Sistema de Gestão")
        # self.app.attributes("-fullscreen", True)

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=1)

        self.sidebar_frame, self.botoes_menu = sidebar(self.app)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.conteudo_frame = ctk.CTkFrame(self.app, fg_color="#ffffff", corner_radius=0)
        self.conteudo_frame.grid(row=0, column=1, sticky="nsew")
        self.conteudo_frame.grid_rowconfigure(2, weight=1)
        self.conteudo_frame.grid_columnconfigure(0, weight=1)

        self.criar_topo()
        self.criar_acoes()
        self.criar_corpo()
        self.carregar_watermark()

        # 🔗 AQUI VEM DO BANCO DEPOIS
        self.usuarios = []
        self.carregar_tabela(self.usuarios)

        self.app.mainloop()

    # ───────────── TOPO ─────────────
    def criar_topo(self):
        topo = ctk.CTkFrame(self.conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
        topo.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            topo,
            text="👤  LISTA DE USUÁRIOS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

    # ───────────── AÇÕES ─────────────
    def criar_acoes(self):
        acoes = ctk.CTkFrame(self.conteudo_frame, fg_color="#f5f5f5", height=60, corner_radius=8)
        acoes.grid(row=1, column=0, sticky="ew", padx=20, pady=15)

        acoes.grid_columnconfigure(0, weight=1)
        acoes.grid_columnconfigure(1, weight=0)
        acoes.grid_columnconfigure(2, weight=1)
        acoes.grid_columnconfigure(3, weight=0)

        self.busca = ctk.CTkEntry(acoes, placeholder_text="Buscar usuário...", width=300)
        self.busca.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.busca.bind("<KeyRelease>", self.aplicar_filtro)

        filtro_frame = ctk.CTkFrame(acoes, fg_color="transparent")
        filtro_frame.grid(row=0, column=1)

        ctk.CTkLabel(filtro_frame, text="Filtrar por:").pack(side="left", padx=(0, 10))

        self.filtro = ctk.StringVar(value="Todos")
        for opcao in ["Todos", "Aluno", "Professor", "Coordenador"]:
            ctk.CTkRadioButton(
                filtro_frame,
                text=opcao,
                variable=self.filtro,
                value=opcao,
                command=self.aplicar_filtro
            ).pack(side="left", padx=5)

        ctk.CTkButton(
            acoes,
            text="+ Cadastro",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#004a8f"
        ).grid(row=0, column=3, padx=20, pady=10, sticky="e")

    # ───────────── CORPO ─────────────
    def criar_corpo(self):
        self.corpo = ctk.CTkFrame(self.conteudo_frame, fg_color="#ffffff", corner_radius=0)
        self.corpo.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.corpo.grid_columnconfigure(0, weight=1)
        self.corpo.grid_rowconfigure(1, weight=1)

        tabela_header = ctk.CTkFrame(self.corpo, fg_color="#003f7f", height=40)
        tabela_header.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            tabela_header,
            text="USUÁRIOS CADASTRADOS",
            text_color="white",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=10)

        self.tabela = ctk.CTkScrollableFrame(self.corpo, fg_color="#ffffff")
        self.tabela.grid(row=1, column=0, sticky="nsew")

    # ───────────── WATERMARK ─────────────
    def carregar_watermark(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(BASE_DIR, "assets", "img", "LOGOAZUL.png")

        img = Image.open(logo_path).convert("RGBA")
        alpha = img.split()[3]
        alpha = alpha.point(lambda p: p * 0.12)
        img.putalpha(alpha)

        self.watermark_img = ctk.CTkImage(light_image=img, size=(700, 700))

    # ───────────── TABELA ─────────────
    def carregar_tabela(self, lista):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        watermark = ctk.CTkLabel(self.tabela, image=self.watermark_img, text="")
        watermark.pack(pady=120)
        watermark.lower()

        for u in lista:
            linha = ctk.CTkFrame(
                self.tabela,
                fg_color="#ffffff",
                corner_radius=8,
                border_width=1,
                border_color="#e0e0e0"
            )
            linha.pack(fill="x", pady=8, padx=10)

            ctk.CTkLabel(
                linha,
                text=f"👤 Nome: {u[1]} {u[2]}",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(10, 2))

            ctk.CTkLabel(
                linha,
                text=f"📧 Email: {u[3]}",
                anchor="w"
            ).pack(anchor="w", padx=15, pady=2)

            ctk.CTkLabel(
                linha,
                text=f"📝 Descrição: {u[4]}",
                wraplength=900,
                justify="left",
                anchor="w"
            ).pack(anchor="w", padx=15, pady=2)

            ctk.CTkLabel(
                linha,
                text=f"🏷️ Tipo: {u[5]}",
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(2, 10))

    # ───────────── FILTRO ─────────────
    def aplicar_filtro(self, *args):
        texto = self.busca.get().lower()
        tipo = self.filtro.get()

        resultado = []
        for u in self.usuarios:
            bate_texto = texto in " ".join(map(str, u)).lower()
            bate_tipo = tipo == "Todos" or u[5] == tipo

            if bate_texto and bate_tipo:
                resultado.append(u)

        self.carregar_tabela(resultado)


if __name__ == "__main__":
    ListaUsuariosApp()
