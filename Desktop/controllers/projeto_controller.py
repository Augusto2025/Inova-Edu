from models.projetos_model import ProjetoModel

class ProjetoController:
    def __init__(self):
        self.model = ProjetoModel()

    def listar_projetos(self, id_turma):
        dados_brutos = self.model.buscar_por_turma(id_turma)
        lista_formatada = []
        
        for p in dados_brutos:
            # p[0] = idProjeto
            # p[1] = Imagem
            # p[2] = Nome_projeto
            # p[3] = data_de_criacao
            # p[4] = Descricao
            lista_formatada.append({
                "idprojeto": p[0],
                "imagem": p[1],
                "nome_projeto": p[2],
                "data": p[3].strftime('%d/%m/%Y') if p[3] else "Sem data",
                "descricao": p[4]
            })
        return lista_formatada