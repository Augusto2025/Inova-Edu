import customtkinter as ctk
from tkinter import filedialog

# Cores do Sistema
AZUL_SENAC = "#004A8D"
LARANJA_SENAC = "#F7941D"
BRANCO = "#FFFFFF"
CINZA_SENAC = "#E9E9E9"
CINZA_CLARO = "#F5F5F5"
CINZA_FUNDO = "#F0F2F5"

class EditarPerfilView(ctk.CTkFrame):
    def __init__(self, master, usuario_dados, controller):
        super().__init__(master, fg_color=CINZA_FUNDO)
        self.janela = master
        self.controller = controller
        self.dados = usuario_dados
        
        self.pack(fill="both", expand=True)
        
        # 1. Renderiza o Header (estilo Desktop Perfil)
        self.render_header()
        
        # 2. Scrollable container para o conteúdo central
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)
        
        self.render_tela()

    def render_header(self):
        """Header unificado com o estilo do Perfil Desktop"""
        self.header = ctk.CTkFrame(self, fg_color=AZUL_SENAC, height=80, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header, text="✏️ Editar Perfil Acadêmico", 
            font=("Roboto", 22, "bold"), text_color=BRANCO
        ).pack(side="left", padx=30)

        # Botão para voltar rápido
        ctk.CTkButton(
            self.header, text="Voltar", width=100, height=32,
            fg_color="transparent", border_width=2, border_color=BRANCO,
            hover_color="#003566", font=("Roboto", 12, "bold"),
            command=self.voltar_perfil
        ).pack(side="right", padx=30)

    def render_tela(self):
        # Título Centralizado
        ctk.CTkLabel(
            self.scroll_container, 
            text="Configurações de Perfil", 
            font=("Roboto", 32, "bold"), 
            text_color=AZUL_SENAC
        ).pack(pady=(40, 10))

        # Main Card (.editar-form)
        self.form_card = ctk.CTkFrame(
            self.scroll_container, 
            fg_color=BRANCO, 
            width=480, 
            corner_radius=25,
            border_width=0
        )
        self.form_card.pack(pady=20, padx=20)
        self.form_card.pack_propagate(False)
        self.form_card.configure(height=820) # Ajustado para o conteúdo

        # --- ÁREA DA FOTA (Bola Perfeita com Borda) ---
        foto_area = ctk.CTkFrame(self.form_card, fg_color="transparent")
        foto_area.pack(pady=30)

        # Container da borda (Círculo Externo)
        self.borda_foto = ctk.CTkFrame(
            foto_area,
            width=160, height=160,
            corner_radius=80, # Bola perfeita
            fg_color=AZUL_SENAC
        )
        self.borda_foto.pack()
        self.borda_foto.pack_propagate(False)

        # Label da Foto (Círculo Interno)
        self.lbl_foto = ctk.CTkLabel(
            self.borda_foto, 
            text="👤", 
            font=("Arial", 65),
            width=152, height=152, 
            fg_color=CINZA_CLARO, 
            corner_radius=76 # Bola perfeita
        )
        self.lbl_foto.place(relx=0.5, rely=0.5, anchor="center")

        # Botão flutuante para alterar foto (estilo CSS)
        self.btn_foto = ctk.CTkLabel(
            foto_area, text="Alterar Foto", 
            fg_color=AZUL_SENAC, text_color=BRANCO,
            width=130, height=35, corner_radius=12,
            font=("Roboto", 12, "bold"),
            cursor="hand2"
        )
        self.btn_foto.pack(pady=15)
        self.btn_foto.bind("<Button-1>", lambda e: self.escolher_imagem())

        # --- INPUTS ---
        self.container_inputs = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.container_inputs.pack(fill="x", padx=40)

        self.ent_nome = self.criar_campo("Nome", self.dados.get('nome', ''))
        self.ent_sobrenome = self.criar_campo("Sobrenome", self.dados.get('sobrenome', ''))
        self.ent_email = self.criar_campo("Email", self.dados.get('email', ''))
        self.ent_senha = self.criar_campo("Nova senha:", "", show="*", placeholder="Deixe em branco para manter")
        
        # Textarea para Descrição
        ctk.CTkLabel(
            self.container_inputs, text="Descrição", 
            font=("Roboto", 13, "bold"), text_color=AZUL_SENAC
        ).pack(anchor="w", pady=(10, 5))
        
        self.txt_desc = ctk.CTkTextbox(
            self.container_inputs, height=100, 
            fg_color=CINZA_CLARO, border_color=CINZA_SENAC, border_width=2,
            corner_radius=10, font=("Roboto", 14)
        )
        self.txt_desc.pack(fill="x", pady=(0, 15))
        self.txt_desc.insert("0.0", self.dados.get('descricao', ''))

        # --- AÇÕES FINAL ---
        botoes_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=40, pady=20)

        btn_cancelar = ctk.CTkButton(
            botoes_frame, text="Cancelar", 
            fg_color="#E2E8F0", hover_color="#CBD5E1",
            text_color="#475569", width=120, height=45, corner_radius=12,
            font=("Roboto", 13, "bold"),
            command=self.voltar_perfil
        )
        btn_cancelar.pack(side="left")

        btn_salvar = ctk.CTkButton(
            botoes_frame, text="Salvar Alterações", 
            fg_color=AZUL_SENAC, hover_color=LARANJA_SENAC,
            text_color=BRANCO, width=200, height=45, corner_radius=12,
            font=("Roboto", 13, "bold"),
            command=self.salvar_alteracoes
        )
        btn_salvar.pack(side="right")

    def criar_campo(self, label_text, valor_inicial, show=None, placeholder=""):
        lbl = ctk.CTkLabel(self.container_inputs, text=label_text, font=("Roboto", 13, "bold"), text_color=AZUL_SENAC)
        lbl.pack(anchor="w", pady=(10, 0))
        
        entry = ctk.CTkEntry(
            self.container_inputs, 
            fg_color=CINZA_CLARO, border_color=CINZA_SENAC, border_width=2,
            height=45, corner_radius=12, show=show,
            placeholder_text=placeholder, font=("Roboto", 14)
        )
        entry.pack(fill="x", pady=(5, 5))
        entry.insert(0, valor_inicial)
        return entry

    def escolher_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
        if caminho:
            print(f"Nova imagem: {caminho}")

    def salvar_alteracoes(self):
        # Aqui você chamaria o controller.atualizar_perfil()
        print("Salvando...")

    def voltar_perfil(self):
        self.destroy()
        # Aqui você deve chamar a função que renderiza a UserProfileSystem novamente