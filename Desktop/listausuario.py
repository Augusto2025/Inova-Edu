import customtkinter as ctk
from tkinter import messagebox
from sidebar_C import sidebar
from PIL import Image
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ───────────── FUNÇÕES DE FILTRO ─────────────
def carregar_tabela(lista):
    for widget in tabela.winfo_children():
        widget.destroy()

    # ───── MARCA D'ÁGUA ─────
    watermark = ctk.CTkLabel(
        tabela,
        image=watermark_img,
        text=""
    )
    watermark.pack(pady=120)
    watermark.lower()

    for u in lista:
        linha = ctk.CTkFrame(tabela, fg_color="#ffffff")
        linha.grid(sticky="ew", pady=2)

        for i, w in enumerate(pesos):
            linha.grid_columnconfigure(i, weight=w)

        ctk.CTkLabel(linha, text=u[0], font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=10)
        ctk.CTkLabel(linha, text=u[1]).grid(row=0, column=1, padx=10, sticky="w")
        ctk.CTkLabel(linha, text=u[2]).grid(row=0, column=2, padx=10, sticky="w")
        ctk.CTkLabel(linha, text=u[3]).grid(row=0, column=3, padx=10, sticky="w")
        ctk.CTkLabel(linha, text=u[4]).grid(row=0, column=4, padx=10, sticky="w")
        ctk.CTkLabel(linha, text=u[5]).grid(row=0, column=5, padx=10, sticky="w")

        acoes_btn = ctk.CTkFrame(linha, fg_color="transparent")
        acoes_btn.grid(row=0, column=6, padx=10, sticky="w")

        ctk.CTkButton(acoes_btn, text="✏️", width=35).pack(side="left", padx=2)
        ctk.CTkButton(
            acoes_btn,
            text="🗑️",
            width=35,
            fg_color="#dc3545",
            hover_color="#b52a37"
        ).pack(side="left", padx=2)


def aplicar_filtro(*args):
    texto = busca.get().lower()
    tipo = filtro.get()

    resultado = []
    for u in usuarios:
        bate_texto = texto in " ".join(u).lower()
        bate_tipo = tipo == "Todos" or u[5] == tipo

        if bate_texto and bate_tipo:
            resultado.append(u)

    carregar_tabela(resultado)


# ───────────── APP ─────────────
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1300x650")
    app.title("Sistema de Gestão")
    app.attributes("-fullscreen", True)

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)

    sidebar_frame, botoes_menu = sidebar(app)
    sidebar_frame.grid(row=0, column=0, sticky="ns")

    conteudo_frame = ctk.CTkFrame(app, fg_color="#ffffff", corner_radius=0)
    conteudo_frame.grid(row=0, column=1, sticky="nsew")
    conteudo_frame.grid_rowconfigure(2, weight=1)
    conteudo_frame.grid_columnconfigure(0, weight=1)

    # ───────────── TOPO ─────────────
    topo = ctk.CTkFrame(conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
    topo.grid(row=0, column=0, sticky="ew")

    ctk.CTkLabel(
        topo,
        text="👤  LISTA DE USUÁRIOS",
        text_color="white",
        font=ctk.CTkFont(size=18, weight="bold")
    ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

    # ───────────── AÇÕES ─────────────
    acoes = ctk.CTkFrame(conteudo_frame, fg_color="#f5f5f5", height=60, corner_radius=8)
    acoes.grid(row=1, column=0, sticky="ew", padx=20, pady=15)

    acoes.grid_columnconfigure(0, weight=1)
    acoes.grid_columnconfigure(1, weight=0)
    acoes.grid_columnconfigure(2, weight=1)
    acoes.grid_columnconfigure(3, weight=0)

    busca = ctk.CTkEntry(acoes, placeholder_text="Buscar usuário...", width=300)
    busca.grid(row=0, column=0, padx=15, pady=10, sticky="w")
    busca.bind("<KeyRelease>", aplicar_filtro)

    filtro_frame = ctk.CTkFrame(acoes, fg_color="transparent")
    filtro_frame.grid(row=0, column=1)

    ctk.CTkLabel(filtro_frame, text="Filtrar por:").pack(side="left", padx=(0, 10))

    filtro = ctk.StringVar(value="Todos")
    for opcao in ["Todos", "Aluno", "Professor", "Coordenador"]:
        ctk.CTkRadioButton(
            filtro_frame,
            text=opcao,
            variable=filtro,
            value=opcao,
            command=aplicar_filtro
        ).pack(side="left", padx=5)

    ctk.CTkButton(
        acoes,
        text="+ Cadastro",
        text_color="white",
        font=ctk.CTkFont(size=18, weight="bold"),
        fg_color="#004a8f"
    ).grid(row=0, column=3, padx=20, pady=10, sticky="e")

    # ───────────── CORPO ─────────────
    corpo = ctk.CTkFrame(conteudo_frame, fg_color="#ffffff", corner_radius=0)
    corpo.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
    corpo.grid_columnconfigure(0, weight=1)
    corpo.grid_rowconfigure(1, weight=1)

    tabela_header = ctk.CTkFrame(corpo, fg_color="#003f7f", height=40)
    tabela_header.grid(row=0, column=0, sticky="ew")

    pesos = [1, 2, 2, 4, 3, 2, 2]
    for i, w in enumerate(pesos):
        tabela_header.grid_columnconfigure(i, weight=w)

    colunas = ["Imagem", "Nome", "Sobrenome", "Email", "Descrição", "Tipo", "Ações"]
    for i, col in enumerate(colunas):
        ctk.CTkLabel(
            tabela_header,
            text=col,
            text_color="white",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=i, padx=10, sticky="w")

    tabela = ctk.CTkScrollableFrame(corpo, fg_color="#ffffff")
    tabela.grid(row=1, column=0, sticky="nsew")

    # ───────────── IMAGEM MARCA D'ÁGUA OFUSCADA ─────────────
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "img", "LOGOAZUL.png")

    img = Image.open(logo_path).convert("RGBA")

    alpha = img.split()[3]
    alpha = alpha.point(lambda p: p * 0.12)  # 12% de visibilidade
    img.putalpha(alpha)

    watermark_img = ctk.CTkImage(
        light_image=img,
        size=(700, 700)
    )

    usuarios = []

    carregar_tabela(usuarios)

    app.mainloop()
