from config.banco import conectar
from psycopg2 import extras  # Importante para o RealDictCursor

class PerfilModel:
    def obter_dados_perfil(self, email):
        cursor = None
        conexao = None
        try:
            conexao = conectar()
            # No PostgreSQL, usamos o cursor_factory para retornar dicionários
            cursor = conexao.cursor(cursor_factory=extras.RealDictCursor)

            # 1. Dados do Usuário
            cursor.execute("SELECT * FROM usuario WHERE \"Email\" = %s", (email,))
            usuario = cursor.fetchone()

            if not usuario:
                return None

            # 2. Dados da Turma
            query_turma = """
                SELECT t.nome 
                FROM usuario_da_turma ut
                JOIN turma t ON ut.id_turma = t.id_turma
                WHERE ut.id_usuario = %s
            """
            cursor.execute(query_turma, (usuario['idusuario'],))
            turma = cursor.fetchone()

            # 3. Certificados
            cursor.execute("SELECT * FROM certificado WHERE usuario_id = %s", (usuario['idusuario'],))
            certificados = cursor.fetchall()

            return {
                "usuario": usuario,
                "turma": turma['nome'] if turma else "Sem Turma",
                "certificados": certificados
            }
        except Exception as e:
            print(f"Erro ao consultar banco (Postgres): {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def salvar_usuario(self, email, nome, sobrenome, bio):
        conexao = conectar()
        cursor = conexao.cursor()
        try:
            # Atenção: Postgres diferencia maiúsculas/minúsculas se usar aspas duplas
            query = "UPDATE usuario SET nome = %s, sobrenome = %s, descricao = %s WHERE email = %s"
            cursor.execute(query, (nome, sobrenome, bio, email))
            conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()