import customtkinter as ctk
from datetime import datetime

class ForumApp:
    def __init__(self, master=None):
        self.master = master if master else ctk.CTk()
        self.ui_built = False
        
        # ========== DADOS COMPLETOS ==========
        self.forums = [
            {
                "name": "Administrador de redes",
                "description": "Discussões sobre administração de redes, protocolos e equipamentos",
                "created": "20/03/2025",
                "topics": [
                    {
                        "title": "Configuração de OSPF",
                        "author": "Lucas Amaral",
                        "created": "20/03/2025",
                        "replies": 4,
                        "views": 45,
                        "last_message": "12:20",
                        "messages": [
                            {"author": "Lucas Amaral", "message": "Galera, lembrando que amanhã é a apresentação dos projetos. Todo mundo com a topologia pronta?", "time": "12:15"},
                            {"author": "Carla Souza", "message": "Quase! Tô finalizando o OSPF ainda. Mais alguém usando?", "time": "12:17"},
                            {"author": "Vinícius Junior", "message": "Eu! Só travando no balanceamento de carga. 😊", "time": "12:17"},
                            {"author": "Diego Maradona", "message": "Fiz isso ontem. Posso te mandar o exemplo!", "time": "12:18"},
                            {"author": "Ana", "message": "Meu foco é segurança com VLANs. Configurei DHCP snooping e port security 🛡️", "time": "12:20"}
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
                            {"author": "Vinícius Junior", "message": "Alguém tem experiência com balanceamento de carga em redes corporativas?", "time": "09:15"},
                            {"author": "Carla Souza", "message": "Uso o HAProxy aqui, muito bom!", "time": "09:30"}
                        ]
                    }
                ]
            },
            {
                "name": "Suporte e manutenção de notebooks",
                "description": "Reparo, manutenção e suporte para notebooks de todas as marcas",
                "created": "12/01/2025",
                "topics": [
                    {
                        "title": "Reparo de placa-mãe Dell Inspiron",
                        "author": "João Silva",
                        "created": "12/01/2025",
                        "replies": 1,
                        "views": 34,
                        "last_message": "10:45",
                        "messages": [
                            {"author": "João Silva", "message": "Alguém tem experiência com reparo de placa mãe em Dell Inspiron 15?", "time": "10:30"},
                            {"author": "Maria Santos", "message": "Sim, já fiz vários. Qual o problema específico?", "time": "10:45"}
                        ]
                    }
                ]
            },
            {
                "name": "Segurança da informação",
                "description": "Firewalls, VLANs, políticas de segurança e boas práticas",
                "created": "28/05/2025",
                "topics": [
                    {
                        "title": "Vulnerabilidades Linux",
                        "author": "Diego Maradona",
                        "created": "28/05/2025",
                        "replies": 1,
                        "views": 56,
                        "last_message": "14:30",
                        "messages": [
                            {"author": "Diego Maradona", "message": "Novas vulnerabilidades descobertas em sistemas Linux. Alguém já aplicou os patches?", "time": "09:45"},
                            {"author": "Roberto Alves", "message": "Testei em ambiente de testes, parece estável.", "time": "14:30"}
                        ]
                    },
                    {
                        "title": "Segurança com VLANs",
                        "author": "Ana",
                        "created": "29/05/2025",
                        "replies": 0,
                        "views": 23,
                        "last_message": "12:20",
                        "messages": [
                            {"author": "Ana", "message": "Configurei DHCP snooping e port security nos switches. Alguém mais trabalha com segmentação de rede? 🛡️", "time": "12:20"}
                        ]
                    }
                ]
            }
        ]
        
        self.current_forum_index = 0
        self.current_topic_index = 0
        self.view_mode = "topics"  # "topics" ou "messages"
    
    # ========== CONSTRUÇÃO DA UI ==========
    def build_ui(self):
        """Constrói a interface completa do fórum"""
        if self.ui_built:
            return
        
        self.ui_built = True
        
        # Limpar master
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # ========== FRAME PRINCIPAL ==========
        main_frame = ctk.CTkFrame(self.master, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # ========== TÍTULO # FORUM ==========
        title_label = ctk.CTkLabel(
            main_frame,
            text="# Forum",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#111827"
        )
        title_label.pack(anchor="w", padx=20, pady=(10, 15))
        
        # ========== BARRA DE PESQUISA ==========
        search_frame = ctk.CTkFrame(main_frame, fg_color="#f9fafb", height=60)
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="## Pesquisar",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f2937"
        )
        search_label.pack(side="left", padx=25, pady=15)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite para buscar fóruns, tópicos ou mensagens...",
            width=400,
            height=38,
            border_width=1,
            border_color="#d1d5db"
        )
        self.search_entry.pack(side="right", padx=25, pady=15)
        
        # ========== CONTEÚDO PRINCIPAL (2 COLUNAS) ==========
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=3)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # ========== COLUNA ESQUERDA - LISTA DE FÓRUNS ==========
        self.build_left_column(content_frame)
        
        # ========== COLUNA DIREITA - CONTEÚDO VARIÁVEL ==========
        self.build_right_column(content_frame)
        
        # ========== CARREGAR DADOS INICIAIS ==========
        self.load_forums_list()
        if self.forums:
            self.load_forum(0)
    
    def build_left_column(self, parent):
        """Constrói a coluna esquerda com a lista de fóruns"""
        left_column = ctk.CTkFrame(parent, fg_color="#f9fafb")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Título "### Fóruns"
        forums_title = ctk.CTkLabel(
            left_column,
            text="### Fóruns",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f2937"
        )
        forums_title.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Lista de fóruns (scrollável)
        self.forums_list_frame = ctk.CTkScrollableFrame(
            left_column,
            fg_color="transparent"
        )
        self.forums_list_frame.pack(fill="both", expand=True, padx=10)
        
        # Botão Criar Fórum
        self.create_forum_btn = ctk.CTkButton(
            left_column,
            text="+ Criar novo fórum",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4f46e5",
            hover_color="#4338ca",
            corner_radius=8,
            command=self.create_new_forum
        )
        self.create_forum_btn.pack(pady=20, padx=20)
    
    def build_right_column(self, parent):
        """Constrói a coluna direita com conteúdo dinâmico"""
        self.right_column = ctk.CTkFrame(parent, fg_color="white")
        self.right_column.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        self.right_column.grid_columnconfigure(0, weight=1)
        self.right_column.grid_rowconfigure(1, weight=1)
        
        # ========== HEADER ==========
        self.header_frame = ctk.CTkFrame(self.right_column, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(25, 10))
        
        # Botão Voltar (inicialmente escondido)
        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="← Voltar para tópicos",
            width=150,
            height=32,
            fg_color="transparent",
            hover_color="#f3f4f6",
            text_color="#4b5563",
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=12),
            command=self.show_topics_view
        )
        
        # Título do fórum/tópico atual
        self.current_title = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#111827"
        )
        self.current_title.pack(side="left")
        
        # Descrição do fórum
        self.description_label = ctk.CTkLabel(
            self.right_column,
            text="",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="#6b7280"
        )
        self.description_label.pack(anchor="w", padx=30, pady=(0, 15))
        
        # Separador
        separator = ctk.CTkFrame(self.right_column, height=1, fg_color="#e5e7eb")
        separator.pack(fill="x", padx=30, pady=(0, 15))
        
        # ========== ÁREA DE CONTEÚDO ==========
        self.content_frame = ctk.CTkScrollableFrame(
            self.right_column,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # ========== BOTÃO NOVO TÓPICO ==========
        self.new_topic_btn = ctk.CTkButton(
            self.right_column,
            text="+ Novo tópico",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=8,
            command=self.create_new_topic
        )
        
        # ========== CAMPO DE RESPOSTA ==========
        self.reply_frame = ctk.CTkFrame(self.right_column, fg_color="white")
        self.reply_frame.pack(fill="x", padx=30, pady=(0, 25))
        self.reply_frame.pack_forget()  # Escondido inicialmente
        
        self.reply_entry = ctk.CTkTextbox(
            self.reply_frame,
            height=65,
            border_width=1,
            border_color="#e5e7eb",
            font=ctk.CTkFont(size=13)
        )
        self.reply_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.reply_entry.insert("1.0", "Digite sua resposta...")
        
        self.send_btn = ctk.CTkButton(
            self.reply_frame,
            text="Enviar",
            width=100,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.send_message
        )
        self.send_btn.pack(side="right")
    
    # ========== FUNÇÕES DOS FÓRUNS ==========
    def load_forums_list(self):
        """Carrega a lista de fóruns na coluna esquerda"""
        for widget in self.forums_list_frame.winfo_children():
            widget.destroy()
        
        for i, forum in enumerate(self.forums):
            self.create_forum_item(forum, i)
    
    def create_forum_item(self, forum, index):
        """Cria um item na lista de fóruns com nome, contador e data"""
        # Cor de fundo diferente para o fórum selecionado
        bg_color = "#ffffff" if index != self.current_forum_index else "#e0f2fe"
        border_color = "#e5e7eb" if index != self.current_forum_index else "#3b82f6"
        
        forum_frame = ctk.CTkFrame(
            self.forums_list_frame,
            fg_color=bg_color,
            corner_radius=8,
            border_width=1,
            border_color=border_color
        )
        forum_frame.pack(fill="x", pady=(0, 10))
        forum_frame.bind("<Button-1>", lambda e: self.load_forum(index))
        
        # ===== NOME DO FÓRUM =====
        name_frame = ctk.CTkFrame(forum_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=15, pady=(12, 5))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=forum["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827"
        )
        name_label.pack(side="left")
        name_label.bind("<Button-1>", lambda e: self.load_forum(index))
        
        # Contador de tópicos
        topic_count = len(forum["topics"])
        count_label = ctk.CTkLabel(
            name_frame,
            text=f"📌 {topic_count}",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        count_label.pack(side="right")
        count_label.bind("<Button-1>", lambda e: self.load_forum(index))
        
        # ===== DESCRIÇÃO =====
        desc_frame = ctk.CTkFrame(forum_frame, fg_color="transparent")
        desc_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        desc_text = forum["description"][:40] + "..." if len(forum["description"]) > 40 else forum["description"]
        desc_label = ctk.CTkLabel(
            desc_frame,
            text=f"📋 {desc_text}",
            font=ctk.CTkFont(size=11),
            text_color="#4b5563"
        )
        desc_label.pack(side="left")
        desc_label.bind("<Button-1>", lambda e: self.load_forum(index))
        
        # ===== DATA E AÇÕES =====
        footer_frame = ctk.CTkFrame(forum_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        date_label = ctk.CTkLabel(
            footer_frame,
            text=f"Criado: {forum['created']}",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280"
        )
        date_label.pack(side="left")
        date_label.bind("<Button-1>", lambda e: self.load_forum(index))
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=30,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#e5e7eb",
            text_color="#4b5563",
            command=lambda idx=index: self.edit_forum(idx)
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=30,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#fee2e2",
            text_color="#ef4444",
            command=lambda idx=index: self.confirm_delete_forum(idx)
        )
        delete_btn.pack(side="left")
        
        # Link
        link_label = ctk.CTkLabel(
            footer_frame,
            text="🔗",
            font=ctk.CTkFont(size=12)
        )
        link_label.pack(side="right", padx=(10, 0))
        link_label.bind("<Button-1>", lambda e: self.load_forum(index))
    
    def load_forum(self, index):
        """Carrega um fórum e mostra a lista de tópicos"""
        self.current_forum_index = index
        self.view_mode = "topics"
        forum = self.forums[index]
        
        # Atualizar cabeçalho
        self.current_title.configure(text=f"## {forum['name']}")
        self.description_label.configure(text=f"📋 {forum['description']}")
        
        # Esconder botão voltar e mostrar botão novo tópico
        self.back_button.pack_forget()
        self.new_topic_btn.pack(pady=(0, 15), padx=30)
        
        # Esconder campo de resposta
        self.reply_frame.pack_forget()
        
        # Limpar e carregar tópicos
        self.clear_content()
        self.load_topics()
        
        # Atualizar lista de fóruns
        self.load_forums_list()
    
    # ========== FUNÇÕES DOS TÓPICOS ==========
    def load_topics(self):
        """Carrega a lista de tópicos do fórum atual"""
        forum = self.forums[self.current_forum_index]
        
        if not forum["topics"]:
            empty_label = ctk.CTkLabel(
                self.content_frame,
                text="📭 Nenhum tópico ainda",
                font=ctk.CTkFont(size=16),
                text_color="#9ca3af"
            )
            empty_label.pack(pady=50)
            
            sub_label = ctk.CTkLabel(
                self.content_frame,
                text="Seja o primeiro a criar um tópico!",
                font=ctk.CTkFont(size=14),
                text_color="#6b7280"
            )
            sub_label.pack(pady=(0, 50))
            return
        
        for i, topic in enumerate(forum["topics"]):
            self.create_topic_widget(topic, i)
    
    def create_topic_widget(self, topic, index):
        """Cria um widget para cada tópico"""
        topic_frame = ctk.CTkFrame(
            self.content_frame,
            border_width=1,
            border_color="#e5e7eb",
            corner_radius=8,
            fg_color="white"
        )
        topic_frame.pack(fill="x", pady=(0, 12))
        topic_frame.bind("<Button-1>", lambda e: self.load_topic(index))
        
        # Título do tópico
        title_frame = ctk.CTkFrame(topic_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=18, pady=(15, 8))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"📌 {topic['title']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#111827"
        )
        title_label.pack(side="left")
        title_label.bind("<Button-1>", lambda e: self.load_topic(index))
        
        # Autor e data
        info_frame = ctk.CTkFrame(topic_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=18, pady=(0, 10))
        
        author_label = ctk.CTkLabel(
            info_frame,
            text=f"👤 {topic['author']}",
            font=ctk.CTkFont(size=13),
            text_color="#4b5563"
        )
        author_label.pack(side="left", padx=(0, 15))
        author_label.bind("<Button-1>", lambda e: self.load_topic(index))
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=f"📅 {topic['created']}",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        date_label.pack(side="left")
        date_label.bind("<Button-1>", lambda e: self.load_topic(index))
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        stats_frame.pack(side="right")
        
        replies_label = ctk.CTkLabel(
            stats_frame,
            text=f"💬 {topic['replies']} respostas",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        replies_label.pack(side="left", padx=(0, 15))
        replies_label.bind("<Button-1>", lambda e: self.load_topic(index))
        
        views_label = ctk.CTkLabel(
            stats_frame,
            text=f"👁️ {topic['views']} visualizações",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        views_label.pack(side="left")
        views_label.bind("<Button-1>", lambda e: self.load_topic(index))
        
        # Última mensagem
        last_msg_frame = ctk.CTkFrame(topic_frame, fg_color="#f9fafb", corner_radius=6)
        last_msg_frame.pack(fill="x", padx=18, pady=(0, 15))
        
        last_msg_label = ctk.CTkLabel(
            last_msg_frame,
            text=f"🕒 Última mensagem: {topic['last_message']}",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#6b7280"
        )
        last_msg_label.pack(anchor="w", padx=12, pady=8)
        last_msg_label.bind("<Button-1>", lambda e: self.load_topic(index))
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(topic_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=18, pady=(0, 15))
        
        view_btn = ctk.CTkButton(
            actions_frame,
            text="Ver tópico",
            width=100,
            height=32,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=ctk.CTkFont(size=12),
            command=lambda: self.load_topic(index)
        )
        view_btn.pack(side="left", padx=(0, 10))
        
        edit_topic_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Editar",
            width=80,
            height=32,
            fg_color="transparent",
            hover_color="#f3f4f6",
            text_color="#4b5563",
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=12),
            command=lambda idx=index: self.edit_topic(idx)
        )
        edit_topic_btn.pack(side="left", padx=(0, 10))
        
        delete_topic_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Excluir",
            width=80,
            height=32,
            fg_color="transparent",
            hover_color="#fee2e2",
            text_color="#ef4444",
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=12),
            command=lambda idx=index: self.confirm_delete_topic(idx)
        )
        delete_topic_btn.pack(side="left")
    
    # ========== FUNÇÕES DAS MENSAGENS ==========
    def load_topic(self, index):
        """Carrega um tópico e mostra as mensagens"""
        self.current_topic_index = index
        self.view_mode = "messages"
        topic = self.forums[self.current_forum_index]["topics"][index]
        
        # Incrementar visualizações
        topic['views'] += 1
        
        # Atualizar cabeçalho
        self.current_title.configure(text=f"## {topic['title']}")
        self.description_label.configure(text=f"📌 Tópico criado por {topic['author']} em {topic['created']}")
        
        # Mostrar botão voltar e esconder botão novo tópico
        self.back_button.pack(side="left", padx=(0, 15))
        self.new_topic_btn.pack_forget()
        
        # Mostrar campo de resposta
        self.reply_frame.pack(fill="x", pady=(0, 25))
        
        # Limpar e carregar mensagens
        self.clear_content()
        self.load_messages()
        
        # Atualizar lista de fóruns
        self.load_forums_list()
    
    def load_messages(self):
        """Carrega as mensagens do tópico atual"""
        topic = self.forums[self.current_forum_index]["topics"][self.current_topic_index]
        
        for i, message in enumerate(topic["messages"]):
            self.create_message_widget(message, i)
    
    def create_message_widget(self, message, index):
        """Cria um widget para cada mensagem"""
        if index > 0:
            separator = ctk.CTkFrame(
                self.content_frame,
                height=1,
                fg_color="#e5e7eb"
            )
            separator.pack(fill="x", pady=(15, 0))
        
        msg_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        msg_frame.pack(fill="x", padx=10, pady=(15, 0))
        
        author_label = ctk.CTkLabel(
            msg_frame,
            text=message["author"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#111827"
        )
        author_label.pack(anchor="w")
        
        message_label = ctk.CTkLabel(
            msg_frame,
            text=message["message"],
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left",
            text_color="#1f2937"
        )
        message_label.pack(anchor="w", pady=(8, 5))
        
        time_label = ctk.CTkLabel(
            msg_frame,
            text=message["time"],
            font=ctk.CTkFont(size=11),
            text_color="#9ca3af"
        )
        time_label.pack(anchor="w")
    
    def show_topics_view(self):
        """Volta para a visualização de tópicos"""
        self.view_mode = "topics"
        forum = self.forums[self.current_forum_index]
        
        self.current_title.configure(text=f"## {forum['name']}")
        self.description_label.configure(text=f"📋 {forum['description']}")
        
        self.back_button.pack_forget()
        self.new_topic_btn.pack(pady=(0, 15), padx=30)
        self.reply_frame.pack_forget()
        
        self.clear_content()
        self.load_topics()
    
    def clear_content(self):
        """Limpa a área de conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # ========== AÇÕES ==========
    def send_message(self):
        """Envia uma nova mensagem no tópico atual"""
        message = self.reply_entry.get("1.0", "end-1c").strip()
        if message and message != "Digite sua resposta...":
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            new_message = {
                "author": "Você",
                "message": message,
                "time": current_time
            }
            
            topic = self.forums[self.current_forum_index]["topics"][self.current_topic_index]
            topic["messages"].append(new_message)
            topic["replies"] += 1
            topic["last_message"] = current_time
            
            self.clear_content()
            self.load_messages()
            
            self.reply_entry.delete("1.0", "end")
            self.reply_entry.insert("1.0", "Digite sua resposta...")
            self.load_forums_list()
    
    def create_new_topic(self):
        """Abre diálogo para criar novo tópico"""
        # Implementação do diálogo (resumido)
        print("Abrir diálogo para criar novo tópico")
    
    def create_new_forum(self):
        """Abre diálogo para criar novo fórum"""
        print("Abrir diálogo para criar novo fórum")
    
    def edit_forum(self, index):
        """Editar fórum"""
        print(f"Editar fórum {index}")
    
    def confirm_delete_forum(self, index):
        """Confirmar exclusão de fórum"""
        print(f"Confirmar exclusão do fórum {index}")
    
    def edit_topic(self, index):
        """Editar tópico"""
        print(f"Editar tópico {index}")
    
    def confirm_delete_topic(self, index):
        """Confirmar exclusão de tópico"""
        print(f"Confirmar exclusão do tópico {index}")
    
    # ========== RUN ==========
    def run(self):
        """Método chamado pela sidebar_AP.py"""
        print("[FORUM] Executando versão COMPLETA...")
        
        if not self.ui_built:
            self.build_ui()
        
        if hasattr(self.master, 'pack'):
            self.master.pack(expand=True, fill="both")