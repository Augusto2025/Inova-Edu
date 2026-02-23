from config.banco import conectar

class ProjetoModel:
    def buscar_por_turma(self, id_turma):
        try:
            conn = conectar()
            cursor = conn.cursor()
            # Selecionando exatamente as colunas que você informou
            query = """SELECT idProjeto, Nome_projeto, data_de_criacao 
                       FROM projeto 
                       WHERE ID_Turma = %s"""
            
            cursor.execute(query, (id_turma,))
            dados = cursor.fetchall()
            conn.close()
            return dados
        except Exception as e:
            print(f"Erro ao buscar projetos no banco: {e}")
            return []