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
<<<<<<< HEAD
        self._botoes = []
        
        # Área principal para trocar o conteúdo (será definida depois)
        self.main_content = None
        
        self._build_ui()
    
    def set_main_content(self, main_content_frame):
        """Define o frame onde o conteúdo será carregado"""
        self.main_content = main_content_frame
        print(f"[SIDEBAR] Área principal definida: {main_content_frame}")
    
    def _build_ui(self):
        menu_container = ctk.CTkFrame(self, fg_color="transparent")
        menu_container.pack(fill="both", expand=True, padx=10, pady=20)
        
        self._add_logo(menu_container)
        
        ctk.CTkLabel(
            menu_container,
            text="INOVA EDU",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.cor_texto
        ).pack()
        
        ctk.CTkFrame(menu_container, height=2, fg_color=self.cor_texto).pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            menu_container,
            text="MENU LATERAL",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.cor_texto
        ).pack(pady=(15, 10))
        
        # === OPÇÕES DO MENU ===
        opcoes_menu = {
            " Repositório": self.abrir_repositorio,
            " Fórum": self.abrir_forum,
            " Eventos": self.abrir_eventos,
        }
        
        for texto_botao, comando in opcoes_menu.items():
            btn = ctk.CTkButton(
                menu_container,
                text=texto_botao,
                height=50,
                anchor="w",
                text_color=self.cor_texto,
                command=comando,
                font=ctk.CTkFont(size=14),
                corner_radius=5,
                border_width=0,
                fg_color=f"{azulClaro}",
                hover_color=f"{azulEscuro}"
            )
            btn.pack(fill="x", pady=3)
            self._botoes.append(btn)
            print(f"[SIDEBAR] Botão criado: {texto_botao}")
        
        # Espaço flexível
        ctk.CTkLabel(menu_container, text="").pack(fill="both", expand=True)
        
        # Perfil
        perfil_btn = ctk.CTkButton(
            menu_container,
            text=" Perfil",
            height=50,
            anchor="w",
            text_color=self.cor_texto,
            command=self.abrir_perfil,
            font=ctk.CTkFont(size=14),
            corner_radius=5,
            border_width=0,
            fg_color=f"{azulClaro}",
            hover_color=f"{azulEscuro}"
        )
        perfil_btn.pack(fill="x", pady=3)
        self._botoes.append(perfil_btn)
        
        # Logout
        ctk.CTkButton(
            menu_container,
            text=" Logout",
            height=50,
            anchor="w",
            text_color=self.cor_texto,
            command=self.fazer_logout,
            font=ctk.CTkFont(size=14),
            corner_radius=5,
            border_width=0,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", pady=(3, 0))
    
    def _add_logo(self, parent):
        try:
            # Ajuste o caminho conforme sua estrutura
            caminho_logo = "assets/LOGOBRANCO.png"
            if os.path.exists(caminho_logo):
                pil = Image.open(caminho_logo)
                self._logo_img = ctk.CTkImage(light_image=pil, size=(80, 100))
                ctk.CTkLabel(parent, image=self._logo_img, text="").pack()
            else:
                ctk.CTkLabel(parent, text="INOVA", font=ctk.CTkFont(size=22, weight="bold")).pack()
        except Exception as e:
            print(f"[SIDEBAR] Erro ao carregar logo: {e}")
            ctk.CTkLabel(parent, text="INOVA", font=ctk.CTkFont(size=22, weight="bold")).pack()
    
    # ========== MÉTODOS DE NAVEGAÇÃO ==========
    
    def limpar_main_content(self):
        """Limpa o conteúdo da área principal"""
        if self.main_content:
            print("[SIDEBAR] Limpando área principal...")
            for widget in self.main_content.winfo_children():
                widget.destroy()
        else:
            print("[SIDEBAR] ERRO: main_content não definido!")
    
    def abrir_repositorio(self):
        """Abre a tela de repositório/cursos"""
        print("[SIDEBAR] Abrindo Repositório...")
        
        if not self.main_content:
            print("[SIDEBAR] ERRO: main_content não definido!")
            return
        
        self.limpar_main_content()
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Repositório de Cursos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#111827"
        )
        titulo.pack(anchor="w", padx=30, pady=(30, 20))
        
        # Frame de cursos
        cursos_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        cursos_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Lista de cursos (exemplo)
        cursos = [
            {"nome": "Desenvolvimento de sistemas", "inicio": "2025-02-01", "termino": "2026-04-05"},
            {"nome": "Administrador de Banco de dados", "inicio": "2025-02-20", "termino": "2026-04-29"},
            {"nome": "Administrador de Redes", "inicio": "2025-02-25", "termino": "2026-05-10"},
            {"nome": "IT Essentials", "inicio": "2025-03-10", "termino": "2026-07-20"},
            {"nome": "Programação Web", "inicio": "2025-05-15", "termino": "2026-08-10"},
            {"nome": "Segurança da Informação", "inicio": "2024-09-01", "termino": "2025-12-20"},
        ]
        
        for curso in cursos:
            self.criar_card_curso(cursos_frame, curso)
    
    def criar_card_curso(self, parent, curso):
        """Cria um card de curso"""
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            border_width=1,
            border_color="#e5e7eb",
            corner_radius=10
        )
        card.pack(fill="x", pady=(0, 15))
        
        # Nome do curso
        nome = ctk.CTkLabel(
            card,
            text=f"### {curso['nome']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#111827"
        )
        nome.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Descrição
        desc_frame = ctk.CTkFrame(card, fg_color="transparent")
        desc_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Descrição",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="#4b5563"
        )
        desc_label.pack(anchor="w")
        
        # Datas
        datas_frame = ctk.CTkFrame(desc_frame, fg_color="transparent")
        datas_frame.pack(anchor="w", padx=(20, 0), pady=(5, 0))
        
        inicio = ctk.CTkLabel(
            datas_frame,
            text=f"Início: {curso['inicio']}",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280"
        )
        inicio.pack(anchor="w")
        
        termino = ctk.CTkLabel(
            datas_frame,
            text=f"Término: {curso['termino']}",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280"
        )
        termino.pack(anchor="w", pady=(2, 0))
        
        # Botão Acessar
        btn_acessar = ctk.CTkButton(
            card,
            text="Acessar Curso",
            width=120,
            height=35,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        btn_acessar.pack(anchor="w", padx=20, pady=(10, 15))
    
    def abrir_forum(self):
        """Abre o Fórum"""
        print("[SIDEBAR] Abrindo Fórum...")
        
        if not self.main_content:
            print("[SIDEBAR] ERRO: main_content não definido!")
            return
        
        try:
            # Importar a view do fórum
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from views.forum_view import ForumView
            
            # Limpar área principal
            self.limpar_main_content()
            
            # Criar e mostrar o fórum
            forum = ForumView(self.main_content)
            forum.run()
            print("[SIDEBAR] Fórum aberto com sucesso!")
            
        except ImportError as e:
            print(f"[SIDEBAR] Erro ao importar ForumView: {e}")
            self.limpar_main_content()
            
            # Mensagem de erro amigável
            erro_frame = ctk.CTkFrame(self.main_content, fg_color="white")
            erro_frame.pack(expand=True)
            
            erro_label = ctk.CTkLabel(
                erro_frame,
                text="❌ Fórum não encontrado",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#ef4444"
            )
            erro_label.pack(pady=(0, 10))
            
            sub_label = ctk.CTkLabel(
                erro_frame,
                text="Verifique se o arquivo views/forum_view.py existe",
                font=ctk.CTkFont(size=14),
                text_color="#6b7280"
            )
            sub_label.pack()
    
    def abrir_eventos(self):
        """Abre a tela de eventos"""
        print("[SIDEBAR] Abrindo Eventos...")
        
        if not self.main_content:
            print("[SIDEBAR] ERRO: main_content não definido!")
            return
        
        self.limpar_main_content()
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Calendário de Eventos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#111827"
        )
        titulo.pack(anchor="w", padx=30, pady=(30, 20))
        
        # Placeholder
        label = ctk.CTkLabel(
            self.main_content,
            text="📅 Eventos (em desenvolvimento)",
            font=ctk.CTkFont(size=18),
            text_color="#6b7280"
        )
        label.pack(expand=True)
    
    def abrir_perfil(self):
        """Abre a tela de perfil"""
        print("[SIDEBAR] Abrindo Perfil...")
        
        if not self.main_content:
            print("[SIDEBAR] ERRO: main_content não definido!")
            return
        
        self.limpar_main_content()
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Perfil do Usuário",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#111827"
        )
        titulo.pack(anchor="w", padx=30, pady=(30, 20))
        
        # Placeholder
        label = ctk.CTkLabel(
            self.main_content,
            text="👤 Perfil (em desenvolvimento)",
            font=ctk.CTkFont(size=18),
            text_color="#6b7280"
        )
        label.pack(expand=True)
    
    def fazer_logout(self):
        """Faz logout e volta para a tela de login"""
        print("[SIDEBAR] Fazendo logout...")
        
        # Destruir janela atual
        self.master.destroy()
        
        # Abrir nova janela de login
        try:
            from views.login_view import tela_login
            
            login_window = ctk.CTk()
            login_window.title("Login - INOVA EDU")
            login_window.attributes("-fullscreen", True)
            
            login_screen = tela_login(login_window)
            login_screen.pack(expand=True, fill="both")
            
            login_window.mainloop()
        except Exception as e:
            print(f"[SIDEBAR] Erro ao abrir login: {e}")
    
    @property
    def botoes(self):
        return list(self._botoes)


# ========== FUNÇÃO SIDEBAR (COMPATÍVEL) ==========
def sidebar(janela, cor_fundo=f"{azulEscuro}", cor_texto=f"{Branco}"):
    """
    Cria a sidebar e retorna a instância e os botões
    Uso: sidebar_instance, botoes = sidebar(self)
    """
=======
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
            "forum": {"modulo": "views.Aluno_e_Professor.forum_view", "classe": "Forum"},
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
>>>>>>> develop
    sb = Sidebar(janela, cor_fundo=cor_fundo, cor_texto=cor_texto)
    sb.pack(side="left", fill="y")
    return sb, []