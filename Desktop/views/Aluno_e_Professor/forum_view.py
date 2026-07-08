import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.forum_controller import ForumController
# Garanta que essas constantes estejam importadas ou definidas no seu escopo global:
AZUL_SENAC = "#004A8D"
CINZA_SENAC = "#cbd5e1"
BRANCO = "#ffffff"

class Forum(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#f8fafc") 
        self.janela = master
        self.controller = ForumController()
        
        self.azul = "#004A8D"
        self.azul_hover = "#003566"
        self.bg_lateral = "#ffffff"
        self.view = "topics"
        
        self.f_bold = ("Segoe UI", 14, "bold")
        self.f_norm = ("Segoe UI", 13)
        self.f_small = ("Segoe UI", 11, "bold")
        
        self.current_forum_id = None
        self.current_forum_name = ""
        self.current_topic_id = None
        self.current_topic_title = ""
        
        self.setup_ui()

    def setup_ui(self):
        from assets.header import HeaderPadrao
        self.header = HeaderPadrao(self, titulo="Fórum de Discussões", comando_voltar=None)

        # CONTAINER INFERIOR
        container_corpo = ctk.CTkFrame(self, fg_color="transparent")
        container_corpo.pack(fill="both", expand=True)

        # 2. SIDEBAR ESTÁTICA (Esquerda)
        self.side = ctk.CTkFrame(container_corpo, width=300, fg_color=self.bg_lateral, corner_radius=0)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        
        ctk.CTkLabel(self.side, text="MEUS FÓRUNS", font=("Segoe UI", 11, "bold"), text_color="#64748b").pack(anchor="w", padx=25, pady=(25, 10))
        
        self.btn_new_f = ctk.CTkButton(self.side, text="+ Criar Novo Fórum", fg_color=self.azul, hover_color=self.azul_hover, font=self.f_bold, corner_radius=10, height=40)
        self.btn_new_f.configure(command=self.toggle_formulario_forum)
        self.btn_new_f.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkFrame(self.side, height=1, fg_color="#e2e8f0").pack(fill="x", padx=20, pady=(10, 10))
        
        self.scroll_side = ctk.CTkScrollableFrame(self.side, fg_color="transparent")
        self.scroll_side.pack(fill="both", expand=True, padx=8)

        # 3. ÁREA DE CONTEÚDO PRINCIPAL (Direita)
        self.main = ctk.CTkFrame(container_corpo, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=35, pady=20)
        
        # 4. BARRA DE CAMINHO (Breadcrumbs)
        self.breadcrumb_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        self.breadcrumb_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_new_t = ctk.CTkButton(self.breadcrumb_frame, text="+ Novo Tópico", height=32, fg_color=self.azul, hover_color=self.azul_hover, font=self.f_bold, corner_radius=8, command=self.toggle_formulario_topico)
        
        # Frame de Rolagem central
        self.content = ctk.CTkScrollableFrame(self.main, fg_color="transparent")
        self.content.pack(fill="both", expand=True, pady=(0, 15))

        # 5. CAIXA DE TEXTO INFERIOR (Chat)
        self.reply_frame = ctk.CTkFrame(self.main, fg_color="#ffffff", height=70, corner_radius=12, border_width=1, border_color="#e2e8f0")
        self.reply_entry = ctk.CTkTextbox(self.reply_frame, height=45, fg_color="transparent", font=self.f_norm, text_color="#334155")
        self.reply_entry.pack(side="left", fill="x", expand=True, padx=15, pady=10)
        
        self.btn_send = ctk.CTkButton(self.reply_frame, text="Enviar", width=100, height=38, fg_color=self.azul, hover_color=self.azul_hover, font=self.f_bold, corner_radius=8, command=self.send_message)
        self.btn_send.pack(side="right", padx=15)

        self.setup_placeholder()
        
        foruns_iniciais = self.controller.listar_foruns()
        if foruns_iniciais:
            self.load_forum(foruns_iniciais[0]["idforum"], foruns_iniciais[0]["nome"])
        else:
            self.load_side_menu()
            self.refresh_ui()

    def setup_placeholder(self):
        ph = "Digite sua mensagem..."
        self.reply_entry.insert("1.0", ph)
        self.reply_entry.bind("<FocusIn>", lambda e: self.reply_entry.delete("1.0", "end") if self.reply_entry.get("1.0", "end-1c") == ph else None)
        self.reply_entry.bind("<FocusOut>", lambda e: self.reply_entry.insert("1.0", ph) if not self.reply_entry.get("1.0", "end-1c").strip() else None)

    def toggle_formulario_forum(self):
        # 1. Configuração do Modal Principal 
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Criar Novo Fórum")
        modal.geometry("500x320")  
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        # 2. Cabeçalho Customizado (Padrão Senac)
        m_header = ctk.CTkFrame(modal, fg_color=self.azul, corner_radius=0, height=60)
        m_header.pack(fill="x")
        ctk.CTkLabel(m_header, text="📁 Novo Espaço de Discussão", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ffffff").pack(pady=15)

        # 3. Área de Conteúdo
        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # --- Campo: Nome do Fórum ---
        ctk.CTkLabel(content, text="Nome do Fórum / Categoria:", font=ctk.CTkFont(weight="bold"), text_color=self.azul).pack(anchor="w", pady=(5, 2))
        txt_forum = ctk.CTkEntry(content, fg_color="#ffffff", border_color="#cbd5e1", border_width=2, height=40, corner_radius=8, placeholder_text="Ex: Dúvidas Gerais, Avisos...")
        txt_forum.pack(fill="x", pady=(0, 15))

        # --- Container Oculto para o Tópico Inicial ---
        frame_topico_opcional = ctk.CTkFrame(content, fg_color="transparent")
        
        ctk.CTkLabel(frame_topico_opcional, text="Título do Tópico Inicial:", font=ctk.CTkFont(weight="bold"), text_color=self.azul).pack(anchor="w", pady=(5, 2))
        txt_topico = ctk.CTkEntry(frame_topico_opcional, fg_color="#ffffff", border_color="#cbd5e1", border_width=2, height=40, corner_radius=8, placeholder_text="Ex: Boas-vindas ao Fórum!")
        txt_topico.pack(fill="x", pady=(0, 15))

        # 4. Lógica de Expansão Dinâmica do Checkbox
        def alternar_campo_topico():
            if chk_estado.get() == 1:
                modal.geometry("500x430")
                frame_topico_opcional.pack(fill="x", before=btn_container)
            else:
                frame_topico_opcional.pack_forget()
                modal.geometry("500x320")

        # Checkbox Customizado
        chk_estado = ctk.IntVar(value=0)
        chk_criar_topico = ctk.CTkCheckBox(
            content, 
            text="Criar um tópico de abertura junto com este fórum", 
            variable=chk_estado,
            command=alternar_campo_topico,
            font=ctk.CTkFont(size=12),
            text_color="#475569",
            fg_color=self.azul,
            hover_color=self.azul_hover
        )
        chk_criar_topico.pack(anchor="w", pady=(0, 20))

        # 5. Lógica de Envio Integrada com as funções do seu Controller
        def salvar_forum_completo():
            nome_forum = txt_forum.get().strip()
            if not nome_forum:
                return

            # Agora 'resultado' será o ID (ex: 5) ou False
            resultado = self.controller.cadastrar_forum(nome_forum)
            
            if resultado and resultado is not True:
                id_forum_vinculo = resultado
                
                # Se o checkbox estava marcado, cria o tópico usando o ID real
                if chk_estado.get() == 1:
                    nome_topico = txt_topico.get().strip() or "Tópico Geral"
                    self.controller.cadastrar_topico(id_forum_vinculo, nome_topico)
                
                # Atualiza o menu lateral da View
                self.load_side_menu()
                
                # Força a interface a abrir e focar o fórum recém-criado
                self.load_forum(id_forum_vinculo, nome_forum)
                
                modal.destroy()

        # 6. Botões de Rodapé
        btn_container = ctk.CTkFrame(content, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_container, text="Cancelar", fg_color="#e2e8f0", hover_color="#cbd5e1", 
                      text_color="#475569", height=38, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=modal.destroy).pack(side="left", padx=(0, 10), expand=True, fill="x")

        ctk.CTkButton(btn_container, text="Criar Fórum", fg_color=self.azul, hover_color=self.azul_hover, 
                      text_color="#ffffff", height=38, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=salvar_forum_completo).pack(side="right", padx=(10, 0), expand=True, fill="x")

    def toggle_formulario_topico(self):
        # Validação básica de segurança: impede abrir o modal se nenhum fórum estiver ativo
        if self.current_forum_id is None:
            messagebox.showwarning("Aviso", "Selecione um fórum na barra lateral antes de criar um tópico.")
            return

        # 1. Configuração do Modal Principal 
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Criar Novo Tópico")
        modal.geometry("500x280")  # Tamanho ideal para um campo + botões
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        # 2. Cabeçalho Customizado (Seguindo o padrão azul do app)
        m_header = ctk.CTkFrame(modal, fg_color=self.azul, corner_radius=0, height=60)
        m_header.pack(fill="x")
        ctk.CTkLabel(m_header, text="💬 Novo Tópico de Discussão", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ffffff").pack(pady=15)

        # 3. Área de Conteúdo interna
        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # --- Campo: Título do Tópico ---
        ctk.CTkLabel(content, text="Título do Novo Tópico:", font=ctk.CTkFont(weight="bold"), text_color=self.azul).pack(anchor="w", pady=(5, 5))
        
        txt_topico = ctk.CTkEntry(
            content, 
            fg_color="#ffffff", 
            border_color="#cbd5e1", 
            border_width=2, 
            height=40, 
            corner_radius=8, 
            placeholder_text="Ex: Dúvidas sobre o projeto integrador..."
        )
        txt_topico.pack(fill="x", pady=(0, 20))
        txt_topico.focus_set()

        # 4. Lógica de Envio Integrada com o Controller
        def salvar_topico_modal():
            titulo_topico = txt_topico.get().strip()
            if not titulo_topico:
                return

            # Executa o cadastro passando o ID do fórum atual guardado na View
            if self.controller.cadastrar_topico(self.current_forum_id, titulo_topico):
                # Recarrega a área central com o novo tópico listado
                self.refresh_ui()
                modal.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível cadastrar o tópico. Tente novamente.")

        # 5. Botões de Ação no Rodapé do Modal
        btn_container = ctk.CTkFrame(content, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom")

        # Botão Cancelar
        ctk.CTkButton(
            btn_container, text="Cancelar", fg_color="#e2e8f0", hover_color="#cbd5e1", 
            text_color="#475569", height=38, corner_radius=8, font=ctk.CTkFont(weight="bold"),
            command=modal.destroy
        ).pack(side="left", padx=(0, 10), expand=True, fill="x")

        # Botão Criar Tópico
        ctk.CTkButton(
            btn_container, text="Criar Tópico", fg_color=self.azul, hover_color=self.azul_hover, 
            text_color="#ffffff", height=38, corner_radius=8, font=ctk.CTkFont(weight="bold"),
            command=salvar_topico_modal
        ).pack(side="right", padx=(10, 0), expand=True, fill="x")

    def salvar_item_inline(self, tipo):
        if tipo == "topic":
            val = self.entry_topico_titulo.get().strip()
            if val and self.current_forum_id is not None:
                if self.controller.cadastrar_topico(self.current_forum_id, val):
                    self.toggle_formulario_topico()
                    self.refresh_ui()

    def editar_item(self, tipo, item_id, valor_atual):
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Editar Registro")
        modal.geometry("500x280")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        m_header = ctk.CTkFrame(modal, fg_color=self.azul, corner_radius=0, height=60)
        m_header.pack(fill="x")
        
        titulo_modal = "📝 Editar Fórum" if tipo == "forum" else ("💬 Editar Tópico" if tipo == "topic" else "✍️ Editar Mensagem")
        ctk.CTkLabel(m_header, text=titulo_modal, font=ctk.CTkFont(size=16, weight="bold"), text_color="#ffffff").pack(pady=15)

        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        prompt_txt = "Novo nome do fórum:" if tipo == "forum" else ("Novo título do tópico:" if tipo == "topic" else "Nova mensagem:")
        ctk.CTkLabel(content, text=prompt_txt, font=ctk.CTkFont(weight="bold"), text_color=self.azul).pack(anchor="w", pady=(5, 5))
        
        txt_input = ctk.CTkEntry(content, fg_color="#ffffff", border_color="#cbd5e1", border_width=2, height=40, corner_radius=8)
        txt_input.pack(fill="x", pady=(0, 20))
        txt_input.insert(0, valor_atual)
        txt_input.focus_set()

        def confirmar_edicao():
            novo_valor = txt_input.get().strip()
            if novo_valor and novo_valor != valor_atual:
                sucesso = False
                if tipo == "forum":
                    sucesso = self.controller.editar_forum(item_id, novo_valor)
                    if sucesso: self.load_side_menu()
                elif tipo == "topic":
                    sucesso = self.controller.editar_topico(item_id, novo_valor)
                    if sucesso: self.refresh_ui()
                elif tipo == "message":
                    sucesso = self.controller.editar_mensagem(item_id, novo_valor)
                    if sucesso: self.refresh_ui()
            modal.destroy()

        btn_container = ctk.CTkFrame(content, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_container, text="Cancelar", fg_color="#e2e8f0", hover_color="#cbd5e1", 
                      text_color="#475569", height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=modal.destroy).pack(side="left", padx=(0, 10), expand=True, fill="x")

        ctk.CTkButton(btn_container, text="Salvar Alterações", fg_color=self.azul, hover_color="#0f172a", 
                      text_color="#ffffff", height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=confirmar_edicao).pack(side="right", padx=(10, 0), expand=True, fill="x")

    def excluir_item(self, tipo, item_id):
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Confirmar Exclusão")
        modal.geometry("450x240")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        COR_ALERTA = "#dc2626"
        m_header = ctk.CTkFrame(modal, fg_color=COR_ALERTA, corner_radius=0, height=60)
        m_header.pack(fill="x")
        ctk.CTkLabel(m_header, text="⚠️ Atenção: Ação Irreversível", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ffffff").pack(pady=15)

        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=35, pady=20)

        termo_traduzido = "este fórum" if tipo == "forum" else ("este tópico" if tipo == "topic" else "esta mensagem")
        lbl_msg = ctk.CTkLabel(content, text=f"Tem certeza que deseja apagar {termo_traduzido} permanentemente?\nEsta ação não poderá ser desfeita.", font=ctk.CTkFont(size=13), text_color="#1e293b", justify="center", wraplength=380)
        lbl_msg.pack(pady=(10, 25))

        def confirmar_exclusao():
            sucesso = False
            if tipo == "forum":
                sucesso = self.controller.excluir_forum(item_id)
                if sucesso:
                    self.current_forum_id = None
                    self.current_forum_name = ""
                    foruns = self.controller.listar_foruns()
                    if foruns: self.load_forum(foruns[0]["idforum"], foruns[0]["nome"])
                    else:
                        self.load_side_menu()
                        self.refresh_ui()
            elif tipo == "topic":
                sucesso = self.controller.excluir_topico(item_id)
                if sucesso: self.go_back()
            elif tipo == "message":
                sucesso = self.controller.excluir_mensagem(item_id)
                if sucesso: self.refresh_ui()
            modal.destroy()

        btn_container = ctk.CTkFrame(content, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_container, text="Não, Cancelar", fg_color="#e2e8f0", hover_color="#cbd5e1", text_color="#475569", height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"), command=modal.destroy).pack(side="left", padx=(0, 10), expand=True, fill="x")
        ctk.CTkButton(btn_container, text="Sim, Apagar", fg_color=COR_ALERTA, hover_color="#b91c1c", text_color="#ffffff", height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"), command=confirmar_exclusao).pack(side="right", padx=(10, 0), expand=True, fill="x")

    def load_side_menu(self):
        for w in self.scroll_side.winfo_children(): 
            w.destroy()
            
        foruns = self.controller.listar_foruns()
        
        # MENSAGEM AMIGÁVEL: Se não houver nenhum fórum cadastrado no banco
        if not foruns:
            msg_frame = ctk.CTkFrame(self.scroll_side, fg_color="transparent")
            msg_frame.pack(fill="x", pady=30, padx=10)
            
            ctk.CTkLabel(msg_frame, text="📭", font=("Segoe UI", 24)).pack(pady=(0, 5))
            ctk.CTkLabel(
                msg_frame, 
                text="Nenhum fórum encontrado.\nCrie um espaço acima para\ncomeçar a interagir!", 
                font=("Segoe UI", 11, "italic"), 
                text_color="#64748b", 
                justify="center"
            ).pack(fill="x")
            return  # Corta a execução para não quebrar o loop

        # Loop original caso existam fóruns
        for f in foruns:
            act = (f["idforum"] == self.current_forum_id)
            linha_f = ctk.CTkFrame(self.scroll_side, fg_color="transparent")
            linha_f.pack(fill="x", pady=3)
            
            btn = ctk.CTkButton(
                linha_f, text=f"  #  {f['nome']}", anchor="w", 
                fg_color="#e0f2fe" if act else "transparent", 
                text_color=self.azul if act else "#475569", 
                font=self.f_bold if act else self.f_norm,
                hover_color="#f1f5f9", height=40, corner_radius=8,
                command=lambda fid=f["idforum"], fn=f["nome"]: self.load_forum(fid, fn)
            )
            btn.pack(side="left", fill="x", expand=True)

            if f.get("pode_gerenciar") or f.get("autor_nome") == self.controller.nome_usuario_logado:
                ctk.CTkButton(linha_f, text="✏️", width=26, height=26, fg_color="transparent", hover_color="#e2e8f0", command=lambda fid=f["idforum"], fn=f["nome"]: self.editar_item("forum", fid, fn)).pack(side="right", padx=2)
                ctk.CTkButton(linha_f, text="🗑️", width=26, height=26, fg_color="transparent", hover_color="#fee2e2", text_color="#ef4444", command=lambda fid=f["idforum"]: self.excluir_item("forum", fid)).pack(side="right", padx=2)

    def update_breadcrumbs(self):
        for w in self.breadcrumb_frame.winfo_children():
            if w != self.btn_new_t: w.destroy()
            
        btn_home = ctk.CTkButton(self.breadcrumb_frame, text="Fóruns", font=self.f_norm, text_color="#64748b", fg_color="transparent", width=10, hover_color="#f1f5f9")
        btn_home.pack(side="left")
        
        if self.current_forum_name:
            ctk.CTkLabel(self.breadcrumb_frame, text=" / ", font=self.f_norm, text_color="#cbd5e1").pack(side="left")
            estado_botao = "normal" if self.view == "messages" else "disabled"
            
            btn_f = ctk.CTkButton(
                self.breadcrumb_frame, text=self.current_forum_name, 
                font=self.f_bold if self.view == "topics" else self.f_norm, 
                text_color=self.azul if self.view == "topics" else "#64748b", 
                fg_color="transparent", width=10, hover_color="#f1f5f9",  
                state=estado_botao, command=self.go_back
            )
            btn_f.pack(side="left")
            
        if self.view == "messages" and self.current_topic_title:
            ctk.CTkLabel(self.breadcrumb_frame, text=" / ", font=self.f_norm, text_color="#cbd5e1").pack(side="left")
            ctk.CTkLabel(self.breadcrumb_frame, text=self.current_topic_title, font=self.f_bold, text_color="#0f172a").pack(side="left")

    def load_forum(self, forum_id, forum_nome):
        self.current_forum_id = forum_id
        self.current_forum_name = forum_nome
        self.view = "topics"
        
        self.btn_new_t.pack(side="right")
        self.reply_frame.pack_forget()
        
        self.update_breadcrumbs()
        self.refresh_ui()
        self.load_side_menu()

    def go_back(self):
        if self.current_forum_id and self.current_forum_name:
            self.load_forum(self.current_forum_id, self.current_forum_name)

    def refresh_ui(self):
        # 1. Limpa tudo o que existe na área de conteúdo central
        for w in self.content.winfo_children(): 
            w.destroy()
        
        # --- CASO GLOBAL: Nenhum Fórum Selecionado (ou nenhum fórum existente) ---
        if self.current_forum_id is None:
            # Desativa o botão de criar tópicos já que não há fórum pai
            self.btn_new_t.pack_forget()
            self.reply_frame.pack_forget()
            
            msg_global = ctk.CTkFrame(self.content, fg_color="transparent")
            msg_global.pack(fill="both", expand=True, pady=80)
            
            ctk.CTkLabel(msg_global, text="👋 Welcome!", font=("Segoe UI", 38)).pack(pady=(0, 10))
            ctk.CTkLabel(
                msg_global, 
                text="Nenhum fórum selecionado no momento.\n\nEscolha um canal na barra lateral esquerda para visualizar os tópicos\nou clique em '+ Criar Novo Fórum' se estiver começando agora!", 
                font=("Segoe UI", 13, "italic"), 
                text_color="#64748b", 
                justify="center"
            ).pack(fill="x")
            return  # Corta a execução aqui

        # --- MODO VISUALIZAÇÃO: TÓPICOS (Fórum Selecionado) ---
        if self.view == "topics":
            topicos = self.controller.listar_topicos(self.current_forum_id)
            
            # Mensagem amigável caso o fórum exista mas não tenha tópicos
            if not topicos:
                msg_main = ctk.CTkFrame(self.content, fg_color="transparent")
                msg_main.pack(fill="both", expand=True, pady=60)
                
                ctk.CTkLabel(msg_main, text="💬", font=("Segoe UI", 36)).pack(pady=(0, 10))
                ctk.CTkLabel(
                    msg_main, 
                    text="Este fórum ainda não possui tópicos de discussão.\nClique em '+ Novo Tópico' ali em cima para iniciar uma conversa!", 
                    font=("Segoe UI", 13, "italic"), 
                    text_color="#64748b", 
                    justify="center"
                ).pack(fill="x")
                return

            # Renderização normal dos cartões de tópicos
            for t in topicos:
                card = ctk.CTkFrame(self.content, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#f1f5f9")
                card.pack(fill="x", pady=6)
                ctk.CTkLabel(card, text=t['titulo'], font=self.f_bold, text_color="#1e293b").pack(side="left", padx=20, pady=18)
                
                btn_ver = ctk.CTkButton(card, text="Abrir Tópico →", width=110, height=32, fg_color="transparent", text_color=self.azul, hover_color="#f0f9ff", font=self.f_bold, corner_radius=6)
                btn_ver.configure(command=lambda tid=t['idtopico'], tt=t['titulo']: self.load_topic(tid, tt))
                btn_ver.pack(side="right", padx=20)
                
                if t.get("pode_gerenciar") or t.get("autor_nome") == self.controller.nome_usuario_logado:
                    ctk.CTkButton(card, text="🗑️", width=30, height=32, fg_color="transparent", hover_color="#fee2e2", text_color="#ef4444", command=lambda tid=t['idtopico']: self.excluir_item("topic", tid)).pack(side="right", padx=5)
                    ctk.CTkButton(card, text="✏️", width=30, height=32, fg_color="transparent", hover_color="#e2e8f0", command=lambda tid=t['idtopico'], tt=t['titulo']: self.editar_item("topic", tid, tt)).pack(side="right")
        
        # --- MODO VISUALIZAÇÃO: MENSAGENS (Chat do Tópico Aberto) ---
        else:
            if self.current_topic_id is not None:
                mensagens = self.controller.listar_mensagens(self.current_topic_id)
                
                if not mensagens:
                    msg_chat = ctk.CTkFrame(self.content, fg_color="transparent")
                    msg_chat.pack(fill="both", expand=True, pady=60)
                    
                    ctk.CTkLabel(msg_chat, text="✨", font=("Segoe UI", 36)).pack(pady=(0, 10))
                    ctk.CTkLabel(
                        msg_chat, 
                        text="Seja o primeiro a responder!\nDigite sua mensagem na caixa abaixo e clique em Enviar.", 
                        font=("Segoe UI", 13, "italic"), 
                        text_color="#64748b", 
                        justify="center"
                    ).pack(fill="x")
                    return

                for m in mensagens:
                    autor = m['autor_nome']
                    is_me = (autor == self.controller.nome_usuario_logado)
                    
                    if is_me:
                        fg_balao, cor_texto, cor_autor, alinhamento, txt_autor, border_color = self.azul, "#ffffff", "#bae6fd", "e", f"{autor} (Você)", self.azul
                    else:
                        fg_balao, cor_texto, cor_autor, alinhamento, txt_autor, border_color = "#f1f5f9", "#1e293b", "#64748b", "w", autor, "#f1f5f9"

                    linha_frame = ctk.CTkFrame(self.content, fg_color="transparent")
                    linha_frame.pack(fill="x", pady=5)
                    
                    balao = ctk.CTkFrame(linha_frame, fg_color=fg_balao, corner_radius=14, border_width=1, border_color=border_color)
                    balao.pack(anchor=alinhamento, padx=10)
                    
                    top_bar = ctk.CTkFrame(balao, fg_color="transparent")
                    top_bar.pack(fill="x", padx=14, pady=(8,0))
                    ctk.CTkLabel(top_bar, text=txt_autor, font=self.f_small, text_color=cor_autor).pack(side="left")
                    
                    if is_me:
                        ctk.CTkButton(top_bar, text="excluir", width=10, height=14, font=("Segoe UI", 10), fg_color="transparent", hover_color="#b91c1c", text_color="#fca5a5", command=lambda mid=m['idmensagem']: self.excluir_item("message", mid)).pack(side="right", padx=(5, 0))
                        ctk.CTkButton(top_bar, text="editar", width=10, height=14, font=("Segoe UI", 10), fg_color="transparent", hover_color=self.azul_hover, text_color="#e0f2fe", command=lambda mid=m['idmensagem'], cont=m['conteudo']: self.editar_item("message", mid, cont)).pack(side="right")
                    
                    ctk.CTkLabel(balao, text=m['conteudo'], font=self.f_norm, text_color=cor_texto, wraplength=550, justify="left").pack(anchor="w", padx=14, pady=(2,10))

    def load_topic(self, topic_id, topic_titulo):
        self.current_topic_id = topic_id
        self.current_topic_title = topic_titulo
        self.view = "messages"
        
        self.btn_new_t.pack_forget()
        self.reply_frame.pack(fill="x", pady=(10, 0))
        self.update_breadcrumbs()
        self.refresh_ui()

    def send_message(self):
        txt = self.reply_entry.get("1.0", "end-1c").strip()
        if txt and txt != "Digite sua mensagem...":
            if self.current_topic_id is not None:
                sucesso = self.controller.enviar_mensagem(self.current_topic_id, txt)
                if sucesso:
                    self.reply_entry.delete("1.0", "end")
                    self.setup_placeholder()
                    self.refresh_ui()
                else:
                    messagebox.showerror("Erro", "Não foi possível enviar a mensagem. Tente novamente.")