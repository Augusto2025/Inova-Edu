from models.usuario_model import UsuarioModel
from tkinter import messagebox

class UsuarioController:
    def __init__(self, view):
        self.view = view
        self.model = UsuarioModel()

    def cadastrar_usuario(self):
        imagem = self.view.imagem_entry.get()
        tipo = self.view.tipo_combo.get()
        nome = self.view.nome_entry.get()
        sobrenome = self.view.sobrenome_entry.get()
        email = self.view.email_entry.get()
        senha = self.view.senha_entry.get()
        descricao = self.view.descricao_entry.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios")
            return

        self.model.cadastrar(
            imagem,
            tipo,
            nome,
            sobrenome,
            email,
            senha,
            descricao
        )

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
