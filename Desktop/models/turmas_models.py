from config.banco import conectar
import traceback

class TurmasModel:
    def buscar_por_curso(self, id_curso):
        conn = None
        try:
            print(f"[MODEL TURMAS] Buscando turmas para o curso ID {id_curso}...")
            conn = conectar()
            cursor = conn.cursor()
            
            # Adicionado o LEFT JOIN para pegar o nome do professor
            # Caso a turma não tenha professor, usamos COALESCE para exibir "Sem Professor"
            # Mude apenas a string da QUERY dentro do seu arquivo turmas_models.py
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
            return dados
            
        except Exception as e:
            print(f"[MODEL TURMAS ERRO] {str(e)}")
            traceback.print_exc() # Ajuda a ver no terminal se o nome da coluna do join estiver errado
            return []
            
        finally:
            if conn:
                try:
                    conn.close()
                    print("[MODEL TURMAS] Conexão encerrada.")
                except:
                    pass