# model/models/login_model.py
from config.banco import conectar

class Cadusuarios:
    def cadstro_usuario(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT Email, Senha FROM usuario")
        usuario = cursor.fetchall()
        conn.close()
        return usuario