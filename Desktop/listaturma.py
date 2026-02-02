import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ───────────── DADOS DAS TURMAS ─────────────
turmas = [
    ("2025.10.111", "Manhã", "2025", "Desenvolvimento de sistemas", "📌", "🔒"),
    ("2025.02.001", "Tarde", "0", "Administrador de Banco de dados", "📌", "🔒"),
    ("2025.10.201", "Noite", "0", "Administrador de Redes", "📌", "🔒"),
    ("2025.12.115", "Manhã", "0", "IT Essentials", "📌", "🔒"),
    ("2025.05.210", "Tarde", "0", "Programação Web", "📌", "🔒"),
    ("2024.09.001", "Noite", "0", "Segurança da Informação", "📌", "🔒"),
    ("2025.06.300", "Manhã", "0", "Design Gráfico", "📌", "🔒"),
    ("2025.07.101", "Noite", "0", "Engenharia de Software", "📌", "🔒"),
    ("2025.10.111", "Manhã", "0", "Desenvolvimento de sistemas", "📌", "🔒"),
    ("2025.10.201", "Noite", "0", "Administrador de Redes", "📌", "🔒"),
    ("2025.12.115", "Manhã", "0", "IT Essentials", "📌", "🔒"),
    ("2025.05.210", "Tarde", "0", "Programação Web", "📌", "🔒"),
    ("2024.09.001", "Noite", "0", "Segurança da Informação", "📌", "🔒"),
]


# ───────────── FUNÇÕES ─────────────
def carregar_tabela(lista_turmas):
    for widget in tabela.winfo_children():
        widget.destroy()

    for idx, turma in enumerate(lista_turmas):
        # Alternar cores das linhas
        cor_fundo = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
        
        linha = ctk.CTkFrame(tabela, fg_color=cor_fundo)
        linha.grid(sticky="ew", pady=2)
        
        for i, w in enumerate(pesos):
            linha.grid_columnconfigure(i, weight=w)

        # Código da turma
        ctk.CTkLabel(
            linha, 
            text=turma[0],
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=10, sticky="w")

        # Turno
        ctk.CTkLabel(
            linha, 
            text=turma[1]
        ).grid(row=0, column=1, padx=10, sticky="w")

        # Ano
        ctk.CTkLabel(
            linha, 
            text=turma[2]
        ).grid(row=0, column=2, padx=10, sticky="w")

        # Curso
        ctk.CTkLabel(
            linha, 
            text=turma[3]
        ).grid(row=0, column=3, padx=10, sticky="w")

        # Usuários (emoji)
        ctk.CTkLabel(
            linha, 
            text=turma[4],
            font=ctk.CTkFont(size=16)
        ).grid(row=0, column=4, padx=10, sticky="w")

        # Frame para ações
        acoes_btn = ctk.CTkFrame(linha, fg_color="transparent")
        acoes_btn.grid(row=0, column=5, padx=10, sticky="w")

        # Botão Visualizar (cadeado)
        ctk.CTkButton(
            acoes_btn,
            text="🔒",
            width=35,
            fg_color="#004a8f",
            hover_color="#003366",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=lambda t=turma: visualizar_turma(t)
        ).pack(side="left", padx=2)

        # Botão Editar
        ctk.CTkButton(
            acoes_btn,
            text="✏️",
            width=35,
            fg_color="#ffc107",
            hover_color="#e0a800",
            text_color="#212529",
            font=ctk.CTkFont(size=12),
            command=lambda t=turma: editar_turma(t)
        ).pack(side="left", padx=2)

        # Botão Excluir
        ctk.CTkButton(
            acoes_btn,
            text="🗑️",
            width=35,
            fg_color="#dc3545",
            hover_color="#b52a37",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=lambda t=turma: excluir_turma(t)
        ).pack(side="left", padx=2)


def aplicar_filtro(*args):
    texto = busca.get().lower()
    turno = filtro_turno.get()
    ano = filtro_ano.get()
    
    resultado = []
    for turma in turmas:
        # Filtro por texto
        bate_texto = texto in "".join(turma).lower()
        
        # Filtro por turno
        bate_turno = turno == "Todos" or turma[1] == turno
        
        # Filtro por ano
        bate_ano = ano == "Todos" or turma[2] == ano
        
        if bate_texto and bate_turno and bate_ano:
            resultado.append(turma)
    
    carregar_tabela(resultado)


def visualizar_turma(turma):
    messagebox.showinfo(
        "Detalhes da Turma",
        f"🔢 Código: {turma[0]}\n\n"
        f"🕒 Turno: {turma[1]}\n"
        f"📅 Ano: {turma[2]}\n"
        f"📚 Curso: {turma[3]}\n"
        f"👥 Usuários: {turma[4]}\n"
        f"🔒 Status: {turma[5]}",
        icon="info"
    )


def editar_turma(turma):
    resposta = messagebox.askyesno(
        "Editar Turma",
        f"Deseja editar a turma '{turma[0]}' - {turma[3]}?",
        icon="question"
    )
    
    if resposta:
        messagebox.showinfo(
            "Em Desenvolvimento",
            "Funcionalidade de edição será implementada em breve!",
            icon="info"
        )


def excluir_turma(turma):
    resposta = messagebox.askyesno(
        "Excluir Turma",
        f"Tem certeza que deseja excluir a turma '{turma[0]}'?\n\n"
        f"Curso: {turma[3]}\n"
        "Esta ação não pode ser desfeita!",
        icon="warning"
    )
    
    if resposta:
        messagebox.showinfo(
            "Turma Excluída",
            f"✅ A turma '{turma[0]}' foi marcada para exclusão.",
            icon="info"
        )


def nova_turma():
    resposta = messagebox.askyesno(
        "Nova Turma",
        "Deseja cadastrar uma nova turma?\n\n"
        "Uma nova janela será aberta para preenchimento dos dados.",
        icon="question"
    )
    
    if resposta:
        messagebox.showinfo(
            "Em Desenvolvimento",
            "Funcionalidade de cadastro será implementada em breve!",
            icon="info"
        )


# ───────────── SIDEBAR SIMPLIFICADA ─────────────
def sidebar(app):
    sidebar_frame = ctk.CTkFrame(
        app,
        width=220,
        corner_radius=0,
        fg_color="#004a8f"
    )
    
    # Logo/ título
    ctk.CTkLabel(
        sidebar_frame,
        text="🎓 GESTÃO\nESCOLAR",
        text_color="white",
        font=ctk.CTkFont(size=20, weight="bold"),
        justify="center"
    ).pack(pady=(30, 20))
    
    # Separador
    ctk.CTkFrame(
        sidebar_frame,
        height=2,
        fg_color="white"
    ).pack(fill="x", padx=20, pady=10)
    
    # Opções do menu
    opcoes = [
        ("📊 Dashboard", "dash"),
        ("📚 Cursos", "cursos"),
        ("👥 Turmas", "turmas"),
        ("👤 Alunos", "alunos"),
        ("👨‍🏫 Professores", "prof"),
        ("📅 Calendário", "cal"),
        ("📈 Relatórios", "rel"),
        ("⚙️ Configurações", "config")
    ]
    
    botoes_menu = []
    
    for texto, cmd in opcoes:
        # Destacar a opção atual (Turmas)
        if cmd == "turmas":
            fg_color = "white"
            text_color = "#004a8f"
        else:
            fg_color = "transparent"
            text_color = "white"
        
        btn = ctk.CTkButton(
            sidebar_frame,
            text=texto,
            command=lambda c=cmd: selecionar_menu(c),
            height=45,
            anchor="w",
            fg_color=fg_color,
            hover_color="#003366",
            text_color=text_color,
            font=ctk.CTkFont(size=14),
            corner_radius=5,
            border_width=0
        )
        btn.pack(fill="x", padx=15, pady=3)
        botoes_menu.append(btn)
    
    # Espaço vazio
    ctk.CTkLabel(sidebar_frame, text="").pack(fill="x", expand=True)
    
    # Botão Sair
    ctk.CTkButton(
        sidebar_frame,
        text="🚪 Sair do Sistema",
        command=app.quit,
        height=45,
        fg_color="white",
        hover_color="#e6e6e6",
        text_color="#004a8f",
        font=ctk.CTkFont(size=14, weight="bold"),
        corner_radius=8
    ).pack(side="bottom", fill="x", padx=15, pady=20)
    
    return sidebar_frame, botoes_menu


def selecionar_menu(opcao):
    if opcao != "turmas":
        messagebox.showinfo(
            "Navegação",
            f"Você selecionou: {opcao}\n\n"
            "Em uma aplicação completa, esta ação carregaria a tela correspondente.",
            icon="info"
        )


# ───────────── APP ─────────────
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1300x650")
    app.title("Sistema de Gestão de Turmas")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)

    sidebar_frame, botoes_menu = sidebar(app)
    sidebar_frame.grid(row=0, column=0, sticky="ns")

    conteudo_frame = ctk.CTkFrame(app, fg_color="#ffffff", corner_radius=0)
    conteudo_frame.grid(row=0, column=1, sticky="nsew")
    conteudo_frame.grid_rowconfigure(2, weight=1)
    conteudo_frame.grid_columnconfigure(0, weight=1)

    # ───────────── CABEÇALHO ─────────────
    topo = ctk.CTkFrame(conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
    topo.grid(row=0, column=0, sticky="ew")
    topo.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        topo,
        text="👥  LISTA DE TURMAS",
        text_color="white",
        font=ctk.CTkFont(size=18, weight="bold")
    ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

    # Botão para nova turma
    ctk.CTkButton(
        topo,
        text="+ Nova Turma",
        fg_color="white",
        text_color="#004a8f",
        hover_color="#e6e6e6",
        width=120,
        height=35,
        font=ctk.CTkFont(size=13, weight="bold"),
        command=nova_turma
    ).grid(row=0, column=2, padx=20)

    # ───────────── BARRA DE AÇÕES ─────────────
    acoes = ctk.CTkFrame(conteudo_frame, fg_color="#f5f5f5", height=80, corner_radius=8)
    acoes.grid(row=1, column=0, sticky="ew", padx=20, pady=15)
    acoes.grid_columnconfigure(1, weight=1)

    # Frame para filtros
    filtros_frame = ctk.CTkFrame(acoes, fg_color="transparent")
    filtros_frame.grid(row=0, column=0, padx=15, pady=10, sticky="w")
    filtros_frame.grid_columnconfigure(0, weight=1)

    # Campo de busca
    busca = ctk.CTkEntry(
        filtros_frame, 
        placeholder_text="Buscar por código ou curso...", 
        width=250,
        height=35,
        border_width=2,
        border_color="#ddd",
        fg_color="white",
        text_color="#333",
        font=ctk.CTkFont(size=13)
    )
    busca.grid(row=0, column=0, sticky="w")
    busca.bind("<KeyRelease>", aplicar_filtro)

    # Filtro por turno
    ctk.CTkLabel(
        filtros_frame,
        text="Turno:",
        font=ctk.CTkFont(size=12, weight="bold")
    ).grid(row=1, column=0, sticky="w", pady=(10, 5))

    filtro_turno = ctk.StringVar(value="Todos")
    turno_frame = ctk.CTkFrame(filtros_frame, fg_color="transparent")
    turno_frame.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    for opcao in ["Todos", "Manhã", "Tarde", "Noite"]:
        ctk.CTkRadioButton(
            turno_frame,
            text=opcao,
            variable=filtro_turno,
            value=opcao,
            command=aplicar_filtro,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=5)

    # Filtro por ano
    ctk.CTkLabel(
        filtros_frame,
        text="Ano:",
        font=ctk.CTkFont(size=12, weight="bold")
    ).grid(row=3, column=0, sticky="w", pady=(5, 0))

    filtro_ano = ctk.StringVar(value="Todos")
    ano_frame = ctk.CTkFrame(filtros_frame, fg_color="transparent")
    ano_frame.grid(row=4, column=0, sticky="w", pady=(0, 5))
    
    for opcao in ["Todos", "2025", "2024", "0"]:
        ctk.CTkRadioButton(
            ano_frame,
            text=opcao,
            variable=filtro_ano,
            value=opcao,
            command=aplicar_filtro,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=5)

    # Frame para botões e estatísticas
    botoes_frame = ctk.CTkFrame(acoes, fg_color="transparent")
    botoes_frame.grid(row=0, column=1, padx=15, pady=10, sticky="e")

    # Botão de busca
    ctk.CTkButton(
        botoes_frame,
        text="🔍 Buscar",
        width=100,
        height=35,
        fg_color="#004a8f",
        hover_color="#003366",
        text_color="white",
        font=ctk.CTkFont(size=13),
        command=aplicar_filtro
    ).pack(side="left", padx=5)

    # Botão para atualizar
    ctk.CTkButton(
        botoes_frame,
        text="🔄 Atualizar",
        width=100,
        height=35,
        fg_color="#6c757d",
        hover_color="#5a6268",
        text_color="white",
        font=ctk.CTkFont(size=13),
        command=lambda: carregar_tabela(turmas)
    ).pack(side="left", padx=5)

    # Estatísticas
    estat_frame = ctk.CTkFrame(botoes_frame, fg_color="transparent")
    estat_frame.pack(side="left", padx=(20, 0))

    ctk.CTkLabel(
        estat_frame,
        text=f"📊 Total: {len(turmas)} turmas",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#004a8f"
    ).pack()

    # Contagem por turno
    manha = sum(1 for t in turmas if t[1] == "Manhã")
    tarde = sum(1 for t in turmas if t[1] == "Tarde")
    noite = sum(1 for t in turmas if t[1] == "Noite")
    
    ctk.CTkLabel(
        estat_frame,
        text=f"🕒 Manhã: {manha} | Tarde: {tarde} | Noite: {noite}",
        font=ctk.CTkFont(size=10),
        text_color="#666666"
    ).pack()

    # ───────────── CORPO COM TABELA ─────────────
    corpo = ctk.CTkFrame(conteudo_frame, fg_color="#ffffff", corner_radius=0)
    corpo.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
    corpo.grid_rowconfigure(1, weight=1)
    corpo.grid_columnconfigure(0, weight=1)

    # Cabeçalho da tabela
    tabela_header = ctk.CTkFrame(corpo, fg_color="#003f7f", height=40)
    tabela_header.grid(row=0, column=0, sticky="ew")

    # Pesos das colunas (ajustados para turmas)
    pesos = [3, 2, 2, 4, 2, 3]  # 6 colunas
    
    for i, w in enumerate(pesos):
        tabela_header.grid_columnconfigure(i, weight=w)

    # Nomes das colunas
    colunas = ["Código", "Turno", "Ano", "Curso", "Usuários", "Ações"]
    for i, col in enumerate(colunas):
        ctk.CTkLabel(
            tabela_header,
            text=col,
            text_color="white",
            font=ctk.CTkFont(weight="bold", size=13)
        ).grid(row=0, column=i, padx=10, sticky="w")

    # Área da tabela com scroll
    tabela = ctk.CTkScrollableFrame(corpo, fg_color="#ffffff")
    tabela.grid(row=1, column=0, sticky="nsew")

    # Carregar turmas inicialmente
    carregar_tabela(turmas)

    app.mainloop()