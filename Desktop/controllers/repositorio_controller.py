from models.repositorio_model import RepositorioModel

class RepositorioController:
    def __init__(self):
        self.model = RepositorioModel()

    def listar_conteudo(self, turma_id, pasta_id=None):
        pastas_raw, arquivos_raw = self.model.buscar_conteudo(turma_id, pasta_id)
        
        # Formata as datas para o padrão brasileiro
        for p in pastas_raw:
            p['data'] = p['data'].strftime('%d/%m/%Y') if p['data'] else "---"
        
        for a in arquivos_raw:
            a['data'] = a['data'].strftime('%d/%m/%Y') if a['data'] else "---"
            
        return pastas_raw, arquivos_raw