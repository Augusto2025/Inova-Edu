# model/models/login_model.py
from config.banco import conectar

class LoginUsuario:
    def exibir_usuarios(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT Email, Senha, Tipo FROM usuario")
        usuario = cursor.fetchall()
        conn.close()
        return usuario