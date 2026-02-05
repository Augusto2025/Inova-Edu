from models.login_model import LoginUsuario

def autenticar(user, senha, tipo):
    usuarios = LoginUsuario().exibir_usuarios()
    for email_user, senha_user, tipo_user in usuarios:
        if user != email_user and senha != senha_user:
                text = str("Email e senha incorretos.")
                return (text, False)
        elif user != email_user:
                text = str("Email incorreto.")
                return (text, False)
        elif user == email_user and senha != senha_user:
                text = str("Senha incorreta.")
                return text, False
        else:
              tipo = tipo_user
              return tipo, True