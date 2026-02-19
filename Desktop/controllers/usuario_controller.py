from models.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()

    def salvar_usuario(
        self,
        nome,
        sobrenome,
        email,
        tipo,
        imagem,
        descricao
    ):
        # senha provisória (depois você melhora isso)
        senha_padrao = "123456"

        self.model.cadastrar(
            imagem,
            tipo,
            nome,
            sobrenome,
            email,
            senha_padrao,
            descricao
        )
