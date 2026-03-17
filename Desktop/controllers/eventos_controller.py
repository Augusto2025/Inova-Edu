# controllers/eventos_controller.py
from models.eventos_model import Eventos
import traceback

class EventosController:
    def __init__(self):
        self.eventos_model = Eventos()
    
    def obter_todos_eventos(self):
        """Busca todos os eventos e garante retorno seguro para a View"""
        try:
            print("[CONTROLLER EVENTOS] Obtendo todos os eventos...")
            eventos = self.eventos_model.obter_todos_eventos()
            
            # Garante que se o model retornar None por algum motivo, a View receba uma lista
            return eventos if eventos else []
            
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            # Retorna lista vazia para o calendário não quebrar ao tentar iterar
            return []
    
    def obter_evento_por_id(self, id_evento):
        """Busca um evento específico"""
        try:
            print(f"[CONTROLLER EVENTOS] Obtendo evento ID {id_evento}...")
            evento = self.eventos_model.obter_evento_por_id(id_evento)
            return evento
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            print(f"[CONTROLLER EVENTOS TRACEBACK] {traceback.format_exc()}")
            raise
    
    def obter_eventos_do_usuario(self, id_usuario):
        """Busca eventos de um usuário"""
        try:
            print(f"[CONTROLLER EVENTOS] Obtendo eventos do usuário {id_usuario}...")
            eventos = self.eventos_model.obter_eventos_por_usuario(id_usuario)
            return eventos
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            print(f"[CONTROLLER EVENTOS TRACEBACK] {traceback.format_exc()}")
            raise
    
    def criar_evento(self, nome, hora, data, descricao, endereco, id_usuario):
        """Cria um novo evento com validação de dados"""
        try:
            print(f"[CONTROLLER EVENTOS] Criando evento: {nome}")
            
            # Validação: CustomTkinter .get() pode retornar string vazia
            if not nome.strip() or not hora.strip() or not data.strip():
                return ("Nome, Data e Hora são obrigatórios!", False)
            
            self.eventos_model.criar_evento(nome, hora, data, descricao, endereco, id_usuario)
            return ("Evento criado com sucesso!", True)
            
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            return (f"Erro ao criar evento: {str(e)}", False)
    
    def deletar_evento(self, id_evento):
        """Deleta um evento"""
        try:
            print(f"[CONTROLLER EVENTOS] Deletando evento {id_evento}...")
            self.eventos_model.deletar_evento(id_evento)
            return ("Evento deletado com sucesso!", True)
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            print(f"[CONTROLLER EVENTOS TRACEBACK] {traceback.format_exc()}")
            return (f"Erro ao deletar evento: {str(e)}", False)
