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

    def salvar_certificado(self, nome, descricao, data_inicio, data_final, usuario_id):
        conexao = None
        cursor = None
        try:
            conexao = conectar() # Sua função de conexão que já funciona
            cursor = conexao.cursor()
            
            # Query usando os nomes das colunas que vimos na sua foto anterior
            query = """
                INSERT INTO certificado (nome, descricao, data_inicio, data_final, usuario_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            # Executa a inserção
            cursor.execute(query, (nome, descricao, data_inicio, data_final, usuario_id))
            
            # IMPORTANTE: No Postgres, você precisa dar COMMIT para salvar de fato
            conexao.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao inserir no banco: {e}")
            if conexao:
                conexao.rollback() # Cancela se der erro
            return False
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar_projetos_do_usuario(self, id_usuario):
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor(cursor_factory=extras.RealDictCursor)
            
            # Ajustando para "Data_criacao" (seguindo a lógica do Nome_projeto)
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
            # Se der erro de novo, o print abaixo vai te mostrar os nomes reais das colunas
            print(f"[BANCO ERRO] Falha ao listar projetos: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()