# controllers/eventos_controller.py
from models.eventos_model import Eventos
import traceback

class EventosController:
    def __init__(self):
        self.eventos_model = Eventos()
        
        # IMPORTAÇÃO LOCAL: Evita loops de importação circular no Python
        from models.sessao import UsuarioSessao
        from models.forum_model import ForumModel
        
        sessao = UsuarioSessao()
        email_logado = sessao.email
        
        model_usuario = ForumModel()
        dados_usuario = model_usuario.obter_usuario_por_email(email_logado)
        
        if dados_usuario:
            self.id_usuario_logado = dados_usuario[0]
            self.nome_usuario_logado = dados_usuario[1]
            # ASSUMIDO: O índice [2] é o tipo/cargo do usuário no banco (ex: 'Professor')
            # Mude o número se o campo de cargo estiver em outra coluna na tabela de Usuários
            self.cargo_usuario_logado = dados_usuario[2] if len(dados_usuario) > 2 else "Aluno"
            
            print(f"[CONTROLLER EVENTOS] Usuário: {self.nome_usuario_logado} | Cargo: {self.cargo_usuario_logado}")
        else:
            # Fallback de segurança caso rode isolado
            self.id_usuario_logado = 1
            self.nome_usuario_logado = "Professor Teste"
            self.cargo_usuario_logado = "Professor"

    def e_professor(self):
        """Retorna True se o usuário logado for um Professor"""
        return str(self.cargo_usuario_logado).strip().lower() == "professor"

    def obter_todos_eventos(self):
        """Busca todos os eventos e formata em dicionários"""
        try:
            dados = self.eventos_model.obter_todos_eventos()
            lista_formatada = []
            
            for ev in dados:
                id_criador = ev[6]
                
                # REGRA: Só pode gerenciar se for o criador DO evento E for Professor
                pode_gerenciar = (id_criador == self.id_usuario_logado) and self.e_professor()
                
                lista_formatada.append({
                    "id": ev[0],
                    "nome": ev[1],
                    "hora": ev[2],
                    "data": ev[3],
                    "descricao": ev[4],
                    "endereco": ev[5],
                    "id_usuario": id_criador,
                    "pode_gerenciar": pode_gerenciar
                })
            return lista_formatada
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            return []

    def criar_evento(self, nome, hora, data, descricao, endereco):
        """Cria um novo evento limitando os tamanhos para não quebrar o Django"""
        try:
            if not self.e_professor():
                return ("Apenas professores podem criar eventos!", False)

            if not nome.strip() or not hora.strip() or not data.strip():
                return ("Nome, Data e Hora são obrigatórios!", False)
            
            # Ajustando limites baseados no seu models.Model do Django para não estourar max_length
            desc_limpa = descricao.strip()[:100] # max_length=100 no Django
            end_limpo = endereco.strip()[:30]   # max_length=30 no Django
            nome_limpo = nome.strip()[:50]     # max_length=50 no Django

            sucesso = self.eventos_model.criar_evento(
                nome_limpo, hora.strip(), data.strip(), 
                desc_limpa, end_limpo, self.id_usuario_logado
            )
            return ("Evento criado com sucesso!", True) if sucesso else ("Erro ao salvar.", False)
        except Exception as e:
            return (f"Erro: {str(e)}", False)

    def atualizar_evento(self, id_evento, nome, hora, data, descricao, endereco):
        """Edita salvando compatível com o Django"""
        try:
            if not self.e_professor():
                return ("Permissão negada!", False)

            desc_limpa = descricao.strip()[:100]
            end_limpo = endereco.strip()[:30]
            nome_limpo = nome.strip()[:50]

            sucesso = self.eventos_model.editar_evento(
                id_evento, nome_limpo, hora.strip(), data.strip(), desc_limpa, end_limpo
            )
            return ("Evento atualizado!", True) if sucesso else ("Erro ao atualizar.", False)
        except Exception as e:
            return (f"Erro: {str(e)}", False)

    def deletar_evento(self, id_evento):
        try:
            if not self.e_professor():
                return ("Permissão negada!", False)
            self.eventos_model.deletar_evento(id_evento)
            return ("Deletado!", True)
        except Exception as e:
            return (f"Erro: {str(e)}", False)