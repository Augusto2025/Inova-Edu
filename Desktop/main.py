import customtkinter as ctk
from views.login_view import tela_login

class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1350x700")
        self.title("Sistema Acadêmico - INOVA EDU")

        self.login_screen = tela_login(self)
        self.login_screen.pack(expand=True, fill="both")


if __name__ == "__main__":
    # Inicia com a tela de perfil acadêmico
    app = main()
    app.mainloop()


# ------ Estou testando o login padronizado ------
# depois tu coloca alinhado com o meu login esse teu código abaixo

# from Desktop.menu_com_perfil import sidebar

# Para iniciar em uma tela específica, por exemplo:
# def iniciar_sistema(tela_inicial="perfil_academico"):
#     """Iniciar o sistema com a tela inicial especificada"""
#     ctk.set_appearance_mode("light")
    
#     if tela_inicial == "perfil_academico":
#         from perfil_academico import UserProfileSystem
#         app = UserProfileSystem()
#     elif tela_inicial == "home":
#         from Desktop.menu_com_perfil import Home
#         app = Home()
#     else:
#         # Tela padrão com menu lateral
#         app = ctk.CTk()
#         app.geometry("1350x700")
#         app.title("Sistema Acadêmico - INOVA EDU")
#         sidebar(app)
    
#     app.run()

# if __name__ == "__main__":
#     # Inicia com a tela de perfil acadêmico
#     iniciar_sistema("perfil_academico")