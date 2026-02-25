from config.banco import conectar
from psycopg2.extras import RealDictCursor
import traceback

class RepositorioModel:
    def buscar_conteudo(self, projeto_id, pasta_pai_id=None):
        conn = None
        try:
            conn = conectar()
            # RealDictCursor faz o resultado virar um dicionário (ex: pasta['nome'])
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # 1. Buscar Pastas (Baseado no print da tabela 'pasta')
            # Alterado: p.turma_id -> p.projeto_id
            query_pastas = """
                SELECT p.id, p.nome, COALESCE(u."Nome", 'Sistema') as autor, p.criada_em as data
                FROM pasta p
                LEFT JOIN usuario u ON p.criada_por_id = u."idUsuario"
                WHERE p.projeto_id = %s AND p.pasta_pai_id IS NOT DISTINCT FROM %s
            """
            cursor.execute(query_pastas, (projeto_id, pasta_pai_id))
            pastas = cursor.fetchall()

            # 2. Buscar Arquivos (Baseado no print da tabela 'arquivo')
            # Alterado: a.turma_id -> a.projeto_id
            query_arquivos = """
                SELECT a.id, a.nome, COALESCE(u."Nome", 'Sistema') as autor, a.enviado_em as data, a.url
                FROM arquivo a
                LEFT JOIN usuario u ON a.enviado_por_id = u."idUsuario"
                WHERE a.projeto_id = %s AND a.pasta_id IS NOT DISTINCT FROM %s
            """
            cursor.execute(query_arquivos, (projeto_id, pasta_pai_id))
            arquivos = cursor.fetchall()

            return pastas, arquivos

        except Exception as e:
            print(f"[REPOSITORIO MODEL ERRO]: {e}")
            traceback.print_exc()
            return [], []
            
        finally:
            if conn:
                conn.close()