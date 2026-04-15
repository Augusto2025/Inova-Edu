class UsuarioSessao:
    _instance = None
    email = None  # Vamos guardar o e-mail aqui após o login

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsuarioSessao, cls).__new__(cls)
        return cls._instance