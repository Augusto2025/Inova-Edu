import customtkinter as ctk

class ProjectsView:
    def __init__(self, controller):
        self.parent = None
        self.controller = controller
    
    def setup_ui(self):
        """
        Configurar interface de projetos
        """
        if not self.parent:
            return
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Projetos que Estou Participando",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Container de projetos
        self.projects_container = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="#F8F9FA"
        )
        self.projects_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def update_projects_display(self, projects):
        """
        Atualizar exibição de projetos
        """
        if not hasattr(self, 'projects_container'):
            return
        
        # Limpar container
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        
        # Adicionar cada projeto
        for projeto in projects:
            self.create_project_card(projeto)
    
    def create_project_card(self, projeto):
        """
        Criar card de projeto
        """
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