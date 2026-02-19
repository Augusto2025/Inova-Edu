from models.projetos_model import ProjetoModel

class ProjetoController:
    def __init__(self):
        self.model = ProjetoModel()

    def listar_projetos(self, id_turma):
        dados_brutos = self.model.buscar_por_turma(id_turma)
        lista_formatada = []
        
        for p in dados_brutos:
            # p[0] = idProjeto
            # p[1] = Nome_projeto
            # p[2] = data_de_criacao
            lista_formatada.append({
                "idprojeto": p[0],
                "nome_projeto": p[1],
                "data": p[2].strftime('%d/%m/%Y') if p[2] else "Sem data"
            })
        return lista_formatada