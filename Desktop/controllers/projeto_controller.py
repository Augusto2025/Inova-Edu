from models.projetos_model import ProjetoModel

class ProjetoController:
    def __init__(self):
        self.model = ProjetoModel()

    def listar_projetos(self, id_turma):
        dados_brutos = self.model.buscar_por_turma(id_turma)
        lista_formatada = []
        
        for p in dados_brutos:
            lista_formatada.append({
                "id": p[0],
                "nome": p[1],
                "caminho": p[2], # Caminho_do_arquivo (ex: link do GitHub ou pasta)
                "data": p[3].strftime('%d/%m/%Y') if p[3] else "Sem data"
            })
        return lista_formatada

    def excluir_projeto(self, id_projeto):
        return self.model.deletar_projeto(id_projeto)
    
    def usuario_eh_professor(self):
        # Aqui você deve acessar onde guardou os dados do login (ex: Session)
        # Exemplo hipotético:
        from models.login_model import exibir_usuarios
        return exibir_usuarios().get("tipo") == "Professor"