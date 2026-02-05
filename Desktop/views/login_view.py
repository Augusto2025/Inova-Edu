import customtkinter as ctk
from controllers.login_controller import autenticar

class tela_login(ctk.CTkFrame):  # use CamelCase por convenção
    def __init__(self, master):  
        super().__init__(master)

        # este frame precisa ser adicionado à janela pelo chamador (pack/grid)
        # Ex.: no main.py: TelaLogin(root).pack(expand=True, fill="both")

        print("Tela de login iniciada")
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both", padx=40, pady=40)

        self.container.grid_columnconfigure((0, 1), weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.left = ctk.CTkFrame(self.container, fg_color="#1f6aa5")
        self.left.grid(row=0, column=0, sticky="nsew")

        # titulo do lado esquerdo
        ctk.CTkLabel(
            self.left, text="Bem-vindo!", font=("Arial", 34, "bold"), text_color="white"
        ).pack(pady=(120, 10))
        ctk.CTkLabel(
            self.left, text="Sistema Desktop\nProfinal", font=("Arial", 18), text_color="white"
        ).pack()
        ctk.CTkLabel(
            self.left, text="Faça login para continuar", font=("Arial", 14), text_color="white"
        ).pack(pady=10)

        self.right = ctk.CTkFrame(self.container, fg_color="white")
        self.right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            self.right, text="LOGIN", font=("Arial", 30, "bold"), text_color="#1f6aa5"
        ).pack(pady=(120, 30))

        self.usuario = ctk.CTkEntry(self.right, placeholder_text="Usuário", width=280, height=45)
        self.usuario.pack(pady=10)

        self.senha = ctk.CTkEntry(
            self.right, placeholder_text="Senha", show="*", width=280, height=45
        )
        self.senha.pack(pady=10)

        self.erro = ctk.CTkLabel(self.right, text="", text_color="red")
        self.erro.pack()

        ctk.CTkButton(
            self.right,
            text="Entrar",
            width=280,
            height=45,
            font=("Arial", 16),
            command=self.autentificacao,
        ).pack(pady=30)

    
    def autentificacao(self):
        tipo = ""
        result = autenticar(self.usuario.get(), self.senha.get(), tipo)
        if result[1]:  # Se o segundo valor da tupla é True (autenticado)
            tipo = result[0]  # O tipo de usuário retornado

            # Abre a HOME como nova janela
            if tipo == "Aluno" or tipo == "Professor":
                self.destroy()  # Fecha a tela de login
                
                from views.Aluno_e_Professor.home_view import Home
                self.home_aluno_screen = Home(self.master)
                self.home_aluno_screen.pack(expand=True, fill="both")
            elif tipo == "Coordenador":
                # falta implementar a tela do coordenador
                pass
        else:
            # result é uma tupla (mensagem, False)
            mensagem, ok = result
            self.erro.configure(text=mensagem)

