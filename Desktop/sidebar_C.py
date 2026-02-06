import customtkinter as ctk
from PIL import Image
import sys
import os

# Variável global para controlar a janela atual
janela_global = None


def sidebar(janela, cor_fundo="#004A8D", cor_texto="#ecf0f1"):
    global janela_global
    janela_global = janela

    # ================= IMPORTAÇÃO DAS TELAS =================
    def importar_classes():
        try:
<<<<<<< HEAD
            from cadastro_usuario import CadastroUsuarios
            from cadastro_turma import CadastroTurmas
=======
            from cadastro_turma import CadastroTurmas
            from cadastro_usuario import CadastroUsuarios
>>>>>>> develop
            from cadastro_curso import CadastroCursos

            try:
                from listausuario import ListaUsuarios
                from listaturma import ListaTurmas
                from listacurso import ListaCursos
                return (
                    CadastroUsuarios,
                    CadastroTurmas,
                    CadastroCursos,
                    ListaUsuarios,
                    ListaTurmas,
                    ListaCursos,
                )
            except ImportError:
                return CadastroUsuarios, CadastroTurmas, CadastroCursos, None, None, None

        except ImportError:
            class MockClasse:
                def run(self):
                    print("Tela não encontrada")

            return MockClasse, MockClasse, MockClasse, MockClasse, MockClasse, MockClasse


    # ================= DETECTAR TELA ATUAL =================
    nome_arquivo = os.path.basename(sys.argv[0])
    print(f"DEBUG: Tela atual -> {nome_arquivo}")

    def detectar_tela(arquivo_alvo):
        if nome_arquivo == arquivo_alvo:
            return None

        (
            CadastroUsuarios,
            CadastroTurmas,
            CadastroCursos,
            ListaUsuarios,
            ListaTurmas,
            ListaCursos,
        ) = importar_classes()

        mapeamento = {
            "cadastro_usuario.py": CadastroUsuarios,
            "cadastro_turma.py": CadastroTurmas,
            "cadastro_curso.py": CadastroCursos,
            "listausuario.py": ListaUsuarios,
            "listaturma.py": ListaTurmas,
            "listacurso.py": ListaCursos,
        }

        classe = mapeamento.get(arquivo_alvo)
        if not classe:
            return None

        def navegar():
            global janela_global
            if janela_global:
                janela_global.destroy()
            classe().run()

        return navegar


    # ================= MENU LATERAL =================
    menu_frame = ctk.CTkFrame(
        janela,
        width=250,
        corner_radius=0,
        fg_color=cor_fundo
    )
    menu_frame.pack(side="left", fill="y")

    menu_container = ctk.CTkFrame(menu_frame, fg_color="transparent")
    menu_container.pack(fill="both", expand=True, padx=10, pady=20)

    # ================= LOGO =================
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        imagem_path = os.path.join(BASE_DIR, "LOGOBRANCO.png")

        imagem_pil = Image.open(imagem_path)
        imagem_ctk = ctk.CTkImage(light_image=imagem_pil, size=(80, 100))

        ctk.CTkLabel(menu_container, image=imagem_ctk, text="").pack()
    except:
        ctk.CTkLabel(
            menu_container,
            text="LOGO",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=cor_texto
        ).pack()

    ctk.CTkLabel(
        menu_container,
        text="INOVA EDU",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color=cor_texto
    ).pack(pady=(5, 10))

    ctk.CTkFrame(menu_container, height=2, fg_color=cor_texto).pack(fill="x", pady=10)

    ctk.CTkLabel(
        menu_container,
        text="MENU LATERAL",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=cor_texto
    ).pack(pady=(10, 10))

    # ================= BOTÕES =================
    opcoes_menu = {
        " Cadastrar Usuário": "cadastro_usuario.py",
        " Cadastrar Turmas": "cadastro_turma.py",
        " Cadastrar Cursos": "cadastro_curso.py",
        " Listar Usuários": "listausuario.py",
        " Listar Turmas": "listaturma.py",
        " Listar Cursos": "listacurso.py",
    }

    botoes_menu = []

    for texto, arquivo in opcoes_menu.items():
        comando = detectar_tela(arquivo)

        botao = ctk.CTkButton(
            menu_container,
            text=texto,
            height=45,
            anchor="w",
            text_color=cor_texto,
            command=comando,
            fg_color="#419FFD",
            hover_color="#003366",
            corner_radius=6,
            state="normal" if comando else "disabled",
            font=ctk.CTkFont(size=14)
        )
        botao.pack(fill="x", pady=4)
        botoes_menu.append(botao)

    # ================= ESPAÇO FLEXÍVEL =================
    ctk.CTkLabel(menu_container, text="").pack(expand=True)

    # ================= LOGOUT =================
    ctk.CTkButton(
        menu_container,
        text="Logout",
        command=janela.destroy,
        height=45,
        fg_color="#e74c3c",
        hover_color="#c0392b",
        text_color=cor_texto,
        font=ctk.CTkFont(size=14, weight="bold"),
        corner_radius=8
    ).pack(fill="x", pady=(0, 5))

    return menu_frame, botoes_menu


# ================= TESTE =================
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("1200x700")
    app.title("Sistema Acadêmico")

    sidebar(app)

    app.mainloop()