import customtkinter as ctk

class UsuarioView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self, text="Cadastro de Usuário", font=("Arial", 18)).pack(pady=10)

        self.imagem_entry = ctk.CTkEntry(self, placeholder_text="Imagem (caminho)")
        self.imagem_entry.pack(pady=5)

        self.tipo_combo = ctk.CTkComboBox(
            self,
            values=["Admin", "Usuário"]
        )
        self.tipo_combo.pack(pady=5)

        self.nome_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.nome_entry.pack(pady=5)

        self.sobrenome_entry = ctk.CTkEntry(self, placeholder_text="Sobrenome")
        self.sobrenome_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        self.senha_entry = ctk.CTkEntry(
            self,
            placeholder_text="Senha",
            show="*"
        )
        self.senha_entry.pack(pady=5)

        self.descricao_entry = ctk.CTkEntry(self, placeholder_text="Descrição")
        self.descricao_entry.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Cadastrar",
            command=self.controller.cadastrar_usuario
        ).pack(pady=15)
  