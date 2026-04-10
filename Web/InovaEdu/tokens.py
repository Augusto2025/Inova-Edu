import hashlib

class GeradorTokenManual:
    def make_token(self, usuario):
        # Cria um hash único usando o ID e a Senha atual do usuário
        valor = f"{usuario.idusuario}{usuario.senha}"
        return hashlib.sha256(valor.encode()).hexdigest()

    def check_token(self, usuario, token):
        # Verifica se o hash gerado agora é igual ao que veio no link
        return self.make_token(usuario) == token

token_generator = GeradorTokenManual()