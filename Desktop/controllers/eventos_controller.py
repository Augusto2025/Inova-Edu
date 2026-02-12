# controllers/eventos_controller.py
from models.eventos_model import Eventos
import traceback

class EventosController:
    def __init__(self):
        self.eventos_model = Eventos()
    
    def obter_todos_eventos(self):
        """Busca todos os eventos"""
        try:
            print("[CONTROLLER EVENTOS] Obtendo todos os eventos...")
            eventos = self.eventos_model.obter_todos_eventos()
            return eventos
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            print(f"[CONTROLLER EVENTOS TRACEBACK] {traceback.format_exc()}")
            raise
    
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
        """Cria um novo evento"""
        try:
            print(f"[CONTROLLER EVENTOS] Criando evento: {nome}")
            if not nome or not hora or not data or not endereco:
                raise ValueError("Preencha todos os campos obrigatórios")
            
            self.eventos_model.criar_evento(nome, hora, data, descricao, endereco, id_usuario)
            return ("Evento criado com sucesso!", True)
        except Exception as e:
            print(f"[CONTROLLER EVENTOS ERRO] {str(e)}")
            print(f"[CONTROLLER EVENTOS TRACEBACK] {traceback.format_exc()}")
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
