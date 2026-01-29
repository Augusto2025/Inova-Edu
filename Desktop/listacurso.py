import customtkinter as ctk
from tkinter import messagebox
from sidebar_C import sidebar

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1200x600")
    app.title("Sistema de Gestão")
    
    # Configurar o sistema de grid
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)  # Coluna do conteúdo principal
    
    # Criar sidebar na coluna 0
    sidebar_frame, botoes_menu = sidebar(app)
    
    # Área de conteúdo principal (branca)
    conteudo_frame = ctk.CTkFrame(
        app, 
        fg_color="#ffffff",  # Branco
        corner_radius=0
    )
    conteudo_frame.grid(row=0, column=1, sticky="nsew")
    
    # Adicionar algum conteúdo à área branca
  
    
    app.mainloop()