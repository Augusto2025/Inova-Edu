from config.banco import conectar
from psycopg2 import extras  # Importante para o RealDictCursor

class PerfilModel:
    def obter_dados_perfil(self, email):
        cursor = None
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor(cursor_factory=extras.RealDictCursor)

            # 1. Dados do Usuário
            # Usamos ILIKE para evitar problemas de Maiúsculo/Minúsculo no e-mail digitado
            cursor.execute('SELECT * FROM usuario WHERE "Email" ILIKE %s', (email,))
            usuario = cursor.fetchone()

            if not usuario:
                print(f"DEBUG: Usuário com e-mail {email} não encontrado.")
                return None

            # --- TRUQUE PARA EVITAR O ERRO 'idusuario' ---
            # Tentamos pegar o ID de qualquer jeito que ele possa existir no banco
            id_usuario = usuario.get('idusuario') or usuario.get('idUsuario') or usuario.get('id_usuario')
            
            if not id_usuario:
                print(f"DEBUG: Colunas disponíveis no banco: {list(usuario.keys())}")
                raise KeyError("Não foi possível encontrar a coluna de ID do usuário.")

            # 2. Dados da Turma
            query_turma = """
                SELECT t.nome
                FROM usuario_da_turma ut
                JOIN turma t ON ut."ID_Turma" = t."id_turma"
                WHERE ut.id_usuario = %s
            """
            cursor.execute(query_turma, (id_usuario,))
            turma = cursor.fetchone()

            # 3. Certificados
            cursor.execute("SELECT * FROM certificado WHERE usuario_id = %s", (id_usuario,))
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