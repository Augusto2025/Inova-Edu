# sidebar_oo.py
import customtkinter as ctk
from PIL import Image
import sys
import os
import importlib
from assets.cores import *


class Sidebar(ctk.CTkFrame):
    """
    Sidebar orientado a objetos para CustomTkinter.

    Uso na Home (sem mudar sua lógica):
        from sidebar_oo import sidebar
        sidebar(self.janela)

    Regras:
      - Mapeia as outras telas e tenta primeiro `app.run()` do módulo.
      - Se não houver `app.run()`, tenta `Classe().run()` (fallback).
      - Corrigido "enventos.py" -> "eventos.py".
      - Botão "Repositório" (Home) fica desativado, como no seu fluxo.
    """

    def __init__(self, master, *, cor_fundo=azulEscuro, cor_texto=Branco):
        super().__init__(master, width=250, corner_radius=0, fg_color=cor_fundo)
        self.master = master
        self.cor_texto = cor_texto
        self._logo_img = None
        self._botoes = []

        # Nome do arquivo principal executado (compat com sua lógica antiga)
        self._arquivo_atual = os.path.basename(sys.argv[0])
        print(f"DEBUG: Arquivo atual: {self._arquivo_atual}")

        self._build_ui()

    # ------------------- UI -------------------
    def _build_ui(self):
        menu_container = ctk.CTkFrame(self, fg_color="transparent")
        menu_container.pack(fill="both", expand=True, padx=10, pady=20)

        self._add_logo(menu_container)

        ctk.CTkLabel(
            menu_container,
            text="INOVA EDU",
            font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
            text_color=self.cor_texto
        ).pack()

        ctk.CTkFrame(menu_container, height=2, fg_color=self.cor_texto).pack(fill="x", pady=5)

        ctk.CTkLabel(
            menu_container,
            text="MENU LATERAL",
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            text_color=self.cor_texto
        ).pack(pady=(15, 10))

        opcoes_menu = {
            " Repositório": ("home.py", "Home"),
            " Fórum": ("cadastro_usuario.py", "Cadastro de Usuários"),
            " Eventos": ("eventos.py", "Calendário de Eventos"),  # corrigido
        }

        for texto_botao, (arquivo_alvo, nome_tela) in opcoes_menu.items():
            comando = self._detectar_tela(arquivo_alvo, nome_tela)
            btn = ctk.CTkButton(
                menu_container,
                text=texto_botao,
                height=50,
                anchor="w",
                text_color=self.cor_texto,
                command=comando if comando else (lambda: None),
                font=ctk.CTkFont(size=14, family="Arial"),
                corner_radius=5,
                border_width=0,
                fg_color=f"{azulClaro}",
                hover_color=f"{azulEscuro}",
                state="normal" if comando else "disabled"
            )
            btn.pack(fill="x", pady=3)
            self._botoes.append(btn)
            print(f"DEBUG: Botão '{texto_botao}' - Comando: {'Ativo' if comando else 'Desativado (None)'}")

        # Espaço flexível
        ctk.CTkLabel(menu_container, text="").pack(fill="both", expand=True)

        # Perfil (parte de baixo)
        texto_botao = " Perfil"
        arquivo_alvo, nome_tela = "perfil_academico.py", "Perfil do Usuário"
        comando2 = self._detectar_tela(arquivo_alvo, nome_tela)

        perfil_btn = ctk.CTkButton(
            menu_container,
            text="Perfil",
            height=50,
            anchor="w",
            text_color=self.cor_texto,
            command=comando2 if comando2 else (lambda: None),
            font=ctk.CTkFont(size=14, family="Arial"),
            corner_radius=5,
            border_width=0,
            fg_color=f"{azulClaro}",
            hover_color=f"{azulEscuro}",
            state="normal" if comando2 else "disabled"
        )
        perfil_btn.pack(fill="x", pady=3)
        self._botoes.append(perfil_btn)
        print(f"DEBUG: Botão '{texto_botao}' - Comando: {'Ativo' if comando2 else 'Desativado (None)'}")

        # Sair
        ctk.CTkButton(
            menu_container,
            text="Logout",
            command=self.master.quit,
            height=45,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color=self.cor_texto,
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            corner_radius=8
        ).pack(side="bottom", fill="x", pady=(0, 5))

    def _add_logo(self, parent):
        try:
            pil = Image.open("Desktop/assets/LOGOBRANCO.png")
            self._logo_img = ctk.CTkImage(light_image=pil, size=(80, 100))
            ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
        except Exception:
            ctk.CTkLabel(parent, text="LOGO", font=ctk.CTkFont(size=22)).pack()

    # ------------------- Navegação -------------------
    def _detectar_tela(self, arquivo_alvo: str, nome_exibicao: str):
        # Sidebar aparece só na Home → botão "Repositório" desativado
        if arquivo_alvo == "home.py":
            print("DEBUG: Estamos na Home - botão Repositório desativado")
            return None

        # (REMOVIDO) Não desativar botão apenas porque o arquivo atual é o mesmo

        def navegar():
            print(f"DEBUG: Navegando para {arquivo_alvo}")
            self._fechar_janela()
            self._abrir_destino(arquivo_alvo)

        return navegar

    def _fechar_janela(self):
        toplevel = self.winfo_toplevel()
        try:
            toplevel.destroy()
        except Exception:
            try:
                toplevel.quit()
            except Exception:
                pass

    def _abrir_destino(self, arquivo_alvo: str):
        mapa = {
            "cadastro_usuario.py": {
                "module": "cadastro_usuario",
                "class": "CadastroUsuarios"
            },
            "eventos.py": {  # corrigido
                "module": "views.Aluno_e_Professor.eventos",
                "class": "CalendarioDesktopApp"
            },
            "perfil_academico.py": {
                "module": "perfil_academico",
                "class": "UserProfileSystem"
            }
        }

        alvo = mapa.get(arquivo_alvo)
        if not alvo:
            print(f"DEBUG: Destino '{arquivo_alvo}' não mapeado.")
            return

        mod_name = alvo["module"]
        cls_name = alvo["class"]

        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:
            print(f"DEBUG: Falha ao importar módulo '{mod_name}': {e}")
            return

        # 1) Tenta app.run()
        app = getattr(mod, "app", None)
        if app and hasattr(app, "run") and callable(app.run):
            try:
                app.run()
                return
            except Exception as e:
                print(f"DEBUG: Erro ao chamar app.run() de '{mod_name}': {e}")

        # 2) Tenta Classe().run()
        cls = getattr(mod, cls_name, None)
        if cls:
            try:
                inst = cls()
                if hasattr(inst, "run") and callable(inst.run):
                    inst.run()
                    return
                else:
                    print(f"DEBUG: Classe '{cls_name}' não possui método run().")
            except Exception as e:
                print(f"DEBUG: Erro ao instanciar/chamar '{cls_name}': {e}")

        print(f"DEBUG: Não foi possível abrir destino '{arquivo_alvo}'.")

    @property
    def botoes(self):
        return list(self._botoes)


# -------- Adaptador com a MESMA assinatura que você usa na Home --------
def sidebar(janela, cor_fundo=f"{azulEscuro}", cor_texto=f"{Branco}"):
    """
    Mantém compatibilidade com:
        sidebar(self.janela)
    Retorna (sidebar_instance, botoes)
    """
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    sb.pack(side="left", fill="y")
    return sb, sb.botoes