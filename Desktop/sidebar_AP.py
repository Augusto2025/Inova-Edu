import customtkinter as ctk
from PIL import Image
import sys
import os
import importlib
from assets.cores import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, *, cor_fundo=azulEscuro, cor_texto=Branco):
        # Aumentada a largura levemente para melhor equilíbrio visual
        super().__init__(master, width=280, corner_radius=0, fg_color=cor_fundo)
        self.master = master
        self.cor_texto = cor_texto
        self._logo_img = None
        
        # Definição de Fontes Modernas
        self.fonte_principal = ctk.CTkFont(family="Segoe UI", size=16, weight="normal")
        self.fonte_bold = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.fonte_titulo = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        self.pack_propagate(False) 
        self._build_ui()

    def _build_ui(self):
        # Container com margens generosas para um ar "limpo"
        self.menu_container = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_container.pack(fill="both", expand=True, padx=20, pady=30)

        # Seção Superior (Logo e Título)
        self._add_logo(self.menu_container)
        
        ctk.CTkLabel(
            self.menu_container, 
            text="INOVA EDU",
            font=self.fonte_titulo,
            text_color=self.cor_texto
        ).pack(pady=(15, 25))

        # Divisor Elegante (Linha fina com baixa opacidade)
        ctk.CTkFrame(self.menu_container, height=1, fg_color="#334155").pack(fill="x", pady=(0, 25))

        # --- Rodapé (Ordem inversa para o pack side="bottom") ---
        self._criar_botao_sair(self.menu_container)
        self._criar_botao_perfil(self.menu_container)

        # --- Menu Principal ---
        self._criar_botoes_menu(self.menu_container)

    def _add_logo(self, parent):
        try:
            caminho = resource_path(os.path.join("assets", "img", "LOGOBRANCO.png"))
            pil = Image.open(caminho)
            self._logo_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(100, 120))
            ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
        except Exception as e:
            ctk.CTkLabel(parent, text="🎓", font=ctk.CTkFont(size=55)).pack()

    def _criar_botoes_menu(self, parent):
        botoes = [
            ("🏠   Repositório", "home"),
            ("💬   Fórum", "forum"),
            ("📅   Eventos", "eventos"),
        ]
        for texto, id_tela in botoes:
            btn = ctk.CTkButton(
                parent, 
                text=texto, 
                height=55, # Altura uniforme e maior
                anchor="w",
                font=self.fonte_principal,
                fg_color="transparent", # Visual limpo, ganha cor no hover
                hover_color=azulClaro,
                text_color=self.cor_texto,
                corner_radius=12,
                border_spacing=20, # Texto mais afastado da borda
                command=lambda t=id_tela: self._navegar(t)
            )
            btn.pack(fill="x", pady=6)

    def _criar_botao_perfil(self, parent):
        ctk.CTkButton(
            parent, 
            text="👤   Meu Perfil", 
            height=55, 
            anchor="w",
            font=self.fonte_principal,
            fg_color="transparent",
            hover_color=azulClaro,
            text_color=self.cor_texto,
            corner_radius=12,
            border_spacing=20,
            command=lambda: self._navegar("perfil")
        ).pack(side="bottom", fill="x", pady=(0, 20))

    def _criar_botao_sair(self, parent):
        # Estilo "Danger" moderno (Soft Red)
        ctk.CTkButton(
            parent, 
            text="Sair do Sistema", 
            command=self.master.quit,
            height=52, 
            fg_color="#ef4444", # Vermelho vibrante moderno
            hover_color="#b91c1c",
            text_color="#ffffff", 
            font=self.fonte_bold,
            corner_radius=15 # Bem arredondado para destacar como ação final
        ).pack(side="bottom", fill="x")

    def _navegar(self, nome_tela):
        for widget in self.master.winfo_children():
            if widget != self:
                widget.destroy()

        mapa_telas = {
            "home": {"modulo": "views.Aluno_e_Professor.home_view", "classe": "Home"},
            "eventos": {"modulo": "views.Aluno_e_Professor.eventos_view", "classe": "CalendarioDesktopApp"},
            "forum": {"modulo": "views.Aluno_e_Professor.forum_view", "classe": "Forum"},
            "perfil": {"modulo": "perfil_academico", "classe": "UserProfileSystem"}
        }
        
        if nome_tela not in mapa_telas:
            return

        config = mapa_telas[nome_tela]
        try:
            mod = importlib.import_module(config["modulo"])
            importlib.reload(mod)
            cls = getattr(mod, config["classe"])
            nova_tela = cls(self.master)
            nova_tela.pack(side="right", fill="both", expand=True)
        except Exception as e:
            print(f"Erro ao carregar tela {nome_tela}: {e}")

def sidebar(janela, cor_fundo=azulEscuro, cor_texto=Branco):
# >>>>>>> develop
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    sb.pack(side="left", fill="y")
    return sb, []