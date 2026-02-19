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
        self.configure(fg_color="#f0f2f5") 
        
        # --- LÓGICA MVC: BUSCA DE DADOS ---
        self.controller = TurmasController()
        # O controller retorna o dicionário agrupado por ano vindo do banco
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
        # 1. HEADER SUPERIOR
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Gestão de Turmas", 
                     font=ctk.CTkFont(size=24, weight="bold"), 
                     text_color=Branco).pack(side="left", padx=30)

        # Barra de Pesquisa (Filtro)
        self.entry_busca = ctk.CTkEntry(header, placeholder_text="Pesquisar turma...", width=300, height=35)
        self.entry_busca.pack(side="right", padx=30)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_turmas)

        # 2. ÁREA DE CONTEÚDO COM SCROLL
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.renderizar_conteudo(self.turmas_por_ano)

    def renderizar_conteudo(self, dados):
        """Limpa e renderiza as seções de turmas"""
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        if not dados:
            ctk.CTkLabel(self.main_scroll, text="Nenhuma turma encontrada.", 
                         font=ctk.CTkFont(size=16), text_color="#64748b").pack(pady=50)
            return

        # Gerar Seções por Ano
        for ano, turmas in dados.items():
            self.renderizar_secao(ano, turmas)

    def renderizar_secao(self, ano, turmas):
        # Container da Seção (Ano)
        section_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section_container.pack(fill="x", pady=(10, 20))

        # Título da Seção (Ex: Ano Letivo 2025)
        title_frame = ctk.CTkFrame(section_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(title_frame, text=f"Ano Letivo {ano}", font=ctk.CTkFont(size=18, weight="bold"), 
                     text_color="#64748b").pack(side="left", padx=10)
        
        ctk.CTkFrame(title_frame, height=2, fg_color="#e2e8f0").pack(side="left", fill="x", expand=True, padx=10)

        # Grid para os Cards (Máximo 3 colunas)
        grid_container = ctk.CTkFrame(section_container, fg_color="transparent")
        grid_container.pack(fill="x")
        grid_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, turma in enumerate(turmas):
            self.criar_card_turma(grid_container, turma, i)

    def criar_card_turma(self, master, turma, idx):
        # Lógica de posicionamento no Grid
        linha = idx // 3
        coluna = idx % 3

        # Card principal
        card = ctk.CTkFrame(master, fg_color="#ffffff", width=300, height=200, corner_radius=15, 
                            border_width=1, border_color="#e2e8f0")
        card.grid(row=linha, column=coluna, padx=10, pady=10, sticky="n")
        card.pack_propagate(False)

        # Faixa lateral de cor (Accent)
        accent = ctk.CTkFrame(card, width=6, fg_color=turma.get("cor", "#3b82f6"), corner_radius=0)
        accent.pack(side="left", fill="y")

        # Conteúdo do Card
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(content, text=turma["cod"], font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color="#1e293b").pack(anchor="w")
        
        ctk.CTkLabel(content, text=f"Turno: {turma['turno']}", font=ctk.CTkFont(size=13), 
                     text_color="#64748b").pack(anchor="w")

        ctk.CTkLabel(content, text=f"👥 {turma.get('alunos', 0)} Alunos matriculados", font=ctk.CTkFont(size=12), 
                     text_color="#94a3b8").pack(anchor="w", pady=(10, 0))

        # Container de Botões (Rodapé)
        button_row = ctk.CTkFrame(content, fg_color="transparent")
        button_row.pack(side="bottom", fill="x", pady=(10, 0))

        # Botão Usuários
        btn_usuarios = ctk.CTkButton(button_row, text="Usuários", height=32, width=100,
                                     fg_color="#f1f5f9", text_color="#475569", hover_color="#e2e8f0",
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     command=lambda: print(f"Usuários da turma: {turma['cod']}"))
        btn_usuarios.pack(side="left", expand=True, padx=(0, 5))

        # Botão Projetos
        btn_projetos = ctk.CTkButton(button_row, text="Projetos", height=32, width=100,
                                      fg_color="#3b82f6", text_color="#ffffff", hover_color="#2563eb",
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      command=lambda t=turma: self.abrir_projetos(t["id"], t["cod"]))
        btn_projetos.pack(side="left", expand=True, padx=(5, 0))
    
    def filtrar_turmas(self, event=None):
        """Filtra as turmas exibidas com base na entrada de texto"""
        termo = self.entry_busca.get().lower()
        dados_filtrados = {}

        for ano, lista_turmas in self.turmas_por_ano.items():
            filtradas = [t for t in lista_turmas if termo in t["cod"].lower() or termo in t["turno"].lower()]
            if filtradas:
                dados_filtrados[ano] = filtradas
        
        self.renderizar_conteudo(dados_filtrados)

    def abrir_projetos(self, turma_id, turma_nome):
        try:
            from views.Aluno_e_Professor.projetos_view import ProjetosDesktopDashboard
            from controllers.projeto_controller import ProjetoController # Importe o controller aqui

            # 1. Instancie o controller
            controller_projeto = ProjetoController()

            # 2. Pegue o tipo do usuário
            tipo_user = getattr(self.janela, 'tipo_usuario', 'Professor') 

            self.pack_forget()
            
            # 3. Passe o controller como o 5º argumento
            self.tela_projetos = ProjetosDesktopDashboard(
                master=self.janela, 
                id_turma=turma_id, 
                nome_turma=turma_nome, 
                tipo_usuario=tipo_user,
                controller=controller_projeto  # <--- Faltava isso!
            )
            self.tela_projetos.pack(side="right", fill="both", expand=True)
            
        except Exception as e:
            print("Erro", f"Não foi possível carregar projetos: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1150x750")
    app = TurmasDesktopDashboard(root)
    root.mainloop()