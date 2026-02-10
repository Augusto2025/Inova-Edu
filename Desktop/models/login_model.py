# model/models/login_model.py
from config.banco import conectar
import traceback

class LoginUsuario:
    def exibir_usuarios(self):
        conn = None
        try:
            print("[MODEL] Conectando...")
            conn = conectar()
            cursor = conn.cursor()
            print("[MODEL] Executando query...")
            cursor.execute("SELECT Email, Senha, Tipo FROM usuario")
            usuario = cursor.fetchall()
            cursor.close()
            print(f"[MODEL] {len(usuario)} usuarios encontrados")
            return usuario
        except Exception as e:
            print(f"[MODEL ERRO] {str(e)}")
            print(f"[MODEL TRACEBACK] {traceback.format_exc()}")
            return []
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass