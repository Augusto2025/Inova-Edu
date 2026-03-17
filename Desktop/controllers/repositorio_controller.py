from models.repositorio_model import RepositorioModel

class RepositorioController:
    def __init__(self):
        self.model = RepositorioModel()

    def listar_conteudo(self, projeto_id, pasta_id=None):
        # Certifique-se de que o Model está recebendo o ID correto do projeto
        pastas_raw, arquivos_raw = self.model.buscar_conteudo(projeto_id, pasta_id)
        
        # Formata as datas para o padrão brasileiro
        # Usamos try/except ou verificamos se é um objeto datetime para evitar erro no strftime
        for p in pastas_raw:
            if hasattr(p['data'], 'strftime'):
                p['data'] = p['data'].strftime('%d/%m/%Y')
            else:
                p['data'] = "---"
        
        for a in arquivos_raw:
            if hasattr(a['data'], 'strftime'):
                a['data'] = a['data'].strftime('%d/%m/%Y')
            else:
                a['data'] = "---"
            
        return pastas_raw, arquivos_raw