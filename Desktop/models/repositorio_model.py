from config.banco import conectar
from psycopg2.extras import RealDictCursor
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, cached, invalidate_on_write, CacheTags

class RepositorioModel:
    def buscar_conteudo(self, projeto_id, pasta_pai_id=None):
        """Busca pastas e arquivos com cache (TTL 2 min)"""
        return self._buscar_conteudo_cached(projeto_id, pasta_pai_id)

    @cached(ttl=120, tags=[CacheTags.REPOSITORIO, CacheTags.projeto_especifico(0)], key_prefix="repo")
    def _buscar_conteudo_cached(self, projeto_id, pasta_pai_id=None):
        """Implementação real com cache automático"""
        # Nota: O decorator @cached usa os args para gerar a chave
        # Mas tags dinâmicas precisam de tratamento especial
        projeto_id = int(projeto_id)

        # Atualiza tags dinamicamente para este projeto específico
        cache_key = f"repo:buscar_conteudo:{projeto_id}:{pasta_pai_id}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # 1. Buscar Pastas
            query_pastas = """
                SELECT p.id, p.nome, COALESCE(u."Nome", 'Sistema') as autor, p.criada_em as data
                FROM pasta p
                LEFT JOIN usuario u ON p.criada_por_id = u."idUsuario"
                WHERE p.projeto_id = %s AND p.pasta_pai_id IS NOT DISTINCT FROM %s
            """
            cursor.execute(query_pastas, (projeto_id, pasta_pai_id))
            pastas = cursor.fetchall()

            # 2. Buscar Arquivos
            query_arquivos = """
                SELECT a.id, a.nome, COALESCE(u."Nome", 'Sistema') as autor, a.enviado_em as data, a.url
                FROM arquivo a
                LEFT JOIN usuario u ON a.enviado_por_id = u."idUsuario"
                WHERE a.projeto_id = %s AND a.pasta_id IS NOT DISTINCT FROM %s
            """
            cursor.execute(query_arquivos, (projeto_id, pasta_pai_id))
            arquivos = cursor.fetchall()

            result = (pastas, arquivos)

            # Cacheia com tag específica do projeto
            cache.set(cache_key, result, ttl=120, tags=[
                CacheTags.REPOSITORIO,
                CacheTags.projeto_especifico(projeto_id)
            ])
            return result

        except Exception as e:
            print(f"[REPOSITORIO MODEL ERRO]: {e}")
            traceback.print_exc()
            return [], []

        finally:
            if conn:
                conn.close()

    # Métodos de escrita - invalidam cache
    @invalidate_on_write(tags=[CacheTags.REPOSITORIO])
    def criar_pasta(self, projeto_id, nome, pasta_pai_id, usuario_id):
        """Cria nova pasta e invalida cache do repositório"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pasta (projeto_id, nome, pasta_pai_id, criada_por_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (projeto_id, nome, pasta_pai_id, usuario_id))
            nova_pasta_id = cursor.fetchone()[0]
            conn.commit()
            return nova_pasta_id
        except Exception as e:
            if conn: conn.rollback()
            print(f"[REPOSITORIO MODEL ERRO CRIAR PASTA]: {e}")
            traceback.print_exc()
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.REPOSITORIO])
    def criar_arquivo(self, projeto_id, nome, url, pasta_id, usuario_id):
        """Cria novo arquivo e invalida cache do repositório"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO arquivo (projeto_id, nome, url, pasta_id, enviado_por_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (projeto_id, nome, url, pasta_id, usuario_id))
            novo_arquivo_id = cursor.fetchone()[0]
            conn.commit()
            return novo_arquivo_id
        except Exception as e:
            if conn: conn.rollback()
            print(f"[REPOSITORIO MODEL ERRO CRIAR ARQUIVO]: {e}")
            traceback.print_exc()
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.REPOSITORIO])
    def deletar_pasta(self, pasta_id):
        """Deleta pasta e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pasta WHERE id = %s', (pasta_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[REPOSITORIO MODEL ERRO DELETAR PASTA]: {e}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.REPOSITORIO])
    def deletar_arquivo(self, arquivo_id):
        """Deleta arquivo e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM arquivo WHERE id = %s', (arquivo_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[REPOSITORIO MODEL ERRO DELETAR ARQUIVO]: {e}")
            return False
        finally:
            if conn: conn.close()