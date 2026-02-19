import customtkinter as ctk
from PIL import Image
import sys
import os


# Variável global para controlar a janela atual
janela_global = None

def sidebar(janela, cor_fundo="#004A8D", cor_texto="#ecf0f1"):
    global janela_global
    janela_global = janela
    
    # Pega nome do arquivo atual
    nome_arquivo = os.path.basename(sys.argv[0])
    print(f"DEBUG: Arquivo atual: {nome_arquivo}")

    def detectar_tela(arquivo_alvo, nome_exibicao):
        """Retorna o comando correto ou None se já está na mesma tela"""
        # Se já está neste arquivo, retorna None
        if nome_arquivo == arquivo_alvo:
            print(f"DEBUG: Já está em {arquivo_alvo} - retornando None")
            return None
        
        def navegar():
            global janela_global
            print(f"DEBUG: Navegando para {arquivo_alvo}")
            if janela_global:
                janela_global.destroy()
            
            # Mapeamento dinâmico de classes
            if arquivo_alvo == "home.py":
                from Desktop.menu_com_perfil import Home
                Home().run()
            elif arquivo_alvo == "cadastro_usuario.py":
                from cadastro_usuario import CadastroUsuarios
                CadastroUsuarios().run()
            elif arquivo_alvo == "cadastro_curso.py":
                from cadastro_curso import CadastroCursos
                CadastroCursos().run()
            elif arquivo_alvo == "perfil_academico.py":
                from Desktop.perfil_academico import UserProfileSystem
                UserProfileSystem().run()
            else:
                print(f"Classe não encontrada para {arquivo_alvo}")
        
        return navegar

    # Frame do menu lateral
    menu_frame = ctk.CTkFrame(
        janela, 
        width=250,
        corner_radius=0,
        fg_color=cor_fundo
    )
    menu_frame.pack(side="left", fill="y")
    
    # Container para conteúdo do menu
    menu_container = ctk.CTkFrame(menu_frame, fg_color="transparent")
    menu_container.pack(fill="both", expand=True, padx=10, pady=20)

    # Carregar imagem 
    try:
        imagem_pil = Image.open("Desktop/LOGOBRANCO.png")
        imagem_ctk = ctk.CTkImage(
            light_image=imagem_pil,
            size=(80,100)
        )
        logo_image = ctk.CTkLabel(menu_container, image=imagem_ctk, text="")
        logo_image.pack()
    except:
        # Fallback se imagem não existir
        ctk.CTkLabel(menu_container, text="LOGO", font=ctk.CTkFont(size=22)).pack()

    logo_label = ctk.CTkLabel(
        menu_container,
        text="INOVA EDU",
        font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
        text_color=cor_texto
    )
    logo_label.pack()
    
    # Separador
    ctk.CTkFrame(menu_container, height=2, fg_color=cor_texto).pack(fill="x", pady=5)
    
    # Título do menu
    titulo_label = ctk.CTkLabel(
        menu_container,
        text="MENU LATERAL",
        font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
        text_color=cor_texto
    )
    titulo_label.pack(pady=(15, 10))
    
    # Opções do menu - AGORA COM PERFIL
    opcoes_menu = {
        " 🏠 Repositório": ("home.py", "Home"),
        " 👥 Fórum": ("cadastro_turma.py", "Cadastro de Turmas"),
        " 📚 Eventos": ("cadastro_curso.py", "Cadastro de Cursos"),
        " 👤 Meu Perfil": ("perfil_academico.py", "Perfil Acadêmico"),
    }
    
    botoes_menu = []

    for texto_botao, (arquivo_alvo, nome_tela) in opcoes_menu.items():
        comando = detectar_tela(arquivo_alvo, nome_tela)
        
        botao = ctk.CTkButton(
            menu_container,
            text=texto_botao,
            height=50,
            anchor="w",
            text_color=cor_texto,
            command=comando if comando else lambda: None,
            font=ctk.CTkFont(size=14, family="Arial"),
            corner_radius=5,
            border_width=0,
            fg_color="#419FFD",
            hover_color="#003366",
            state="normal" if comando else "disabled"
        )
        botao.pack(fill="x", pady=3)
        botoes_menu.append(botao)
        
        print(f"DEBUG: Botão '{texto_botao}' - Comando: {'Ativo' if comando else 'Desativado (None)'}")
        
    # Espaço flexível
    ctk.CTkLabel(menu_container, text="").pack(fill="both", expand=True)
    
    # Botão Sair
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