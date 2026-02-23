import customtkinter as ctk
from PIL import Image
import sys
import os
import importlib
from assets.cores import *

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, *, cor_fundo=azulEscuro, cor_texto=Branco):
        super().__init__(master, width=250, corner_radius=0, fg_color=cor_fundo)
        self.master = master
        self.cor_texto = cor_texto
        self._logo_img = None
        self.pack_propagate(False) 
        self._build_ui()

    def _build_ui(self):
        self.menu_container = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_container.pack(fill="both", expand=True, padx=15, pady=20)

        # Topo
        self._add_logo(self.menu_container)
        ctk.CTkLabel(
            self.menu_container, text="INOVA EDU",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.cor_texto
        ).pack(pady=(10, 0))

        ctk.CTkFrame(self.menu_container, height=2, fg_color=self.cor_texto).pack(fill="x", pady=10)

        # Rodapé (Logout embaixo, Perfil logo acima)
        self._criar_botao_sair(self.menu_container)
        self._criar_botao_perfil(self.menu_container)

        # Meio (Menu principal)
        self._criar_botoes_menu(self.menu_container)

    def _add_logo(self, parent):
        try:
            caminho = "Desktop/assets/img/LOGOBRANCO.png"
            pil = Image.open(caminho)
            self._logo_img = ctk.CTkImage(light_image=pil, size=(80, 100))
            ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
        except:
            ctk.CTkLabel(parent, text="🎓", font=ctk.CTkFont(size=40)).pack()

    def _criar_botoes_menu(self, parent):
        botoes = [
            ("🏠 Repositório", "home"),
            ("💬 Fórum", "forum"),
            ("📅 Eventos", "eventos"),
        ]
        for texto, id_tela in botoes:
            ctk.CTkButton(
                parent, text=texto, height=50, anchor="w",
                fg_color=azulClaro, hover_color=azulEscuro,
                text_color=self.cor_texto,
                command=lambda t=id_tela: self._navegar(t)
            ).pack(fill="x", pady=3)

    def _criar_botao_perfil(self, parent):
        ctk.CTkButton(
            parent, text="👤 Perfil", height=50, anchor="w",
            fg_color=azulClaro, hover_color=azulEscuro,
            text_color=self.cor_texto,
            command=lambda: self._navegar("perfil")
        ).pack(side="bottom", fill="x", pady=(0, 10))

    def _criar_botao_sair(self, parent):
        ctk.CTkButton(
            parent, text="Logout", command=self.master.quit,
            height=45, fg_color="#e74c3c", hover_color="#c0392b",
            text_color=Branco, font=ctk.CTkFont(weight="bold"),
            corner_radius=8
        ).pack(side="bottom", fill="x")

    def _navegar(self, nome_tela):
        # 1. Limpa apenas as telas de conteúdo (quem não é a Sidebar)
        for widget in self.master.winfo_children():
            if widget != self:
                widget.destroy()

        mapa_telas = {
            "home": {"modulo": "views.Aluno_e_Professor.home_view", "classe": "Home"},
            "eventos": {"modulo": "views.Aluno_e_Professor.eventos_view", "classe": "CalendarioDesktopApp"},
            "forum": {"modulo": "views.Aluno_e_Professor.forum_view", "classe": "ForumApp"},
            "perfil": {"modulo": "perfil_academico", "classe": "UserProfileSystem"}
        }
        
        if nome_tela not in mapa_telas:
            return

        config = mapa_telas[nome_tela]
        try:
            # Import dinâmico para evitar erro circular
            mod = importlib.import_module(config["modulo"])
            importlib.reload(mod) # Opcional: garante que pegue mudanças no código
            cls = getattr(mod, config["classe"])
            
            # 2. Instancia a nova tela. 
            # IMPORTANTE: Passamos o self.master (a janela principal)
            nova_tela = cls(self.master)
            
            # 3. Empacota na DIREITA para não cobrir a sidebar
            nova_tela.pack(side="right", fill="both", expand=True)
            
        except Exception as e:
            print(f"Erro ao carregar tela {nome_tela}: {e}")

def sidebar(janela, cor_fundo=azulEscuro, cor_texto=Branco):
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    sb.pack(side="left", fill="y")
    return sb, []