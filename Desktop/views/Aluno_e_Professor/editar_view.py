import customtkinter as ctk
from tkinter import filedialog
from models.sessao import UsuarioSessao 

# Cores do Sistema
AZUL_SENAC = "#004A8D"
LARANJA_SENAC = "#F7941D"
BRANCO = "#FFFFFF"
CINZA_SENAC = "#E9E9E9"
CINZA_CLARO = "#F5F5F5"

class EditarPerfilView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color=BRANCO)
        self.janela = master
        self.controller = controller
        self.sessao = UsuarioSessao()
        
        # --- BUSCA DE DADOS VIA MODEL PELO CONTROLLER ---
        # Usamos o model que já está dentro do seu controller para pegar os dados reais
        try:
            perfil_completo = self.controller.model.obter_dados_perfil(self.sessao.email)
            self.dados_banco = perfil_completo.get('usuario', {})
        except Exception as e:
            print(f"Erro ao carregar dados para edição: {e}")
            self.dados_banco = {}

        self.pack(fill="both", expand=True)
        self.render_header()
        
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll_container.pack(fill="both", expand=True)
        
        self.render_tela()

    def render_header(self):
        self.header = ctk.CTkFrame(self, fg_color=AZUL_SENAC, height=80, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header, text="✏️ Editar Perfil Acadêmico", 
            font=("Roboto", 22, "bold"), text_color=BRANCO
        ).pack(side="left", padx=30)

        ctk.CTkButton(
            self.header, text="Voltar", width=100, height=32,
            fg_color="transparent", border_width=2, border_color=BRANCO,
            hover_color="#003566", font=("Roboto", 12, "bold"),
            command=self.voltar_perfil
        ).pack(side="right", padx=30)

    def render_tela(self):
        self.main_content = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.main_content.pack(pady=40, padx=50, fill="x")

        # --- SEÇÃO FOTO (Mantida) ---
        foto_section = ctk.CTkFrame(self.main_content, fg_color="transparent")
        foto_section.pack(fill="x", pady=(0, 40))
        self.borda_foto = ctk.CTkFrame(foto_section, width=180, height=180, corner_radius=90, fg_color=AZUL_SENAC)
        self.borda_foto.pack(side="left", padx=(0, 30))
        self.borda_foto.pack_propagate(False)
        self.lbl_foto = ctk.CTkLabel(self.borda_foto, text="👤", font=("Arial", 75), width=172, height=172, fg_color=CINZA_CLARO, corner_radius=86)
        self.lbl_foto.place(relx=0.5, rely=0.5, anchor="center")

        # --- FORMULÁRIO COM DADOS REAIS ---
        form_grid = ctk.CTkFrame(self.main_content, fg_color="transparent")
        form_grid.pack(fill="x")
        form_grid.columnconfigure((0, 1), weight=1)

        # Lógica de extração de dados do banco (tratando maiúsculas/minúsculas como no seu controller)
        u = self.dados_banco
        nome_db = u.get('nome') or u.get('Nome', '')
        sobrenome_db = u.get('sobrenome') or u.get('Sobrenome', '')
        bio_db = u.get('descricao') or u.get('Descricao', '')

        # Coluna 1
        col1 = ctk.CTkFrame(form_grid, fg_color="transparent")
        col1.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) 
        self.ent_nome = self.criar_campo(col1, "Nome", nome_db)
        self.ent_email = self.criar_campo(col1, "E-mail Acadêmico", self.sessao.email)
        self.ent_email.configure(state="disabled") # E-mail geralmente não se edita

        # Coluna 2
        col2 = ctk.CTkFrame(form_grid, fg_color="transparent")
        col2.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        self.ent_sobrenome = self.criar_campo(col2, "Sobrenome", sobrenome_db)
        self.ent_senha = self.criar_campo(col2, "Alterar Senha", "", show="*", placeholder="Digite para alterar")

        # Descrição
        ctk.CTkLabel(self.main_content, text="Biografia / Descrição", font=("Roboto", 14, "bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(20, 5), padx=20)
        self.txt_desc = ctk.CTkTextbox(self.main_content, height=150, fg_color=CINZA_CLARO, border_color=CINZA_SENAC, border_width=2, corner_radius=12, font=("Roboto", 14))
        self.txt_desc.pack(fill="x", pady=(0, 30), padx=20)
        self.txt_desc.insert("0.0", bio_db)

        # Botões de Ação
        acoes_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=20)

        ctk.CTkButton(
            acoes_frame, text="Salvar Alterações", 
            fg_color=LARANJA_SENAC, hover_color="#E68510",
            text_color=BRANCO, width=220, height=50, corner_radius=12,
            font=("Roboto", 16, "bold"),
            command=self.salvar_alteracoes
        ).pack(side="right")

    def criar_campo(self, master, label_text, valor_inicial, show=None, placeholder=""):
        container = ctk.CTkFrame(master, fg_color="transparent")
        container.pack(fill="x", pady=10, padx=20)
        ctk.CTkLabel(container, text=label_text, font=("Roboto", 14, "bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(0, 5))
        entry = ctk.CTkEntry(container, fg_color=CINZA_CLARO, border_color=CINZA_SENAC, border_width=2, height=45, corner_radius=10, show=show, placeholder_text=placeholder, font=("Roboto", 14))
        entry.pack(fill="x")
        entry.insert(0, valor_inicial)
        return entry

    def salvar_alteracoes(self):
        # Chama o método que já existe no seu controller!
        nome = self.ent_nome.get()
        sobrenome = self.ent_sobrenome.get()
        bio = self.txt_desc.get("0.0", "end").strip()
        senha = self.ent_senha.get()
        # Isso vai usar a lógica do banco que você já escreveu no controller
        self.controller.salvar_alteracoes_perfil(nome, sobrenome, bio, senha)

        # Atualiza a sessão local para não precisar deslogar e logar
        self.sessao.nome = nome
        self.sessao.sobrenome = sobrenome
        self.sessao.senha = senha
        self.sessao.descricao = bio

        self.voltar_perfil()

    def escolher_imagem(self):
        filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])

    def voltar_perfil(self):
        from views.Aluno_e_Professor.profile_view import UserProfileSystem
    
        self.pack_forget() 
        
        tela_perfil = UserProfileSystem(self.janela, self.controller)
        tela_perfil.pack(side="right", fill="both", expand=True)