import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from sidebar_C import sidebar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ───────────── DADOS DOS CURSOS ─────────────
cursos = [
    ("Desenvolvimento de Sistemas", "01/02/2025", "15/12/2025", "💻", "Curso de desenvolvimento fullstack"),
    ("Administração de Banco de Dados", "15/03/2025", "20/12/2025", "🗄️", "Administração e otimização de bancos relacionais"),
    ("Redes de Computadores", "10/04/2025", "30/11/2025", "🌐", "Configuração e manutenção de redes"),
    ("Programação Web", "05/05/2025", "10/12/2025", "🕸️", "Desenvolvimento web moderno"),
    ("Segurança da Informação", "20/06/2025", "25/11/2025", "🔒", "Proteção de dados e sistemas"),
    ("Design Gráfico", "01/07/2025", "15/12/2025", "🎨", "Design digital e interfaces"),
    ("Engenharia de Software", "12/08/2025", "30/12/2025", "⚙️", "Metodologias ágeis e arquitetura"),
    ("Data Science", "25/09/2025", "05/12/2025", "📊", "Análise de dados e machine learning"),
    ("Mobile Development", "08/10/2025", "20/12/2025", "📱", "Desenvolvimento de apps móveis"),
    ("Cloud Computing", "15/11/2025", "28/02/2026", "☁️", "Serviços em nuvem e DevOps"),
    ("Inteligência Artificial", "03/12/2025", "15/03/2026", "🤖", "Algoritmos de IA e deep learning"),
    ("UX/UI Design", "10/01/2026", "25/04/2026", "✨", "Design de experiência do usuário"),
]


# ───────────── FUNÇÕES ─────────────
def carregar_tabela(lista_cursos):
    for widget in tabela.winfo_children():
        widget.destroy()

    for idx, curso in enumerate(lista_cursos):
        # Alternar cores das linhas
        cor_fundo = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
        
        linha = ctk.CTkFrame(tabela, fg_color=cor_fundo)
        linha.grid(sticky="ew", pady=2)
        
        for i, w in enumerate(pesos):
            linha.grid_columnconfigure(i, weight=w)

        # Nome do curso
        ctk.CTkLabel(
            linha, 
            text=curso[0],
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=10, sticky="w")

        # Data de início
        ctk.CTkLabel(
            linha, 
            text=curso[1],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=1, padx=10, sticky="w")

        # Data de término
        ctk.CTkLabel(
            linha, 
            text=curso[2],
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=10, sticky="w")

        # Imagem (emoji)
        ctk.CTkLabel(
            linha, 
            text=curso[3],
            font=ctk.CTkFont(size=20)
        ).grid(row=0, column=3, padx=10, sticky="w")

        # Descrição (com tooltip se for muito longa)
        descricao = curso[4]
        if len(descricao) > 30:
            descricao_label = ctk.CTkLabel(
                linha, 
                text=descricao[:27] + "...",
                font=ctk.CTkFont(size=11),
                cursor="hand2"
            )
            descricao_label.grid(row=0, column=4, padx=10, sticky="w")
            # Tooltip para descrição completa
            descricao_label.bind("<Enter>", lambda e, d=curso[4]: mostrar_tooltip(e, d))
            descricao_label.bind("<Leave>", lambda e: ocultar_tooltip(e))
        else:
            ctk.CTkLabel(
                linha, 
                text=descricao,
                font=ctk.CTkFont(size=11)
            ).grid(row=0, column=4, padx=10, sticky="w")

        # Frame para ações
        acoes_btn = ctk.CTkFrame(linha, fg_color="transparent")
        acoes_btn.grid(row=0, column=5, padx=10, sticky="w")

        # Botão Visualizar
        ctk.CTkButton(
            acoes_btn,
            text="👁️",
            width=35,
            fg_color="#004a8f",
            hover_color="#003366",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=lambda c=curso: visualizar_curso(c)
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
            command=lambda c=curso: editar_curso(c)
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
            command=lambda c=curso: excluir_curso(c)
        ).pack(side="left", padx=2)

        # Botão Alunos (se houver)
        ctk.CTkButton(
            acoes_btn,
            text="👥",
            width=35,
            fg_color="#28a745",
            hover_color="#218838",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=lambda c=curso: ver_alunos(c)
        ).pack(side="left", padx=2)


def mostrar_tooltip(event, texto):
    """Mostra tooltip com descrição completa"""
    tooltip = ctk.CTkToplevel(event.widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
    
    label = ctk.CTkLabel(
        tooltip,
        text=texto,
        fg_color="#333333",
        text_color="white",
        corner_radius=5,
        padx=10,
        pady=5
    )
    label.pack()
    
    # Guarda referência para destruir depois
    event.widget.tooltip = tooltip


def ocultar_tooltip(event):
    """Remove o tooltip"""
    if hasattr(event.widget, 'tooltip'):
        event.widget.tooltip.destroy()


def aplicar_filtro(*args):
    texto = busca.get().lower()
    status = filtro_status.get()
    
    resultado = []
    for curso in cursos:
        # Filtro por texto (busca em nome e descrição)
        bate_texto = texto in curso[0].lower() or texto in curso[4].lower()
        
        # Filtro por status (ativo/concluído)
        bate_status = status == "Todos"
        if status == "Ativos":
            # Considera ativo se término for futuro ou 0
            bate_status = curso[2] == "0" or not curso[2].endswith("2024")
        elif status == "Concluídos":
            bate_status = curso[2].endswith("2024")
        
        if bate_texto and bate_status:
            resultado.append(curso)
    
    carregar_tabela(resultado)
    atualizar_estatisticas(len(resultado))


def atualizar_estatisticas(total_filtrado=None):
    """Atualiza as estatísticas exibidas"""
    if total_filtrado is None:
        total_filtrado = len(cursos)
    
    # Contagem por status
    ativos = sum(1 for c in cursos if c[2] == "0" or not c[2].endswith("2024"))
    concluidos = sum(1 for c in cursos if c[2].endswith("2024"))
    
    total_label.configure(text=f"📊 Total: {total_filtrado} cursos")
    status_label.configure(text=f"📈 Ativos: {ativos} | ✅ Concluídos: {concluidos}")


def visualizar_curso(curso):
    messagebox.showinfo(
        "Detalhes do Curso",
        f"📚 Nome: {curso[0]}\n\n"
        f"📅 Início: {curso[1]}\n"
        f"📅 Término: {curso[2]}\n"
        f"{curso[3]} Imagem/Ícone\n"
        f"📝 Descrição: {curso[4]}\n\n"
        f"👥 Matriculados: [Em desenvolvimento]",
        icon="info"
    )


def editar_curso(curso):
    resposta = messagebox.askyesno(
        "Editar Curso",
        f"Deseja editar o curso '{curso[0]}'?\n\n"
        f"Descrição: {curso[4][:50]}...",
        icon="question"
    )
    
    if resposta:
        messagebox.showinfo(
            "Em Desenvolvimento",
            "Funcionalidade de edição será implementada em breve!",
            icon="info"
        )


def excluir_curso(curso):
    resposta = messagebox.askyesno(
        "Excluir Curso",
        f"Tem certeza que deseja excluir o curso '{curso[0]}'?\n\n"
        f"Esta ação removerá todas as turmas associadas a este curso!",
        icon="warning"
    )
    
    if resposta:
        messagebox.showinfo(
            "Curso Excluído",
            f"✅ O curso '{curso[0]}' foi marcado para exclusão.",
            icon="info"
        )


def ver_alunos(curso):
    messagebox.showinfo(
        "Alunos do Curso",
        f"👥 Lista de alunos matriculados em '{curso[0]}':\n\n"
        f"[Funcionalidade em desenvolvimento]\n\n"
        f"Total estimado: 25 alunos",
        icon="info"
    )


def novo_curso():
    resposta = messagebox.askyesno(
        "Novo Curso",
        "Deseja cadastrar um novo curso?\n\n"
        "Uma nova janela será aberta para preenchimento dos dados.",
        icon="question"
    )
    
    if resposta:
        messagebox.showinfo(
            "Em Desenvolvimento",
            "Funcionalidade de cadastro será implementada em breve!",
            icon="info"
        )


# ───────────── APP ─────────────
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1300x650")
    app.title("Sistema de Gestão de Cursos")
    app.attributes("-fullscreen", True)

    # Container principal
    main_container = ctk.CTkFrame(app)
    main_container.pack(fill="both", expand=True)
    
    # Adicionar sidebar
    sidebar_frame, botoes_menu = sidebar(main_container)
    
    # Frame do conteúdo
    conteudo_frame = ctk.CTkFrame(main_container, fg_color="#ffffff")
    conteudo_frame.pack(side="left", fill="both", expand=True)
    
    # Configurar grid do conteúdo
    conteudo_frame.grid_rowconfigure(2, weight=1)
    conteudo_frame.grid_columnconfigure(0, weight=1)

    # ───────────── CABEÇALHO ─────────────
    topo = ctk.CTkFrame(conteudo_frame, height=60, fg_color="#004a8f", corner_radius=0)
    topo.grid(row=0, column=0, sticky="ew")
    topo.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        topo,
        text="📚  LISTA DE CURSOS", 
        text_color="white",
        font=ctk.CTkFont(size=18, weight="bold")
    ).grid(row=0, column=0, padx=20, pady=15, sticky="w")



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
        placeholder_text="Buscar por nome ou descrição...", 
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

    # Filtro por status
    ctk.CTkLabel(
        filtros_frame,
        text="Status:",
        font=ctk.CTkFont(size=12, weight="bold")
    ).grid(row=1, column=0, sticky="w", pady=(10, 5))

    filtro_status = ctk.StringVar(value="Todos")
    status_frame = ctk.CTkFrame(filtros_frame, fg_color="transparent")
    status_frame.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    for opcao in ["Todos", "Ativos", "Concluídos"]:
        ctk.CTkRadioButton(
            status_frame,
            text=opcao,
            variable=filtro_status,
            value=opcao,
            command=aplicar_filtro,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=5)

    # Frame para botões e estatísticas
    botoes_frame = ctk.CTkFrame(acoes, fg_color="transparent")
    botoes_frame.grid(row=0, column=1, padx=15, pady=10, sticky="e")


 

    # Estatísticas
    estat_frame = ctk.CTkFrame(botoes_frame, fg_color="transparent")
    estat_frame.pack(side="left", padx=(20, 0))

   
    
   

    # ───────────── CORPO COM TABELA ─────────────
    corpo = ctk.CTkFrame(conteudo_frame, fg_color="#ffffff", corner_radius=0)
    corpo.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
    corpo.grid_rowconfigure(1, weight=1)
    corpo.grid_columnconfigure(0, weight=1)

    # Cabeçalho da tabela
    tabela_header = ctk.CTkFrame(corpo, fg_color="#003f7f", height=40)
    tabela_header.grid(row=0, column=0, sticky="ew")

    # Pesos das colunas (ajustados para cursos)
    pesos = [3, 2, 2, 1, 4, 3]  # 6 colunas: Nome, Início, Término, Imagem, Descrição, Ações
    
    for i, w in enumerate(pesos):
        tabela_header.grid_columnconfigure(i, weight=w)

    # Nomes das colunas
    colunas = ["Nome", "Início", "Término", "Imagem", "Descrição", "Ações"]
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

    # Carregar cursos inicialmente
    carregar_tabela(cursos)

    app.mainloop()