# controllers/eventos_controller.py
from models.eventos_model import Eventos
from config.banco import conectar  # Importação correta da função de conexão do seu projeto
import traceback

class EventosController:
    def __init__(self):
        self.eventos_model = Eventos()
        
        # IMPORTAÇÃO LOCAL DA SESSÃO
        from models.sessao import UsuarioSessao
        
        sessao = UsuarioSessao()
        self.email_logado = str(sessao.email).strip() if (sessao and hasattr(sessao, 'email') and sessao.email) else ""
        
        # Valores padrão de segurança (caso não encontre a sessão)
        self.id_usuario_logado = None
        self.nome_usuario_logado = "Visitante"
        self.cargo_usuario_logado = "aluno"

        # SE O EMAIL ESTIVER VAZIO (Ambiente de desenvolvimento local),
        # forçamos como Professor para você conseguir testar sem barreiras
        if not self.email_logado or self.email_logado == "None":
            self.id_usuario_logado = 2  # ID do Alcides
            self.nome_usuario_logado = "Alcides (Desenvolvimento)"
            self.cargo_usuario_logado = "professor"
            print("[EVENTOS SECURITY] Sem sessão ativa. Modo Desenvolvedor: Acesso de Professor Liberado.")
        else:
            conn = None
            try:
                # Chamando a função do seu projeto para obter a conexão
                conn = conectar()
                with conn.cursor() as cursor:
                    # Buscando exatamente pelos nomes de colunas que vimos no seu Django Model
                    sql = 'SELECT "idUsuario", "Nome", "Tipo" FROM usuario WHERE "Email" = %s'
                    cursor.execute(sql, (self.email_logado,))
                    dados_usuario = cursor.fetchone()
                    
                    print(f"[EVENTOS SECURITY] Dados vindos do banco: {dados_usuario}")
                    
                    if dados_usuario:
                        self.id_usuario_logado = dados_usuario[0]
                        self.nome_usuario_logado = dados_usuario[1]
                        # Captura a string da coluna 'Tipo' mapeada pelo Django
                        self.cargo_usuario_logado = str(dados_usuario[2]).strip().lower()
                        
            except Exception as e:
                print(f"[ERRO CRITICAL SECURITY] Falha ao ler a tabela usuario: {e}")
            finally:
                if conn:
                    conn.close()

        print(f"[FINAL ACCESS LEVEL] Usuário: {self.nome_usuario_logado} | Tipo: {self.cargo_usuario_logado}")

    def e_professor(self):
        """Retorna True se o tipo de usuário for Professor"""
        if self.cargo_usuario_logado in ["professor", "prof", "docente"]:
            return True
        if "professor" in self.email_logado.lower() or "prof" in self.email_logado.lower():
            return True
        return False

    def obter_todos_eventos(self):
        """Mapeado com 'r' perfeitamente para corresponder à View"""
        try:
            dados = self.eventos_model.obter_todos_eventos()
            lista_formatada = []
            usuario_e_professor = self.e_professor()
            
            for ev in dados:
                lista_formatada.append({
                    "id": ev[0],
                    "nome": ev[1],
                    "hora": ev[2],
                    "data": ev[3],
                    "descricao": ev[4],
                    "endereco": ev[5],
                    "id_usuario": ev[6],
                    "pode_gerenciar": usuario_e_professor 
                })
            return lista_formatada
        except Exception as e:
            print(f"[ERRO SQL CONTROLLER] {str(e)}")
            return []

    def criar_evento(self, nome, hora, data, descricao, endereco):
        try:
            if not self.e_professor(): return ("Acesso negado", False)
            sucesso = self.eventos_model.criar_evento(
                nome.strip()[:50], hora.strip(), data.strip(), 
                descricao.strip()[:100], endereco.strip()[:30], self.id_usuario_logado
            )
            return ("Sucesso", True) if sucesso else ("Erro", False)
        except Exception as e: return (str(e), False)

    def atualizar_evento(self, id_evento, nome, hora, data, descricao, endereco):
        try:
            if not self.e_professor(): return ("Acesso negado", False)
            sucesso = self.eventos_model.editar_evento(
                id_evento, nome.strip()[:50], hora.strip(), data.strip(), 
                descricao.strip()[:100], endereco.strip()[:30]
            )
            return ("Sucesso", True) if sucesso else ("Erro", False)
        except Exception as e: return (str(e), False)

    def deletar_evento(self, id_evento):
        try:
            if not self.e_professor(): return ("Acesso negado", False)
            self.eventos_model.deletar_evento(id_evento)
            return ("Sucesso", True)
        except Exception as e: return (str(e), False)