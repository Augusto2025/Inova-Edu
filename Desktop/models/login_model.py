# models/login_model.py
from config.banco import conectar
import traceback
from typing import List, Tuple, Optional

class LoginUsuario:
    def exibir_usuarios(self) -> List[Tuple[str, str, str]]:
        """
        Retorna lista de usuários para autenticação.
        RETORNA: (email, senha_hash, tipo) - NUNCA a senha em texto plano
        """
        conn = None
        try:
            print("[MODEL] Conectando ao PostgreSQL...")
            conn = conectar()
            cursor = conn.cursor()
            print("[MODEL] Executando query...")
            # Seleciona o hash da senha, não a senha em texto plano
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

    def buscar_usuario_por_email(self, email: str) -> Optional[Tuple[str, str, str]]:
        """
        Busca um usuário específico por email.
        RETORNA: (email, senha_hash, tipo) ou None se não encontrado
        """
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = 'SELECT "Email", "Senha", "Tipo" FROM usuario WHERE "Email" ILIKE %s'
            cursor.execute(query, (email,))
            usuario = cursor.fetchone()
            cursor.close()
            return usuario

        except Exception as e:
            print(f"[MODEL ERRO] Erro ao buscar usuário: {str(e)}")
            return None

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass