from models.turmas_models import TurmasModel

class TurmasController:
    def __init__(self):
        self.model = TurmasModel()

    def obter_turmas_filtradas(self, id_curso):
        if id_curso is None:
            print("ERRO: ID do curso não foi fornecido ao Controller!")
            return {}
            
        dados_brutos = self.model.buscar_por_curso(id_curso)
        turmas_agrupadas = {}

        for linha in dados_brutos:
            # Desestruturando os dados e adicionando o professor (índice 4 da linha)
            id_t, cod, turno, ano, professor = linha[0], linha[1], linha[2], str(linha[3]), linha[4]
            
            # Adicionado a chave "professor" no dicionário que a View lê
            turma_dict = {
                "id": id_t,
                "cod": cod,
                "turno": turno,
                "professor": professor, # <- O dado novo entra aqui
                "alunos": 0, 
                "cor": "#3b82f6"
            }

            if ano not in turmas_agrupadas:
                turmas_agrupadas[ano] = []
            turmas_agrupadas[ano].append(turma_dict)
            
        return turmas_agrupadas