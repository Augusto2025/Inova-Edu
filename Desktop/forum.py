import customtkinter as ctk
from datetime import datetime
import tkinter.messagebox as messagebox
import re

# Configuração de cores moderna
CORES = {
    "primaria": "#4361ee",      # Azul vibrante
    "secundaria": "#3f37c9",     # Azul escuro
    "destaque": "#4cc9f0",       # Azul claro
    "sucesso": "#06d6a0",        # Verde
    "aviso": "#ffd166",          # Amarelo
    "perigo": "#ef476f",         # Rosa/vermelho
    "fundo": "#f8f9fa",          # Cinza muito claro
    "card": "#ffffff",            # Branco
    "texto_primario": "#212529", # Quase preto
    "texto_secundario": "#6c757d", # Cinza
    "borda": "#dee2e6",           # Cinza claro
    "mencao": "#1e88e5",           # Azul para menções
    "mencao_fundo": "#e3f2fd"      # Fundo azul claro para menções
}

class ForumApp:
    def __init__(self, master=None):
        self.master = master if master else ctk.CTk()
        self.master.title("Fórum de Discussões")
        self.master.geometry("1300x800")
        
        self.ui_built = False
        self.current_forum_index = 0
        self.current_topic_index = 0
        self.view_mode = "topics"
        
        # Dados dos fóruns
        self.forums = [
            {
                "name": "Administrador de redes",
                "description": "Discussões sobre administração de redes, protocolos e equipamentos",
                "created": "20/03/2025",
                "icon": "🌐",
                "topics": [
                    {
                        "title": "Configuração de OSPF",
                        "author": "Lucas Amaral",
                        "created": "20/03/2025",
                        "replies": 4,
                        "views": 45,
                        "last_message": "12:20",
                        "messages": [
                            {"author": "Lucas Amaral", "message": "Galera, lembrando que amanhã é a apresentação dos projetos. @carla você já terminou a topologia?", "time": "12:15"},
                            {"author": "Carla Souza", "message": "Quase! @lucas estou finalizando o OSPF ainda. Mais alguém usando?", "time": "12:17"},
                            {"author": "Vinícius Junior", "message": "Eu! @carla só travando no balanceamento de carga. 😊", "time": "12:17"},
                            {"author": "Diego Maradona", "message": "@vinicius fiz isso ontem. Posso te mandar o exemplo!", "time": "12:18"},
                            {"author": "Ana", "message": "Meu foco é segurança com VLANs. @lucas configurei DHCP snooping e port security 🛡️", "time": "12:20"}
                        ]
                    },
                    {
                        "title": "Balanceamento de carga",
                        "author": "Vinícius Junior",
                        "created": "21/03/2025",
                        "replies": 1,
                        "views": 12,
                        "last_message": "09:30",
                        "messages": [
                            {"author": "Vinícius Junior", "message": "Alguém tem experiência com balanceamento de carga em redes corporativas? @carla você conhece?", "time": "09:15"},
                            {"author": "Carla Souza", "message": "@vinicius Uso o HAProxy aqui, muito bom!", "time": "09:30"}
                        ]
                    }
                ]
            },
            {
                "name": "Suporte e manutenção de notebooks",
                "description": "Reparo, manutenção e suporte para notebooks",
                "created": "12/01/2025",
                "icon": "💻",
                "topics": []
            },
            {
                "name": "Segurança da informação",
                "description": "Firewalls, VLANs e políticas de segurança",
                "created": "28/05/2025",
                "icon": "🔒",
                "topics": []
            }
        ]
        
        self.build_ui()
    
    def build_ui(self):
        """Constrói a interface do fórum"""
        if self.ui_built:
            return
        
        self.ui_built = True
        
        # Frame principal com fundo suave
        main_frame = ctk.CTkFrame(self.master, fg_color=CORES["fundo"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header decorativo
        self.build_header(main_frame)
        
        # Conteúdo principal (2 colunas)
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=3)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Coluna esquerda - Lista de fóruns
        self.build_left_column(content_frame)
        
        # Coluna direita - Conteúdo
        self.build_right_column(content_frame)
        
        # Carregar dados
        self.load_forums_list()
        if self.forums:
            self.load_forum(0)
    
    def build_header(self, parent):
        """Header estilizado"""
        header = ctk.CTkFrame(parent, fg_color=CORES["primaria"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Título com ícone
        titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
        titulo_frame.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            titulo_frame,
            text="💬",
            font=ctk.CTkFont(size=32),
            text_color="white"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            titulo_frame,
            text="Fórum de Discussões",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(side="left")
        
        # Badge de estatísticas
        stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        stats_frame.pack(side="right", padx=30)
        
        total_foruns = len(self.forums)
        total_topics = sum(len(f["topics"]) for f in self.forums)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"📌 {total_foruns} fóruns  |  💬 {total_topics} tópicos",
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack()
    
    def build_left_column(self, parent):
        """Coluna esquerda com lista de fóruns"""
        left_column = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Título da seção
        title_frame = ctk.CTkFrame(left_column, fg_color="transparent", height=60)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="📋 FÓRUNS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(side="left")
        
        # Barra de pesquisa
        self.search_entry = ctk.CTkEntry(
            left_column,
            placeholder_text="🔍 Buscar fóruns...",
            height=40,
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=10
        )
        self.search_entry.pack(fill="x", padx=20, pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.search_forums)
        
        # Lista de fóruns
        self.forums_list_frame = ctk.CTkScrollableFrame(
            left_column,
            fg_color="transparent",
            scrollbar_button_color=CORES["texto_secundario"]
        )
        self.forums_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Botão Criar Fórum
        self.create_forum_btn = ctk.CTkButton(
            left_column,
            text="+ Novo Fórum",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color="#05b586",
            corner_radius=10,
            command=self.criar_novo_forum
        )
        self.create_forum_btn.pack(pady=20, padx=20)
    
    def build_right_column(self, parent):
        """Coluna direita com conteúdo"""
        self.right_column = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        self.right_column.grid(row=0, column=1, sticky="nsew")
        self.right_column.grid_columnconfigure(0, weight=1)
        self.right_column.grid_rowconfigure(1, weight=1)
        
        # ===== ÁREA DE NAVEGAÇÃO (BOTÃO VOLTAR) =====
        self.nav_frame = ctk.CTkFrame(self.right_column, fg_color="transparent", height=50)
        self.nav_frame.pack(fill="x", padx=25, pady=(15, 5))
        self.nav_frame.pack_propagate(False)
        
        # Botão Voltar
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Voltar para tópicos",
            width=140,
            height=35,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["primaria"],
            border_width=1,
            border_color=CORES["primaria"],
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=20,
            command=self.show_topics_view
        )
        
        # ===== HEADER DO CONTEÚDO =====
        self.header_frame = ctk.CTkFrame(self.right_column, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=25, pady=(5, 10))
        
        # Título atual
        self.current_title = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["texto_primario"]
        )
        self.current_title.pack(side="left")
        
        # Badge de contexto
        self.context_badge = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=CORES["destaque"],
            text_color="white",
            corner_radius=12,
            width=70,
            height=24
        )
        
        # Descrição
        self.description_label = ctk.CTkLabel(
            self.right_column,
            text="",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color=CORES["texto_secundario"]
        )
        self.description_label.pack(anchor="w", padx=30, pady=(0, 15))
        
        # Separador decorativo
        separator = ctk.CTkFrame(self.right_column, height=2, fg_color=CORES["borda"])
        separator.pack(fill="x", padx=30, pady=(0, 15))
        
        # ===== ÁREA DE CONTEÚDO =====
        self.content_frame = ctk.CTkScrollableFrame(
            self.right_column,
            fg_color="transparent",
            scrollbar_button_color=CORES["texto_secundario"]
        )
        self.content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # ===== BOTÃO NOVO TÓPICO =====
        self.new_topic_btn = ctk.CTkButton(
            self.right_column,
            text="+ Novo Tópico",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color="#05b586",
            corner_radius=10,
            command=self.criar_novo_topico
        )
        
        # ===== ÁREA DE RESPOSTA =====
        self.reply_frame = ctk.CTkFrame(self.right_column, fg_color="transparent")
        self.reply_frame.pack(fill="x", padx=25, pady=(0, 20))
        self.reply_frame.pack_forget()
        
        # Campo de texto
        self.reply_entry = ctk.CTkTextbox(
            self.reply_frame,
            height=80,
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        self.reply_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.reply_entry.insert("1.0", "Digite sua resposta...")
        
        # Botão Enviar
        self.send_btn = ctk.CTkButton(
            self.reply_frame,
            text="Enviar",
            width=100,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=CORES["primaria"],
            hover_color=CORES["secundaria"],
            corner_radius=10,
            command=self.send_message
        )
        self.send_btn.pack(side="right")
        
        # Eventos do campo de resposta
        self.reply_entry.bind("<FocusIn>", self.clear_reply_placeholder)
        self.reply_entry.bind("<FocusOut>", self.restore_reply_placeholder)
    
    # ========== FUNÇÕES DOS FÓRUNS ==========
    def load_forums_list(self):
        """Carrega a lista de fóruns"""
        for widget in self.forums_list_frame.winfo_children():
            widget.destroy()
        
        for i, forum in enumerate(self.forums):
            self.create_forum_card(forum, i)
    
    def create_forum_card(self, forum, index):
        """Cria um card de fórum com botões de editar e excluir"""
        is_selected = index == self.current_forum_index
        
        card = ctk.CTkFrame(
            self.forums_list_frame,
            fg_color="white" if not is_selected else "#e8f0fe",
            corner_radius=12,
            border_width=1,
            border_color=CORES["borda"] if not is_selected else CORES["primaria"],
        )
        card.pack(fill="x", pady=(0, 10))
        card.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Linha superior: ícone, nome e contador
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=12, pady=(12, 5))
        
        # Ícone
        icon_label = ctk.CTkLabel(
            top_frame,
            text=forum.get("icon", "📁"),
            font=ctk.CTkFont(size=16)
        )
        icon_label.pack(side="left", padx=(0, 8))
        icon_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Nome
        name_label = ctk.CTkLabel(
            top_frame,
            text=forum["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        )
        name_label.pack(side="left")
        name_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Contador de tópicos
        topic_count = len(forum["topics"])
        count_badge = ctk.CTkLabel(
            top_frame,
            text=f"{topic_count} 📌",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=CORES["destaque"] if topic_count > 0 else CORES["borda"],
            text_color="white" if topic_count > 0 else CORES["texto_secundario"],
            corner_radius=10,
            width=40,
            height=20
        )
        count_badge.pack(side="right")
        
        # Descrição resumida
        desc_text = forum["description"][:35] + "..." if len(forum["description"]) > 35 else forum["description"]
        desc_label = ctk.CTkLabel(
            card,
            text=desc_text,
            font=ctk.CTkFont(size=11),
            text_color=CORES["texto_secundario"]
        )
        desc_label.pack(anchor="w", padx=12)
        desc_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Linha de ações: data e botões
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=12, pady=(8, 12))
        
        # Data de criação
        date_label = ctk.CTkLabel(
            actions_frame,
            text=f"Criado: {forum['created']}",
            font=ctk.CTkFont(size=10),
            text_color=CORES["texto_secundario"]
        )
        date_label.pack(side="left")
        
        # Botões de ação
        btns_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btns_frame.pack(side="right")
        
        # Botão Editar
        edit_btn = ctk.CTkButton(
            btns_frame,
            text="✏️ Editar",
            width=70,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=12,
            command=lambda idx=index: self.editar_forum(idx)
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        # Botão Excluir
        delete_btn = ctk.CTkButton(
            btns_frame,
            text="🗑️ Excluir",
            width=70,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            hover_color="#fee2e2",
            text_color=CORES["perigo"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=12,
            command=lambda idx=index: self.excluir_forum(idx)
        )
        delete_btn.pack(side="left")
    
    def load_forum(self, index):
        """Carrega um fórum"""
        self.current_forum_index = index
        self.view_mode = "topics"
        forum = self.forums[index]
        
        # Atualizar header
        self.current_title.configure(text=f"📌 {forum['name']}")
        self.description_label.configure(text=forum["description"])
        
        # Esconder botão voltar e badge
        self.back_button.pack_forget()
        self.context_badge.pack_forget()
        
        # Mostrar botão novo tópico
        self.new_topic_btn.pack(pady=(0, 15), padx=25)
        
        # Esconder área de resposta
        self.reply_frame.pack_forget()
        
        # Recarregar
        self.clear_content()
        self.load_topics()
        self.load_forums_list()
    
    # ========== FUNÇÕES DOS TÓPICOS ==========
    def load_topics(self):
        """Carrega a lista de tópicos"""
        forum = self.forums[self.current_forum_index]
        
        # Limpar o conteúdo antes de carregar
        self.clear_content()
        
        if not forum["topics"]:
            self.show_empty_state("📭 Nenhum tópico ainda", "Seja o primeiro a criar um tópico!")
            return
        
        for i, topic in enumerate(forum["topics"]):
            self.create_topic_card(topic, i)
    
    def create_topic_card(self, topic, index):
        """Cria um card de tópico com botões de editar e excluir"""
        card = ctk.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color=CORES["borda"]
        )
        card.pack(fill="x", pady=(0, 15))
        
        # Header do card
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(15, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            header,
            text=f"💬 {topic['title']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=CORES["texto_primario"]
        )
        title_label.pack(side="left")
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        stats_frame.pack(side="right")
        
        views_label = ctk.CTkLabel(
            stats_frame,
            text=f"👁️ {topic['views']}",
            font=ctk.CTkFont(size=12),
            text_color=CORES["texto_secundario"]
        )
        views_label.pack(side="left", padx=(0, 10))
        
        replies_label = ctk.CTkLabel(
            stats_frame,
            text=f"💬 {topic['replies']}",
            font=ctk.CTkFont(size=12),
            text_color=CORES["texto_secundario"]
        )
        replies_label.pack(side="left")
        
        # Informações do autor
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=18, pady=(0, 10))
        
        author_label = ctk.CTkLabel(
            info_frame,
            text=f"👤 {topic['author']}  •  📅 {topic['created']}",
            font=ctk.CTkFont(size=12),
            text_color=CORES["texto_secundario"]
        )
        author_label.pack(side="left")
        
        # Badge de última mensagem
        last_msg_frame = ctk.CTkFrame(card, fg_color=CORES["fundo"], corner_radius=8)
        last_msg_frame.pack(fill="x", padx=18, pady=(0, 15))
        
        last_msg_label = ctk.CTkLabel(
            last_msg_frame,
            text=f"🕒 Última mensagem: {topic['last_message']}",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=CORES["texto_secundario"]
        )
        last_msg_label.pack(anchor="w", padx=12, pady=8)
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=18, pady=(0, 15))
        
        # Botão Ver Tópico
        view_btn = ctk.CTkButton(
            actions_frame,
            text="Ver Tópico",
            width=100,
            height=32,
            fg_color=CORES["primaria"],
            hover_color=CORES["secundaria"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=lambda: self.load_topic(index)
        )
        view_btn.pack(side="left", padx=(0, 10))
        
        # Botões de edição
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Editar",
            width=80,
            height=32,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            command=lambda idx=index: self.editar_topico(idx)
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Excluir",
            width=80,
            height=32,
            fg_color="transparent",
            hover_color="#fee2e2",
            text_color=CORES["perigo"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            command=lambda idx=index: self.excluir_topico(idx)
        )
        delete_btn.pack(side="left")
    
    # ========== FUNÇÕES DAS MENSAGENS ==========
    def load_topic(self, index):
        """Carrega um tópico"""
        self.current_topic_index = index
        self.view_mode = "messages"
        topic = self.forums[self.current_forum_index]["topics"][index]
        
        # Incrementar visualizações
        topic['views'] += 1
        
        # MOSTRAR BOTÃO VOLTAR NO TOPO
        self.back_button.pack(side="left", padx=(0, 15))
        
        # Atualizar header
        self.current_title.configure(text=f"💬 {topic['title']}")
        self.description_label.configure(text=f"Por {topic['author']} • {topic['created']}")
        
        # Badge de respostas
        self.context_badge.configure(text=f"{topic['replies']} respostas")
        self.context_badge.pack(side="left", padx=(0, 15))
        
        # Esconder botão novo tópico
        self.new_topic_btn.pack_forget()
        
        # Mostrar área de resposta
        self.reply_frame.pack(fill="x", pady=(0, 20))
        
        # Recarregar
        self.clear_content()
        self.load_messages()
        self.load_forums_list()
    
    def load_messages(self):
        """Carrega as mensagens"""
        topic = self.forums[self.current_forum_index]["topics"][self.current_topic_index]
        
        for i, message in enumerate(topic["messages"]):
            self.create_message_card(message, i)
    
    def create_message_card(self, message, index):
        """Cria um card de mensagem com menções destacadas"""
        is_op = index == 0
        
        card = ctk.CTkFrame(
            self.content_frame,
            fg_color="white" if not is_op else "#f0f7ff",
            corner_radius=15,
            border_width=1,
            border_color=CORES["borda"] if not is_op else CORES["primaria"]
        )
        card.pack(fill="x", pady=(0, 15))
        
        # Avatar e autor
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(15, 10))
        
        # Avatar
        avatar_frame = ctk.CTkFrame(
            header,
            fg_color=CORES["primaria"],
            width=40,
            height=40,
            corner_radius=20
        )
        avatar_frame.pack(side="left", padx=(0, 12))
        avatar_frame.pack_propagate(False)
        
        avatar_letter = message["author"][0].upper()
        ctk.CTkLabel(
            avatar_frame,
            text=avatar_letter,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Informações do autor
        author_info = ctk.CTkFrame(header, fg_color="transparent")
        author_info.pack(side="left")
        
        ctk.CTkLabel(
            author_info,
            text=message["author"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            author_info,
            text=message["time"],
            font=ctk.CTkFont(size=11),
            text_color=CORES["texto_secundario"]
        ).pack(anchor="w")
        
        # Badge OP
        if is_op:
            op_badge = ctk.CTkLabel(
                header,
                text="OP",
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=CORES["destaque"],
                text_color="white",
                corner_radius=8,
                width=30,
                height=20
            )
            op_badge.pack(side="right")
        
        # ===== MENSAGEM COM MENÇÕES DESTACADAS =====
        msg_frame = ctk.CTkFrame(card, fg_color="transparent")
        msg_frame.pack(anchor="w", padx=70, pady=(0, 15))
        
        # Processar mensagem para destacar menções
        self.criar_mensagem_com_mencoes(msg_frame, message["message"])
        
        # Botão Responder
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=70, pady=(0, 15))
        
        reply_btn = ctk.CTkButton(
            actions_frame,
            text="↩️ Responder",
            width=100,
            height=28,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            font=ctk.CTkFont(size=11),
            corner_radius=15,
            command=lambda: self.responder_mensagem(message)
        )
        reply_btn.pack(side="left")
    
    def criar_mensagem_com_mencoes(self, parent, texto):
        """Cria uma mensagem com menções destacadas em azul"""
        # Padrão para encontrar @usuario (qualquer combinação de letras após @)
        padrao = r'(@\w+)'
        
        # Encontrar todas as partes do texto (incluindo menções)
        partes = re.split(padrao, texto)
        
        for parte in partes:
            if parte.startswith('@') and len(parte) > 1:
                # É uma menção
                usuario = parte[1:]  # Remove o @
                
                # Frame para a menção (com fundo azul claro)
                mencao_frame = ctk.CTkFrame(
                    parent,
                    fg_color=CORES["mencao_fundo"],
                    corner_radius=8
                )
                mencao_frame.pack(side="left", padx=1)
                
                mencao_label = ctk.CTkLabel(
                    mencao_frame,
                    text=parte,  # Mostra com o @
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=CORES["mencao"],
                    cursor="hand2"
                )
                mencao_label.pack(padx=3, pady=1)
                
                # Evento de clique
                mencao_label.bind("<Button-1>", lambda e, u=usuario: self.ao_clicar_em_mencao(u))
                mencao_frame.bind("<Button-1>", lambda e, u=usuario: self.ao_clicar_em_mencao(u))
                
            elif parte.strip():
                # Texto normal
                if parte.strip():
                    label = ctk.CTkLabel(
                        parent,
                        text=parte,
                        font=ctk.CTkFont(size=14),
                        text_color=CORES["texto_primario"]
                    )
                    label.pack(side="left")
    
    def ao_clicar_em_mencao(self, usuario):
        """Quando clicar em uma menção, prepara resposta"""
        texto_atual = self.reply_entry.get("1.0", "end-1c")
        if texto_atual == "Digite sua resposta...":
            self.reply_entry.delete("1.0", "end")
            self.reply_entry.insert("1.0", f"@{usuario} ")
        else:
            self.reply_entry.insert("end", f"\n@{usuario} ")
        self.reply_entry.focus()
    
    def show_topics_view(self):
        """Voltar para lista de tópicos"""
        self.view_mode = "topics"
        forum = self.forums[self.current_forum_index]
        
        # Esconder botão voltar
        self.back_button.pack_forget()
        
        # Atualizar header
        self.current_title.configure(text=f"📌 {forum['name']}")
        self.description_label.configure(text=forum["description"])
        
        # Esconder badge
        self.context_badge.pack_forget()
        
        # Mostrar botão novo tópico
        self.new_topic_btn.pack(pady=(0, 15), padx=25)
        
        # Esconder área de resposta
        self.reply_frame.pack_forget()
        
        # Recarregar
        self.clear_content()
        self.load_topics()
    
    def show_empty_state(self, title, subtitle):
        """Mostra estado vazio"""
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        empty_frame.pack(expand=True, pady=100)
        
        ctk.CTkLabel(
            empty_frame,
            text="📭",
            font=ctk.CTkFont(size=64)
        ).pack()
        
        ctk.CTkLabel(
            empty_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text=subtitle,
            font=ctk.CTkFont(size=14),
            text_color=CORES["texto_secundario"]
        ).pack()
    
    def clear_content(self):
        """Limpa conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # ========== FUNÇÕES DE AÇÃO ==========
    def criar_novo_forum(self):
        """Abre diálogo para criar novo fórum"""
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("Criar Novo Fórum")
        dialog.geometry("500x500")
        dialog.grab_set()
        dialog.focus_force()
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (500 // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(
            content,
            text="📁 Criar Novo Fórum",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(pady=(0, 25))
        
        # Nome
        ctk.CTkLabel(
            content,
            text="Nome do Fórum:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        nome_entry = ctk.CTkEntry(content, height=40, corner_radius=8)
        nome_entry.pack(fill="x", pady=(0, 20))
        
        # Descrição
        ctk.CTkLabel(
            content,
            text="Descrição:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        desc_entry = ctk.CTkTextbox(content, height=120, corner_radius=8)
        desc_entry.pack(fill="x", pady=(0, 20))
        
        # Ícone
        ctk.CTkLabel(
            content,
            text="Ícone (opcional):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        icon_entry = ctk.CTkEntry(content, placeholder_text="Ex: 🌐, 💻, 🔒", height=40, corner_radius=8)
        icon_entry.pack(fill="x", pady=(0, 25))
        
        # Botões
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        cancelar_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=120,
            height=45,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            command=dialog.destroy
        )
        cancelar_btn.pack(side="left", padx=(0, 10))
        
        def salvar():
            nome = nome_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            icon = icon_entry.get().strip() or "📁"
            
            if nome and desc:
                novo_forum = {
                    "name": nome,
                    "description": desc,
                    "created": datetime.now().strftime("%d/%m/%Y"),
                    "icon": icon,
                    "topics": []
                }
                self.forums.append(novo_forum)
                self.load_forums_list()
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Fórum '{nome}' criado com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
        
        salvar_btn = ctk.CTkButton(
            btn_frame,
            text="Criar Fórum",
            width=140,
            height=45,
            fg_color=CORES["sucesso"],
            hover_color="#05b586",
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=salvar
        )
        salvar_btn.pack(side="right")
    
    def editar_forum(self, index):
        """Abre diálogo para editar fórum"""
        forum = self.forums[index]
        
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("Editar Fórum")
        dialog.geometry("500x500")
        dialog.grab_set()
        dialog.focus_force()
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (500 // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(
            content,
            text="✏️ Editar Fórum",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(pady=(0, 25))
        
        # Nome
        ctk.CTkLabel(
            content,
            text="Nome do Fórum:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        nome_entry = ctk.CTkEntry(content, height=40, corner_radius=8)
        nome_entry.insert(0, forum["name"])
        nome_entry.pack(fill="x", pady=(0, 20))
        
        # Descrição
        ctk.CTkLabel(
            content,
            text="Descrição:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        desc_entry = ctk.CTkTextbox(content, height=120, corner_radius=8)
        desc_entry.insert("1.0", forum["description"])
        desc_entry.pack(fill="x", pady=(0, 20))
        
        # Ícone
        ctk.CTkLabel(
            content,
            text="Ícone:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        icon_entry = ctk.CTkEntry(content, height=40, corner_radius=8)
        icon_entry.insert(0, forum.get("icon", "📁"))
        icon_entry.pack(fill="x", pady=(0, 25))
        
        # Botões
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        cancelar_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=120,
            height=45,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            command=dialog.destroy
        )
        cancelar_btn.pack(side="left", padx=(0, 10))
        
        def salvar():
            nome = nome_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            icon = icon_entry.get().strip() or "📁"
            
            if nome and desc:
                self.forums[index]["name"] = nome
                self.forums[index]["description"] = desc
                self.forums[index]["icon"] = icon
                
                # Se for o fórum atual, atualizar header
                if index == self.current_forum_index:
                    self.current_title.configure(text=f"📌 {nome}")
                    self.description_label.configure(text=desc)
                
                self.load_forums_list()
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Fórum '{nome}' editado com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
        
        salvar_btn = ctk.CTkButton(
            btn_frame,
            text="Salvar Alterações",
            width=160,
            height=45,
            fg_color=CORES["primaria"],
            hover_color=CORES["secundaria"],
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=salvar
        )
        salvar_btn.pack(side="right")
    
    def excluir_forum(self, index):
        """Confirma e exclui fórum"""
        forum = self.forums[index]
        
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o fórum '{forum['name']}'?\n\nTodos os tópicos e mensagens serão perdidos!"
        )
        
        if resposta:
            # Remover fórum
            del self.forums[index]
            
            # Se não houver mais fóruns, criar um padrão
            if len(self.forums) == 0:
                self.forums.append({
                    "name": "Fórum Principal",
                    "description": "Fórum padrão do sistema",
                    "created": datetime.now().strftime("%d/%m/%Y"),
                    "icon": "📁",
                    "topics": []
                })
                self.load_forum(0)
            else:
                # Ajustar índice atual
                if index >= len(self.forums):
                    self.load_forum(len(self.forums) - 1)
                elif index == self.current_forum_index:
                    # Se excluiu o fórum atual, carregar o primeiro
                    self.load_forum(0)
                else:
                    # Se excluiu outro fórum, manter o atual
                    self.load_forum(self.current_forum_index)
            
            self.load_forums_list()
            messagebox.showinfo("Sucesso", "Fórum excluído com sucesso!")
    
    def criar_novo_topico(self):
        """Abre diálogo para criar novo tópico"""
        forum = self.forums[self.current_forum_index]
        
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("Criar Novo Tópico")
        dialog.geometry("600x600")
        dialog.grab_set()
        dialog.focus_force()
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (600 // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (600 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(
            content,
            text=f"💬 Novo Tópico em: {forum['name']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(pady=(0, 25))
        
        # Título
        ctk.CTkLabel(
            content,
            text="Título do Tópico:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        titulo_entry = ctk.CTkEntry(content, height=40, corner_radius=8)
        titulo_entry.pack(fill="x", pady=(0, 20))
        
        # Mensagem
        ctk.CTkLabel(
            content,
            text="Mensagem:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        msg_entry = ctk.CTkTextbox(content, height=150, corner_radius=8)
        msg_entry.pack(fill="x", pady=(0, 20))
        
        # Autor (opcional)
        ctk.CTkLabel(
            content,
            text="Autor (opcional):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        autor_entry = ctk.CTkEntry(content, placeholder_text="Deixe em branco para usar 'Você'", height=40, corner_radius=8)
        autor_entry.pack(fill="x", pady=(0, 25))
        
        # Botões
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        cancelar_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=120,
            height=45,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            command=dialog.destroy
        )
        cancelar_btn.pack(side="left", padx=(0, 10))
        
        def salvar():
            titulo = titulo_entry.get().strip()
            mensagem = msg_entry.get("1.0", "end-1c").strip()
            autor = autor_entry.get().strip() or "Você"
            
            if titulo and mensagem:
                now = datetime.now()
                
                novo_topico = {
                    "title": titulo,
                    "author": autor,
                    "created": now.strftime("%d/%m/%Y"),
                    "replies": 0,
                    "views": 0,
                    "last_message": now.strftime("%H:%M"),
                    "messages": [
                        {"author": autor, "message": mensagem, "time": now.strftime("%H:%M")}
                    ]
                }
                
                self.forums[self.current_forum_index]["topics"].append(novo_topico)
                self.load_forum(self.current_forum_index)
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Tópico '{titulo}' criado com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Preencha título e mensagem!")
        
        salvar_btn = ctk.CTkButton(
            btn_frame,
            text="Criar Tópico",
            width=140,
            height=45,
            fg_color=CORES["sucesso"],
            hover_color="#05b586",
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=salvar
        )
        salvar_btn.pack(side="right")
    
    def editar_topico(self, index):
        """Abre diálogo para editar tópico"""
        topic = self.forums[self.current_forum_index]["topics"][index]
        
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("Editar Tópico")
        dialog.geometry("500x350")
        dialog.grab_set()
        dialog.focus_force()
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (500 // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (350 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(
            content,
            text="✏️ Editar Tópico",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(pady=(0, 25))
        
        # Título
        ctk.CTkLabel(
            content,
            text="Título do Tópico:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto_primario"]
        ).pack(anchor="w", pady=(0, 5))
        
        titulo_entry = ctk.CTkEntry(content, height=40, corner_radius=8)
        titulo_entry.insert(0, topic["title"])
        titulo_entry.pack(fill="x", pady=(0, 25))
        
        # Botões
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        cancelar_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=120,
            height=45,
            fg_color="transparent",
            hover_color=CORES["fundo"],
            text_color=CORES["texto_secundario"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            command=dialog.destroy
        )
        cancelar_btn.pack(side="left", padx=(0, 10))
        
        def salvar():
            titulo = titulo_entry.get().strip()
            
            if titulo:
                self.forums[self.current_forum_index]["topics"][index]["title"] = titulo
                
                # Se for o tópico atual, atualizar header
                if self.view_mode == "messages" and index == self.current_topic_index:
                    self.current_title.configure(text=f"💬 {titulo}")
                
                # Recarregar lista de tópicos
                self.load_topics()
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Tópico editado com sucesso!")
            else:
                messagebox.showwarning("Atenção", "O título não pode estar vazio!")
        
        salvar_btn = ctk.CTkButton(
            btn_frame,
            text="Salvar Alterações",
            width=160,
            height=45,
            fg_color=CORES["primaria"],
            hover_color=CORES["secundaria"],
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=salvar
        )
        salvar_btn.pack(side="right")
    
    def excluir_topico(self, index):
        """Confirma e exclui tópico"""
        topic = self.forums[self.current_forum_index]["topics"][index]
        
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o tópico '{topic['title']}'?\n\nTodas as mensagens serão perdidas!"
        )
        
        if resposta:
            # Remover tópico
            del self.forums[self.current_forum_index]["topics"][index]
            
            # ATUALIZAÇÃO EM TEMPO REAL
            self.clear_content()
            
            # Se estava visualizando este tópico, voltar para lista
            if self.view_mode == "messages" and index == self.current_topic_index:
                self.show_topics_view()
            else:
                # Recarregar a lista de tópicos
                self.load_topics()
            
            # Atualizar contador no card do fórum
            self.load_forums_list()
            
            # Verificar se ainda há tópicos
            forum_atual = self.forums[self.current_forum_index]
            if not forum_atual["topics"]:
                self.show_empty_state("📭 Nenhum tópico ainda", "Seja o primeiro a criar um tópico!")
            
            messagebox.showinfo("Sucesso", "Tópico excluído com sucesso!")
    
    def responder_mensagem(self, mensagem):
        """Preenche o campo de resposta com uma menção"""
        autor = mensagem["author"]
        primeiro_nome = autor.split()[0].lower() if autor else "usuario"
        texto_atual = self.reply_entry.get("1.0", "end-1c")
        
        if texto_atual == "Digite sua resposta...":
            self.reply_entry.delete("1.0", "end")
            self.reply_entry.insert("1.0", f"@{primeiro_nome} ")
        else:
            self.reply_entry.insert("end", f"\n@{primeiro_nome} ")
        
        self.reply_entry.focus()
    
    # ========== UTILITÁRIOS ==========
    def clear_reply_placeholder(self, event):
        if self.reply_entry.get("1.0", "end-1c") == "Digite sua resposta...":
            self.reply_entry.delete("1.0", "end")
    
    def restore_reply_placeholder(self, event):
        if not self.reply_entry.get("1.0", "end-1c").strip():
            self.reply_entry.insert("1.0", "Digite sua resposta...")
    
    def send_message(self):
        """Envia mensagem"""
        message = self.reply_entry.get("1.0", "end-1c").strip()
        if message and message != "Digite sua resposta...":
            now = datetime.now()
            
            nova_mensagem = {
                "author": "Você",
                "message": message,
                "time": now.strftime("%H:%M")
            }
            
            topic = self.forums[self.current_forum_index]["topics"][self.current_topic_index]
            topic["messages"].append(nova_mensagem)
            topic["replies"] += 1
            topic["last_message"] = now.strftime("%H:%M")
            
            # Recarregar mensagens
            self.clear_content()
            self.load_messages()
            
            # Atualizar badge
            self.context_badge.configure(text=f"{topic['replies']} respostas")
            
            # Limpar campo
            self.reply_entry.delete("1.0", "end")
            self.reply_entry.insert("1.0", "Digite sua resposta...")
            
            messagebox.showinfo("Sucesso", "Mensagem enviada!")
    
    def search_forums(self, event=None):
        """Busca fóruns"""
        search_term = self.search_entry.get().lower()
        
        if not search_term:
            self.load_forums_list()
            return
        
        filtered = [f for f in self.forums if search_term in f["name"].lower()]
        
        for widget in self.forums_list_frame.winfo_children():
            widget.destroy()
        
        if filtered:
            for i, forum in enumerate(filtered):
                self.create_forum_card(forum, i)
        else:
            no_results = ctk.CTkLabel(
                self.forums_list_frame,
                text="🔍 Nenhum fórum encontrado",
                font=ctk.CTkFont(size=13),
                text_color=CORES["texto_secundario"]
            )
            no_results.pack(pady=30)
    
    def run(self):
        """Inicia o fórum"""
        if not self.ui_built:
            self.build_ui()
        
        if hasattr(self.master, 'mainloop'):
            self.master.mainloop()


if __name__ == "__main__":
    app = ForumApp()
    app.run()