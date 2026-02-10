import customtkinter as ctk
from PIL import Image
from sidebar_C import sidebar


class HomeCoordenador(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # MOSTRAR O FRAME
        self.pack(fill="both", expand=True)

        # ================= CONFIGURAÇÃO GLOBAL =================
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # ================= CONFIGURAÇÃO DA JANELA =================
        self.master.title("Home - INOVA EDU")

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        largura = int(largura_tela * 0.9)
        altura = int(altura_tela * 0.9)
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        self.master.geometry(f"{largura}x{altura}+{x}+{y}")

        # ================= SIDEBAR (EXTERNO) =================
        self.sidebar = sidebar(self)
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
        imagem = Image.open("assets/img/LOGOAZUL.png")

        img = ctk.CTkImage(
            light_image=imagem,
            size=(420, 350)  # ajuste se quiser maior ou menor
        )

        self.imagem_label = ctk.CTkLabel(
            self.area_central,
            image=img,
            text=""
        )
        self.imagem_label.pack()
