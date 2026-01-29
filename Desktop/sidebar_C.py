import customtkinter as ctk
from PIL import Image
from cadastro_turma import CadastroTurmas
from cadastro_usuario import CadastroUsuarios
from cadastro_curso import CadastroCursos

def sidebar(janela, cor_fundo="#004A8D", cor_texto="#ecf0f1"):
    # Faz com que o menu se estique conforme a tela
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(1, weight=1)

    # Frame do menu lateral - IMPORTANTE: rowspan para ocupar todas as linhas
    menu_frame = ctk.CTkFrame(
        janela, 
        width=250,
        corner_radius=0,
        fg_color=cor_fundo
    )
    menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    menu_frame.grid_propagate(False)
    
    # Container para conteúdo do menu - que preenche todo o frame
    menu_container = ctk.CTkFrame(menu_frame, fg_color="transparent")
    menu_container.pack(fill="both", expand=True, padx=10, pady=20)

    imagem_pil = Image.open("Desktop/LOGOBRANCO.png")

    imagem_ctk = ctk.CTkImage(
        light_image=imagem_pil,
        size=(80,100)
    )

    # Logo do sistema
    logo_frame = ctk.CTkFrame(menu_container, fg_color="transparent")
    logo_frame.pack(pady=(0, 20))
    
    logo_image = ctk.CTkLabel(logo_frame, image=imagem_ctk, text="")
    logo_image.pack()

    logo_label = ctk.CTkLabel(
        logo_frame,
        text="INOVA EDU",
        font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
        text_color=cor_texto
    )
    logo_label.pack()
    
    # Separador
    separador = ctk.CTkFrame(
        menu_container, 
        height=2,
        fg_color=cor_texto
    )
    separador.pack(fill="x", pady=5)
    
    # Título do menu
    titulo_label = ctk.CTkLabel(
        menu_container,
        text="MENU LATERAL",
        font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
        text_color=cor_texto
    )
    titulo_label.pack(pady=(15, 10))
    
    # Opções do menu
    opcoes_menu = [
        " Cadastrar Aluno",
        " Listas dos Alunos",
        " Cadastrar Turmas",
        " Listas das Turmas",
        " Cadastrar Cursos",
        " Listas dos Cursos",
    ]
    
    botoes_menu = []

    for opcao in opcoes_menu:
        if opcao == "Cadastrar Aluno":
            comando = lambda: CadastroUsuarios().run()
        elif opcao == "Cadastrar Cursos":
            comando = lambda: CadastroCursos().run()
        elif opcao == "Cadastrar Turmas":
            comando = lambda: CadastroTurmas().run()
        else:
            comando = ""

        botao = ctk.CTkButton(
            menu_container,
            text=f"   {opcao}",
            height=50,
            anchor="w",
            text_color=cor_texto,
            command=comando,
            font=ctk.CTkFont(size=14, family="Arial"),
            corner_radius=5,
            border_width=0
        )
        botao.pack(fill="x", pady=3)
        botoes_menu.append(botao)
        
    # **ESPAÇO FLEXÍVEL** - Isso faz o conteúdo acima e abaixo se ajustarem
    espaco_flexivel = ctk.CTkLabel(menu_container, text="")
    espaco_flexivel.pack(fill="both", expand=True)
    
    # Separador antes do botão sair
    ctk.CTkFrame(menu_container, height=1, fg_color="#ffffff").pack(fill="x", pady=(10, 5), side="bottom")
    
    # Botão Sair (sempre no final)
    sair_btn = ctk.CTkButton(
        menu_container,
        text="Logout",
        command=janela.quit,
        height=45,
        fg_color="#e74c3c",
        hover_color="#c0392b",
        text_color=cor_texto,
        font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
        corner_radius=8
    )
    sair_btn.pack(side="bottom", fill="x", pady=(0, 5))
    
    return menu_frame, botoes_menu

if __name__ == "__main__":
    # Testar a versão mais simples
    app = ctk.CTk()
    app.geometry("1200x700")
    app.title("Sidebar")
    app._set_appearance_mode("light")
    
    # Criar menu
    menu_frame, botoes = sidebar(app)
    
    app.mainloop()