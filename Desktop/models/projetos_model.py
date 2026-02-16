from config.banco import conectar

class ProjetoModel:
    def buscar_por_turma(self, id_turma):
        try:
            conn = conectar()
            cursor = conn.cursor()
            # Usando as colunas reais: idProjeto, Nome_projeto, Caminho_do_arquivo
            query = """SELECT idProjeto, Nome_projeto, Caminho_do_arquivo, Data_de_criacao 
                       FROM projeto 
                       WHERE ID_Turma = %s"""
            cursor.execute(query, (id_turma,))
            dados = cursor.fetchall()
            conn.close()
            return dados
        except Exception as e:
            print(f"Erro ao buscar projetos no banco: {e}")
            return []

    def deletar_projeto(self, id_projeto):
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = "DELETE FROM projeto WHERE idProjeto = %s"
            cursor.execute(query, (id_projeto,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False