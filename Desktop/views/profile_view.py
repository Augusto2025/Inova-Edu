import customtkinter as ctk

print("DEBUG: Carregando ProfileView...")

class ProfileView:
    def __init__(self, parent, controller):
        print("DEBUG: Inicializando ProfileView...")
        self.parent = parent
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configurar interface principal
        """
        print("DEBUG: Configurando UI da ProfileView...")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Título
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="👤 Meu Perfil Acadêmico",
            font=("Arial", 28, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Container do perfil
        self.profile_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.profile_frame.pack(fill="both", expand=True)
        
        # Painel esquerdo
        self.left_panel = ctk.CTkFrame(self.profile_frame, width=350, corner_radius=15)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20))
        self.left_panel.pack_propagate(False)
        
        # Painel direito
        self.right_panel = ctk.CTkFrame(self.profile_frame, corner_radius=15)
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Configurar painéis
        self.setup_left_panel()
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """
        Configurar painel esquerdo (informações pessoais)
        """
        profile_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        profile_header.pack(pady=20)
        
        # Container da foto
        self.photo_container = ctk.CTkFrame(
            profile_header,
            width=180,
            height=180,
            corner_radius=90,
            fg_color="transparent",
            border_color="#E0E0E0",
            border_width=2
        )
        self.photo_container.pack()
        self.photo_container.pack_propagate(False)
        
        self.photo_label = ctk.CTkLabel(
            self.photo_container,
            text="👤",
            font=("Arial", 64),
            text_color="#808080",
            fg_color="transparent"
        )
        self.photo_label.pack(pady=0)
        
        # Botão para alterar foto
        ctk.CTkButton(
            profile_header,
            text="📷 Alterar Foto",
            command=self.controller.change_photo,
            width=180,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14)
        ).pack(pady=10)
        
        # Informações do usuário
        self.setup_user_info()
    
    def setup_user_info(self):
        """
        Configurar informações do usuário
        """
        info_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        info_frame.pack(pady=20, padx=20, fill="x")
        
        # Nome
        self.name_label = ctk.CTkLabel(
            info_frame,
            text="Carregando...",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        )
        self.name_label.pack(pady=(0, 10))
        
        ctk.CTkButton(
            info_frame,
            text="✏️ Editar Nome",
            command=self.controller.edit_name,
            width=180,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=(0, 20))
        
        # Curso
        course_frame = ctk.CTkFrame(info_frame, fg_color="#F0F7FF", corner_radius=8)
        course_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            course_frame,
            text="🎓 Curso Atual",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(10, 5))
        
        self.course_label = ctk.CTkLabel(
            course_frame,
            text="Carregando...",
            font=("Arial", 15),
            text_color="#3498DB"
        )
        self.course_label.pack(pady=(0, 10))
        
        # Biografia
        ctk.CTkLabel(
            info_frame,
            text="📝 Biografia",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.bio_text = ctk.CTkTextbox(
            info_frame,
            height=120,
            font=("Arial", 13),
            wrap="word",
            fg_color="#F8F9FA",
            border_color="#E0E0E0",
            border_width=1
        )
        self.bio_text.pack(fill="x", pady=(0, 10))
        self.bio_text.configure(state="disabled")
        
        ctk.CTkButton(
            info_frame,
            text="✏️ Editar Biografia",
            command=self.controller.edit_bio,
            width=180,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=5)
    
    def setup_right_panel(self):
        """
        Configurar painel direito (abas)
        """
        # Criar Tabview
        self.tabview = ctk.CTkTabview(self.right_panel)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Adicionar abas
        self.tabview.add("📜 Certificados")
        self.tabview.add("🚀 Projetos")
        
        # Configurar aba de certificados
        self.setup_certificates_tab()
        
        # Configurar aba de projetos
        self.setup_projects_tab()
    
    def setup_certificates_tab(self):
        """Configurar aba de certificados"""
        cert_tab = self.tabview.tab("📜 Certificados")
        
        header_frame = ctk.CTkFrame(cert_tab, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Meus Certificados",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        ctk.CTkButton(
            header_frame,
            text="+ Adicionar Certificado",
            command=self.controller.add_certificate,
            width=200,
            height=40,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14, "bold")
        ).pack(side="right")
        
        # Container da lista de certificados
        self.cert_list_container = ctk.CTkFrame(cert_tab, fg_color="transparent")
        self.cert_list_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def setup_projects_tab(self):
        """Configurar aba de projetos"""
        projetos_tab = self.tabview.tab("🚀 Projetos")
        
        header_frame = ctk.CTkFrame(projetos_tab, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Projetos que Estou Participando",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Container de projetos
        self.projects_container = ctk.CTkScrollableFrame(
            projetos_tab,
            fg_color="#F8F9FA"
        )
        self.projects_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def update_profile_info(self, user_data):
        """Atualizar informações do perfil"""
        print(f"DEBUG: Atualizando perfil: {user_data.get('nome', '')}")
        self.name_label.configure(text=user_data.get("nome", ""))
        self.course_label.configure(text=user_data.get("curso", ""))
        
        self.bio_text.configure(state="normal")
        self.bio_text.delete("1.0", "end")
        self.bio_text.insert("1.0", user_data.get("bio", ""))
        self.bio_text.configure(state="disabled")
    
    def update_certificates_display(self, certificates):
        """Atualizar exibição de certificados"""
        print(f"DEBUG: Atualizando {len(certificates)} certificados")
        
        # Limpar container
        for widget in self.cert_list_container.winfo_children():
            widget.destroy()
        
        if not certificates:
            self.show_empty_certificates()
            return
        
        # Criar lista com scroll
        cert_scroll_frame = ctk.CTkScrollableFrame(
            self.cert_list_container,
            fg_color="#F8F9FA"
        )
        cert_scroll_frame.pack(fill="both", expand=True)
        
        # Adicionar cada certificado
        for idx, cert in enumerate(certificates):
            self.create_certificate_card(cert_scroll_frame, cert, idx)
    
    def show_empty_certificates(self):
        """Mostrar estado vazio de certificados"""
        empty_frame = ctk.CTkFrame(
            self.cert_list_container,
            fg_color="transparent",
            height=250
        )
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="📄",
            font=("Arial", 64),
            text_color="#BDC3C7"
        ).pack(pady=(40, 20))
        
        ctk.CTkLabel(
            empty_frame,
            text="Nenhum certificado adicionado",
            font=("Arial", 18),
            text_color="#7F8C8D"
        ).pack()
        
        ctk.CTkLabel(
            empty_frame,
            text="Clique em 'Adicionar Certificado' para adicionar seu primeiro certificado",
            font=("Arial", 14),
            text_color="#BDC3C7"
        ).pack(pady=(10, 0))
    
    def create_certificate_card(self, parent, cert, index):
        """Criar card de certificado"""
        card = ctk.CTkFrame(
            parent,
            height=100,
            corner_radius=12,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1
        )
        card.pack(fill="x", pady=8, padx=5)
        card.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Informações principais
        main_info = ctk.CTkFrame(content_frame, fg_color="transparent")
        main_info.pack(side="left", fill="both", expand=True)
        
        # Ícone
        icon_frame = ctk.CTkFrame(main_info, fg_color="transparent")
        icon_frame.pack(side="left")
        
        ctk.CTkLabel(
            icon_frame,
            text="📜",
            font=("Arial", 28)
        ).pack()
        
        # Detalhes
        details_frame = ctk.CTkFrame(main_info, fg_color="transparent")
        details_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        ctk.CTkLabel(
            details_frame,
            text=cert["nome"],
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w")
        
        # Informações adicionais
        info_text = f"📅 {cert['data']}"
        if cert.get('instituicao'):
            info_text += f"  •  🏛️ {cert['instituicao']}"
        if cert.get('carga_horaria'):
            info_text += f"  •  ⏱️ {cert['carga_horaria']}"
        
        ctk.CTkLabel(
            details_frame,
            text=info_text,
            font=("Arial", 13),
            text_color="#7F8C8D"
        ).pack(anchor="w", pady=(5, 0))
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(
            btn_frame,
            text="👁️ Ver",
            command=lambda c=cert: self.controller.view_certificate(c),
            width=80,
            height=32,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 12)
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            command=lambda i=index: self.controller.edit_certificate(i),
            width=80,
            height=32,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 12)
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Excluir",
            command=lambda i=index: self.controller.delete_certificate(i),
            width=80,
            height=32,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=("Arial", 12)
        ).pack(side="left", padx=3)
    
    def update_projects_display(self, projects):
        """Atualizar exibição de projetos"""
        print(f"DEBUG: Atualizando {len(projects)} projetos")
        
        # Limpar container
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        
        # Adicionar cada projeto
        for projeto in projects:
            self.create_project_card(projeto)
    
    def create_project_card(self, projeto):
        """Criar card de projeto"""
        card = ctk.CTkFrame(
            self.projects_container,
            height=100,
            corner_radius=12,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1
        )
        card.pack(fill="x", pady=8, padx=5)
        card.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Cabeçalho do card
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text=projeto["nome"],
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Descrição
        ctk.CTkLabel(
            content_frame,
            text=projeto["descricao"],
            font=("Arial", 13),
            text_color="#7F8C8D",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(8, 0))