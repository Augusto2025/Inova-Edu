import customtkinter as ctk
from tkinter import filedialog, messagebox
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
        
        # Variável temporária para armazenar a nova senha obtida via modal
        self.nova_senha_definida = ""

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

        # --- SEÇÃO FOTO ---
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

        u = self.dados_banco
        nome_db = u.get('nome') or u.get('Nome', '')
        sobrenome_db = u.get('sobrenome') or u.get('Sobrenome', '')
        bio_db = u.get('descricao') or u.get('Descricao', '')

        # Coluna 1
        col1 = ctk.CTkFrame(form_grid, fg_color="transparent")
        col1.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) 
        self.ent_nome = self.criar_campo(col1, "Nome", nome_db)
        self.ent_email = self.criar_campo(col1, "E-mail Acadêmico", self.sessao.email)
        self.ent_email.configure(state="disabled") 

        # Coluna 2
        col2 = ctk.CTkFrame(form_grid, fg_color="transparent")
        col2.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        self.ent_sobrenome = self.criar_campo(col2, "Sobrenome", sobrenome_db)
        
        # MODIFICAÇÃO: Botão para disparar o Modal de Senha no modelo solicitado
        container_btn = ctk.CTkFrame(col2, fg_color="transparent")
        container_btn.pack(fill="x", pady=10, padx=20)
        ctk.CTkLabel(container_btn, text="Segurança de Acesso", font=("Roboto", 14, "bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(0, 5))
        
        self.btn_senha_modal = ctk.CTkButton(
            container_btn, text="🔄 Alterar Senha do Sistema", fg_color=AZUL_SENAC, hover_color="#003566",
            height=45, corner_radius=10, font=("Roboto", 14, "bold"), command=self.abrir_modal_senha
        )
        self.btn_senha_modal.pack(fill="x")

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

    def abrir_modal_senha(self):
        """Janela Modal de Senha baseada perfeitamente no seu modelo de filtros"""
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Alteração de Segurança")
        modal.geometry("500x420")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        # Header do Modal (Igual ao seu modelo)
        m_header = ctk.CTkFrame(modal, fg_color=AZUL_SENAC, corner_radius=0, height=60)
        m_header.pack(fill="x")
        ctk.CTkLabel(m_header, text="🔒 Alterar Senha de Acesso", font=ctk.CTkFont(size=16, weight="bold"), text_color=BRANCO).pack(pady=15)

        # Container do Conteúdo
        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # Input Nova Senha
        ctk.CTkLabel(content, text="Nova Senha:", font=ctk.CTkFont(weight="bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(5, 5))
        txt_nova = ctk.CTkEntry(content, fg_color=BRANCO, border_color=CINZA_SENAC, border_width=2, height=40, corner_radius=8, show="*")
        txt_nova.pack(fill="x", pady=(0, 15))

        # Input Confirmar Senha
        ctk.CTkLabel(content, text="Confirmar Nova Senha:", font=ctk.CTkFont(weight="bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(5, 5))
        txt_confirma = ctk.CTkEntry(content, fg_color=BRANCO, border_color=CINZA_SENAC, border_width=2, height=40, corner_radius=8, show="*")
        txt_confirma.pack(fill="x", pady=(0, 15))

        def validar_e_aplicar():
            senha = txt_nova.get().strip()
            confirma = txt_confirma.get().strip()
            
            if not senha:
                messagebox.showerror("Erro", "O campo de senha não pode ficar em branco!")
                return
            if senha != confirma:
                messagebox.showerror("Erro", "As senhas digitadas não coincidem!")
                return
                
            # Salva na variável da classe para enviar ao salvar o formulário principal
            self.nova_senha_definida = senha
            self.btn_senha_modal.configure(text="✅ Senha Alterada (Pronta)", fg_color="#22c55e", hover_color="#16a34a")
            modal.destroy()

        # Botão Aplicar (Igual ao seu modelo)
        ctk.CTkButton(modal, text="Confirmar Nova Senha", fg_color=AZUL_SENAC, hover_color="#003566", text_color=BRANCO, height=45, font=("Roboto", 14, "bold"),
                      command=validar_e_aplicar).pack(fill="x", padx=40, pady=(0, 25))

    def salvar_alteracoes(self):
        nome = self.ent_nome.get()
        sobrenome = self.ent_sobrenome.get()
        bio = self.txt_desc.get("0.0", "end").strip()
        
        # Se alterou a senha pelo modal, envia a nova, se não, envia a senha atual da sessão
        senha_final = self.nova_senha_definida if self.nova_senha_definida else self.sessao.senha
        
        self.controller.salvar_alteracoes_perfil(nome, sobrenome, bio, senha_final)

        self.sessao.nome = nome
        self.sessao.sobrenome = sobrenome
        self.sessao.senha = senha_final
        self.sessao.descricao = bio

        self.voltar_perfil()

    def escolher_imagem(self):
        filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])

    def voltar_perfil(self):
        """Limpa as views empilhadas de forma segura e renderiza o UserProfileSystem limpo"""
        from views.Aluno_e_Professor.profile_view import UserProfileSystem
    
        # Varre o frame master buscando qualquer fragmento visual anterior e limpa
        for widget in self.janela.winfo_children():
            # Remove views de perfil/edição antigas para evitar sobreposição ou botões fantasmas
            if widget.__class__.__name__ in ["EditarPerfilView", "UserProfileSystem"]:
                widget.pack_forget()
                widget.destroy()
        
        # Renderiza a tela limpa e atualizada no canto direito ao lado da Sidebar fixa
        tela_perfil = UserProfileSystem(self.janela, self.controller)
        tela_perfil.pack(side="right", fill="both", expand=True)