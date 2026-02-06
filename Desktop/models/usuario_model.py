# model/models/login_model.py
from config.banco import conectar

class UsuarioModel:
    def cadastrar(
        self,
        imagem,
        tipo,
        nome,
        sobrenome,
        email,
        senha,
        descricao
    ):
        # depois aqui entra o banco (SQLite, MySQL etc)
        print("📦 Salvando usuário no banco...")
        print(imagem, tipo, nome, sobrenome, email, senha, descricao)
