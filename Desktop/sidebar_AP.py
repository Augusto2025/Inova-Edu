import customtkinter as ctk
from sidebar_C import sidebar

if __name__ == "__main__":

    app = ctk.CTk()
    app._set_appearance_mode("dark")
    app.geometry("1200x600")
    app.title("Teste de tela")

    sidebar(app)
    app.mainloop()