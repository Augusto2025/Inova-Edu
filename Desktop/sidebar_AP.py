# sidebar_AP.py - VERSÃO SIMPLIFICADA SEM VERIFICAÇÃO DE run()
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
        
        # Ajustar sys.path para encontrar módulos MVC
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        self._build_ui()

    def _build_ui(self):
        """Constrói a interface da sidebar"""
        menu_container = ctk.CTkFrame(self, fg_color="transparent")
        menu_container.pack(fill="both", expand=True, padx=10, pady=20)

        # Logo
        self._add_logo(menu_container)

        # Título
        ctk.CTkLabel(
            menu_container,
            text="INOVA EDU",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.cor_texto
        ).pack()

        # Linha divisória
        ctk.CTkFrame(menu_container, height=2, fg_color=self.cor_texto).pack(fill="x", pady=5)

        # Subtítulo
        ctk.CTkLabel(
            menu_container,
            text="MENU LATERAL",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.cor_texto
        ).pack(pady=(15, 10))

        # Botões do menu
        self._criar_botoes_menu(menu_container)

        # Espaço flexível
        ctk.CTkLabel(menu_container, text="").pack(fill="both", expand=True)

        # Botão Perfil
        self._criar_botao_perfil(menu_container)

        # Botão Sair
        self._criar_botao_sair(menu_container)

    def _add_logo(self, parent):
        """Adiciona a logo"""
        try:
            pil = Image.open("Desktop/assets/LOGOBRANCO.png")
            self._logo_img = ctk.CTkImage(light_image=pil, size=(80, 100))
            ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
        except Exception:
            ctk.CTkLabel(parent, text="LOGO", font=ctk.CTkFont(size=22)).pack()

    def _criar_botoes_menu(self, parent):
        """Cria os botões principais do menu"""
        botoes = [
            ("Repositório", "home"),
            ("Fórum", "forum"),
            ("Eventos", "eventos"),
        ]

        for texto, tela in botoes:
            btn = ctk.CTkButton(
                parent,
                text=texto,
                height=50,
                anchor="w",
                text_color=self.cor_texto,
                command=lambda t=tela: self._abrir_tela(t),
                font=ctk.CTkFont(size=14),
                corner_radius=5,
                border_width=0,
                fg_color=azulClaro,
                hover_color=azulEscuro,
            )
            btn.pack(fill="x", pady=3)

    def _criar_botao_perfil(self, parent):
        """Cria botão do perfil"""
        btn = ctk.CTkButton(
            parent,
            text="Perfil",
            height=50,
            anchor="w",
            text_color=self.cor_texto,
            command=lambda: self._abrir_tela("perfil"),
            font=ctk.CTkFont(size=14),
            corner_radius=5,
            border_width=0,
            fg_color=azulClaro,
            hover_color=azulEscuro,
        )
        btn.pack(fill="x", pady=3)

    def _criar_botao_sair(self, parent):
        """Cria botão de sair"""
        ctk.CTkButton(
            parent,
            text="Logout",
            command=self.master.quit,
            height=45,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color=self.cor_texto,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        ).pack(side="bottom", fill="x", pady=(0, 5))

    def _abrir_tela(self, nome_tela):
        """Abre uma tela - SEM VERIFICAÇÃO DE run(), APENAS INSTANCIA DIRETAMENTE"""
        print(f"Abrindo tela: {nome_tela}")
        
        # Mapa das telas
        mapa_telas = {
            "home": {
                "modulo": "views.Aluno_e_Professor.home_view",
                "classe": "Home"
            },
            "eventos": {
                "modulo": "views.Aluno_e_Professor.eventos_view",
                "classe": "CalendarioDesktopApp"
            },
            "forum": {
                "modulo": "cadastro_usuario",
                "classe": "CadastroUsuarios"
            },
            "perfil": {
                "modulo": "perfil_academico",
                "classe": "UserProfileSystem"
            }
        }
        
        if nome_tela not in mapa_telas:
            print(f"Erro: Tela '{nome_tela}' não encontrada")
            return
        
        config = mapa_telas[nome_tela]
        
        # Fechar janela atual
        self.master.destroy()
        
        # Criar nova janela
        nova_janela = ctk.CTk()
        nova_janela.title(f"INOVA EDU - {nome_tela.title()}")
        nova_janela.geometry("1350x700")
        nova_janela.attributes("-fullscreen", True)
        
        try:
            # Importar módulo
            mod = importlib.import_module(config["modulo"])
            
            # Obter classe
            cls = getattr(mod, config["classe"])
            
            # INSTANCIAR DIRETAMENTE - SEM VERIFICAR run()
            print(f"Instanciando {config['classe']} diretamente")
            tela_frame = cls(nova_janela)
            
            # O frame já se empacota no __init__, então só iniciar mainloop
            nova_janela.mainloop()
            
        except ImportError as e:
            print(f"ERRO: Não foi possível importar {config['modulo']}")
            print(f"Path: {sys.path}")
            print(f"Erro: {e}")
        except AttributeError as e:
            print(f"ERRO: Classe {config['classe']} não encontrada em {config['modulo']}")
            print(f"Erro: {e}")
        except Exception as e:
            print(f"ERRO ao abrir {nome_tela}: {e}")
            import traceback
            traceback.print_exc()

# Função de compatibilidade
def sidebar(janela, cor_fundo=azulEscuro, cor_texto=Branco):
    """
    Mantém compatibilidade:
        sidebar_instance, _ = sidebar(janela_principal)
    """
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    sb.pack(side="left", fill="y")
    return sb, []