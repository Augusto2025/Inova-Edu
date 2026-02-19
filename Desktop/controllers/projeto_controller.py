from models.projetos_model import ProjetoModel

class ProjetoController:
    def __init__(self):
        self.model = ProjetoModel()

    def listar_projetos(self, id_turma):
        dados_brutos = self.model.buscar_por_turma(id_turma)
        lista_formatada = []
        for p in dados_brutos:
            lista_formatada.append({
                "idprojeto": p[0],
                "nome_projeto": p[1],
                "descricao": p[2],
                "data": p[3].strftime('%d/%m/%Y') if p[3] else "Sem data"
            })
        return lista_formatada

    # --- NOVO MÉTODO PARA O CHECKLIST ---
    def listar_membros_permissao(self, id_projeto, id_turma):
        """
        Busca todos os alunos da turma e verifica se eles já têm
        permissão de edição no projeto (tabela projeto_alunos_edicao).
        """
        # O model deve retornar: (id_usuario, nome_usuario, tem_permissao)
        dados = self.model.buscar_alunos_com_permissao(id_projeto, id_turma)
        membros = []
        for d in dados:
            membros.append({
                "id": d[0],
                "nome": d[1],
                "tem_permissao": bool(d[2]) # Converte 1 ou 0 para True/False
            })
        return membros

    # --- NOVO MÉTODO PARA SALVAR O CHECKLIST ---
    def atualizar_permissoes(self, id_projeto, lista_ids_selecionados):
        """
        Sincroniza a tabela de junção do MySQL com os IDs selecionados no modal.
        """
        return self.model.sincronizar_alunos_edicao(id_projeto, lista_ids_selecionados)

    def excluir_projeto(self, id_projeto):
        return self.model.deletar_projeto(id_projeto)
    
    def obter_membros_com_status_edicao(self, id_projeto, id_turma):
        dados = self.model.buscar_alunos_com_status_edicao(id_projeto, id_turma)
        membros = []
        for d in dados:
            membros.append({
                "id_usuario": d[0],
                "nome_usuario": d[1],
                "pode_editar": bool(d[2])
            })
        return membros

    # NOME SINCRONIZADO COM O BOTÃO SALVAR DA VIEW
    def atualizar_acessos(self, id_projeto, lista_ids_selecionados):
        return self.model.salvar_permissoes_projeto(id_projeto, lista_ids_selecionados)