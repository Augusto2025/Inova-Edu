import customtkinter as ctk
from PIL import Image
import sys
import os

# Variável global para controlar a janela atual
janela_global = None

def sidebar(janela, cor_fundo="#004A8D", cor_texto="#ecf0f1"):
    global janela_global
    janela_global = janela
    
    # Importar classes DENTRO das funções para evitar circular imports
    def importar_classes():
        try:
            from home import Home
            from cadastro_usuario import CadastroUsuarios
            from eventos import CalendarioDesktopApp
            from perfil_academico import UserProfileSystem
            return CadastroUsuarios, Home, CalendarioDesktopApp, UserProfileSystem
        except ImportError:
            # Classes mock para teste
            class MockCadastro:
                def run(self):
                    print("Classe não encontrada")
            return MockCadastro, MockCadastro, MockCadastro
    
    # Pega nome do arquivo atual
    nome_arquivo = os.path.basename(sys.argv[0])
    print(f"DEBUG: Arquivo atual: {nome_arquivo}")

    def detectar_tela(arquivo_alvo, nome_exibicao):
        """Retorna o comando correto ou None se já está na mesma tela"""
        # Se já está neste arquivo, retorna None
        if nome_arquivo == arquivo_alvo:
            print(f"DEBUG: Já está em {arquivo_alvo} - retornando None")
            return None
        
        # Importa classes agora
        CadastroUsuarios, Home, CalendarioDesktopApp, UserProfileSystem = importar_classes()
        
        # Mapeamento de arquivos para classes
        mapeamento = {
            "cadastro_usuario.py": CadastroUsuarios,
            "home.py": Home,
            "enventos.py": CalendarioDesktopApp,
            "perfil_academico.py": UserProfileSystem
        }
        
        classe = mapeamento.get(arquivo_alvo)
        if not classe:
            return None
        
        def navegar():
            global janela_global
            print(f"DEBUG: Navegando para {arquivo_alvo}")
            if janela_global:
                janela_global.destroy()
            classe().run()
        
        return navegar

    def limpar_tela():
        global janela_global
        if janela_global:
            janela_global.destroy()


    # Frame do menu lateral - use pack em vez de grid
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
    
    # Opções do menu - corrigido
    opcoes_menu = {
        " Repositório": ("home.py", "Home"),
        " Fórum": ("cadastro_usuario.py", "Cadastro de Usuários"),
        " Eventos": ("enventos.py", "Calendário de Eventos"),
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
            command=comando if comando else lambda: None,  # Se None, função vazia
            font=ctk.CTkFont(size=14, family="Arial"),
            corner_radius=5,
            border_width=0,
            fg_color="#419FFD",
            hover_color="#003366",
            state="normal" if comando else "disabled"  # Desabilita se já está na tela
        )
        botao.pack(fill="x", pady=3)
        botoes_menu.append(botao)
        
        # Debug
        print(f"DEBUG: Botão '{texto_botao}' - Comando: {'Ativo' if comando else 'Desativado (None)'}")
    

    # Espaço flexível
    ctk.CTkLabel(menu_container, text="").pack(fill="both", expand=True)

    opcoes_bottom = {
        " Perfil": ("perfil_academico.py", "Perfil do Usuário"),
    }
    botoes_menu_perfil = []

    for texto_botao, (arquivo_alvo, nome_tela) in opcoes_bottom.items():
        comando2 = detectar_tela(arquivo_alvo, nome_tela)
    
    perfil_btn = ctk.CTkButton(
        menu_container,
        text="Perfil",
        height=50,
        anchor="w",
        text_color=cor_texto,
        command=comando2 if comando2 else lambda: None,
        font=ctk.CTkFont(size=14, family="Arial"),
        corner_radius=5,
        border_width=0,
        fg_color="#419FFD",
        hover_color="#003366",
        state="normal" if comando2 else "disabled"
    )
    perfil_btn.pack(fill="x", pady=3)
    botoes_menu_perfil.append(perfil_btn)

    print(f"DEBUG: Botão '{texto_botao}' - Comando: {'Ativo' if comando2 else 'Desativado (None)'}")
    
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

# Arquivo MAIN para testar
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1200x700")
    app.title("Sistema Acadêmico - Menu Principal")
    app._set_appearance_mode("light")
    sidebar(app)
    
    app.mainloop()