from config.banco import conectar
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, invalidate_on_write, CacheTags

class ProjetoModel:
    def buscar_por_turma(self, id_turma):
        """Busca projetos de uma turma (cache 5 min)"""
        cache_key = f"projeto:por_turma:{id_turma}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            print(f"[MODEL PROJETOS] Cache HIT - turma {id_turma}")
            return cached_value

        print(f"[MODEL PROJETOS] Cache MISS - buscando do banco turma {id_turma}")
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()

            query = """
                SELECT "idProjeto", "Imagem","Nome_projeto", data_de_criacao, "Descricao"
                FROM projeto
                WHERE "ID_Turma" = %s
            """

            cursor.execute(query, (id_turma,))
            dados = cursor.fetchall()
            cursor.close()

            print(f"[MODEL PROJETOS] {len(dados)} projetos encontrados")

            cache.set(cache_key, dados, ttl=300, tags=[CacheTags.PROJETO, CacheTags.turma_especifica(id_turma)])
            return dados

        except Exception as e:
            print(f"[MODEL PROJETOS ERRO] Erro ao buscar projetos: {e}")
            return []

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

    @invalidate_on_write(tags=[CacheTags.PROJETO])
    def criar_projeto(self, id_turma, nome, descricao, imagem=None):
        """Cria novo projeto e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projeto ("ID_Turma", "Nome_projeto", "Descricao", "Imagem", data_de_criacao)
                VALUES (%s, %s, %s, %s, CURRENT_DATE) RETURNING "idProjeto"
            """, (id_turma, nome, descricao, imagem))
            projeto_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return projeto_id
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL PROJETOS ERRO CRIAR] {e}")
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.PROJETO])
    def editar_projeto(self, id_projeto, nome, descricao, imagem=None):
        """Edita projeto e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            if imagem:
                cursor.execute("""
                    UPDATE projeto SET "Nome_projeto" = %s, "Descricao" = %s, "Imagem" = %s
                    WHERE "idProjeto" = %s
                """, (nome, descricao, imagem, id_projeto))
            else:
                cursor.execute("""
                    UPDATE projeto SET "Nome_projeto" = %s, "Descricao" = %s
                    WHERE "idProjeto" = %s
                """, (nome, descricao, id_projeto))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL PROJETOS ERRO EDITAR] {e}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.PROJETO])
    def deletar_projeto(self, id_projeto):
        """Deleta projeto e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM projeto WHERE "idProjeto" = %s', (id_projeto,))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL PROJETOS ERRO DELETAR] {e}")
            return False
        finally:
            if conn: conn.close()