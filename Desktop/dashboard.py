# dashboard.py
import customtkinter as ctk
from banco import conectar


def abrir_dashboard(app, tipo, tela_login):
    # limpa tela
    for widget in app.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(app)
    container.pack(expand=True, fill="both")

    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    # sidebar
    sidebar = ctk.CTkFrame(container, fg_color="#1f6aa5", width=200)
    sidebar.grid(row=0, column=0, sticky="nsew")

    ctk.CTkLabel(
        sidebar, text="MENU", font=("Arial", 22, "bold"), text_color="white"
    ).pack(pady=30)

    # conteúdo
    content = ctk.CTkFrame(container, fg_color="white")
    content.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

    def trocar_tela(func):
        for w in content.winfo_children():
            w.destroy()
        content.after(100, func)

    def inicio():
        ctk.CTkLabel(
            content, text="Dashboard", font=("Arial", 32, "bold"), text_color="#1f6aa5"
        ).pack(pady=40)

    def usuarios():
        ctk.CTkLabel(
            content,
            text="Cadastro de usuários",
            font=("Arial", 26, "bold"),
            text_color="#1f6aa5",
        ).pack(pady=20)

    def produtos():
        ctk.CTkLabel(
            content,
            text="Gestão de Produtos",
            font=("Arial", 26, "bold"),
            text_color="#1f6aa5",
        ).pack(pady=20)

    def botao(texto, comando):
        ctk.CTkButton(
            sidebar,
            text=texto,
            fg_color="#1f6aa5",
            hover_color="#174f7d",
            text_color="white",
            font=("Arial", 16),
            height=45,
            command=lambda: trocar_tela(comando),
        ).pack(fill="x", padx=20, pady=6)

    botao("Início", inicio)

    if tipo == "admin":
        botao("Usuários", usuarios)

    botao("Produtos", produtos)
    botao("Sair", tela_login)

    inicio()
