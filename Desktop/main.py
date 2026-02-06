import customtkinter as ctk
from views.login_view import tela_login

ctk.set_appearance_mode("light")
class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("1350x700")
        self.title("Sistema Acadêmico - INOVA EDU")
        self.attributes("-fullscreen", True)

        self.login_screen = tela_login(self)
        self.login_screen.pack(expand=True, fill="both")


if __name__ == "__main__":
    # Inicia com a tela de perfil acadêmico
    app = main()
    app.mainloop()