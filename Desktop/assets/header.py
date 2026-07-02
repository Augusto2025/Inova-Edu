# components/header.py
import customtkinter as ctk

# Importe aqui o seu arquivo onde estão declaradas as suas cores.
# Exemplo: de config.assets_cores importe todas, ou apenas garanta que elas estejam acessíveis.
from assets.cores import azulEscuro, AzulHover, Branco 

class HeaderPadrao(ctk.CTkFrame):
    def __init__(self, master, titulo, comando_voltar=None, **kwargs):
        """
        Asset de Header de linha única.
        :param master: A tela/frame atual (geralmente 'self')
        :param titulo: O nome da tela que vai aparecer escrito
        :param comando_voltar: A função da tela de onde você veio (ex: self.voltar_perfil)
        """
        super().__init__(master, fg_color=azulEscuro, height=100, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.pack(fill="x", side="top")

        # Nome da tela (Lado Esquerdo)
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text=titulo, 
            font=("Roboto", 28, "bold"), 
            text_color=Branco
        )
        self.lbl_titulo.pack(side="left", padx=30)

        # Botão de Voltar para a tela anterior (Lado Direito)
        if comando_voltar:
            self.btn_voltar = ctk.CTkButton(
                self, 
                text="Voltar", 
                width=100, 
                height=32,
                fg_color="transparent", 
                border_width=2, 
                border_color=Branco,
                hover_color=AzulHover,
                text_color=Branco,
                font=("Roboto", 12, "bold"),
                command=comando_voltar
            )
            self.btn_voltar.pack(side="right", padx=30)