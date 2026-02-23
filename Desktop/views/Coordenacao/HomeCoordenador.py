import customtkinter as ctk
from PIL import Image
import os
import sys

# Ajuste de Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class HomeCoordenador(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.janela = master

        from sidebar_C import Sidebar, sidebar
        
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break

        if not sidebar_existente:
            sidebar_existente, _ = sidebar(self.janela)
        
        self.pack(fill="both", expand=True)

        # ================= SIDEBAR =================
        # Passamos 'self' (a Home) como master da sidebar
        self.sidebar_frame, self.botoes_menu = sidebar(self)
        self.sidebar_frame.pack(side="left", fill="y")

        # ================= CONTEÚDO CENTRAL (O PAINEL QUE MUDA) =================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Chamamos a tela inicial (o logo)
        self.mostrar_tela_inicial()

    def mostrar_tela_inicial(self):
        """Limpa o conteúdo e mostra o logo azul"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.area_central = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.area_central.place(relx=0.5, rely=0.5, anchor="center")

        try:
            caminho_imagem = "Desktop/assets/img/LOGOAZUL.png"
            imagem = Image.open(caminho_imagem)
            img = ctk.CTkImage(light_image=imagem, size=(500, 550))
            self.imagem_label = ctk.CTkLabel(self.area_central, image=img, text="")
            self.imagem_label.pack()
        except:
            ctk.CTkLabel(self.area_central, text="INOVA EDU", font=("Arial", 40)).pack()

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x800")
    app = HomeCoordenador(root)
    root.mainloop()