import customtkinter as ctk
from datetime import datetime

class Forum(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#f4f7f9") 
        
        self.janela = master
        self.azul_oficial = "#004A8D"
        
        # Estrutura de Dados (Mantida)
        self.forums = [
            {
                "name": "Administrador de redes",
                "description": "Discussões sobre administração de redes e protocolos",
                "created": "20/03/2025",
                "topics": [
                    {
                        "title": "Configuração de OSPF",
                        "author": "Lucas Amaral",
                        "created": "20/03/2025",
                        "replies": 8,
                        "views": 45,
                        "last_message": "12:20",
                        "messages": [
                            {"author": "Lucas Amaral", "message": "Galera, topologia pronta?", "time": "12:15"},
                            {"author": "Ana", "message": "Sim, tudo certo! 🛡️", "time": "12:20"}
                        ]
                    }
                ]
            }
        ]

        self.current_forum_index = 0
        self.current_topic_index = 0
        self.view_mode = "topics"
        
        self.setup_ui()
        
    def setup_ui(self):
        # ========== HEADER SUPERIOR ==========
        self.header_main = ctk.CTkFrame(self, fg_color=self.azul_oficial, height=100, corner_radius=0)
        self.header_main.pack(fill="x", side="top")
        self.header_main.pack_propagate(False)

        ctk.CTkLabel(
            self.header_main, text="Fórum de discussões", 
            font=ctk.CTkFont(size=28, weight="bold"), text_color="white"
        ).pack(side="left", padx=30)

        # ========== CONTAINER PRINCIPAL ==========
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.side_menu = ctk.CTkFrame(self.container, width=260, fg_color="#ffffff", corner_radius=0)
        self.side_menu.pack(side="left", fill="y")
        self.side_menu.pack_propagate(False)

        ctk.CTkLabel(self.side_menu, text="CATEGORIAS", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94a3b8").pack(anchor="w", padx=20, pady=(25, 10))
        
        # BOTÃO CRIAR FÓRUM (Adicionado)
        self.btn_new_forum = ctk.CTkButton(
            self.side_menu, text="+ CRIAR FÓRUM", fg_color=self.azul_oficial,
            hover_color="#003566", font=ctk.CTkFont(size=15, weight="bold"),
            command=self.create_new_forum
        )
        self.btn_new_forum.pack(fill="x", padx=20, pady=20)

        self.forums_list_frame = ctk.CTkScrollableFrame(self.side_menu, fg_color="transparent")
        self.forums_list_frame.pack(fill="both", expand=True, padx=5)

        # Área de Conteúdo
        self.main_area = ctk.CTkFrame(self.container, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        # Sub-Header (Título à esquerda, Botões à direita)
        self.sub_header = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.sub_header.pack(fill="x", pady=(0, 15))
        
        self.current_forum_title = ctk.CTkLabel(self.sub_header, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1e293b")
        self.current_forum_title.pack(side="left")

        # Container de botões à direita (Novo Tópico / Voltar)
        self.btn_container = ctk.CTkFrame(self.sub_header, fg_color="transparent")
        self.btn_container.pack(side="right")

        self.back_button = ctk.CTkButton(
            self.btn_container, text="← Voltar", width=100, height=35,
            fg_color="#cbd5e1", text_color="#1e293b", hover_color="#94a3b8",
            font=ctk.CTkFont(weight="bold"), command=self.show_topics_view
        )

        self.new_topic_btn = ctk.CTkButton(
            self.btn_container, text="+ NOVO TÓPICO", fg_color=self.azul_oficial, 
            hover_color="#003566", font=ctk.CTkFont(size=12, weight="bold"), 
            command=self.create_new_topic
        )

        # Scroll de Conteúdo
        self.content_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # Campo de Resposta
        self.reply_frame = ctk.CTkFrame(self.main_area, fg_color="#ffffff", height=100, corner_radius=10, border_width=1, border_color="#e2e8f0")
        self.reply_entry = ctk.CTkTextbox(self.reply_frame, height=70, fg_color="transparent")
        self.reply_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        self.send_btn = ctk.CTkButton(
            self.reply_frame, text="ENVIAR", width=100, height=45,
            fg_color=self.azul_oficial, hover_color="#003566", font=ctk.CTkFont(weight="bold"),
            command=self.send_message
        )
        self.send_btn.pack(side="right", padx=15)

        self.load_forums_list()
        self.load_forum(0)
        self.setup_events()

    def setup_events(self):
        def on_focus_in(event):
            if self.reply_entry.get("1.0", "end-1c") == "Digite sua resposta...":
                self.reply_entry.delete("1.0", "end")
        def on_focus_out(event):
            if not self.reply_entry.get("1.0", "end-1c").strip():
                self.reply_entry.insert("1.0", "Digite sua resposta...")
        self.reply_entry.insert("1.0", "Digite sua resposta...")
        self.reply_entry.bind("<FocusIn>", on_focus_in)
        self.reply_entry.bind("<FocusOut>", on_focus_out)

    def load_forums_list(self):
        for widget in self.forums_list_frame.winfo_children(): widget.destroy()
        for i, forum in enumerate(self.forums):
            is_active = (i == self.current_forum_index)
            bg = "#e0f2fe" if is_active else "transparent"
            txt = self.azul_oficial if is_active else "#475569"
            btn = ctk.CTkButton(self.forums_list_frame, text=f"  {forum['name']}", anchor="w", fg_color=bg, text_color=txt, 
                               hover_color="#f1f5f9", height=40, font=ctk.CTkFont(weight="bold" if is_active else "normal"),
                               command=lambda idx=i: self.load_forum(idx))
            btn.pack(fill="x", pady=2)

    def load_forum(self, index):
        self.current_forum_index = index
        self.view_mode = "topics"
        self.current_forum_title.configure(text=self.forums[index]['name'])
        self.back_button.pack_forget()
        self.new_topic_btn.pack(side="right")
        self.reply_frame.pack_forget()
        self.refresh_ui()
        self.load_forums_list()

    def refresh_ui(self):
        for widget in self.content_frame.winfo_children(): widget.destroy()
        forum = self.forums[self.current_forum_index]
        if self.view_mode == "topics":
            for i, topic in enumerate(forum["topics"]):
                card = ctk.CTkFrame(self.content_frame, fg_color="#ffffff", corner_radius=8, border_width=1, border_color="#e2e8f0")
                card.pack(fill="x", pady=6)
                ctk.CTkLabel(card, text=topic['title'], font=ctk.CTkFont(size=16, weight="bold"), text_color="#334155").pack(side="left", padx=20, pady=20)
                ctk.CTkButton(card, text="VER", width=80, fg_color=self.azul_oficial, command=lambda idx=i: self.load_topic(idx)).pack(side="right", padx=20)
        else:
            topic = forum["topics"][self.current_topic_index]
            for msg in topic["messages"]:
                m_card = ctk.CTkFrame(self.content_frame, fg_color="#ffffff", corner_radius=8, border_width=1, border_color="#e2e8f0")
                m_card.pack(fill="x", pady=5)
                ctk.CTkLabel(m_card, text=msg['author'], font=ctk.CTkFont(weight="bold"), text_color=self.azul_oficial).pack(anchor="w", padx=15, pady=(10,0))
                ctk.CTkLabel(m_card, text=msg['message'], wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(5,15))

    def load_topic(self, index):
        self.current_topic_index = index
        self.view_mode = "messages"
        self.current_forum_title.configure(text=self.forums[self.current_forum_index]['topics'][index]['title'])
        self.new_topic_btn.pack_forget()
        self.back_button.pack(side="right")
        self.reply_frame.pack(fill="x", pady=(15, 0))
        self.refresh_ui()

    def show_topics_view(self):
        self.load_forum(self.current_forum_index)

    def create_new_forum(self):
        d = ctk.CTkInputDialog(text="Nome do novo fórum:", title="Novo Fórum")
        name = d.get_input()
        if name:
            self.forums.append({"name": name, "description": "", "created": "", "topics": []})
            self.load_forums_list()

    def send_message(self):
        txt = self.reply_entry.get("1.0", "end-1c").strip()
        if txt and txt != "Digite sua resposta...":
            self.forums[self.current_forum_index]["topics"][self.current_topic_index]["messages"].append({"author": "Você", "message": txt, "time": datetime.now().strftime("%H:%M")})
            self.reply_entry.delete("1.0", "end")
            self.refresh_ui()

    def create_new_topic(self):
        d = ctk.CTkInputDialog(text="Título do tópico:", title="Novo Tópico")
        t = d.get_input()
        if t:
            self.forums[self.current_forum_index]["topics"].append({"title": t, "author": "Você", "created": "Hoje", "replies": 0, "messages": []})
            self.refresh_ui()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x700")
    Forum(master=app).pack(fill="both", expand=True)
    app.mainloop()