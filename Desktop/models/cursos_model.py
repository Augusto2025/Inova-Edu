from config.banco import conectar
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, invalidate_on_write, CacheTags

class CursosModel:
    def exibirCursos(self):
        """Retorna todos os cursos (cache 10 min - mudam pouco)"""
        cache_key = "cursos:exibir_todos"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            print("[CURSOS MODEL] Cache HIT - exibirCursos")
            return cached_value

        print("[CURSOS MODEL] Cache MISS - buscando do banco")
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    "idCurso",
                    "Nome_curso",
                    "imagem_curso",
                    COALESCE(NULLIF(TRIM("Descricao_curso"), ''), 'Sem descrição disponivel') AS "Descricao_curso",
                    "Data_inicio",
                    "Data_final"
                FROM curso
            """

            cursor.execute(query)
            cursos = cursor.fetchall()
            cursor.close()

            # Cache por 10 minutos
            cache.set(cache_key, cursos, ttl=600, tags=[CacheTags.CURSO])
            return cursos

        except Exception as e:
            print(f"[CURSOS MODEL ERRO] {str(e)}")
            return []

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def buscar_por_id(self, id_curso):
        """Busca curso por ID (cache 10 min)"""
        cache_key = f"cursos:por_id:{id_curso}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT "idCurso", "Nome_curso", "imagem_curso", "Descricao_curso", "Data_inicio", "Data_final"
                FROM curso WHERE "idCurso" = %s
            """, (id_curso,))
            curso = cursor.fetchone()
            cursor.close()

            if curso:
                cache.set(cache_key, curso, ttl=600, tags=[CacheTags.CURSO])
            return curso
        except Exception as e:
            print(f"[CURSOS MODEL ERRO ID] {e}")
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.CURSO, CacheTags.TURMA])
    def criar_curso(self, nome, descricao, imagem, data_inicio, data_final):
        """Cria novo curso e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO curso ("Nome_curso", "Descricao_curso", "imagem_curso", "Data_inicio", "Data_final")
                VALUES (%s, %s, %s, %s, %s) RETURNING "idCurso"
            """, (nome, descricao, imagem, data_inicio, data_final))
            curso_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return curso_id
        except Exception as e:
            if conn: conn.rollback()
            print(f"[CURSOS MODEL ERRO CRIAR] {e}")
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.CURSO, CacheTags.TURMA])
    def editar_curso(self, id_curso, nome, descricao, imagem, data_inicio, data_final):
        """Edita curso e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE curso SET "Nome_curso" = %s, "Descricao_curso" = %s, "imagem_curso" = %s,
                               "Data_inicio" = %s, "Data_final" = %s
                WHERE "idCurso" = %s
            """, (nome, descricao, imagem, data_inicio, data_final, id_curso))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[CURSOS MODEL ERRO EDITAR] {e}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.CURSO, CacheTags.TURMA])
    def deletar_curso(self, id_curso):
        """Deleta curso e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM curso WHERE "idCurso" = %s', (id_curso,))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[CURSOS MODEL ERRO DELETAR] {e}")
            return False
        finally:
            if conn: conn.close()