from config.banco import conectar
import traceback

class CursosModel:
    def exibirCursos(self):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Aplicando aspas duplas nos nomes de colunas com maiúsculas/CamelCase
            # O PostgreSQL diferencia "Nome_curso" de "nome_curso"
            query = """
                SELECT 
                    "idCurso", 
                    "Nome_curso", 
                    "imagem_curso", 
                    "Descricao_curso", 
                    "Data_inicio", 
                    "Data_final" 
                FROM curso
            """
            
            cursor.execute(query)
            cursos = cursor.fetchall()
            cursor.close()
            
            return cursos
            
        except Exception as e:
            print(f"[CURSOS MODEL ERRO] {str(e)}")
            # print(traceback.format_exc()) # Opcional: descomente para ver o erro completo
            return []
            
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass