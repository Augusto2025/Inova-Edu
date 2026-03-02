from config.banco import conectar
import traceback

class TurmasModel:
    def buscar_por_curso(self, id_curso):
        conn = None
        try:
            print(f"[MODEL TURMAS] Buscando turmas para o curso ID {id_curso}...")
            conn = conectar()
            cursor = conn.cursor()
            
            # Aplicando aspas duplas nas colunas com maiúsculas
            # Lembre-se: no Postgres, sem aspas ele procura tudo em minúsculo
            query = """
                SELECT "idTurma", "Codigo_Turma", "Turno", "Ano" 
                FROM turma 
                WHERE "ID_Curso" = %s
            """
            
            cursor.execute(query, (id_curso,))
            dados = cursor.fetchall()
            cursor.close()
            
            print(f"[MODEL TURMAS] {len(dados)} turmas encontradas")
            return dados
            
        except Exception as e:
            print(f"[MODEL TURMAS ERRO] {str(e)}")
            # Retornamos uma lista vazia para a interface não quebrar
            return []
            
        finally:
            if conn:
                try:
                    conn.close()
                    print("[MODEL TURMAS] Conexão encerrada.")
                except:
                    pass