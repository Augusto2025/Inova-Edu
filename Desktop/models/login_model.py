# model/models/login_model.py
from config.banco import conectar
import traceback

class LoginUsuario:
    def exibir_usuarios(self):
        conn = None
        try:
            print("[MODEL] Conectando ao PostgreSQL...")
            conn = conectar()
            cursor = conn.cursor()
            print("[MODEL] Executando query...")
            # Mude a linha da query para esta:
            query = 'SELECT "Email", "Senha", "Tipo" FROM usuario'
            cursor.execute(query)
            usuarios = cursor.fetchall()
            cursor.close()
            print(f"[MODEL] {len(usuarios)} usuarios encontrados")
            return usuarios
            
        except Exception as e:
            print(f"[MODEL ERRO] Erro ao buscar usuários no Postgres: {str(e)}")
            print(f"[MODEL TRACEBACK] {traceback.format_exc()}")
            return []
            
        finally:
            if conn:
                try:
                    conn.close()
                    print("[MODEL] Conexão encerrada.")
                except:
                    pass