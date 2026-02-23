import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sidebar_AP import sidebar
from views.forum_view import ForumView

# Criar janela
app = ctk.CTk()
app.geometry("1200x750")
app.title("Teste do Fórum")

# Sidebar
sidebar_instance, botoes = sidebar(app)

# Área principal
main_area = ctk.CTkFrame(app, fg_color="white")
main_area.pack(side="left", fill="both", expand=True)

# Fórum
forum = ForumView(main_area)
forum.run()

app.mainloop()