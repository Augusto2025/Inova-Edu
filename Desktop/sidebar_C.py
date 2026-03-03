import customtkinter as ctk
from PIL import Image
import sys
import os
import importlib

# Tenta importar as cores, senão usa padrão
try:
    from assets.cores import *
except ImportError:
    azulEscuro = "#004A8D"
    azulClaro = "#419FFD"
    Branco = "#ecf0f1"

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, *, cor_fundo=azulEscuro, cor_texto=Branco):
        super().__init__(master, width=250, corner_radius=0, fg_color=cor_fundo)
        self.master = master # Aqui master é a HomeCoordenador
        self.cor_texto = cor_texto
        self._logo_img = None
        self.botoes = []
        
        # Identifica qual arquivo .py está rodando agora para desativar o botão da própria tela
        self.nome_arquivo_atual = os.path.basename(sys.argv[0])

        self.pack_propagate(False)
        self._build_ui()

    def _build_ui(self):
        self.menu_container = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_container.pack(fill="both", expand=True, padx=15, pady=20)

        # ================= TOPO (LOGO) =================
        self._add_logo(self.menu_container)
        
        ctk.CTkLabel(
            self.menu_container, 
            text="INOVA EDU",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.cor_texto
        ).pack(pady=(10, 0))

        ctk.CTkFrame(self.menu_container, height=2, fg_color=self.cor_texto).pack(fill="x", pady=10)

        ctk.CTkLabel(
            self.menu_container,
            text="MENU COORDENAÇÃO",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.cor_texto
        ).pack(pady=(5, 5))

        # ================= MENU (BOTÕES) =================
        self._criar_botoes_menu(self.menu_container)

        # ================= RODAPÉ =================
        # Logout embaixo
        self._criar_botao_sair(self.menu_container)

    def _add_logo(self, parent):
        try:
            caminho = "Desktop/assets/img/LOGOBRANCO.png"
            pil = Image.open(caminho)
            self._logo_img = ctk.CTkImage(light_image=pil, size=(80, 100))
            ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
        except:
            ctk.CTkLabel(parent, text="🎓", font=ctk.CTkFont(size=40)).pack()

    def _criar_botoes_menu(self, parent):
        # Mapeamento: Texto do Botão -> (Modulo, Nome da Classe)
        self.mapa_telas = {
            " Cadastrar Usuário": {"modulo": "cadastro_usuario", "classe": "CadastroUsuarios"},
            " Cadastrar Turmas":  {"modulo": "cadastro_turma",   "classe": "CadastroTurmas"},
            " Cadastrar Cursos":  {"modulo": "cadastro_curso",   "classe": "CadastroCursos"},
            " Listar Usuários":   {"modulo": "listausuario",    "classe": "ListaUsuariosApp"},
            " Listar Turmas":     {"modulo": "listaturma",      "classe": "ListaTurmasApp"},
            " Listar Cursos":     {"modulo": "listacurso",      "classe": "CursosView"},
        }

        for texto, config in self.mapa_telas.items():
            btn = ctk.CTkButton(
                parent, 
                text=texto, 
                height=45, 
                anchor="w",
                fg_color=azulClaro, 
                hover_color="#003366",
                text_color=self.cor_texto,
                command=lambda c=config: self._navegar(c),
                font=ctk.CTkFont(size=13),
                corner_radius=6
            )
            btn.pack(fill="x", pady=4)
            self.botoes.append(btn)

    def _navegar(self, config):
        try:
            # 1. Referência ao content_frame da HomeCoordenador
            # Como você usa 'self.sidebar_frame = sidebar(self)', 
            # o master aqui é o objeto HomeCoordenador.
            home_coordenador = self.master
            conteudo_central = home_coordenador.content_frame

            # 2. Limpar o conteúdo antigo (apaga a imagem ou a tela anterior)
            for widget in conteudo_central.winfo_children():
                widget.destroy()

            # 3. Importar e instanciar dinamicamente
            modulo = importlib.import_module(config["modulo"])
            importlib.reload(modulo) # Garante que carregue mudanças no arquivo
            classe_tela = getattr(modulo, config["classe"])
            
            # 4. Criar a nova tela dentro do content_frame
            nova_tela = classe_tela(conteudo_central)
            nova_tela.pack(fill="both", expand=True)

        except Exception as e:
            print(f"Erro ao navegar: {e}")

    def _criar_botao_sair(self, parent):
        ctk.CTkButton(
            parent, 
            text="Sair", 
            command=self.winfo_toplevel().destroy, # Fecha a janela toda
            height=45, 
            fg_color="#e74c3c", 
            hover_color="#c0392b",
            text_color=Branco, 
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        ).pack(side="bottom", fill="x", pady=(10, 0))

# Wrapper de compatibilidade
def sidebar(janela, cor_fundo=azulEscuro, cor_texto=Branco):
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    return sb, sb.botoes