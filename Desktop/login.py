import customtkinter as ctk
from banco import conectar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

usuarios = {
    "admin": {"senha": "123", "tipo": "admin"},
    "user": {"senha": "123", "tipo": "usuario"},
}

app = ctk.CTk()
app.title("Sistema Desktop")
app.geometry("1000x600")


def limpar_tela():
    for widget in app.winfo_children():
        widget.destroy()


def tela_login():
    limpar_tela()

    container = ctk.CTkFrame(app)
    container.pack(expand=True, fill="both", padx=40, pady=40)

    container.grid_columnconfigure((0, 1), weight=1)
    container.grid_rowconfigure(0, weight=1)

    left = ctk.CTkFrame(container, fg_color="#1f6aa5")
    left.grid(row=0, column=0, sticky="nsew")

    # titulo do lado esquerdo
    ctk.CTkLabel(
        left, text="Bem-vindo!", font=("Arial", 34, "bold"), text_color="white"
    ).pack(pady=(120, 10))
    ctk.CTkLabel(
        left, text="Sistema Desktop\nProfinal", font=("Arial", 18), text_color="white"
    ).pack()
    ctk.CTkLabel(
        left, text="Faça login para continuar", font=("Arial", 14), text_color="white"
    ).pack(pady=10)

    right = ctk.CTkFrame(container, fg_color="white")
    right.grid(row=0, column=1, sticky="nsew")

    ctk.CTkLabel(
        right, text="LOGIN", font=("Arial", 30, "bold"), text_color="#1f6aa5"
    ).pack(pady=(120, 30))

    usuario = ctk.CTkEntry(right, placeholder_text="Usuário", width=280, height=45)
    usuario.pack(pady=10)

    senha = ctk.CTkEntry(
        right, placeholder_text="Senha", show="*", width=280, height=45
    )
    senha.pack(pady=10)

    erro = ctk.CTkLabel(right, text="", text_color="red")
    erro.pack()

    def autenticar():
        user = usuario.get()
        pwd = senha.get()

        if user in usuarios and usuarios[user]["senha"] == pwd:
            (app, usuarios[user]["tipo"], tela_login)
        else:
            erro.configure(text="Usuário ou senha inválidos")

    ctk.CTkButton(
        right,
        text="Entrar",
        width=280,
        height=45,
        font=("Arial", 16),
        command=autenticar,
    ).pack(pady=30)


tela_login()
app.mainloop()
