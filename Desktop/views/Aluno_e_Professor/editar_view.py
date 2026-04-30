import customtkinter as ctk
from tkinter import filedialog
from PIL import Image # Certifique-se de ter o Pillow instalado: pip install Pillow

class EditarPerfilView(ctk.CTkFrame):
    def __init__(self, master, usuario_dados, controller):
        super().__init__(master, fg_color="#F0F2F5") # Cor de fundo do body
        self.janela = master
        self.controller = controller
        self.dados = usuario_dados # Dicionário com nome, sobrenome, email, etc.
        
        self.pack(fill="both", expand=True)
        self.render_tela()

    def render_tela(self):
        # Título (Baseado no .titulo do seu CSS)
        ctk.CTkLabel(
            self, text="Editar Perfil", 
            font=("Roboto", 32, "bold"), 
            text_color="#004A8D"
        ).pack(pady=(40, 20))

        # Main Container (Baseado no .editar-form do seu CSS)
        self.form_card = ctk.CTkFrame(
            self, fg_color="#FFFFFF", width=450, 
            corner_radius=20, border_width=0
        )
        self.form_card.pack(pady=20, padx=20)

        # --- ÁREA DA FOTO ---
        foto_area = ctk.CTkFrame(self.form_card, fg_color="transparent")
        foto_area.pack(pady=25)

        # Placeholder para foto circular (simulando a img do CSS)
        self.lbl_foto = ctk.CTkLabel(
            foto_area, text="👤", font=("Arial", 60),
            width=150, height=150, fg_color="#F5F5F5", 
            corner_radius=75, border_width=4, border_color="#004A8D"
        )
        self.lbl_foto.pack()

        btn_alterar_foto = ctk.CTkButton(
            foto_area, text="Alterar Foto", 
            fg_color="#004A8D", hover_color="#F7941D",
            width=120, height=32, corner_radius=10,
            command=self.escolher_imagem
        )
        btn_alterar_foto.pack(pady=12)

        # --- CAMPOS DE INPUT (Baseado no .inputs do seu CSS) ---
        self.container_inputs = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.container_inputs.pack(fill="x", padx=35, pady=(0, 20))

        self.ent_nome = self.criar_campo("Nome", self.dados.get('nome', ''))
        self.ent_sobrenome = self.criar_campo("Sobrenome", self.dados.get('sobrenome', ''))
        self.ent_email = self.criar_campo("Email", self.dados.get('email', ''))
        self.ent_senha = self.criar_campo("Nova senha:", "", show="*")
        
        # Descrição (Textarea)
        lbl_desc = ctk.CTkLabel(self.container_inputs, text="Descrição", font=("Roboto", 13, "bold"), text_color="#004A8D")
        lbl_desc.pack(anchor="w", pady=(10, 5))
        self.txt_desc = ctk.CTkTextbox(
            self.container_inputs, height=100, 
            fg_color="#F5F5F5", border_color="#E9E9E9", border_width=2
        )
        self.txt_desc.pack(fill="x")
        self.txt_desc.insert("0.0", self.dados.get('descricao', ''))

        # --- BOTÕES (Baseado no .botoes do seu CSS) ---
        botoes_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=35, pady=30)

        btn_cancelar = ctk.CTkButton(
            botoes_frame, text="Cancelar", 
            fg_color="#BBBBBB", hover_color="#999999",
            text_color="white", width=120, height=40, corner_radius=10,
            command=self.voltar_perfil
        )
        btn_cancelar.pack(side="left")

        btn_salvar = ctk.CTkButton(
            botoes_frame, text="Salvar Alterações", 
            fg_color="#004A8D", hover_color="#F7941D",
            text_color="white", width=160, height=40, corner_radius=10,
            command=self.salvar_alteracoes
        )
        btn_salvar.pack(side="right")

    def criar_campo(self, label_text, valor_inicial, show=None):
        lbl = ctk.CTkLabel(self.container_inputs, text=label_text, font=("Roboto", 13, "bold"), text_color="#004A8D")
        lbl.pack(anchor="w", pady=(10, 0))
        
        entry = ctk.CTkEntry(
            self.container_inputs, 
            fg_color="#F5F5F5", border_color="#E9E9E9", border_width=2,
            height=40, corner_radius=10, show=show
        )
        entry.pack(fill="x", pady=(5, 5))
        entry.insert(0, valor_inicial)
        return entry

    def escolher_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
        if caminho:
            print(f"Imagem selecionada: {caminho}")
            # Aqui você pode atualizar o self.lbl_foto usando PIL se desejar

    def salvar_alteracoes(self):
        # Coleta os dados para enviar ao controller
        novos_dados = {
            "nome": self.ent_nome.get(),
            "sobrenome": self.ent_sobrenome.get(),
            "email": self.ent_email.get(),
            "senha": self.ent_senha.get(),
            "descricao": self.txt_desc.get("0.0", "end").strip()
        }
        print(f"Enviando para o controller: {novos_dados}")
        # self.controller.atualizar_perfil_banco(novos_dados)

    def voltar_perfil(self):
        self.pack_forget()
        # Chamar a renderização da view de perfil original