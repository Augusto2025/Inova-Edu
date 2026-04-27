from config.banco import conectar
from psycopg2 import extras

class PerfilModel:
    def obter_dados_perfil(self, email):
        cursor = None
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor(cursor_factory=extras.RealDictCursor)

            # 1. Dados do Usuário
            cursor.execute('SELECT * FROM usuario WHERE "Email" ILIKE %s', (email,))
            usuario = cursor.fetchone()

            if not usuario:
                return None

            # O ID do usuário vindo da tabela usuario
            id_usuario = usuario.get('idusuario') or usuario.get('idUsuario')

            # 2. Dados da Turma (Conforme sua primeira print)
            query_turma = """
                SELECT t."Codigo_Turma" 
                FROM usuario_da_turma ut
                JOIN turma t ON ut."ID_Turma" = t."idTurma"
                WHERE ut."ID_Usuario" = %s
            """
            cursor.execute(query_turma, (id_usuario,))
            turma = cursor.fetchone()

            # 3. Certificados (Conforme sua segunda print)
            # Aqui é minúsculo: usuario_id
            cursor.execute('SELECT * FROM certificado WHERE usuario_id = %s', (id_usuario,))
            certificados = cursor.fetchall()

            return {
                "usuario": usuario,
                "turma": turma['Codigo_Turma'] if turma else "Sem Turma",
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
            # Se as colunas no banco forem "Nome", "Sobrenome", etc., use aspas duplas aqui também!
            query = """
                UPDATE usuario 
                SET nome = %s, sobrenome = %s, descricao = %s 
                WHERE "Email" = %s
            """
            cursor.execute(query, (nome, sobrenome, bio, email))
            conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()