from models.forum_model import ForumModel

class ForumController:
    def __init__(self):
        self.model = ForumModel()
        
        # IMPORTAÇÃO LOCAL: Mantida aqui dentro para o Python carregar o ForumModel primeiro sem dar loop
        from models.sessao import UsuarioSessao
        
        # 1. Recupera a instância da sessão global iniciada no login
        sessao = UsuarioSessao()
        email_logado = sessao.email
        
        # 2. Busca dinamicamente no banco o ID e Nome vinculados a esse e-mail
        dados_usuario = self.model.obter_usuario_por_email(email_logado)
        
        if dados_usuario:
            self.id_usuario_logado = dados_usuario[0]  # idUsuario do banco
            self.nome_usuario_logado = dados_usuario[1] # Nome do banco
            print(f"[CONTROLLER FORUM] Sessão vinculada a: {self.nome_usuario_logado} (ID: {self.id_usuario_logado})")
        else:
            # Fallback de segurança (caso tente rodar a tela isolada sem passar pelo login)
            self.id_usuario_logado = 1 
            self.nome_usuario_logado = "Sistema"
            print("[CONTROLLER FORUM AVISO] E-mail da sessão inválido ou vazio. Usando ID padrão 1.")

    def listar_foruns(self):
        dados = self.model.obter_todos_foruns()
        return [{"idforum": f[0], "nome": f[1], "data_criacao": f[2]} for f in dados]

    def listar_topicos(self, id_forum):
        dados = self.model.obter_topicos_por_forum(id_forum)
        return [{"idtopico": t[0], "forum_id": t[1], "titulo": t[2], "descricao": t[3]} for t in dados]

    def listar_mensagens(self, id_topico):
        dados = self.model.obter_mensagens_por_topico(id_topico)
        return [{"id": m[0], "conteudo": m[1], "data_criacao": m[2], "autor_nome": m[3]} for m in dados]

    def cadastrar_forum(self, nome):
        """Cria apenas o fórum no banco usando o ID dinâmico, sem tópicos adicionais automaticos"""
        if not nome or not nome.strip():
            return False
        
        id_novo_forum = self.model.criar_forum(nome.strip(), self.id_usuario_logado)
        
        # Retorna True se o banco inseriu com sucesso e gerou um ID válido
        if id_novo_forum is not None:
            return True
        return False

    def cadastrar_topico(self, id_forum, titulo):
        if not titulo or not titulo.strip():
            return False
        return self.model.criar_topico(id_forum, titulo.strip(), "", self.id_usuario_logado) is not None

    def enviar_mensagem(self, id_topico, conteudo):
        if not conteudo or not conteudo.strip():
            return False
        return self.model.criar_mensagem(id_topico, self.id_usuario_logado, conteudo.strip())