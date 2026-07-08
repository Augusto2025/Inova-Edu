# views/Aluno_e_Professor/home_view.py
import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime, date
from models.cursos_model import CursosModel
from controllers.cursos_controllers import obter_cursos
from assets.cores import *

class Home(ctk.CTkFrame):
    def __init__(self, master):  
        super().__init__(master, fg_color="#f5f7fb")
        self.janela = master

        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break
        if not sidebar_existente:
            sidebar(self.janela)
        
        self.pack(side="right", fill="both", expand=True)

        self.container_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.container_principal.pack(fill="both", expand=True)

        # Inicializa variáveis de filtro antes da interface
        self.ordenar_var = ctk.StringVar(value="A-Z")
        self.data_inicio = None
        self.data_fim = None

        self.criar_interface()

        # --- Carregamento de dados ---
        self.cursos = obter_cursos()
    
        self.atualizar_cards()

    def criar_interface(self):
        from assets.header import HeaderPadrao
        self.header = HeaderPadrao(self.container_principal, titulo="Cursos", comando_voltar=None)

        # Container de Pesquisa e Filtro à direita (dentro do header)
        search_container = ctk.CTkFrame(self.header, fg_color="transparent")
        search_container.pack(side="right", padx=30)

        # Entrada de Pesquisa estilizada para o Header
        self.nome_filter = ctk.CTkEntry(search_container, width=300, height=35, 
                                        placeholder_text="🔍 Pesquisar por curso...",
                                        fg_color=Branco, text_color="#1e293b",
                                        border_width=0)
        self.nome_filter.pack(side="left", padx=10)
        self.nome_filter.bind("<KeyRelease>", lambda e: self.filtrar_cursos())

        # 2. ÁREA DE CONTEÚDO
        self.conteudo = ctk.CTkFrame(self.container_principal, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True)

        # Scroll area para os cards
        self.scroll_area = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.cards_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.cards_container.pack(expand=True, fill="both") 
        self.cards_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
    
    def filtrar_cursos(self):
        termo = self.nome_filter.get().strip().lower()
        cursos_filtrados = [curso for curso in self.cursos if termo in curso["name"].lower()]
        self.atualizar_cards(cursos_filtrados)

    def atualizar_cards(self, lista=None):
        for w in self.cards_container.winfo_children():
            w.destroy()

        cursos = lista if lista is not None else self.cursos

        if not cursos:
            # Container centralizado para a mensagem de erro
            empty_frame = ctk.CTkFrame(self.cards_container, fg_color="transparent")
            empty_frame.pack(expand=True, pady=100)

            ctk.CTkLabel(empty_frame, text="🔍", font=ctk.CTkFont(size=50)).pack()
            ctk.CTkLabel(empty_frame, 
                         text="Nenhum curso encontrado com esse nome.", 
                         font=ctk.CTkFont(size=18, weight="bold"),
                         text_color=azulEscuro).pack(pady=10)
            ctk.CTkLabel(empty_frame, 
                         text="Tente digitar algo diferente ou verifique os filtros.", 
                         font=ctk.CTkFont(size=14),
                         text_color=CinzaTexto).pack()
            return

        cols = 3
        for idx, curso in enumerate(cursos):
            r = idx // cols
            c = idx % cols
            
            card = ctk.CTkFrame(self.cards_container, width=320, height=380, corner_radius=15, 
                                fg_color=Branco, border_width=1, border_color=azulEscuro)
            card.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
            card.pack_propagate(False)
            
            # Imagem do curso
            img_frame = ctk.CTkFrame(card, fg_color="#ebf0f5", height=140, corner_radius=10)
            img_frame.pack(fill="x", padx=15, pady=(15, 10))
            ctk.CTkLabel(img_frame, text="🎓", font=ctk.CTkFont(size=50)).place(relx=0.5, rely=0.5, anchor="center")
            
            # Nome e Descrição
            ctk.CTkLabel(card, text=curso["name"], font=ctk.CTkFont(size=17, weight="bold"), 
                         text_color="#1e293b", wraplength=280).pack(pady=(5, 2))
            
            desc = curso["description"][:80] + "..." if len(curso["description"]) > 80 else curso["description"]
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=12), text_color="#64748b", 
                         wraplength=280, justify="center").pack(padx=15, pady=5)
            
            # Botão de Ação (Azul para combinar com o tema)
            ctk.CTkButton(card, text="Acessar Curso", fg_color=azulEscuro, hover_color=azulClaro,
                          height=40, width=50, corner_radius=8, font=ctk.CTkFont(weight="bold"),
                          command=lambda c=curso: self.entrar_no_curso(c)).pack(side="bottom", fill="x", padx=20, pady=20)

    def entrar_no_curso(self, curso):
        # Captura o ID e o Nome do dicionário que veio do controller
        id_curso = curso.get("id") 
        nome_curso = curso.get("name")
        
        # DEBUG: Verifique se esses valores aparecem no seu terminal
        print(f"DEBUG HOME: Enviando ID {id_curso} e Nome {nome_curso} para a tela de turmas")
        
        if id_curso is None:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erro", "O curso selecionado não possui um ID válido.")
            print("ERRO CRÍTICO: O curso selecionado não possui um ID!")
            return

        try:
            from views.Aluno_e_Professor.turma_view import TurmasDesktopDashboard 
            self.pack_forget() 
            
            # Instancia passando os 3 argumentos: master, id, nome
            tela_turma = TurmasDesktopDashboard(self.janela, id_curso, nome_curso) 
            tela_turma.pack(side="right", fill="both", expand=True)
            
        except Exception as e:
            print(f"Erro ao navegar: {e}")