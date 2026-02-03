import customtkinter as ctk

class CertificatesView:
    def __init__(self, controller):
        self.parent = None
        self.controller = controller
    
    def setup_ui(self):
        """
        Configurar interface de certificados
        """
        if not self.parent:
            return
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
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
        
        # Container da lista
        self.cert_list_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.cert_list_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def update_certificates_display(self, certificates):
        """
        Atualizar exibição de certificados
        """
        if not hasattr(self, 'cert_list_container'):
            return
        
        # Limpar container
        for widget in self.cert_list_container.winfo_children():
            widget.destroy()
        
        if not certificates:
            self.show_empty_state()
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
    
    def show_empty_state(self):
        """
        Mostrar estado vazio
        """
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
        """
        Criar card de certificado
        """
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