import customtkinter as ctk
from tkinter import messagebox
from dist.InovaEdu._internal.views.Aluno_e_Professor.editar_view import *
from controllers.forum_controller import ForumController

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
        
        # Formulario Inline de Fórum
        self.form_forum_frame = ctk.CTkFrame(self.side, fg_color="#f1f5f9", corner_radius=8)
        self.form_forum_frame.pack_forget()  # Inicialmente escondido
        ctk.CTkLabel(self.form_forum_frame, text="Novo Fórum", font=self.f_bold, text_color="#1e293b").pack(anchor="w", padx=10, pady=(10, 5))
        self.entry_forum_nome = ctk.CTkEntry(self.form_forum_frame, placeholder_text="Nome do fórum...", font=self.f_norm, height=35)
        self.entry_forum_nome.pack(fill="x", padx=10, pady=(10, 5))
        
        btn_sub_f = ctk.CTkFrame(self.form_forum_frame, fg_color="transparent")
        btn_sub_f.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(btn_sub_f, text="Salvar", fg_color=self.azul, hover_color=self.azul_hover, width=60, height=28, font=self.f_small, command=lambda: self.salvar_item_inline("forum")).pack(side="left")
        ctk.CTkButton(btn_sub_f, text="Cancelar", fg_color="#cbd5e1", text_color="#334155", hover_color="#94a3b8", width=60, height=28, font=self.f_small, command=self.toggle_formulario_forum).pack(side="right")
        
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

        # Formulario Inline de Tópico
        self.form_topico_frame = ctk.CTkFrame(self.main, fg_color="#f1f5f9", corner_radius=12,)
        self.form_topico_frame.pack_forget()  # Inicialmente escondido
        ctk.CTkLabel(self.form_topico_frame, text="Novo Tópico", font=self.f_bold, text_color="#1e293b").pack(anchor="w", padx=15, pady=(10, 5))
        self.entry_topico_titulo = ctk.CTkEntry(self.form_topico_frame, placeholder_text="Título do novo tópico...", font=self.f_norm, height=35)
        self.entry_topico_titulo.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkFrame(self.form_topico_frame, height=1, fg_color="#e2e8f0").pack(fill="x", padx=20, pady=(10, 10))
        
        btn_sub_t = ctk.CTkFrame(self.form_topico_frame, fg_color="transparent")
        btn_sub_t.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(btn_sub_t, text="Criar Tópico", fg_color=self.azul, hover_color=self.azul_hover, width=100, height=32, font=self.f_bold, corner_radius=6, command=lambda: self.salvar_item_inline("topic")).pack(side="left")
        ctk.CTkButton(btn_sub_t, text="Cancelar", fg_color="#f1f5f9", text_color="#334155", hover_color="#cbd5e1", width=80, height=32, font=self.f_bold, corner_radius=6, command=self.toggle_formulario_topico).pack(side="left", padx=10)
        
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

    def setup_placeholder(self):
        ph = "Digite sua mensagem..."
        self.reply_entry.insert("1.0", ph)
        self.reply_entry.bind("<FocusIn>", lambda e: self.reply_entry.delete("1.0", "end") if self.reply_entry.get("1.0", "end-1c") == ph else None)
        self.reply_entry.bind("<FocusOut>", lambda e: self.reply_entry.insert("1.0", ph) if not self.reply_entry.get("1.0", "end-1c").strip() else None)

    def toggle_formulario_forum(self):
        if self.form_forum_frame.winfo_manager():
            self.form_forum_frame.pack_forget()
        else:
            self.entry_forum_nome.delete(0, "end")
            self.scroll_side.pack_forget()
            self.form_forum_frame.pack(fill="x", padx=20, pady=(0, 10))
            self.scroll_side.pack(fill="both", expand=True, padx=8)

    def toggle_formulario_topico(self):
        if self.form_topico_frame.winfo_manager():
            self.form_topico_frame.pack_forget()
        else:
            self.entry_topico_titulo.delete(0, "end")
            self.content.pack_forget()
            self.form_topico_frame.pack(fill="x", pady=(0, 15))
            self.content.pack(fill="both", expand=True, pady=(0, 15))

    def salvar_item_inline(self, tipo):
        if tipo == "forum":
            val = self.entry_forum_nome.get().strip()
            if val:
                if self.controller.cadastrar_forum(val):
                    self.toggle_formulario_forum()
                    self.load_side_menu()
        else:
            val = self.entry_topico_titulo.get().strip()
            if val and self.current_forum_id is not None:
                if self.controller.cadastrar_topico(self.current_forum_id, val):
                    self.toggle_formulario_topico()
                    self.refresh_ui()

    # --- NOVOS MÉTODOS DE GERENCIAMENTO (EDITAR/EXCLUIR) ---
    def editar_item(self, tipo, item_id, valor_atual):
        # 1. Configuração Básica do Modal (Inspirado no modal de senha)
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Editar Registro")
        modal.geometry("500x280")  # Um pouco menor por ter apenas 1 campo
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        # 2. Cabeçalho Customizado
        m_header = ctk.CTkFrame(modal, fg_color=AZUL_SENAC, corner_radius=0, height=60)
        m_header.pack(fill="x")
        
        titulo_modal = "📝 Editar Fórum" if tipo == "forum" else ("💬 Editar Tópico" if tipo == "topic" else "✍️ Editar Mensagem")
        ctk.CTkLabel(m_header, text=titulo_modal, font=ctk.CTkFont(size=16, weight="bold"), text_color=BRANCO).pack(pady=15)

        # 3. Área de Conteúdo
        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        prompt_txt = "Novo nome do fórum:" if tipo == "forum" else ("Novo título do tópico:" if tipo == "topic" else "Nova mensagem:")
        ctk.CTkLabel(content, text=prompt_txt, font=ctk.CTkFont(weight="bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(5, 5))
        
        # Campo de entrada de dados
        txt_input = ctk.CTkEntry(content, fg_color=BRANCO, border_color=CINZA_SENAC, border_width=2, height=40, corner_radius=8)
        txt_input.pack(fill="x", pady=(0, 20))
        
        # Preenche o input automaticamente com o valor que já estava salvo no banco
        txt_input.insert(0, valor_atual)
        txt_input.focus_set()

        # 4. Ação de Salvar (Substitui o antigo fluxo do dialog)
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
            
            modal.destroy() # Fecha a janela após terminar

        # 5. Botões de Ação na Base do Modal
        btn_container = ctk.CTkFrame(content, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_container, text="Cancelar", fg_color="#e2e8f0", hover_color="#cbd5e1", 
                      text_color="#475569", height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=modal.destroy).pack(side="left", padx=(0, 10), expand=True, fill="x")

        ctk.CTkButton(btn_container, text="Salvar Alterações", fg_color=AZUL_SENAC, hover_color="#0f172a", 
                      text_color=BRANCO, height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=confirmar_edicao).pack(side="right", padx=(10, 0), expand=True, fill="x")

    def excluir_item(self, tipo, item_id):
        # 1. Configuração do Modal de Alerta
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Confirmar Exclusão")
        modal.geometry("450x240")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        # 2. Cabeçalho de Alerta (Vermelho para indicar ação destrutiva)
        COR_ALERTA = "#dc2626"  # Vermelho escuro/alerta
        m_header = ctk.CTkFrame(modal, fg_color=COR_ALERTA, corner_radius=0, height=60)
        m_header.pack(fill="x")
        
        ctk.CTkLabel(m_header, text="⚠️ Atenção: Ação Irreversível", 
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=BRANCO).pack(pady=15)

        # 3. Área de Conteúdo
        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=35, pady=20)

        # Tradução amigável do termo para o usuário
        termo_traduzido = "este fórum" if tipo == "forum" else ("este tópico" if tipo == "topic" else "esta mensagem")

        lbl_msg = ctk.CTkLabel(
            content, 
            text=f"Tem certeza que deseja apagar {termo_traduzido} permanentemente?\nEsta ação não poderá ser desfeita.", 
            font=ctk.CTkFont(size=13, weight="normal"), 
            text_color="#1e293b",
            justify="center",
            wraplength=380
        )
        lbl_msg.pack(pady=(10, 25))

        # 4. Lógica de Execução (O seu fluxo original mantido intacto)
        def confirmar_exclusao():
            sucesso = False
            if tipo == "forum":
                sucesso = self.controller.excluir_forum(item_id)
                if sucesso:
                    self.current_forum_id = None
                    self.current_forum_name = ""
                    foruns = self.controller.listar_foruns()
                    if foruns:
                        self.load_forum(foruns[0]["idforum"], foruns[0]["nome"])
                    else:
                        self.load_side_menu()
                        self.refresh_ui()
            elif tipo == "topic":
                sucesso = self.controller.excluir_topico(item_id)
                if sucesso: 
                    self.go_back()
            elif tipo == "message":
                sucesso = self.controller.excluir_mensagem(item_id)
                if sucesso: 
                    self.refresh_ui()
            
            modal.destroy() # Fecha o modal após a exclusão

        # 5. Botões de Ação na Base
        btn_container = ctk.CTkFrame(content, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom")

        # Botão Cancelar (Padrão e seguro)
        ctk.CTkButton(btn_container, text="Não, Cancelar", fg_color="#e2e8f0", hover_color="#cbd5e1", 
                      text_color="#475569", height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=modal.destroy).pack(side="left", padx=(0, 10), expand=True, fill="x")

        # Botão Deletar (Destaque em Vermelho de Alerta)
        ctk.CTkButton(btn_container, text="Sim, Apagar", fg_color=COR_ALERTA, hover_color="#b91c1c", 
                      text_color=BRANCO, height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                      command=confirmar_exclusao).pack(side="right", padx=(10, 0), expand=True, fill="x")

    def load_side_menu(self):
        for w in self.scroll_side.winfo_children(): w.destroy()
        for f in self.controller.listar_foruns():
            act = (f["idforum"] == self.current_forum_id)
            
            # Container da linha da sidebar para permitir o botão de excluir fórum se você for o criador
            linha_f = ctk.CTkFrame(self.scroll_side, fg_color="transparent")
            linha_f.pack(fill="x", pady=3)
            
            btn = ctk.CTkButton(
                linha_f, 
                text=f"  #  {f['nome']}", 
                anchor="w", 
                fg_color="#e0f2fe" if act else "transparent", 
                text_color=self.azul if act else "#475569", 
                font=self.f_bold if act else self.f_norm,
                hover_color="#f1f5f9", 
                height=40, 
                corner_radius=8,
                command=lambda fid=f["idforum"], fn=f["nome"]: self.load_forum(fid, fn)
            )
            btn.pack(side="left", fill="x", expand=True)

            # Verifica se quem criou o fórum é o usuário logado (Ajuste a chave se necessário na sua Controller)
            if f.get("pode_gerenciar") or f.get("autor_nome") == self.controller.nome_usuario_logado:
                btn_ed = ctk.CTkButton(linha_f, text="✏️", width=26, height=26, fg_color="transparent", hover_color="#e2e8f0", command=lambda fid=f["idforum"], fn=f["nome"]: self.editar_item("forum", fid, fn))
                btn_ed.pack(side="right", padx=2)
                btn_ex = ctk.CTkButton(linha_f, text="🗑️", width=26, height=26, fg_color="transparent", hover_color="#fee2e2", text_color="#ef4444", command=lambda fid=f["idforum"]: self.excluir_item("forum", fid))
                btn_ex.pack(side="right", padx=2)

    def update_breadcrumbs(self):
        for w in self.breadcrumb_frame.winfo_children():
            if w != self.btn_new_t: w.destroy()
            
        btn_home = ctk.CTkButton(self.breadcrumb_frame, text="Fóruns", font=self.f_norm, text_color="#64748b", fg_color="transparent", width=10, hover_color="#f1f5f9")
        btn_home.pack(side="left")
        
        if self.current_forum_name:
            ctk.CTkLabel(self.breadcrumb_frame, text=" / ", font=self.f_norm, text_color="#cbd5e1").pack(side="left")
            estado_botao = "normal" if self.view == "messages" else "disabled"
            
            btn_f = ctk.CTkButton(
                self.breadcrumb_frame, 
                text=self.current_forum_name, 
                font=self.f_bold if self.view == "topics" else self.f_norm, 
                text_color=self.azul if self.view == "topics" else "#64748b", 
                fg_color="transparent", 
                width=10, 
                hover_color="#f1f5f9",  
                state=estado_botao,     
                command=self.go_back
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
        self.form_topico_frame.pack_forget()
        
        self.update_breadcrumbs()
        self.refresh_ui()
        self.load_side_menu()

    def go_back(self):
        if self.current_forum_id and self.current_forum_name:
            self.load_forum(self.current_forum_id, self.current_forum_name)

    def refresh_ui(self):
        for w in self.content.winfo_children(): w.destroy()
        
        if self.view == "topics":
            if self.current_forum_id is not None:
                for t in self.controller.listar_topicos(self.current_forum_id):
                    card = ctk.CTkFrame(self.content, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#f1f5f9")
                    card.pack(fill="x", pady=6)
                    
                    ctk.CTkLabel(card, text=t['titulo'], font=self.f_bold, text_color="#1e293b").pack(side="left", padx=20, pady=18)
                    
                    btn_ver = ctk.CTkButton(card, text="Abrir Tópico →", width=110, height=32, fg_color="transparent", text_color=self.azul, hover_color="#f0f9ff", font=self.f_bold, corner_radius=6)
                    btn_ver.configure(command=lambda tid=t['idtopico'], tt=t['titulo']: self.load_topic(tid, tt))
                    btn_ver.pack(side="right", padx=20)
                    
                    # Se você criou o tópico, ganha ações de gerenciamento adicionais discretas
                    if t.get("pode_gerenciar") or t.get("autor_nome") == self.controller.nome_usuario_logado:
                        ctk.CTkButton(card, text="🗑️", width=30, height=32, fg_color="transparent", hover_color="#fee2e2", text_color="#ef4444", command=lambda tid=t['idtopico']: self.excluir_item("topic", tid)).pack(side="right", padx=5)
                        ctk.CTkButton(card, text="✏️", width=30, height=32, fg_color="transparent", hover_color="#e2e8f0", command=lambda tid=t['idtopico'], tt=t['titulo']: self.editar_item("topic", tid, tt)).pack(side="right")
        else:
            if self.current_topic_id is not None:
                for m in self.controller.listar_mensagens(self.current_topic_id):
                    autor = m['autor_nome']
                    is_me = (autor == self.controller.nome_usuario_logado)
                    
                    if is_me:
                        fg_balao = self.azul       
                        cor_texto = "#ffffff"     
                        cor_autor = "#bae6fd"     
                        alinhamento = "e"         
                        txt_autor = f"{autor} (Você)"
                        border_color = self.azul
                    else:
                        fg_balao = "#f1f5f9"       
                        cor_texto = "#1e293b"     
                        cor_autor = "#64748b"     
                        alinhamento = "w"         
                        txt_autor = autor
                        border_color = "#f1f5f9"

                    linha_frame = ctk.CTkFrame(self.content, fg_color="transparent")
                    linha_frame.pack(fill="x", pady=5)
                    
                    balao = ctk.CTkFrame(linha_frame, fg_color=fg_balao, corner_radius=14, border_width=1, border_color=border_color)
                    balao.pack(anchor=alinhamento, padx=10)
                    
                    # Topo do balão (Nome e Ações Inline discretas se for o dono)
                    top_bar = ctk.CTkFrame(balao, fg_color="transparent")
                    top_bar.pack(fill="x", padx=14, pady=(8,0))
                    
                    ctk.CTkLabel(top_bar, text=txt_autor, font=self.f_small, text_color=cor_autor).pack(side="left")
                    
                    if is_me:
                        # Pequenos botões de ação textuais com cores que combinam com o fundo azul do balão
                        ctk.CTkButton(top_bar, text="excluir", width=10, height=14, font=("Segoe UI", 10), fg_color="transparent", hover_color="#b91c1c", text_color="#fca5a5", command=lambda mid=m['idmensagem']: self.excluir_item("message", mid)).pack(side="right", padx=(5, 0))
                        ctk.CTkButton(top_bar, text="editar", width=10, height=14, font=("Segoe UI", 10), fg_color="transparent", hover_color=self.azul_hover, text_color="#e0f2fe", command=lambda mid=m['idmensagem'], cont=m['conteudo']: self.editar_item("message", mid, cont)).pack(side="right")
                    
                    ctk.CTkLabel(balao, text=m['conteudo'], font=self.f_norm, text_color=cor_texto, wraplength=550, justify="left").pack(anchor="w", padx=14, pady=(2,10))

    def load_topic(self, topic_id, topic_titulo):
        self.current_topic_id = topic_id
        self.current_topic_title = topic_titulo
        self.view = "messages"
        
        self.btn_new_t.pack_forget()
        self.form_topico_frame.pack_forget() 
        self.reply_frame.pack(fill="x", pady=(10, 0))
        self.update_breadcrumbs()
        self.refresh_ui()

    def send_message(self):
        txt = self.reply_entry.get("1.0", "end-1c").strip()
        if txt and txt != "Digite sua mensagem...":
            if self.current_topic_id is not None:
                if self.controller.enviar_mensagem(self.current_topic_id, txt):
                    self.reply_entry.delete("1.0", "end")
                    self.setup_placeholder()
                    self.refresh_ui()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1150x750")
    Forum(master=app).pack(fill="both", expand=True)
    app.mainloop()