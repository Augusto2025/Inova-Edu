import customtkinter as ctk
from datetime import datetime

# Configuração do tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ForumApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Forum")
        self.root.geometry("1100x750")
        
        # Dados dos fóruns com tópicos/descrição
        self.forums = [
            {
                "name": "Administrador de redes",
                "topic": "Configuração de OSPF e balanceamento de carga",
                "created": "20/03/2025",
                "posts": [
                    {"author": "Lucas Amaral", "message": "Galera, lembrando que amanhã é a apresentação dos projetos. Todo mundo com a topologia pronta?", "time": "12:15", "avatar": "LA"},
                    {"author": "Carla Souza", "message": "Quase! Tô finalizando o OSPF ainda. Mais alguém usando?", "time": "12:17", "avatar": "CS"},
                    {"author": "Vinícius Junior", "message": "Eu! Só travando no balanceamento de carga. 😊", "time": "12:17", "avatar": "VJ"},
                    {"author": "Diego Maradona", "message": "Fiz isso ontem. Posso te mandar o exemplo!", "time": "12:18", "avatar": "DM"},
                    {"author": "Ana", "message": "Meu foco é segurança com VLANs. Configurei DHCP snooping e port security 🛡️", "time": "12:20", "avatar": "AN"}
                ]
            },
            {
                "name": "Suporte e manutenção de notebooks",
                "topic": "Reparo de placas-mãe e substituição de componentes",
                "created": "12/01/2025",
                "posts": [
                    {"author": "João Silva", "message": "Alguém tem experiência com reparo de placa mãe em Dell Inspiron?", "time": "10:30", "avatar": "JS"},
                    {"author": "Maria Santos", "message": "Sim, qual o modelo específico? Já trabalhei com vários.", "time": "10:45", "avatar": "MS"}
                ]
            },
            {
                "name": "Segurança da informação",
                "topic": "Firewalls, VLANs e políticas de segurança",
                "created": "28/05/2025",
                "posts": [
                    {"author": "Carlos Oliveira", "message": "Discussão sobre firewalls de próxima geração e análise comportamental", "time": "09:15", "avatar": "CO"},
                    {"author": "Fernanda Lima", "message": "Recomendo o pfSense para soluções open-source!", "time": "09:30", "avatar": "FL"}
                ]
            }
        ]
        
        self.current_forum_index = 0
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # ========== TÍTULO ==========
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
            placeholder_text="Digite para buscar...",
            width=300,
            height=38,
            border_width=1,
            border_color="#d1d5db"
        )
        self.search_entry.pack(side="right", padx=25, pady=15)
        
        # ========== CONTEÚDO PRINCIPAL ==========
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # ========== COLUNA ESQUERDA - FÓRUNS ==========
        left_column = ctk.CTkFrame(content_frame, fg_color="#f9fafb")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Título "Forums"
        forums_title = ctk.CTkLabel(
            left_column,
            text="### Forums",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f2937"
        )
        forums_title.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Lista de fóruns (scrollável)
        self.forums_list_frame = ctk.CTkScrollableFrame(
            left_column,
            fg_color="transparent",
            scrollbar_button_color="#9ca3af"
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
            corner_radius=8
        )
        self.create_forum_btn.pack(pady=20, padx=20)
        
        # ========== COLUNA DIREITA - CONVERSAS ==========
        self.right_column = ctk.CTkFrame(content_frame, fg_color="white")
        self.right_column.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        self.right_column.grid_columnconfigure(0, weight=1)
        self.right_column.grid_rowconfigure(1, weight=1)
        
        # Header do fórum atual
        forum_header_frame = ctk.CTkFrame(self.right_column, fg_color="transparent")
        forum_header_frame.pack(fill="x", padx=30, pady=(25, 5))
        
        # Título do fórum atual
        self.current_forum_title = ctk.CTkLabel(
            forum_header_frame,
            text="",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#111827"
        )
        self.current_forum_title.pack(side="left")
        
        # Tópico do fórum atual (em destaque)
        topic_frame = ctk.CTkFrame(self.right_column, fg_color="#f3f4f6", corner_radius=8)
        topic_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        topic_icon = ctk.CTkLabel(
            topic_frame,
            text="📌",
            font=ctk.CTkFont(size=16)
        )
        topic_icon.pack(side="left", padx=(15, 10), pady=12)
        
        self.current_forum_topic = ctk.CTkLabel(
            topic_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#374151",
            justify="left"
        )
        self.current_forum_topic.pack(side="left", fill="x", expand=True, pady=12)
        
        # Separador
        separator = ctk.CTkFrame(self.right_column, height=1, fg_color="#e5e7eb")
        separator.pack(fill="x", padx=30, pady=(0, 15))
        
        # Área de conversas
        self.conversations_frame = ctk.CTkScrollableFrame(
            self.right_column,
            fg_color="transparent"
        )
        self.conversations_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Indicador de digitação
        self.typing_frame = ctk.CTkFrame(self.right_column, fg_color="#f9fafb", height=40)
        self.typing_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        self.typing_label = ctk.CTkLabel(
            self.typing_frame,
            text="✏️ Lucas está digitando...",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#6b7280"
        )
        self.typing_label.pack(anchor="w", padx=15, pady=10)
        
        # Campo de resposta
        self.reply_frame = ctk.CTkFrame(self.right_column, fg_color="white")
        self.reply_frame.pack(fill="x", padx=30, pady=(0, 25))
        
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
            hover_color="#1d4ed8"
        )
        self.send_btn.pack(side="right")
        
        # Carregar fóruns e fórum inicial
        self.load_forums_list()
        self.load_forum(0)
        self.setup_events()
    
    def load_forums_list(self):
        """Carrega a lista de fóruns"""
        for widget in self.forums_list_frame.winfo_children():
            widget.destroy()
            
        for i, forum in enumerate(self.forums):
            self.create_forum_list_item(forum, i)
    
    def create_forum_list_item(self, forum, index):
        """Cria um item na lista de fóruns"""
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
        forum_frame.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Nome do fórum com contador
        name_frame = ctk.CTkFrame(forum_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=15, pady=(12, 5))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=forum["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827"
        )
        name_label.pack(side="left")
        name_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Contador de mensagens
        msg_count = len(forum["posts"])
        count_label = ctk.CTkLabel(
            name_frame,
            text=f"💬 {msg_count}",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        count_label.pack(side="right")
        count_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Tópico/Descrição
        topic_frame = ctk.CTkFrame(forum_frame, fg_color="transparent")
        topic_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        topic_label = ctk.CTkLabel(
            topic_frame,
            text=f"📌 {forum['topic'][:40]}..." if len(forum['topic']) > 40 else f"📌 {forum['topic']}",
            font=ctk.CTkFont(size=11),
            text_color="#4b5563"
        )
        topic_label.pack(side="left")
        topic_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Data de criação e ações
        footer_frame = ctk.CTkFrame(forum_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        date_label = ctk.CTkLabel(
            footer_frame,
            text=f"Criado: {forum['created']}",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280"
        )
        date_label.pack(side="left")
        date_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
        
        # Botões de ação (editar e excluir)
        actions_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Botão Editar
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
        
        # Botão Excluir
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=30,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#fee2e2",
            text_color="#ef4444",
            command=lambda idx=index: self.delete_forum(idx)
        )
        delete_btn.pack(side="left")
        
        # Link
        link_label = ctk.CTkLabel(
            footer_frame,
            text="🔗",
            font=ctk.CTkFont(size=12)
        )
        link_label.pack(side="right", padx=(10, 0))
        link_label.bind("<Button-1>", lambda e, idx=index: self.load_forum(idx))
    
    def load_forum(self, index):
        """Carrega um fórum específico"""
        self.current_forum_index = index
        forum = self.forums[index]
        
        # Atualizar título e tópico
        self.current_forum_title.configure(text=f"## {forum['name']}")
        self.current_forum_topic.configure(text=forum["topic"])
        
        # Limpar conversas anteriores
        for widget in self.conversations_frame.winfo_children():
            widget.destroy()
        
        # Carregar posts
        for post in forum["posts"]:
            self.create_post_widget(post)
        
        # Atualizar lista de fóruns
        self.load_forums_list()
    
    def create_post_widget(self, post):
        """Cria um widget para cada post"""
        # Separador
        separator = ctk.CTkFrame(
            self.conversations_frame,
            height=1,
            fg_color="#e5e7eb"
        )
        separator.pack(fill="x", pady=(15, 0))
        
        # Frame do post
        post_frame = ctk.CTkFrame(
            self.conversations_frame,
            fg_color="transparent"
        )
        post_frame.pack(fill="x", padx=10, pady=(15, 0))
        
        # Nome do autor em negrito
        author_label = ctk.CTkLabel(
            post_frame,
            text=post["author"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#111827"
        )
        author_label.pack(anchor="w")
        
        # Mensagem
        message_label = ctk.CTkLabel(
            post_frame,
            text=post["message"],
            font=ctk.CTkFont(size=14),
            wraplength=600,
            justify="left",
            text_color="#1f2937"
        )
        message_label.pack(anchor="w", pady=(8, 5))
        
        # Hora
        time_label = ctk.CTkLabel(
            post_frame,
            text=post["time"],
            font=ctk.CTkFont(size=11),
            text_color="#9ca3af"
        )
        time_label.pack(anchor="w")
    
    def setup_events(self):
        """Configura eventos"""
        self.create_forum_btn.configure(command=self.create_new_forum)
        self.send_btn.configure(command=self.send_message)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_forums())
        
        # Placeholder interativo
        self.reply_entry.bind("<FocusIn>", self.clear_placeholder)
        self.reply_entry.bind("<FocusOut>", self.restore_placeholder)
    
    def clear_placeholder(self, event):
        if self.reply_entry.get("1.0", "end-1c") == "Digite sua resposta...":
            self.reply_entry.delete("1.0", "end")
    
    def restore_placeholder(self, event):
        if not self.reply_entry.get("1.0", "end-1c").strip():
            self.reply_entry.insert("1.0", "Digite sua resposta...")
    
    def create_new_forum(self):
        """Cria um novo fórum com nome e tópico"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Criar novo fórum")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título
        title = ctk.CTkLabel(
            content,
            text="Criar novo fórum",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#111827"
        )
        title.pack(pady=(0, 25))
        
        # Nome do fórum
        name_label = ctk.CTkLabel(
            content,
            text="Nome do fórum:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        )
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_entry = ctk.CTkEntry(
            content,
            placeholder_text="Ex: Programação Python",
            height=40,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13)
        )
        name_entry.pack(fill="x", pady=(0, 20))
        
        # Tópico/Descrição
        topic_label = ctk.CTkLabel(
            content,
            text="Sobre o que é este fórum?",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        )
        topic_label.pack(anchor="w", pady=(0, 5))
        
        topic_textbox = ctk.CTkTextbox(
            content,
            height=100,
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13)
        )
        topic_textbox.pack(fill="x", pady=(0, 25))
        topic_textbox.insert("1.0", "Digite a descrição/tópico do fórum...")
        
        # Botões
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(5, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=110,
            height=40,
            fg_color="transparent",
            hover_color="#f3f4f6",
            text_color="#374151",
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13),
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        def save_forum():
            forum_name = name_entry.get().strip()
            forum_topic = topic_textbox.get("1.0", "end-1c").strip()
            
            if forum_name and forum_topic and forum_topic != "Digite a descrição/tópico do fórum...":
                new_forum = {
                    "name": forum_name,
                    "topic": forum_topic,
                    "created": datetime.now().strftime("%d/%m/%Y"),
                    "posts": []
                }
                self.forums.append(new_forum)
                self.load_forums_list()
                self.load_forum(len(self.forums) - 1)
                dialog.destroy()
            else:
                # Mostrar erro
                error_label = ctk.CTkLabel(
                    content,
                    text="Preencha todos os campos!",
                    font=ctk.CTkFont(size=12),
                    text_color="#ef4444"
                )
                error_label.pack(pady=(10, 0))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Criar fórum",
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#4f46e5",
            hover_color="#4338ca",
            command=save_forum
        )
        save_btn.pack(side="right")
        
        # Placeholder do topic_textbox
        def clear_topic_placeholder(event):
            if topic_textbox.get("1.0", "end-1c") == "Digite a descrição/tópico do fórum...":
                topic_textbox.delete("1.0", "end")
        
        def restore_topic_placeholder(event):
            if not topic_textbox.get("1.0", "end-1c").strip():
                topic_textbox.insert("1.0", "Digite a descrição/tópico do fórum...")
        
        topic_textbox.bind("<FocusIn>", clear_topic_placeholder)
        topic_textbox.bind("<FocusOut>", restore_topic_placeholder)
    
    def edit_forum(self, index):
        """Edita o nome e tópico do fórum"""
        forum = self.forums[index]
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Editar fórum")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título
        title = ctk.CTkLabel(
            content,
            text="Editar fórum",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#111827"
        )
        title.pack(pady=(0, 25))
        
        # Nome do fórum
        name_label = ctk.CTkLabel(
            content,
            text="Nome do fórum:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        )
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_entry = ctk.CTkEntry(
            content,
            height=40,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13)
        )
        name_entry.insert(0, forum["name"])
        name_entry.pack(fill="x", pady=(0, 20))
        
        # Tópico/Descrição
        topic_label = ctk.CTkLabel(
            content,
            text="Sobre o que é este fórum?",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        )
        topic_label.pack(anchor="w", pady=(0, 5))
        
        topic_textbox = ctk.CTkTextbox(
            content,
            height=100,
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13)
        )
        topic_textbox.insert("1.0", forum["topic"])
        topic_textbox.pack(fill="x", pady=(0, 25))
        
        # Botões
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(5, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=110,
            height=40,
            fg_color="transparent",
            hover_color="#f3f4f6",
            text_color="#374151",
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13),
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        def update_forum():
            new_name = name_entry.get().strip()
            new_topic = topic_textbox.get("1.0", "end-1c").strip()
            
            if new_name and new_topic:
                self.forums[index]["name"] = new_name
                self.forums[index]["topic"] = new_topic
                self.load_forums_list()
                
                # Se for o fórum atual, atualizar título e tópico
                if index == self.current_forum_index:
                    self.current_forum_title.configure(text=f"## {new_name}")
                    self.current_forum_topic.configure(text=new_topic)
                
                dialog.destroy()
            else:
                # Mostrar erro
                error_label = ctk.CTkLabel(
                    content,
                    text="Preencha todos os campos!",
                    font=ctk.CTkFont(size=12),
                    text_color="#ef4444"
                )
                error_label.pack(pady=(10, 0))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar alterações",
            width=150,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#4f46e5",
            hover_color="#4338ca",
            command=update_forum
        )
        save_btn.pack(side="right")
    
    def delete_forum(self, index):
        """Exclui um fórum"""
        forum_name = self.forums[index]["name"]
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Excluir fórum")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (450 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        content = ctk.CTkFrame(dialog, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Ícone de alerta
        alert_label = ctk.CTkLabel(
            content,
            text="⚠️",
            font=ctk.CTkFont(size=40)
        )
        alert_label.pack(pady=(0, 15))
        
        # Mensagem
        msg_label = ctk.CTkLabel(
            content,
            text=f"Tem certeza que deseja excluir o fórum?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#111827"
        )
        msg_label.pack(pady=(0, 5))
        
        forum_name_label = ctk.CTkLabel(
            content,
            text=f"\"{forum_name}\"",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ef4444"
        )
        forum_name_label.pack(pady=(0, 10))
        
        sub_msg = ctk.CTkLabel(
            content,
            text="Todas as mensagens serão permanentemente perdidas.",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280"
        )
        sub_msg.pack(pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=110,
            height=40,
            fg_color="transparent",
            hover_color="#f3f4f6",
            text_color="#374151",
            border_width=1,
            border_color="#d1d5db",
            font=ctk.CTkFont(size=13),
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        def confirm_delete():
            # Remover fórum
            del self.forums[index]
            
            # Ajustar índice atual
            if len(self.forums) > 0:
                if index >= len(self.forums):
                    index = len(self.forums) - 1
                self.load_forum(index)
            else:
                # Criar fórum padrão se não houver nenhum
                default_forum = {
                    "name": "Fórum principal",
                    "topic": "Discussões gerais",
                    "created": datetime.now().strftime("%d/%m/%Y"),
                    "posts": []
                }
                self.forums.append(default_forum)
                self.load_forum(0)
            
            self.load_forums_list()
            dialog.destroy()
        
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Sim, excluir",
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=confirm_delete
        )
        delete_btn.pack(side="right")
    
    def send_message(self):
        """Envia uma nova mensagem"""
        message = self.reply_entry.get("1.0", "end-1c").strip()
        if message and message != "Digite sua resposta...":
            # Adicionar mensagem ao fórum atual
            new_post = {
                "author": "Você",
                "message": message,
                "time": datetime.now().strftime("%H:%M"),
                "avatar": "VC"
            }
            self.forums[self.current_forum_index]["posts"].append(new_post)
            
            # Recarregar conversas e lista
            self.load_forum(self.current_forum_index)
            self.load_forums_list()
            
            # Limpar campo
            self.reply_entry.delete("1.0", "end")
            self.reply_entry.insert("1.0", "Digite sua resposta...")
    
    def search_forums(self):
        """Busca nos fóruns"""
        search_term = self.search_entry.get().lower()
        
        if not search_term:
            self.load_forums_list()
            return
        
        # Filtrar fóruns que correspondem à busca
        filtered_forums = []
        for forum in self.forums:
            if (search_term in forum["name"].lower() or 
                search_term in forum["topic"].lower() or
                any(search_term in post["message"].lower() or 
                    search_term in post["author"].lower() 
                    for post in forum["posts"])):
                filtered_forums.append(forum)
        
        # Atualizar lista com resultados
        for widget in self.forums_list_frame.winfo_children():
            widget.destroy()
        
        if filtered_forums:
            for i, forum in enumerate(filtered_forums):
                self.create_forum_list_item(forum, i)
        else:
            no_results = ctk.CTkLabel(
                self.forums_list_frame,
                text="🔍 Nenhum fórum encontrado",
                font=ctk.CTkFont(size=13),
                text_color="#6b7280"
            )
            no_results.pack(pady=30)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ForumApp()
    app.run()