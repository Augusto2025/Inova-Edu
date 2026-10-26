from config.banco import conectar
from psycopg2 import extras
from security.crypto import hash_password
from security.validators import validate_password
from security.logger import get_logger

logger = get_logger(__name__)


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
            logger.error(f"Erro ao consultar banco (Postgres): {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def salvar_usuario(self, email, nome, sobrenome, bio, senha):
        """
        Atualiza dados do usuário.
        Se senha fornecida, faz hash antes de salvar.
        """
        # Valida senha se fornecida
        if senha and senha.strip() != "":
            valido, erro = validate_password(senha)
            if not valido:
                logger.warning(f"Senha inválida para {email}: {erro}")
                return False, erro

            # Hash da senha
            senha_hash = hash_password(senha)
        else:
            senha_hash = None

        conexao = conectar()
        cursor = conexao.cursor()
        try:
            if senha_hash:
                sql = """
                    UPDATE usuario
                    SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s, "Senha" = %s
                    WHERE "Email" = %s
                """
                params = (nome, sobrenome, bio, senha_hash, email)
            else:
                sql = """
                    UPDATE usuario
                    SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s
                    WHERE "Email" = %s
                """
                params = (nome, sobrenome, bio, email)
            cursor.execute(sql, params)
            conexao.commit()
            logger.info(f"Perfil atualizado para: {email}")
            return True, None
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil: {e}")
            return False, str(e)
        finally:
            cursor.close()
            conexao.close()

    def salvar_certificado(self, nome, descricao, data_inicio, data_final, usuario_id):
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            query = """
                INSERT INTO certificado (nome, descricao, data_inicio, data_final, usuario_id)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (nome, descricao, data_inicio, data_final, usuario_id))
            conexao.commit()
            return True, None

        except Exception as e:
            logger.error(f"Erro ao inserir certificado: {e}")
            if conexao:
                conexao.rollback()
            return False, str(e)
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar_projetos_do_usuario(self, id_usuario):
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor(cursor_factory=extras.RealDictCursor)

            query = """
                SELECT
                    p."idProjeto" as idprojeto,
                    p."Nome_projeto" as nome_projeto,
                    p."data_de_criacao" as data
                FROM projeto p
                JOIN usuario_da_turma ut ON p."ID_Turma" = ut."ID_Turma"
                WHERE ut."ID_Usuario" = %s
            """
            cursor.execute(query, (id_usuario,))
            projetos = cursor.fetchall()

            for p in projetos:
                if p.get('data'):
                    p['data'] = p['data'].strftime('%d/%m/%Y')
                else:
                    p['data'] = "Sem data"

            return projetos
        except Exception as e:
            logger.error(f"Falha ao listar projetos: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def excluir_certificado(self, id_certificado, id_usuario=None):
        """Exclui o certificado do banco de dados respeitando o nome exato da coluna idCertificado."""
        conn = None
        try:
            conn = conectar()
            with conn.cursor() as cursor:
                sql = """
                    DELETE FROM certificado
                    WHERE "idCertificado" = %s
                """
                cursor.execute(sql, (id_certificado,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Erro ao excluir certificado: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()