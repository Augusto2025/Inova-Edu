import customtkinter as ctk
from PIL import Image
import os



class HomeCoordenador(ctk.CTk):
    def __init__(self, master):
        super().__init__(master)

        # ================= CONFIGURAÇÃO GLOBAL =================
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        
        
        self.title("Home - INOVA EDU")

        # Tamanho da tela
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        largura = int(largura_tela * 0.9)
        altura = int(altura_tela * 0.9)
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # ================= SIDEBAR =================
        self.menu_frame = ctk.CTkFrame(self, width=250, fg_color="#004A8D", corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")

        self.menu_container = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.menu_container.pack(fill="both", expand=True, padx=10, pady=20)

        # Logo
        self._logo_sidebar()

        ctk.CTkLabel(
            self.menu_container,
            text="INOVA EDU",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        ).pack(pady=(5, 10))

        ctk.CTkFrame(self.menu_container, height=2, fg_color="white").pack(fill="x", pady=10)

        ctk.CTkLabel(
            self.menu_container,
            text="MENU",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=(10, 10))

        # Botões do menu
        self._botoes_menu()

        ctk.CTkLabel(self.menu_container, text="").pack(expand=True)

        ctk.CTkButton(
            self.menu_container,
            text="Sair",
            command=self.destroy,
            height=45,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        ).pack(fill="x", pady=(0, 5))

        # ================= CONTEÚDO CENTRAL =================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self._logo_central(largura, altura)

        self.mensagem_label = ctk.CTkLabel(
            self.content_frame,
            text="Clique em uma opção do menu para começar",
            font=ctk.CTkFont(size=20),
            text_color="#666666"
        )
        self.mensagem_label.place(relx=0.5, rely=0.7, anchor="center")

    # ================= MÉTODOS =================

    def _logo_sidebar(self):
        try:
            imagem = Image.open("LOGOBRANCO.png")
            logo_img = ctk.CTkImage(light_image=imagem, size=(80, 100))
            ctk.CTkLabel(self.menu_container, image=logo_img, text="").pack()
        except:
            ctk.CTkLabel(
                self.menu_container,
                text="LOGO",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="white"
            ).pack()

    def _logo_central(self, largura, altura):
        try:
            imagem = Image.open("LOGOBRANCO.png")
            tamanho = min(int(largura * 0.35), int(altura * 0.5))
            logo_img = ctk.CTkImage(
                light_image=imagem,
                size=(tamanho, int(tamanho * 1.25))
            )
            self.logo_label = ctk.CTkLabel(self.content_frame, image=logo_img, text="")
        except:
            self.logo_label = ctk.CTkLabel(
                self.content_frame,
                text="INOVA\nEDU",
                font=ctk.CTkFont(size=100, weight="bold"),
                text_color="#004A8D",
                justify="center"
            )

        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

    def _botoes_menu(self):
        opcoes = {
            "Cadastrar Usuário": self.abrir_cadastro_usuario,
            "Cadastrar Turmas": self.abrir_cadastro_turma,
            "Cadastrar Cursos": self.abrir_cadastro_curso,
            "Listar Usuários": self.abrir_lista_usuario,
            "Listar Turmas": self.abrir_lista_turma,
            "Listar Cursos": self.abrir_lista_curso,
        }

        for texto, comando in opcoes.items():
            btn = ctk.CTkButton(
                self.menu_container,
                text=" " + texto,
                height=45,
                anchor="w",
                command=comando,
                fg_color="#419FFD",
                hover_color="#003366",
                text_color="white",
                font=ctk.CTkFont(size=14),
                corner_radius=6
            )
            btn.pack(fill="x", pady=4)

    # ================= NAVEGAÇÃO =================

    def _limpar_tela(self):
        self.logo_label.place_forget()
        self.mensagem_label.place_forget()

    def abrir_cadastro_usuario(self):
        self._limpar_tela()
        from cadastro_usuario import CadastroUsuarios
        CadastroUsuarios()

    def abrir_cadastro_turma(self):
        self._limpar_tela()
        from cadastro_turma import CadastroTurmas
        CadastroTurmas()

    def abrir_cadastro_curso(self):
        self._limpar_tela()
        from cadastro_curso import CadastroCursos
        CadastroCursos()

    def abrir_lista_usuario(self):
        self._limpar_tela()
        from listausuario import ListaUsuarios
        ListaUsuarios()

    def abrir_lista_turma(self):
        self._limpar_tela()
        from listaturma import ListaTurmas
        ListaTurmas()

    def abrir_lista_curso(self):
        self._limpar_tela()
        from listacurso import ListaCursos
        ListaCursos()


# if __name__ == "__main__":
#     app = HomeCoordenador()
#     app.mainloop()
