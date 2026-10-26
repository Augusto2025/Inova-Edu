from config.banco import conectar
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import cache, invalidate_on_write, CacheTags

class TurmasModel:
    def buscar_por_curso(self, id_curso):
        """Busca turmas de um curso (cache 5 min)"""
        cache_key = f"turma:por_curso:{id_curso}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            print(f"[MODEL TURMAS] Cache HIT - curso {id_curso}")
            return cached_value

        print(f"[MODEL TURMAS] Cache MISS - buscando do banco curso {id_curso}")
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    t."idTurma",
                    t."Codigo_Turma",
                    t."Turno",
                    t."Ano",
                    COALESCE(u."Nome", 'Sem Professor Designado') AS nome_professor
                FROM turma t
                LEFT JOIN usuario u ON t.professor_id = u."idUsuario"
                WHERE t."ID_Curso" = %s
            """

            cursor.execute(query, (id_curso,))
            dados = cursor.fetchall()
            cursor.close()

            print(f"[MODEL TURMAS] {len(dados)} turmas encontradas")

            cache.set(cache_key, dados, ttl=300, tags=[CacheTags.TURMA, CacheTags.CURSO])
            return dados

        except Exception as e:
            print(f"[MODEL TURMAS ERRO] {str(e)}")
            traceback.print_exc()
            return []

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def buscar_por_professor(self, professor_id):
        """Busca turmas de um professor (cache 5 min)"""
        cache_key = f"turma:por_professor:{professor_id}"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t."idTurma", t."Codigo_Turma", t."Turno", t."Ano", c."Nome_Curso"
                FROM turma t
                JOIN curso c ON t."ID_Curso" = c."idCurso"
                WHERE t.professor_id = %s
            """, (professor_id,))
            dados = cursor.fetchall()
            cursor.close()

            cache.set(cache_key, dados, ttl=300, tags=[CacheTags.TURMA, CacheTags.usuario_especifico(professor_id)])
            return dados
        except Exception as e:
            print(f"[MODEL TURMAS ERRO PROF] {str(e)}")
            return []
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.TURMA, CacheTags.CURSO])
    def criar_turma(self, id_curso, codigo, turno, ano, professor_id=None):
        """Cria nova turma e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO turma ("ID_Curso", "Codigo_Turma", "Turno", "Ano", professor_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING "idTurma"
            """, (id_curso, codigo, turno, ano, professor_id))
            turma_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return turma_id
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL TURMAS ERRO CRIAR] {e}")
            return None
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.TURMA, CacheTags.CURSO])
    def editar_turma(self, id_turma, codigo, turno, ano, professor_id=None):
        """Edita turma e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE turma SET "Codigo_Turma" = %s, "Turno" = %s, "Ano" = %s, professor_id = %s
                WHERE "idTurma" = %s
            """, (codigo, turno, ano, professor_id, id_turma))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL TURMAS ERRO EDITAR] {e}")
            return False
        finally:
            if conn: conn.close()

    @invalidate_on_write(tags=[CacheTags.TURMA, CacheTags.CURSO])
    def deletar_turma(self, id_turma):
        """Deleta turma e invalida cache"""
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM turma WHERE "idTurma" = %s', (id_turma,))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            print(f"[MODEL TURMAS ERRO DELETAR] {e}")
            return False
        finally:
            if conn: conn.close()