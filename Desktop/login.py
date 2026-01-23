import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Dados de login
usuarios = {
    "admin": {"senha": "123", "tipo": "admin"},
    "user": {"senha": "123", "tipo": "usuario"}
}

# app principal
app = ctk.CTk()
app.title("Sistema Desktop")
app.geometry("1000x600")

# Função limpar tela
def limpar_tela():
    for widget in app.winfo_children():
        widget.destroy()

# tela login
def tela_login():
    limpar_tela()

    container = ctk.CTkFrame(app)
    container.pack(expand=True, fill="both", padx=40, pady=40)

    container.grid_columnconfigure((0, 1), weight=1)
    container.grid_rowconfigure(0, weight=1)

    # ------ lado esquerdo ------
    left = ctk.CTkFrame(container, fg_color="#1f6aa5")
    left.grid(row=0, column=0, sticky="nsew")

    # titulo do lado esquerdo
    ctk.CTkLabel(left, text="Bem-vindo!", font=("Arial", 34, "bold"), text_color="white").pack(pady=(120, 10))
    ctk.CTkLabel(left, text="Sistema Desktop\nProfinal", font=("Arial", 18), text_color="white").pack()
    ctk.CTkLabel(left, text="Faça login para continuar", font=("Arial", 14), text_color="white").pack(pady=10)

    # ------ lado direito ------
    right = ctk.CTkFrame(container, fg_color="white")
    right.grid(row=0, column=1, sticky="nsew")

    ctk.CTkLabel(right, text="LOGIN", font=("Arial", 30, "bold"), text_color="#1f6aa5").pack(pady=(120, 30))

    # input usuario
    usuario = ctk.CTkEntry(right, placeholder_text="Usuário", width=280, height=45)
    usuario .pack(pady=10)

    # frame da senha
    senha_frame = ctk.CTkFrame(right, fg_color="transparent")
    senha_frame.pack(pady=10)

    # input senha
    senha = ctk.CTkEntry(senha_frame, placeholder_text="Senha", show="*", width=280, height=45)
    senha.pack(side="left", padx=(0, 5))

    # função para verificar usuario e senha já listados do dicionário se tive ele vai para outra tela, senão ele manda uma mensagem de erro
    def autenticar():
        user = usuario.get()
        pwd = senha.get()

        if user in usuarios and usuarios[user]["senha"] == pwd:
            abrir_dashboard(usuarios[user]["tipo"])
        else:
            erro.configure(text="Usuário ou senha inválidos")

    # command serve para usar uma função assim que clicado
    ctk.CTkButton(right, text="Entrar", width=280, height=45, font=("Arial", 16), command=autenticar).pack(pady=30)

    erro = ctk.CTkLabel(right, text="", text_color="red")
    erro.pack()

def abrir_dashboard(tipo):
    limpar_tela()

    container = ctk.CTkFrame(app)    
    container.pack(expand=True, fill="both")

    container.columnconfigure(1, weight=1)
    container.grid_rowconfigure(0, weight=1)
    
    # sidebar
    sidebar = ctk.CTkFrame(container, fg_color="#1f6aa5")
    sidebar.grid(row=0, column=0,sticky="nsew")

    ctk.CTkLabel(sidebar, text="MENU", font=("Arial", 22, "bold"), text_color="white").pack(pady=30)

    # conteudo
    content = ctk.CTkFrame(container, fg_color="white")
    content.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

    def trocar_tela(func):
        for w in content.winfo_children():
            w.destroy()
        content.after(100, func) # pequena animação

    def inicio():
        ctk.CTkLabel(content, text="Dashboard", font=("Arial", 32, "bold"), text_color="#1f6aa5").pack(pady=40)
        # ctk.CTkLabel(content, text="Computador", font=("Arial", 120)).pack()

    def usuarios():
        ctk.CTkLabel(content, text="Cadastro de usuários", font=("Arial", 26, "bold"),text_color="#1f6aa5").pack(pady=20)

    def produtos():
        ctk.CTkLabel(content, text="Gestão de Produtos", font=("Arial", 26, "bold"),text_color="#1f6aa5").pack(pady=20)

    def botao(texto, comando):
        ctk.CTkButton(
            sidebar,
            text=texto,
            fg_color="#1f6aa5",
            hover_color="#174f7d",
            text_color="white",
            font=("Arial", 16),
            height=45,
            command=lambda: trocar_tela(comando)
        ).pack(fill="x", padx=20, pady=6)

    botao("início", inicio)

    if tipo == "admin":
        botao("Usuário", usuarios)

    botao("Produtos", produtos)
    botao("Sair", tela_login)

    inicio()

# start
tela_login()
app.mainloop()