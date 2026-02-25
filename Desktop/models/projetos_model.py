from config.banco import conectar
import traceback

class ProjetoModel:
    def buscar_por_turma(self, id_turma):
        conn = None
        try:
            print(f"[MODEL PROJETOS] Buscando projetos da turma ID {id_turma}...")
            conn = conectar()
            cursor = conn.cursor()
            
            # Colunas com maiúsculas protegidas por aspas duplas
            # 'data_de_criacao' e 'projeto' parecem estar em minúsculo, mantemos assim.
            query = """
                SELECT "idProjeto", "Nome_projeto", data_de_criacao 
                FROM projeto 
                WHERE "ID_Turma" = %s
            """
            
            cursor.execute(query, (id_turma,))
            dados = cursor.fetchall()
            cursor.close()
            
            print(f"[MODEL PROJETOS] {len(dados)} projetos encontrados")
            return dados
            
        except Exception as e:
            print(f"[MODEL PROJETOS ERRO] Erro ao buscar projetos: {e}")
            # print(traceback.format_exc()) # Opcional para debug profundo
            return []
            
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass