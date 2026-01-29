import customtkinter as ctk
from sidebar_C import sidebar

if __name__ == "__main__":

    app = ctk.CTk()
    app._set_appearance_mode("dark")
    app.geometry("1200x600")
    app.title("Teste de tela")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    sidebar(app)
    app.mainloop()