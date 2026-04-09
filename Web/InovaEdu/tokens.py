from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Usamos apenas o ID e a senha atual para gerar o hash.
        # Se a senha mudar, o token antigo invalida automaticamente.
        return str(user.idusuario) + str(timestamp) + str(user.senha)

token_generator = TokenGenerator()