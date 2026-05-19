import customtkinter as ctk
from controllers.forum_controller import ForumController

class Forum(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#f4f7f9")
        # Inicializa o controller real do banco de dados
        self.controller = ForumController()
        
        self.azul, self.view = "#004A8D", "topics"
        self.f_bold, self.f_norm = ("Arial", 14, "bold"), ("Arial", 13)
        
        # Guardas de estado baseados nos IDs vindos do banco de dados
        self.current_forum_id = None
        self.current_forum_name = ""
        self.current_topic_id = None
        
        self.setup_ui()

    def setup_ui(self):
        # Header e Layout Principal
        self.header = ctk.CTkFrame(self, fg_color=self.azul, height=70, corner_radius=0)
        self.header.pack(fill="x"); self.header.pack_propagate(False)
        ctk.CTkLabel(self.header, text="Fórum de discussões", font=("Arial", 24, "bold"), text_color="white").pack(side="left", padx=30, pady=15)

        self.side = ctk.CTkFrame(self, width=240, fg_color="#ffffff", corner_radius=0)
        self.side.pack(side="left", fill="y"); self.side.pack_propagate(False)
        
        ctk.CTkLabel(self.side, text="CATEGORIAS", font=("Arial", 11, "bold"), text_color="#94a3b8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkButton(self.side, text="+ CRIAR FÓRUM", fg_color=self.azul, hover_color="#003566", font=self.f_bold, command=lambda: self.add_item("forum")).pack(fill="x", padx=20, pady=10)
        
        self.scroll_side = ctk.CTkScrollableFrame(self.side, fg_color="transparent")
        self.scroll_side.pack(fill="both", expand=True, padx=5)

        # Área de Conteúdo
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        sub = ctk.CTkFrame(self.main, fg_color="transparent")
        sub.pack(fill="x", pady=(0, 10))
        self.title_lbl = ctk.CTkLabel(sub, text="", font=("Arial", 20, "bold"), text_color="#1e293b")
        self.title_lbl.pack(side="left")

        # Botão voltar agora retorna para a listagem de tópicos do fórum atual
        self.btn_back = ctk.CTkButton(sub, text="← Voltar", width=90, fg_color="#cbd5e1", text_color="#1e293b", hover_color="#94a3b8", font=self.f_bold, command=lambda: self.load_forum(self.current_forum_id, self.current_forum_name))
        self.btn_new_t = ctk.CTkButton(sub, text="+ NOVO TÓPICO", fg_color=self.azul, hover_color="#003566", font=self.f_bold, command=lambda: self.add_item("topic"))

        self.content = ctk.CTkScrollableFrame(self.main, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        # Campo de Resposta
        self.reply_frame = ctk.CTkFrame(self.main, fg_color="#ffffff", height=80, corner_radius=10, border_width=1, border_color="#e2e8f0")
        self.reply_entry = ctk.CTkTextbox(self.reply_frame, height=50, fg_color="transparent")
        self.reply_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        ctk.CTkButton(self.reply_frame, text="ENVIAR", width=90, fg_color=self.azul, font=self.f_bold, command=self.send_message).pack(side="right", padx=15)

        self.setup_placeholder()
        
        # Carrega o primeiro fórum do banco de dados na inicialização inicial, caso exista algum cadastrado
        foruns_iniciais = self.controller.listar_foruns()
        if foruns_iniciais:
            self.load_forum(foruns_iniciais[0]["idforum"], foruns_iniciais[0]["nome"])
        else:
            self.load_side_menu()

    def setup_placeholder(self):
        ph = "Digite sua resposta..."
        self.reply_entry.insert("1.0", ph)
        self.reply_entry.bind("<FocusIn>", lambda e: self.reply_entry.delete("1.0", "end") if self.reply_entry.get("1.0", "end-1c") == ph else None)
        self.reply_entry.bind("<FocusOut>", lambda e: self.reply_entry.insert("1.0", ph) if not self.reply_entry.get("1.0", "end-1c").strip() else None)

    def load_side_menu(self):
        for w in self.scroll_side.winfo_children(): w.destroy()
        # Busca a lista atualizada direto do banco pelo Controller
        for f in self.controller.listar_foruns():
            act = (f["idforum"] == self.current_forum_id)
            ctk.CTkButton(self.scroll_side, text=f"  {f['nome']}", anchor="w", fg_color="#e0f2fe" if act else "transparent", 
                          text_color=self.azul if act else "#475569", font=self.f_bold if act else self.f_norm,
                          hover_color="#f1f5f9", height=35, command=lambda fid=f["idforum"], fn=f["nome"]: self.load_forum(fid, fn)).pack(fill="x", pady=2)

    def load_forum(self, forum_id, forum_nome):
        self.current_forum_id = forum_id
        self.current_forum_name = forum_nome
        self.view = "topics"
        
        self.title_lbl.configure(text=forum_nome)
        self.btn_back.pack_forget()
        self.btn_new_t.pack(side="right")
        self.reply_frame.pack_forget()
        
        self.refresh_ui()
        self.load_side_menu()

    def refresh_ui(self):
        for w in self.content.winfo_children(): w.destroy()
        
        if self.view == "topics":
            if self.current_forum_id is not None:
                # Busca os tópicos associados à FK deste fórum
                for t in self.controller.listar_topicos(self.current_forum_id):
                    card = ctk.CTkFrame(self.content, fg_color="#ffffff", corner_radius=8, border_width=1, border_color="#e2e8f0")
                    card.pack(fill="x", pady=4)
                    ctk.CTkLabel(card, text=t['titulo'], font=self.f_bold, text_color="#334155").pack(side="left", padx=15, pady=15)
                    ctk.CTkButton(card, text="VER", width=70, fg_color=self.azul, command=lambda tid=t['idtopico'], tt=t['titulo']: self.load_topic(tid, tt)).pack(side="right", padx=15)
        else:
            if self.current_topic_id is not None:
                # Busca as mensagens associadas a este tópico trazendo o nome do autor via JOIN
                for m in self.controller.listar_mensagens(self.current_topic_id):
                    card = ctk.CTkFrame(self.content, fg_color="#ffffff", corner_radius=8, border_width=1, border_color="#e2e8f0")
                    card.pack(fill="x", pady=4)
                    ctk.CTkLabel(card, text=m['autor_nome'], font=self.f_bold, text_color=self.azul).pack(anchor="w", padx=15, pady=(8,0))
                    ctk.CTkLabel(card, text=m['conteudo'], font=self.f_norm, wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(3,10))

    def load_topic(self, topic_id, topic_titulo):
        self.current_topic_id = topic_id
        self.view = "messages"
        
        self.title_lbl.configure(text=topic_titulo)
        self.btn_new_t.pack_forget()
        self.btn_back.pack(side="right")
        self.reply_frame.pack(fill="x", pady=(10, 0))
        self.refresh_ui()

    def add_item(self, tipo):
        txt = "Nome do novo fórum:" if tipo == "forum" else "Título do tópico:"
        d = ctk.CTkInputDialog(text=txt, title="Criar Novo")
        val = d.get_input()
        
        if val and val.strip():
            if tipo == "forum":
                # Salva o fórum no banco
                if self.controller.cadastrar_forum(val.strip()):
                    self.load_side_menu()
            else:
                if self.current_forum_id is not None:
                    # Salva o tópico atrelado ao fórum ativo no banco
                    if self.controller.cadastrar_topico(self.current_forum_id, val.strip()):
                        self.refresh_ui()

    def send_message(self):
        txt = self.reply_entry.get("1.0", "end-1c").strip()
        if txt and txt != "Digite sua resposta...":
            if self.current_topic_id is not None:
                # Dispara a gravação da mensagem no banco pelo Controller
                if self.controller.enviar_mensagem(self.current_topic_id, txt):
                    self.reply_entry.delete("1.0", "end")
                    self.refresh_ui()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x700")
    Forum(master=app).pack(fill="both", expand=True)
    app.mainloop()