import customtkinter as ctk
from PIL import Image
import sys
import os

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
        self.master = master
        self.cor_texto = cor_texto
        self._logo_img = None
        self.botoes = []  # Lista para armazenar os objetos dos botões
        
        # Identifica qual arquivo .py está rodando agora
        self.nome_arquivo_atual = os.path.basename(sys.argv[0])
        print(f"DEBUG: Tela atual -> {self.nome_arquivo_atual}")

        # Carrega as classes das outras telas
        self.classes_telas = self._importar_classes()

        self.pack_propagate(False)
        self._build_ui()

    def _importar_classes(self):
        """Lógica de importação trazida da primeira sidebar"""
        try:
            try:
                from cadastro_usuario import CadastroUsuarios
                from cadastro_turma import CadastroTurmas
                from cadastro_curso import CadastroCursos
                from listausuario import ListaUsuariosApp
                from listaturma import ListaTurmasApp
                from listacurso import CursosView
                
                return {
                    "cadastro_usuario.py": CadastroUsuarios,
                    "cadastro_turma.py": CadastroTurmas,
                    "cadastro_curso.py": CadastroCursos,
                    "listausuario.py": ListaUsuariosApp,
                    "listaturma.py": ListaTurmasApp,
                    "listacurso.py": CursosView,
                }
            except ImportError:
                return {}
        except Exception as e:
            print(f"Erro ao importar classes: {e}")
            return {}

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
            text="MENU LATERAL",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.cor_texto
        ).pack(pady=(5, 5))

        # ================= MENU (BOTÕES) =================
        self._criar_botoes_menu(self.menu_container)

        # ================= RODAPÉ =================
        ctk.CTkLabel(self.menu_container, text="").pack(expand=True)
        self._criar_botao_sair(self.menu_container)

    def _add_logo(self, parent):
        try:
            caminho = "Desktop/assets/img/LOGOBRANCO.png"
            pil = Image.open(caminho)
            self._logo_img = ctk.CTkImage(light_image=pil, size=(80, 100))
            ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
        except:
            ctk.CTkLabel(
                parent, 
                text="LOGO", 
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=self.cor_texto
            ).pack()

    def _criar_botoes_menu(self, parent):
        opcoes_menu = {
            " Cadastrar Usuário": "cadastro_usuario.py",
            " Cadastrar Turmas": "cadastro_turma.py",
            " Cadastrar Cursos": "cadastro_curso.py",
            " Listar Usuários": "listausuario.py",
            " Listar Turmas": "listaturma.py",
            " Listar Cursos": "listacurso.py",
        }

        self.botoes = [] # Limpa lista antes de criar

        for texto, arquivo_alvo in opcoes_menu.items():
            
            estado = "normal"
            comando = lambda a=arquivo_alvo: self._navegar(a)
            
            # Lógica de bloqueio do botão atual
            if self.nome_arquivo_atual == arquivo_alvo:
                estado = "disabled"
                comando = None
            elif arquivo_alvo not in self.classes_telas:
                estado = "disabled" 

            btn = ctk.CTkButton(
                parent, 
                text=texto, 
                height=45, 
                anchor="w",
                fg_color=azulClaro, 
                hover_color="#003366",
                text_color=self.cor_texto,
                state=estado,
                command=comando,
                font=ctk.CTkFont(size=14),
                corner_radius=6
            )
            btn.pack(fill="x", pady=4)
            self.botoes.append(btn) # Adiciona à lista que será retornada

    def _navegar(self, arquivo_alvo):
        classe_destino = self.classes_telas.get(arquivo_alvo)
        if classe_destino:
            # Importante: Interrompe loops do CTk antes de destruir para evitar "invalid command"
            self.master.quit() 
            self.master.destroy()
            classe_destino().run()
        else:
            print(f"Classe para {arquivo_alvo} não encontrada.")

    def _criar_botao_sair(self, parent):
        ctk.CTkButton(
            parent, 
            text="Logout", 
            command=self.master.destroy,
            height=45, 
            fg_color="#e74c3c", 
            hover_color="#c0392b",
            text_color=self.cor_texto, 
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        ).pack(side="bottom", fill="x", pady=(0, 5))

# ================= WRAPPER DE COMPATIBILIDADE =================
def sidebar(janela, cor_fundo=azulEscuro, cor_texto=Branco):
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    sb.pack(side="left", fill="y")
    
    # CORREÇÃO PRINCIPAL: Retorna o objeto Frame E a lista de botões
    # Isso satisfaz a chamada: self.sidebar_frame, self.botoes_menu = sidebar(...)
    return sb, sb.botoes 

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.geometry("1200x700")
    sidebar(app)
    app.mainloop()