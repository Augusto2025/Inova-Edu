import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.forum_controller import ForumController

# Paleta de Cores e Estilos
AZUL_SENAC = "#004A8D"
AZUL_HOVER = "#003566"
BG_TELA = "#f8fafc"
BG_HOVER = "#e2e8f0"
CARD_BG = "#ffffff"
TEXTO_ESCURO = "#0f172a"
TEXTO_MUTED = "#64748b"
BORDA_COLOR = "#e2e8f0"
COR_ERRO = "#dc2626"


class Forum(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color=BG_TELA)
        self.janela = master
        self.controller = ForumController()

        # Modos de Visualização: "hub" | "topics" | "messages"
        self.view = "hub"
        
        self.current_forum_id = None
        self.current_forum_name = ""
        self.current_topic_id = None
        self.current_topic_title = ""

        # Tipografias
        self.f_title = ("Segoe UI", 18, "bold")
        self.f_subtitle = ("Segoe UI", 14, "bold")
        self.f_bold = ("Segoe UI", 13, "bold")
        self.f_norm = ("Segoe UI", 13)
        self.f_small = ("Segoe UI", 11)

        self.setup_ui()

    def setup_ui(self):
        """Estrutura base da interface"""
        from assets.header import HeaderPadrao
        self.header = HeaderPadrao(self, titulo="Fórum Acadêmico", comando_voltar=None)

        # Container de Ações no Header
        self.header_action_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.header_action_frame.pack(side="right", padx=20)

        # 1. BARRA SUPERIOR (Apenas Breadcrumbs)
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.top_bar.pack(fill="x", side="top", padx=25, pady=(4, 0))
        
        self.breadcrumb_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.breadcrumb_frame.pack(side="left")

        # 2. ÁREA CENTRAL DE CONTEÚDO (Com Rolagem)
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=25, pady=(5, 15))

        # 3. CAIXA FIXA DE RESPOSTA NO RODAPÉ (Ativa apenas na view 'messages')
        self.reply_frame = ctk.CTkFrame(self, fg_color="#ffffff", height=75, corner_radius=12, border_width=1, border_color=BORDA_COLOR)
        
        self.reply_entry = ctk.CTkTextbox(self.reply_frame, height=45, fg_color="transparent", font=self.f_norm, text_color=TEXTO_ESCURO)
        self.reply_entry.pack(side="left", fill="x", expand=True, padx=15, pady=10)
        
        self.btn_send = ctk.CTkButton(
            self.reply_frame, text="Enviar Resposta", width=120, height=38,
            fg_color=AZUL_SENAC, hover_color=AZUL_HOVER, font=self.f_bold,
            corner_radius=8, command=self.send_message
        )
        self.btn_send.pack(side="right", padx=15)
        self.setup_placeholder()

        # Inicia na visão inicial (Hub)
        self.show_hub()

    def setup_placeholder(self):
        ph = "Escreva sua resposta aqui..."
        self.reply_entry.delete("1.0", "end")
        self.reply_entry.insert("1.0", ph)
        self.reply_entry.bind("<FocusIn>", lambda e: self.reply_entry.delete("1.0", "end") if self.reply_entry.get("1.0", "end-1c") == ph else None)
        self.reply_entry.bind("<FocusOut>", lambda e: self.reply_entry.insert("1.0", ph) if not self.reply_entry.get("1.0", "end-1c").strip() else None)

    # =========================================================================
    # NAVEGAÇÃO, BREADCRUMBS E AÇÕES DO HEADER
    # =========================================================================
    def update_header_and_breadcrumbs(self):
        """Atualiza a rota fluida e os botões de ação do Header"""
        for w in self.breadcrumb_frame.winfo_children():
            w.destroy()
        for w in self.header_action_frame.winfo_children():
            w.destroy()

        # Nível 1: Hub
        ctk.CTkButton(
            self.breadcrumb_frame, text="🏠 Hub de Fóruns",
            font=self.f_bold if self.view == "hub" else self.f_norm,
            text_color=AZUL_SENAC if self.view == "hub" else TEXTO_MUTED,
            fg_color="transparent", hover_color="#e2e8f0", width=10,
            command=self.show_hub
        ).pack(side="left")

        # Nível 2: Categoria Selecionada
        if self.view in ["topics", "messages"] and self.current_forum_name:
            ctk.CTkLabel(self.breadcrumb_frame, text=" / ", font=self.f_norm, text_color="#94a3b8").pack(side="left")
            ctk.CTkButton(
                self.breadcrumb_frame, text=f"📁 {self.current_forum_name}",
                font=self.f_bold if self.view == "topics" else self.f_norm,
                text_color=AZUL_SENAC if self.view == "topics" else TEXTO_MUTED,
                fg_color="transparent", hover_color="#e2e8f0", width=10,
                command=lambda: self.show_forum(self.current_forum_id, self.current_forum_name)
            ).pack(side="left")

        # Nível 3: Tópico Aberto
        if self.view == "messages" and self.current_topic_title:
            ctk.CTkLabel(self.breadcrumb_frame, text=" / ", font=self.f_norm, text_color="#94a3b8").pack(side="left")
            ctk.CTkLabel(self.breadcrumb_frame, text=f"💬 {self.current_topic_title}", font=self.f_bold, text_color=TEXTO_ESCURO).pack(side="left")

        # Botão de Criar no Header
        if self.view == "hub":
            ctk.CTkButton(
                self.header_action_frame, text="+ Criar Novo Fórum",
                fg_color="transparent", text_color="#ffffff", border_color="#ffffff", border_width=1,
                hover_color=AZUL_HOVER, font=self.f_bold, corner_radius=8, height=34,
                command=self.modal_novo_forum
            ).pack(side="right")
        elif self.view == "topics":
            ctk.CTkButton(
                self.header_action_frame, text="+ Criar Novo Tópico",
                fg_color="transparent", text_color="#ffffff", border_color="#ffffff", border_width=1,
                hover_color=AZUL_HOVER, font=self.f_bold, corner_radius=8, height=34,
                command=self.modal_novo_topico
            ).pack(side="right")

    # =========================================================================
    # NÍVEL 1: HUB CENTRAL DE FÓRUNS (Com Separação: Meus vs Outros)
    # =========================================================================
    def show_hub(self):
        self.view = "hub"
        self.current_forum_id = None
        self.current_forum_name = ""
        self.current_topic_id = None
        self.current_topic_title = ""

        self.reply_frame.pack_forget()
        self.update_header_and_breadcrumbs()
        self.render_hub_view()

    def render_hub_view(self):
        for w in self.main_container.winfo_children():
            w.destroy()

        sec_header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sec_header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(sec_header, text="Categorias & Espaços de Discussão", font=self.f_title, text_color=TEXTO_ESCURO).pack(side="left")

        foruns = self.controller.listar_foruns() or []

        # Estado Vazio
        if not foruns:
            empty_box = ctk.CTkFrame(self.main_container, fg_color="transparent")
            empty_box.pack(fill="x", pady=20, ipady=20)
            
            ctk.CTkLabel(empty_box, text="💬", font=("Segoe UI", 42)).pack(pady=(0, 8))
            ctk.CTkLabel(empty_box, text="Nenhum Fórum Encontrado", font=self.f_title, text_color=TEXTO_ESCURO).pack()
            ctk.CTkLabel(empty_box, text="Ainda não existem categorias criadas. Seja o primeiro a inaugurar um espaço de discussão!", font=self.f_norm, text_color=TEXTO_MUTED).pack(pady=(6, 16))
            
            ctk.CTkButton(
                empty_box, text="+ Criar o Primeiro Fórum", fg_color=AZUL_SENAC, hover_color=AZUL_HOVER,
                font=self.f_bold, corner_radius=8, height=36, width=200, command=self.modal_novo_forum
            ).pack()
            return

        # Separação: Meus Fóruns vs Outros Fóruns
        meus_foruns = [f for f in foruns if f.get("pode_gerenciar") or f.get("autor_nome") == self.controller.nome_usuario_logado]
        outros_foruns = [f for f in foruns if f not in meus_foruns]

        def criar_card_forum(f):
            fid = f["idforum"]
            fnome = f["nome"]
            autor = f.get("autor_nome", "")
            pode_gerenciar = f.get("pode_gerenciar") or autor == self.controller.nome_usuario_logado

            card = ctk.CTkFrame(self.main_container, fg_color=CARD_BG, corner_radius=12, border_width=1, border_color=BORDA_COLOR)
            card.pack(fill="x", pady=6)

            left_info = ctk.CTkFrame(card, fg_color="transparent")
            left_info.pack(side="left", padx=20, pady=16)

            ctk.CTkLabel(left_info, text="📁", font=("Segoe UI", 22)).pack(side="left", padx=(0, 15))
            
            title_box = ctk.CTkFrame(left_info, fg_color="transparent")
            title_box.pack(side="left")
            ctk.CTkLabel(title_box, text=fnome, font=self.f_subtitle, text_color=TEXTO_ESCURO, anchor="w").pack(anchor="w")
            
            desc = f"Criado por você" if pode_gerenciar else f"Criado por: {autor}" if autor else "Espaço aberto para dúvidas e trocas de conhecimento"
            ctk.CTkLabel(title_box, text=desc, font=self.f_small, text_color=TEXTO_MUTED, anchor="w").pack(anchor="w")

            right_actions = ctk.CTkFrame(card, fg_color="transparent")
            right_actions.pack(side="right", padx=15)

            if pode_gerenciar:
                ctk.CTkButton(right_actions, text="✏️", width=32, height=32, fg_color="transparent", hover_color="#f1f5f9", command=lambda id=fid, n=fnome: self.modal_editar("forum", id, n)).pack(side="left", padx=2)
                ctk.CTkButton(right_actions, text="🗑️", width=32, height=32, fg_color="transparent", hover_color="#fee2e2", text_color=COR_ERRO, command=lambda id=fid: self.modal_excluir("forum", id)).pack(side="left", padx=2)

            ctk.CTkButton(
                right_actions, text="Acessar Fórum →", fg_color="#e0f2fe", hover_color="#bae6fd",
                text_color=AZUL_SENAC, font=self.f_bold, height=36, corner_radius=8,
                command=lambda id=fid, n=fnome: self.show_forum(id, n)
            ).pack(side="left", padx=(10, 0))

        # Renderiza Meus Fóruns
        if meus_foruns:
            ctk.CTkLabel(self.main_container, text="👤 Meus Fóruns", font=self.f_subtitle, text_color=AZUL_SENAC, anchor="w").pack(fill="x", pady=(5, 5))
            for f in meus_foruns:
                criar_card_forum(f)

        # Renderiza Outros Fóruns
        if outros_foruns:
            pad_top = 20 if meus_foruns else 5
            ctk.CTkLabel(self.main_container, text="🌐 Outros Fóruns", font=self.f_subtitle, text_color=AZUL_SENAC, anchor="w").pack(fill="x", pady=(pad_top, 5))
            for f in outros_foruns:
                criar_card_forum(f)

    # =========================================================================
    # NÍVEL 2: VISÃO DA CATEGORIA (Com Separação: Meus Tópicos vs Outros)
    # =========================================================================
    def show_forum(self, forum_id, forum_nome):
        self.view = "topics"
        self.current_forum_id = forum_id
        self.current_forum_name = forum_nome
        self.current_topic_id = None
        self.current_topic_title = ""

        self.reply_frame.pack_forget()
        self.update_header_and_breadcrumbs()
        self.render_topics_view()

    def render_topics_view(self):
        for w in self.main_container.winfo_children():
            w.destroy()

        topicos = self.controller.listar_topicos(self.current_forum_id) or []

        header_card = ctk.CTkFrame(self.main_container, fg_color=AZUL_SENAC, corner_radius=12)
        header_card.pack(fill="x", pady=(0, 15))
        
        info_sub = ctk.CTkFrame(header_card, fg_color="transparent")
        info_sub.pack(fill="x", padx=20, pady=18)
        
        ctk.CTkLabel(info_sub, text=f"📁 {self.current_forum_name}", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(anchor="w")
        ctk.CTkLabel(info_sub, text=f"Exibindo {len(topicos)} tópico(s) cadastrado(s) nesta categoria", font=self.f_small, text_color="#bae6fd").pack(anchor="w")

        # Estado Vazio
        if not topicos:
            empty = ctk.CTkFrame(self.main_container, fg_color="transparent")
            empty.pack(fill="x", pady=20, ipady=20)
            
            ctk.CTkLabel(empty, text="📌", font=("Segoe UI", 42)).pack(pady=(0, 8))
            ctk.CTkLabel(empty, text="Nenhum Tópico Criado Ainda", font=self.f_title, text_color=TEXTO_ESCURO).pack()
            ctk.CTkLabel(empty, text=f"A categoria '{self.current_forum_name}' ainda não possui discussões abertas.", font=self.f_norm, text_color=TEXTO_MUTED).pack(pady=(6, 16))
            
            ctk.CTkButton(
                empty, text="+ Iniciar Primeiro Tópico", fg_color=AZUL_SENAC, hover_color=AZUL_HOVER,
                font=self.f_bold, corner_radius=8, height=36, width=200, command=self.modal_novo_topico
            ).pack()
            return

        # Separação: Meus Tópicos vs Outros Tópicos
        meus_topicos = [t for t in topicos if t.get("pode_gerenciar") or t.get("autor_nome") == self.controller.nome_usuario_logado]
        outros_topicos = [t for t in topicos if t not in meus_topicos]

        def criar_card_topico(t):
            tid = t["idtopico"]
            ttitulo = t["titulo"]
            autor = t.get("autor_nome", "")
            pode_gerenciar = t.get("pode_gerenciar") or autor == self.controller.nome_usuario_logado

            card = ctk.CTkFrame(self.main_container, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDA_COLOR)
            card.pack(fill="x", pady=5)

            left = ctk.CTkFrame(card, fg_color="transparent")
            left.pack(side="left", padx=20, pady=14)

            ctk.CTkLabel(left, text="💬", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
            
            info_box = ctk.CTkFrame(left, fg_color="transparent")
            info_box.pack(side="left")
            ctk.CTkLabel(info_box, text=ttitulo, font=self.f_bold, text_color=TEXTO_ESCURO, anchor="w").pack(anchor="w")
            if autor and not pode_gerenciar:
                ctk.CTkLabel(info_box, text=f"Criado por: {autor}", font=self.f_small, text_color=TEXTO_MUTED, anchor="w").pack(anchor="w")

            right = ctk.CTkFrame(card, fg_color="transparent")
            right.pack(side="right", padx=15)

            if pode_gerenciar:
                ctk.CTkButton(right, text="✏️", width=30, height=30, fg_color="transparent", hover_color="#f1f5f9", command=lambda id=tid, t=ttitulo: self.modal_editar("topic", id, t)).pack(side="left", padx=2)
                ctk.CTkButton(right, text="🗑️", width=30, height=30, fg_color="transparent", hover_color="#fee2e2", text_color=COR_ERRO, command=lambda id=tid: self.modal_excluir("topic", id)).pack(side="left", padx=2)

            ctk.CTkButton(
                right, text="Abrir Tópico →", fg_color="transparent", hover_color="#f0f9ff",
                text_color=AZUL_SENAC, font=self.f_bold, height=32,
                command=lambda id=tid, t=ttitulo: self.show_thread(id, t)
            ).pack(side="left", padx=(5, 0))

        # Renderiza Meus Tópicos
        if meus_topicos:
            ctk.CTkLabel(self.main_container, text="👤 Meus Tópicos", font=self.f_subtitle, text_color=AZUL_SENAC, anchor="w").pack(fill="x", pady=(5, 5))
            for t in meus_topicos:
                criar_card_topico(t)

        # Renderiza Outros Tópicos
        if outros_topicos:
            pad_top = 20 if meus_topicos else 5
            ctk.CTkLabel(self.main_container, text="🌐 Outros Tópicos", font=self.f_subtitle, text_color=AZUL_SENAC, anchor="w").pack(fill="x", pady=(pad_top, 5))
            for t in outros_topicos:
                criar_card_topico(t)

    # =========================================================================
    # NÍVEL 3: THREAD DA CONVERSA (Chat de Mensagens)
    # =========================================================================
    def show_thread(self, topic_id, topic_titulo):
        self.view = "messages"
        self.current_topic_id = topic_id
        self.current_topic_title = topic_titulo

        self.reply_frame.pack(fill="x", side="bottom", padx=25, pady=(0, 15))
        self.update_header_and_breadcrumbs()
        self.render_thread_view()

    def render_thread_view(self):
        for w in self.main_container.winfo_children():
            w.destroy()

        mensagens = self.controller.listar_mensagens(self.current_topic_id) or []

        top_title = ctk.CTkFrame(self.main_container, fg_color="transparent")
        top_title.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(top_title, text=f"📌 {self.current_topic_title}", font=self.f_title, text_color=TEXTO_ESCURO).pack(anchor="w")

        # Estado Vazio
        if not mensagens:
            msg_empty = ctk.CTkFrame(self.main_container, fg_color="transparent")
            msg_empty.pack(fill="x", pady=20, ipady=20)
            
            ctk.CTkLabel(msg_empty, text="✨", font=("Segoe UI", 42)).pack(pady=(0, 8))
            ctk.CTkLabel(msg_empty, text="Sua conversa começa aqui!", font=self.f_title, text_color=TEXTO_ESCURO).pack()
            ctk.CTkLabel(msg_empty, text="Ainda não há respostas nesta discussão. Escreva sua dúvida ou mensagem na caixa abaixo!", font=self.f_norm, text_color=TEXTO_MUTED).pack(pady=(6, 0))
            return

        for m in mensagens:
            autor = m.get("autor_nome", "Usuário")
            is_me = (autor == self.controller.nome_usuario_logado)

            raw_data = m.get("Data_criacao") or m.get("data_criacao")
            data_formatada = ""
            if raw_data:
                try:
                    data_formatada = raw_data.strftime("%d/%m/%Y %H:%M") if hasattr(raw_data, "strftime") else str(raw_data)[:16].replace("-", "/")
                except:
                    data_formatada = ""

            if is_me:
                fg_balao, cor_texto, cor_autor, align, txt_autor = AZUL_SENAC, "#ffffff", "#bae6fd", "e", f"{autor} (Você)"
                cor_hora = "#cbd5e1"
            else:
                fg_balao, cor_texto, cor_autor, align, txt_autor = CARD_BG, TEXTO_ESCURO, TEXTO_MUTED, "w", autor
                cor_hora = TEXTO_MUTED

            linha = ctk.CTkFrame(self.main_container, fg_color="transparent")
            linha.pack(fill="x", pady=6)

            balao = ctk.CTkFrame(linha, fg_color=fg_balao, corner_radius=12, border_width=1, border_color=AZUL_SENAC if is_me else BORDA_COLOR)
            balao.pack(anchor=align, padx=5)

            top_bar = ctk.CTkFrame(balao, fg_color="transparent")
            top_bar.pack(fill="x", padx=14, pady=(8, 2))

            ctk.CTkLabel(top_bar, text=txt_autor, font=self.f_bold, text_color=cor_autor).pack(side="left")

            if is_me:
                mid = m["idmensagem"]
                mcont = m["conteudo"]
                ctk.CTkButton(top_bar, text="excluir", width=10, height=14, font=("Segoe UI", 10), fg_color="transparent", hover_color="#b91c1c", text_color="#fca5a5", command=lambda id=mid: self.modal_excluir("message", id)).pack(side="right", padx=(5, 0))
                ctk.CTkButton(top_bar, text="editar", width=10, height=14, font=("Segoe UI", 10), fg_color="transparent", hover_color=AZUL_HOVER, text_color="#e0f2fe", command=lambda id=mid, c=mcont: self.modal_editar("message", id, c)).pack(side="right")

            ctk.CTkLabel(balao, text=m["conteudo"], font=self.f_norm, text_color=cor_texto, wraplength=600, justify="left").pack(anchor="w", padx=14, pady=(2, 4))

            if data_formatada:
                bot_bar = ctk.CTkFrame(balao, fg_color="transparent")
                bot_bar.pack(fill="x", padx=14, pady=(0, 6))
                ctk.CTkLabel(bot_bar, text=data_formatada, font=("Segoe UI", 9, "italic"), text_color=cor_hora).pack(side="right")

    def send_message(self):
        txt = self.reply_entry.get("1.0", "end-1c").strip()
        if txt and txt != "Escreva sua resposta aqui...":
            if self.current_topic_id is not None:
                if self.controller.enviar_mensagem(self.current_topic_id, txt):
                    self.reply_entry.delete("1.0", "end")
                    self.setup_placeholder()
                    self.render_thread_view()
                else:
                    messagebox.showerror("Erro", "Não foi possível enviar a mensagem.")

    # =========================================================================
    # MODAIS CUSTOMIZADOS
    # =========================================================================
    def modal_novo_forum(self):
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Novo Fórum")
        modal.geometry("480x280")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)

        m_head = ctk.CTkFrame(modal, fg_color=AZUL_SENAC, corner_radius=0, height=55)
        m_head.pack(fill="x")
        ctk.CTkLabel(m_head, text="📁 Novo Espaço de Discussão", font=self.f_subtitle, text_color="#ffffff").pack(pady=15)

        body = ctk.CTkFrame(modal, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(body, text="Nome do Fórum / Categoria:", font=self.f_bold, text_color=AZUL_SENAC).pack(anchor="w", pady=(0, 5))
        txt_name = ctk.CTkEntry(body, fg_color="#ffffff", border_color="#cbd5e1", height=40, corner_radius=8, placeholder_text="Ex: Banco de Dados, Programação...")
        txt_name.pack(fill="x", pady=(0, 20))
        txt_name.focus_set()

        def salvar():
            nome = txt_name.get().strip()
            if nome:
                if self.controller.cadastrar_forum(nome):
                    self.show_hub()
                    modal.destroy()

        btns = ctk.CTkFrame(body, fg_color="transparent")
        btns.pack(fill="x", side="bottom")

        ctk.CTkButton(btns, text="Cancelar", fg_color="#e2e8f0", text_color=TEXTO_ESCURO, hover_color="#cbd5e1", height=38, command=modal.destroy).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(btns, text="Criar Fórum", fg_color=AZUL_SENAC, text_color="#ffffff", hover_color=AZUL_HOVER, height=38, command=salvar).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def modal_novo_topico(self):
        if self.current_forum_id is None:
            return

        modal = ctk.CTkToplevel(self.janela)
        modal.title("Novo Tópico")
        modal.geometry("480x280")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)

        m_head = ctk.CTkFrame(modal, fg_color=AZUL_SENAC, corner_radius=0, height=55)
        m_head.pack(fill="x")
        ctk.CTkLabel(m_head, text="💬 Novo Tópico de Discussão", font=self.f_subtitle, text_color="#ffffff").pack(pady=15)

        body = ctk.CTkFrame(modal, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(body, text="Título do Novo Tópico:", font=self.f_bold, text_color=AZUL_SENAC).pack(anchor="w", pady=(0, 5))
        txt_title = ctk.CTkEntry(body, fg_color="#ffffff", border_color="#cbd5e1", height=40, corner_radius=8, placeholder_text="Ex: Dúvida sobre a entrega do Projeto...")
        txt_title.pack(fill="x", pady=(0, 20))
        txt_title.focus_set()

        def salvar():
            titulo = txt_title.get().strip()
            if titulo:
                if self.controller.cadastrar_topico(self.current_forum_id, titulo):
                    self.render_topics_view()
                    modal.destroy()

        btns = ctk.CTkFrame(body, fg_color="transparent")
        btns.pack(fill="x", side="bottom")

        ctk.CTkButton(btns, text="Cancelar", fg_color="#e2e8f0", text_color=TEXTO_ESCURO, hover_color="#cbd5e1", height=38, command=modal.destroy).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(btns, text="Criar Tópico", fg_color=AZUL_SENAC, text_color="#ffffff", hover_color=AZUL_HOVER, height=38, command=salvar).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def modal_editar(self, tipo, item_id, valor_atual):
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Editar Registro")
        modal.geometry("480x280")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)

        m_head = ctk.CTkFrame(modal, fg_color=AZUL_SENAC, corner_radius=0, height=55)
        m_head.pack(fill="x")
        ctk.CTkLabel(m_head, text="📝 Editar Registro", font=self.f_subtitle, text_color="#ffffff").pack(pady=15)

        body = ctk.CTkFrame(modal, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(body, text="Novo Texto:", font=self.f_bold, text_color=AZUL_SENAC).pack(anchor="w", pady=(0, 5))
        txt_input = ctk.CTkEntry(body, fg_color="#ffffff", border_color="#cbd5e1", height=40, corner_radius=8)
        txt_input.pack(fill="x", pady=(0, 20))
        txt_input.insert(0, valor_atual)
        txt_input.focus_set()

        def salvar():
            val = txt_input.get().strip()
            if val and val != valor_atual:
                if tipo == "forum":
                    if self.controller.editar_forum(item_id, val): self.show_hub()
                elif tipo == "topic":
                    if self.controller.editar_topico(item_id, val): self.render_topics_view()
                elif tipo == "message":
                    if self.controller.editar_mensagem(item_id, val): self.render_thread_view()
            modal.destroy()

        btns = ctk.CTkFrame(body, fg_color="transparent")
        btns.pack(fill="x", side="bottom")

        ctk.CTkButton(btns, text="Cancelar", fg_color="#e2e8f0", text_color=TEXTO_ESCURO, hover_color="#cbd5e1", height=38, command=modal.destroy).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(btns, text="Salvar Alterações", fg_color=AZUL_SENAC, text_color="#ffffff", hover_color=AZUL_HOVER, height=38, command=salvar).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def modal_excluir(self, tipo, item_id):
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Confirmar Exclusão")
        modal.geometry("420x220")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)

        m_head = ctk.CTkFrame(modal, fg_color=COR_ERRO, corner_radius=0, height=55)
        m_head.pack(fill="x")
        ctk.CTkLabel(m_head, text="⚠️ Atenção: Confirmar Exclusão", font=self.f_subtitle, text_color="#ffffff").pack(pady=15)

        body = ctk.CTkFrame(modal, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=25, pady=15)

        termo = "este fórum" if tipo == "forum" else ("este tópico" if tipo == "topic" else "esta mensagem")
        ctk.CTkLabel(body, text=f"Tem certeza de que deseja apagar {termo}?\nEsta ação é permanente.", font=self.f_norm, text_color=TEXTO_ESCURO, justify="center").pack(pady=(5, 15))

        def confirmar():
            if tipo == "forum":
                if self.controller.excluir_forum(item_id): self.show_hub()
            elif tipo == "topic":
                if self.controller.excluir_topico(item_id): self.render_topics_view()
            elif tipo == "message":
                if self.controller.excluir_mensagem(item_id): self.render_thread_view()
            modal.destroy()

        btns = ctk.CTkFrame(body, fg_color="transparent")
        btns.pack(fill="x", side="bottom")

        ctk.CTkButton(btns, text="Cancelar", fg_color="#e2e8f0", text_color=TEXTO_ESCURO, hover_color="#cbd5e1", height=36, command=modal.destroy).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(btns, text="Sim, Apagar", fg_color=COR_ERRO, text_color="#ffffff", hover_color="#b91c1c", height=36, command=confirmar).pack(side="right", expand=True, fill="x", padx=(5, 0))