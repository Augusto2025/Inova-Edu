import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Inova Edu")
app.geometry("1000x600")

# --------- Funções ---------

def limpar_tela():
    for widget in app.winfo_children():
        widget.destroy()

# --------- Telas ---------



app.mainloop()