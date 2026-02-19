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
            id_t, cod, turno, ano = linha[0], linha[1], linha[2], str(linha[3])
            
            # Criamos o dicionário que a View já sabe ler
            turma_dict = {
                "id": id_t,
                "cod": cod,
                "turno": turno,
                "alunos": 0, # Se tiver tabela de matrícula, faria um count aqui
                "cor": "#3b82f6"
            }

            if ano not in turmas_agrupadas:
                turmas_agrupadas[ano] = []
            turmas_agrupadas[ano].append(turma_dict)
            
        return turmas_agrupadas