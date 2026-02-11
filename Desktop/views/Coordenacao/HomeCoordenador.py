import customtkinter as ctk
from PIL import Image
import os
# =================
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *
from sidebar_C import sidebar





class HomeCoordenador(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # ================= CONFIGURAÇÃO GLOBAL =================
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # ================= MOSTRAR O FRAME =================
        self.pack(fill="both", expand=True)

        # ================= CONFIGURAÇÃO DA JANELA =================
        # self.master.title("Home - INOVA EDU")

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        largura = int(largura_tela * 0.9)
        altura = int(altura_tela * 0.9)
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        self.master.geometry(f"{largura}x{altura}+{x}+{y}")

        # ================= SIDEBAR (EXTERNO) =================
        retorno_sidebar = sidebar(self)

        # 🔹 Se o sidebar retornar tupla, pega só o frame
        if isinstance(retorno_sidebar, tuple):
            self.sidebar = retorno_sidebar[0]
        else:
            self.sidebar = retorno_sidebar

        self.sidebar.pack(side="left", fill="y")

        # ================= CONTEÚDO CENTRAL =================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # ================= ÁREA CENTRAL (LIVRE PRA IMAGEM) =================
        self.area_central = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.area_central.place(relx=0.5, rely=0.5, anchor="center")

        # ================= IMAGEM CENTRAL =================
        caminho_imagem = os.path.join("assets", "img", "LOGOAZUL.png")

        imagem = Image.open(caminho_imagem)

        img = ctk.CTkImage(
            light_image=imagem,
            size=(500, 550)  # ajuste se quiser a img
        )

        self.imagem_label = ctk.CTkLabel(
            self.area_central,
            image=img,
            text=""
        )
        self.imagem_label.pack()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x800")
    app = HomeCoordenador(root)
    root.mainloop()