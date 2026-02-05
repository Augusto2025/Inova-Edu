import customtkinter as ctk
from PIL import Image
import sys
import os

def home_tela_grande_simples():
    # Configurar janela
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    janela = ctk.CTk()
    
    # Pegar tamanho da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    # Usar 90% da tela
    largura = int(largura_tela * 0.9)
    altura = int(altura_tela * 0.9)
    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2
    
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.title("Home - INOVA EDU")
    
    # ==================== SIDEBAR (baseada na sua) ====================
    janela_global = janela
    
    def importar_classes():
        try:
            from cadastro_usuario import CadastroUsuarios
            from cadastro_turma import CadastroTurmas
            from cadastro_curso import CadastroCursos
            from listausuario import ListaUsuarios
            from listaturma import ListaTurmas
            from listacurso import ListaCursos
            return (CadastroUsuarios, CadastroTurmas, CadastroCursos,
                    ListaUsuarios, ListaTurmas, ListaCursos)
        except:
            class Mock:
                def run(self):
                    print("Tela não encontrada")
            return Mock, Mock, Mock, Mock, Mock, Mock
    
    def navegar_para(arquivo):
        (CadastroUsuarios, CadastroTurmas, CadastroCursos,
         ListaUsuarios, ListaTurmas, ListaCursos) = importar_classes()
        
        mapeamento = {
            "cadastro_usuario.py": CadastroUsuarios,
            "cadastro_turma.py": CadastroTurmas,
            "cadastro_curso.py": CadastroCursos,
            "listausuario.py": ListaUsuarios,
            "listaturma.py": ListaTurmas,
            "listacurso.py": ListaCursos,
        }
        
        classe = mapeamento.get(arquivo)
        if classe:
            def acao():
                # Esconder logo
                if hasattr(janela, 'logo_label'):
                    janela.logo_label.place_forget()
                    if hasattr(janela, 'mensagem_label'):
                        janela.mensagem_label.place_forget()
                
                # Fechar esta janela e abrir a nova
                janela.destroy()
                nova_janela = classe()
                
                # Configurar nova janela também grande
                try:
                    nova_janela_root = nova_janela.root if hasattr(nova_janela, 'root') else nova_janela
                    nova_largura = int(largura_tela * 0.9)
                    nova_altura = int(altura_tela * 0.9)
                    nova_x = (largura_tela - nova_largura) // 2
                    nova_y = (altura_tela - nova_altura) // 2
                    nova_janela_root.geometry(f"{nova_largura}x{nova_altura}+{nova_x}+{nova_y}")
                except:
                    pass
                
                nova_janela.run()
            return acao
        return None
    
    # Sidebar
    menu_frame = ctk.CTkFrame(janela, width=250, fg_color="#004A8D", corner_radius=0)
    menu_frame.pack(side="left", fill="y")
    
    menu_container = ctk.CTkFrame(menu_frame, fg_color="transparent")
    menu_container.pack(fill="both", expand=True, padx=10, pady=20)
    
    # Logo na sidebar
    try:
        imagem = Image.open("LOGOBRANCO.png")
        logo_img = ctk.CTkImage(light_image=imagem, size=(80, 100))
        ctk.CTkLabel(menu_container, image=logo_img, text="").pack()
    except:
        ctk.CTkLabel(menu_container, text="LOGO", font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack()
    
    ctk.CTkLabel(menu_container, text="INOVA EDU", font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(pady=(5,10))
    ctk.CTkFrame(menu_container, height=2, fg_color="white").pack(fill="x", pady=10)
    ctk.CTkLabel(menu_container, text="MENU", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(pady=(10,10))
    
    # Botões
    opcoes = {
        " Cadastrar Usuário": "cadastro_usuario.py",
        " Cadastrar Turmas": "cadastro_turma.py",
        " Cadastrar Cursos": "cadastro_curso.py",
        " Listar Usuários": "listausuario.py",
        " Listar Turmas": "listaturma.py",
        " Listar Cursos": "listacurso.py",
    }
    
    for texto, arquivo in opcoes.items():
        cmd = navegar_para(arquivo)
        btn = ctk.CTkButton(
            menu_container,
            text=texto,
            height=45,
            anchor="w",
            command=cmd,
            fg_color="#419FFD",
            hover_color="#003366",
            text_color="white",
            font=ctk.CTkFont(size=14),
            corner_radius=6
        )
        btn.pack(fill="x", pady=4)
    
    ctk.CTkLabel(menu_container, text="").pack(expand=True)
    
    ctk.CTkButton(
        menu_container,
        text="Sair",
        command=janela.destroy,
        height=45,
        fg_color="#e74c3c",
        hover_color="#c0392b",
        text_color="white",
        font=ctk.CTkFont(size=14, weight="bold"),
        corner_radius=8
    ).pack(fill="x", pady=(0,5))
    
    # ==================== LOGO CENTRAL GRANDE ====================
    content_frame = ctk.CTkFrame(janela, fg_color="transparent")
    content_frame.pack(side="right", fill="both", expand=True)
    
    # Logo central (bem grande para tela grande)
    try:
        imagem = Image.open("LOGOBRANCO.png")
        logo_tamanho = min(int(largura * 0.35), int(altura * 0.5))
        logo_img = ctk.CTkImage(light_image=imagem, size=(logo_tamanho, int(logo_tamanho*1.25)))
        janela.logo_label = ctk.CTkLabel(content_frame, image=logo_img, text="")
    except:
        janela.logo_label = ctk.CTkLabel(
            content_frame,
            text="INOVA\nEDU",
            font=ctk.CTkFont(size=100, weight="bold"),
            text_color="#004A8D",
            justify="center"
        )
    
    janela.logo_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Mensagem
    janela.mensagem_label = ctk.CTkLabel(
        content_frame,
        text="Clique em uma opção do menu para começar",
        font=ctk.CTkFont(size=20),
        text_color="#666666"
    )
    janela.mensagem_label.place(relx=0.5, rely=0.7, anchor="center")
    
    return janela

if __name__ == "__main__":
    app = home_tela_grande_simples()
    app.mainloop()