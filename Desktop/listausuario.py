import customtkinter as ctk
from tkinter import messagebox
from sidebar_C import sidebar
from PIL import Image
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ListaUsuariosApp(ctk.CTkFrame):
    def __init__(self, master):
        # Inicializa como um Frame vinculado ao master (content_frame)
        super().__init__(master, fg_color="#ffffff", corner_radius=0)
        
        # ───────────── DADOS DOS CURSOS ─────────────
        self.cursos = [
            ("Desenvolvimento de Sistemas", "Manhã", "2025", "💻", 32),
            ("Banco de Dados", "Tarde", "2025", "🗄️", 28),
            ("Redes de Computadores", "Noite", "2024", "🌐", 25),
            ("Programação Web", "Manhã", "2025", "🕸️", 30),
        ]

        # Variáveis de Filtro
        self.busca_var = ctk.StringVar()
        self.filtro_turno = ctk.StringVar(value="Todos")

        # Configuração de Grid do Frame Principal
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Montagem dos Componentes
        self.criar_topo()
        self.criar_acoes()
        self.criar_corpo()
        self.carregar_watermark()
        
        # Carga inicial de dados
        self.carregar_tabela(self.cursos)

    # ───────────── TOPO (Design Azul) ─────────────
    def criar_topo(self):
        topo = ctk.CTkFrame(self, height=60, fg_color="#004a8f", corner_radius=0)
        topo.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            topo,
            text="📚  LISTA DE CURSOS",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

    # ───────────── AÇÕES (Busca e Rádios) ─────────────
    def criar_acoes(self):
        acoes = ctk.CTkFrame(self, fg_color="#f5f5f5", height=60, corner_radius=8)
        acoes.grid(row=1, column=0, sticky="ew", padx=20, pady=15)

        acoes.grid_columnconfigure(0, weight=1)

        # Entrada de Busca
        self.busca = ctk.CTkEntry(
            acoes, 
            placeholder_text="Buscar curso por nome...", 
            width=300,
            textvariable=self.busca_var
        )
        self.busca.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.busca.bind("<KeyRelease>", self.aplicar_filtro)

        # Frame de Filtros de Turno
        filtro_frame = ctk.CTkFrame(acoes, fg_color="transparent")
        filtro_frame.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(filtro_frame, text="Turno:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))

        for turno in ["Todos", "Manhã", "Tarde", "Noite"]:
            ctk.CTkRadioButton(
                filtro_frame,
                text=turno,
                variable=self.filtro_turno,
                value=turno,
                command=self.aplicar_filtro,
                radiobutton_width=18,
                radiobutton_height=18
            ).pack(side="left", padx=5)

        # Botão Cadastro
        ctk.CTkButton(
            acoes,
            text="+ Novo Curso",
            fg_color="#004a8f",
            hover_color="#003366",
            width=120,
            command=lambda: messagebox.showinfo("Cadastro", "Tela de Cadastro de Cursos")
        ).grid(row=0, column=2, padx=15, sticky="e")

    # ───────────── CORPO E TABELA ─────────────
    def criar_corpo(self):
        self.corpo_container = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.corpo_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.corpo_container.grid_columnconfigure(0, weight=1)
        self.corpo_container.grid_rowconfigure(1, weight=1)

        # Header da Lista
        header = ctk.CTkFrame(self.corpo_container, fg_color="#003f7f", height=40)
        header.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            header, text="CURSOS DISPONÍVEIS", 
            text_color="white", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=10)

        # Scrollable Frame para os Cards
        self.tabela = ctk.CTkScrollableFrame(self.corpo_container, fg_color="#ffffff", corner_radius=0)
        self.tabela.grid(row=1, column=0, sticky="nsew")

    # ───────────── LOGO FUNDO (Watermark) ─────────────
    def carregar_watermark(self):
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(BASE_DIR, "assets", "img", "LOGOAZUL.png")
            img = Image.open(logo_path).convert("RGBA")
            alpha = img.split()[3].point(lambda p: p * 0.12) # 12% Opacidade
            img.putalpha(alpha)
            self.watermark_img = ctk.CTkImage(light_image=img, size=(600, 600))
        except:
            self.watermark_img = None

    # ───────────── RENDERIZAÇÃO DOS CARDS ─────────────
    def carregar_tabela(self, lista):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        if self.watermark_img:
            wm = ctk.CTkLabel(self.tabela, image=self.watermark_img, text="")
            wm.place(relx=0.5, rely=0.5, anchor="center")
            wm.lower()

        for curso in lista:
            card = ctk.CTkFrame(self.tabela, fg_color="#ffffff", border_width=1, border_color="#e0e0e0", corner_radius=10)
            card.pack(fill="x", pady=8, padx=15)

            # Info Esquerda
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", padx=20, pady=15, fill="x", expand=True)

            ctk.CTkLabel(info, text=f"{curso[3]} {curso[0]}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#004a8f").pack(anchor="w")
            ctk.CTkLabel(info, text=f"🕒 Turno: {curso[1]}  |  📅 Ano: {curso[2]}  |  👥 Alunos: {curso[4]}").pack(anchor="w", pady=2)

            # Botões Direita
            btn_area = ctk.CTkFrame(card, fg_color="transparent")
            btn_area.pack(side="right", padx=20)

            ctk.CTkButton(btn_area, text="✏️ Editar", width=80, height=28, fg_color="#ffc107", text_color="black", 
                          command=lambda c=curso: self.editar_curso(c)).pack(side="left", padx=5)
            
            ctk.CTkButton(btn_area, text="🗑️", width=40, height=28, fg_color="#dc3545", 
                          command=lambda c=curso: self.excluir_curso(c)).pack(side="left")

    # ───────────── LÓGICA ─────────────
    def aplicar_filtro(self, *args):
        texto = self.busca_var.get().lower()
        turno = self.filtro_turno.get()
        res = [c for c in self.cursos if (texto in c[0].lower()) and (turno == "Todos" or c[1] == turno)]
        self.carregar_tabela(res)

    def editar_curso(self, curso):
        messagebox.showinfo("Editar", f"Editando: {curso[0]}")

    def excluir_curso(self, curso):
        confirmar = messagebox.askyesno("Excluir", f"Tem certeza que deseja excluir {curso[0]}?")
        if confirmar: print(f"Excluído: {curso[0]}")

# ───────────── TESTE ISOLADO ─────────────
if __name__ == "__main__":
    root = ctk.CTk()
    root.attributes("-fullscreen", True)
    
    # Simulação da estrutura principal com sidebar
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)
    
    sidebar_frame, _ = sidebar(main_frame)
    sidebar_frame.grid(row=0, column=0, sticky="ns")
    
    content_area = ctk.CTkFrame(main_frame)
    content_area.grid(row=0, column=1, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    app = ListaUsuariosApp(content_area)
    app.pack(fill="both", expand=True)
    
    root.mainloop()