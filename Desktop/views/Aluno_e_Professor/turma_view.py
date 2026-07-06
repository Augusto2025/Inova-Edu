import customtkinter as ctk
import os
import sys

# Adiciona o caminho base para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importação do Controller
from controllers.turma_controllers import TurmasController
from assets.cores import *

class TurmasDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master, id_curso, nome_curso):
        super().__init__(master)
        self.janela = master
        self.id_curso = id_curso
        self.nome_curso = nome_curso
        
        # Configuração visual do Frame Principal
        self.configure(fg_color="#f8fafc") # Um cinza claro mais moderno (Slate 50)
        
        # --- LÓGICA MVC: BUSCA DE DADOS ---
        self.controller = TurmasController()
        self.turmas_por_ano = self.controller.obter_turmas_filtradas(self.id_curso)
        
        # --- INTEGRAÇÃO COM A SIDEBAR ---
        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break
        if not sidebar_existente:
            sidebar(self.janela)

        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        from assets.header import HeaderPadrao
        header = HeaderPadrao(self, titulo=f"Turmas de {self.nome_curso}", comando_voltar=self.voltar_home)
        
        # Barra de Pesquisa Moderna
        self.entry_busca = ctk.CTkEntry(
            header, 
            placeholder_text="🔍 Pesquisar por código, turno ou professor...", 
            width=350, 
            height=38,
            corner_radius=8,
            border_color="#cbd5e1"
        )
        self.entry_busca.pack(side="right", padx=30)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_turmas)

        # ÁREA DE CONTEÚDO COM SCROLL
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=25, pady=15)

        self.renderizar_conteudo(self.turmas_por_ano)

    def voltar_home(self):
        self.pack_forget()
        from views.Aluno_e_Professor.home_view import Home
        self.tela_home = Home(self.janela)
        self.tela_home.pack(side="right", fill="both", expand=True)

    def renderizar_conteudo(self, dados):
        """Limpa e renderiza as seções de turmas"""
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        if not dados:
            ctk.CTkLabel(self.main_scroll, text="Nenhuma turma localizada.", 
             font=ctk.CTkFont(size=16, weight="medium"), text_color="#94a3b8") # <-- mude para "normal" ou remova o weight
            return

        # Gerar Seções por Ano
        for ano, turmas in dados.items():
            self.renderizar_secao(ano, turmas)

    def renderizar_secao(self, ano, turmas):
        # Container da Seção (Ano)
        section_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section_container.pack(fill="x", pady=(10, 25))

        # Título da Seção Linha divisória fina
        title_frame = ctk.CTkFrame(section_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(title_frame, text=f"Ano Letivo {ano}", font=ctk.CTkFont(size=16, weight="bold"), 
                     text_color="#475569").pack(side="left", padx=5)
        
        ctk.CTkFrame(title_frame, height=1, fg_color="#e2e8f0").pack(side="left", fill="x", expand=True, padx=15)

        # Grid Responsivo para os Cards
        grid_container = ctk.CTkFrame(section_container, fg_color="transparent")
        grid_container.pack(fill="x")
        grid_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="cards")
        
        for i, turma in enumerate(turmas):
            self.criar_card_turma(grid_container, turma, i)

    def criar_card_turma(self, master, turma, idx):
        linha = idx // 3
        coluna = idx % 3

        # REMOVIDO: width, height e pack_propagate(False) para o card expandir com o conteúdo
        card = ctk.CTkFrame(master, fg_color="#ffffff", corner_radius=12, 
                            border_width=1, border_color="#e2e8f0")
        card.grid(row=linha, column=coluna, padx=12, pady=12, sticky="nsew")

        # Pequena barra sutil decorativa no topo
        top_accent = ctk.CTkFrame(card, height=4, fg_color=turma.get("cor", "#3b82f6"), corner_radius=0)
        top_accent.pack(side="top", fill="x")

        # Container interno com padding adequado
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=16)

        # 1. DESTAQUE: Nome do Professor
        nome_docente = turma.get("professor", "Sem docente designado")
        lbl_professor = ctk.CTkLabel(
            content, 
            text=nome_docente, 
            font=ctk.CTkFont(size=16, weight="bold"), 
            text_color="#0f172a",
            wraplength=220, # Quebra a linha se o nome for muito grande
            justify="left"
        )
        lbl_professor.pack(anchor="w", pady=(0, 4))
        
        # 2. SECUNDÁRIO: Identificação da Turma
        lbl_turma = ctk.CTkLabel(
            content, 
            text=f"Turma: {turma['cod']}", 
            font=ctk.CTkFont(size=13, weight="normal"), 
            text_color="#64748b"
        )
        lbl_turma.pack(anchor="w", pady=(0, 6))

        # 3. TERCIÁRIO: Turno
        lbl_turno = ctk.CTkLabel(
            content, 
            text=f"⏰ {turma['turno'].capitalize()}", 
            font=ctk.CTkFont(size=11, weight="normal"), 
            text_color="#94a3b8"
        )
        lbl_turno.pack(anchor="w", pady=(0, 14)) # Espaço extra antes do botão

        # Botão Único de Ação (Projetos) - Agora usando pack normal no fluxo correto
        btn_projetos = ctk.CTkButton(
            content, 
            text="Ver Projetos", 
            height=36,
            fg_color="#edf2f7", 
            text_color="#2b6cb0", 
            hover_color="#e2e8f0",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=lambda t=turma: self.abrir_projetos(t["id"], t["cod"])
        )
        btn_projetos.pack(fill="x", side="top") # side="top" garante que ele siga a fila abaixo do turno
    
    def filtrar_turmas(self, event=None):
        """Filtra buscando por código, turno ou nome do professor"""
        termo = self.entry_busca.get().lower()
        dados_filtrados = {}

        for ano, lista_turmas in self.turmas_por_ano.items():
            filtradas = [
                t for t in lista_turmas if 
                termo in t["cod"].lower() or 
                termo in t["turno"].lower() or 
                termo in t.get("professor", "").lower()
            ]
            if filtradas:
                dados_filtrados[ano] = filtradas
        
        self.renderizar_conteudo(dados_filtrados)

    def abrir_projetos(self, turma_id, turma_nome):
        try:
            from views.Aluno_e_Professor.projetos_view import ProjetosDesktopDashboard
            from controllers.projeto_controller import ProjetoController

            controller_projeto = ProjetoController()
            tipo_user = getattr(self.janela, 'tipo_usuario', 'Professor') 

            self.pack_forget()
            
            self.tela_projetos = ProjetosDesktopDashboard(
                master=self.janela, 
                id_turma=turma_id, 
                nome_turma=turma_nome, 
                tipo_usuario=tipo_user,
                controller=controller_projeto
            )
            self.tela_projetos.pack(side="right", fill="both", expand=True)
            
        except Exception as e:
            print("Erro", f"Não foi possível carregar projetos: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1150x750")
    app = TurmasDesktopDashboard(root, id_curso=1, nome_curso="Análise de Sistemas")
    root.mainloop()