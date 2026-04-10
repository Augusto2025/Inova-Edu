import customtkinter as ctk
import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path para facilitar imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cores do Sistema (Definidas globalmente para o Header e o Corpo)
AZUL_SENAC = "#004A8D"
BRANCO = "#FFFFFF"

print("DEBUG: Iniciando perfil_academico.py com Header Customizado")

class UserProfileSystem(ctk.CTkFrame):
    def __init__(self, master=None):
        # 1. Configuração inicial
        super().__init__(master, fg_color="#F0F2F5") 
        self.janela = master

        # Cores do Sistema para o corpo
        self.laranja_senac = "#F7941D"
        self.branco = BRANCO
        self.cinza_texto = "#666666"
        self.verde_sucesso = "#28a745"

        # 2. Busca/Criação da Sidebar
        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break

        if not sidebar_existente:
            sidebar_existente, _ = sidebar(self.janela)
        
        # 3. Construção da Interface (Header + Conteúdo)
        self.render_header()
        
        # Frame Principal Scrollable (Conteúdo abaixo do Header)
        self.main_content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.create_directories()
        
        # --- CONSTRUÇÃO DO VISUAL DO PERFIL ---
        self.render_visual_profile()

    def render_header(self):
        """
        Cria o Header azul sólido no topo da tela
        """
        self.header = ctk.CTkFrame(self, fg_color=AZUL_SENAC, height=100, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Título dentro da Header (Lado Esquerdo)
        ctk.CTkLabel(
            self.header, 
            text="👤 Meu Perfil Acadêmico", 
            font=ctk.CTkFont(size=26, weight="bold"), 
            text_color=BRANCO
        ) .pack(side="left", padx=30)

        # Container de Ações (Lado Direito)
        self.header_actions = ctk.CTkFrame(self.header, fg_color="transparent")
        self.header_actions.pack(side="right", padx=30)

    def render_visual_profile(self):
        """
        Replicando o visual do perfil dentro do frame scrollable
        """
        
        # --- CARD DE PERFIL (profile-card) ---
        profile_card = ctk.CTkFrame(self.main_content_frame, fg_color=self.branco, corner_radius=30)
        profile_card.pack(fill="x", pady=(0, 20))

        # Layout do Header do Card (Foto + Info)
        header_layout = ctk.CTkFrame(profile_card, fg_color="transparent")
        header_layout.pack(fill="x", padx=25, pady=25)

        # Container da Foto
        foto_container = ctk.CTkFrame(header_layout, fg_color="transparent")
        foto_container.pack(side="left")

        self.lbl_foto = ctk.CTkLabel(
            foto_container, 
            text="👤", 
            font=("Arial", 60),
            width=110, 
            height=110, 
            fg_color="#E0E0E0", 
            corner_radius=55
        )
        self.lbl_foto.pack()

        # Informações do Perfil
        info_frame = ctk.CTkFrame(header_layout, fg_color="transparent")
        info_frame.pack(side="left", padx=25, fill="both", expand=True)

        ctk.CTkLabel(info_frame, text="Nome do Aluno Sobrenome", 
                     font=("Roboto", 26, "bold"), text_color=AZUL_SENAC).pack(anchor="w")

        # Badge da Turma
        badge_turma = ctk.CTkLabel(info_frame, text=" Turma 1024-X - ADS (Noite) ", 
                                   fg_color=AZUL_SENAC, text_color="white", 
                                   corner_radius=12, font=("Roboto", 12, "bold"))
        badge_turma.pack(anchor="w", pady=5)

        ctk.CTkLabel(info_frame, text="Descrição do perfil acadêmico e biografia do aluno...", 
                     font=("Roboto", 14), text_color=self.cinza_texto, wraplength=500, justify="left").pack(anchor="w", pady=5)

        # Botão Editar Perfil (Dentro do Card)
        ctk.CTkButton(profile_card, text="✎ Editar Perfil", fg_color=self.verde_sucesso, 
                      width=130, height=35, corner_radius=20).place(relx=0.97, rely=0.15, anchor="ne")

        # --- SEÇÃO DE CERTIFICADOS ---
        self.create_section_title("🎓 Meus Certificados", show_add=True)
        
        cert_grid = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        cert_grid.pack(fill="x", pady=10)
        cert_grid.columnconfigure((0, 1), weight=1)

        for i in range(2):
            card = ctk.CTkFrame(cert_grid, fg_color=self.branco, corner_radius=12, border_width=1, border_color="#E0E0E0")
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkFrame(card, width=4, fg_color=AZUL_SENAC).pack(side="left", fill="y")
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=15, pady=15)
            
            ctk.CTkLabel(content, text="📜 Nome do Certificado", font=("Roboto", 16, "bold"), text_color="#333").pack(anchor="w")
            ctk.CTkLabel(content, text="Descrição breve do certificado...", font=("Roboto", 13), text_color=self.cinza_texto).pack(anchor="w", pady=5)
            
            actions = ctk.CTkFrame(content, fg_color="transparent")
            actions.pack(fill="x", pady=(10, 0))
            ctk.CTkButton(actions, text="Editar", width=70, height=28, fg_color=AZUL_SENAC).pack(side="left", padx=5)
            ctk.CTkButton(actions, text="Excluir", width=70, height=28, fg_color="#FF4D4D").pack(side="left")

        # --- SEÇÃO DE PROJETOS ---
        self.create_section_title("📊 Projetos que participo", show_add=False)
        
        proj_grid = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        proj_grid.pack(fill="x", pady=10)
        proj_grid.columnconfigure((0, 1, 2), weight=1)

        for i in range(3):
            card = ctk.CTkFrame(proj_grid, fg_color=self.branco, corner_radius=12, border_width=1, border_color="#E0E0E0")
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text="Projeto InovaEdu", font=("Roboto", 16, "bold"), text_color=AZUL_SENAC).pack(pady=(15, 5))
            ctk.CTkLabel(card, text="👥 ADS - 2026", font=("Roboto", 12), text_color=self.cinza_texto).pack()
            
            ctk.CTkButton(card, text="📂 Entrar no Repositório", fg_color=AZUL_SENAC, height=32).pack(pady=20, padx=20, fill="x")

    def create_section_title(self, text, show_add=False):
        frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(20, 10), padx=5)
        
        ctk.CTkLabel(frame, text=text, font=("Roboto", 20, "bold"), text_color=AZUL_SENAC).pack(side="left")
        
        if show_add:
            ctk.CTkButton(frame, text="+ Adicionar", fg_color=self.verde_sucesso, width=100, corner_radius=20).pack(side="right")

    def create_directories(self):
        os.makedirs("assets", exist_ok=True)
        os.makedirs("certificados", exist_ok=True)
        os.makedirs("dados_usuario", exist_ok=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = ctk.CTk()
    app.geometry("1200x800")
    
    # Simulação da tela de perfil ocupando o espaço ao lado da sidebar
    app_frame = UserProfileSystem(master=app)
    app_frame.pack(fill="both", expand=True) 
    
    app.mainloop()