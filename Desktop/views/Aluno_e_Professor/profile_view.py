import customtkinter as ctk
import os
import sys
from datetime import datetime
# Importação do Controller
from controllers.perfil_controller import ProfileController

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

AZUL_SENAC = "#004A8D"
BRANCO = "#FFFFFF"

class UserProfileSystem(ctk.CTkFrame):
    def __init__(self, master=None, email_usuario=None):
        super().__init__(master, fg_color="#F0F2F5") 
        self.janela = master
        self.email_usuario = email_usuario

        # Cores
        self.laranja_senac = "#F7941D"
        self.branco = BRANCO
        self.cinza_texto = "#666666"
        self.verde_sucesso = "#28a745"

        # 1. Instanciar o Controller
        self.controller = ProfileController(self, self.email_usuario)

        # 2. Sidebar
        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break
        if not sidebar_existente:
            sidebar(self.janela)
        
        # 3. Interface
        self.render_header()
        
        self.main_content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.create_directories()
        self.render_visual_profile()

        # 4. CARREGAR DADOS INICIAIS VIA CONTROLLER
        self.controller.inicializar_perfil()

    def render_header(self):
        self.header = ctk.CTkFrame(self, fg_color=AZUL_SENAC, height=100, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header, 
            text="👤 Meu Perfil Acadêmico", 
            font=ctk.CTkFont(size=26, weight="bold"), 
            text_color=BRANCO
        ).pack(side="left", padx=30)

        self.header_actions = ctk.CTkFrame(self.header, fg_color="transparent")
        self.header_actions.pack(side="right", padx=30)

        # Botão Atualizar (Estilo "Hoje")
        ctk.CTkButton(
            self.header_actions, text="Atualizar Dados", width=140, height=35,
            fg_color=BRANCO, text_color=AZUL_SENAC, font=ctk.CTkFont(weight="bold"),
            command=self.controller.inicializar_perfil 
        ).pack(side="left", padx=10)

    def render_visual_profile(self):
        # --- CARD DE PERFIL ---
        profile_card = ctk.CTkFrame(self.main_content_frame, fg_color=self.branco, corner_radius=30)
        profile_card.pack(fill="x", pady=(0, 20))

        header_layout = ctk.CTkFrame(profile_card, fg_color="transparent")
        header_layout.pack(fill="x", padx=25, pady=25)

        # Foto
        foto_container = ctk.CTkFrame(header_layout, fg_color="transparent")
        foto_container.pack(side="left")
        self.lbl_foto = ctk.CTkLabel(
            foto_container, text="👤", font=("Arial", 60),
            width=110, height=110, fg_color="#E0E0E0", corner_radius=55
        )
        self.lbl_foto.pack()
        # Bind para clicar na foto e mudar
        self.lbl_foto.bind("<Button-1>", lambda e: self.controller.gerenciar_foto_perfil())

        # Informações Dinâmicas (Armazenadas em self para o Controller alterar)
        info_frame = ctk.CTkFrame(header_layout, fg_color="transparent")
        info_frame.pack(side="left", padx=25, fill="both", expand=True)

        self.lbl_nome_usuario = ctk.CTkLabel(info_frame, text="Carregando...", 
                                     font=("Roboto", 26, "bold"), text_color=AZUL_SENAC)
        self.lbl_nome_usuario.pack(anchor="w")

        self.lbl_badge_turma = ctk.CTkLabel(info_frame, text=" Sem Turma ", 
                                   fg_color=AZUL_SENAC, text_color="white", 
                                   corner_radius=12, font=("Roboto", 12, "bold"))
        self.lbl_badge_turma.pack(anchor="w", pady=5)

        self.lbl_descricao_usuario = ctk.CTkLabel(info_frame, text="...", 
                                     font=("Roboto", 14), text_color=self.cinza_texto, 
                                     wraplength=500, justify="left")
        self.lbl_descricao_usuario.pack(anchor="w", pady=5)

        # Botão Editar
        ctk.CTkButton(profile_card, text="✎ Editar Perfil", fg_color=self.verde_sucesso, 
                      width=130, height=35, corner_radius=20,
                      command=lambda: self.controller.salvar_alteracoes_perfil("Novo", "Nome", "Nova Bio") # Exemplo
                      ).place(relx=0.97, rely=0.15, anchor="ne")

        # --- SEÇÕES ---
        self.create_section_title("🎓 Meus Certificados", show_add=True)
        self.cert_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.cert_container.pack(fill="x", pady=10)

        self.create_section_title("📊 Projetos que participo", show_add=False)
        self.proj_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.proj_container.pack(fill="x", pady=10)

    # --- MÉTODOS QUE O CONTROLLER VAI USAR ---

    def atualizar_dados_principais(self, nome, sobrenome, descricao, turma_nome):
        """Atualiza os textos principais da tela"""
        self.lbl_nome_usuario.configure(text=f"{nome} {sobrenome}")
        self.lbl_descricao_usuario.configure(text=descricao if descricao else "Estudante Senac")
        if turma_nome:
            self.lbl_badge_turma.configure(text=f" {turma_nome} ")

    def renderizar_certificados(self, certificados):
        """Cria os cards de certificados dinamicamente"""
        for widget in self.cert_container.winfo_children():
            widget.destroy()
        
        for i, cert in enumerate(certificados):
            card = ctk.CTkFrame(self.cert_container, fg_color=self.branco, corner_radius=12)
            card.pack(side="left", padx=10, pady=10, expand=True, fill="both")
            ctk.CTkLabel(card, text=f"📜 {cert['nome']}", font=("Roboto", 14, "bold")).pack(pady=10)
            # Botão excluir chamando controller
            ctk.CTkButton(card, text="Excluir", fg_color="#FF4D4D", height=20,
                          command=lambda c=cert['idCertificado']: self.controller.operacao_certificado('EXCLUIR', cert_id=c)).pack(pady=5)

    def create_section_title(self, text, show_add=False):
        frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(20, 10), padx=5)
        ctk.CTkLabel(frame, text=text, font=("Roboto", 20, "bold"), text_color=AZUL_SENAC).pack(side="left")
        if show_add:
            ctk.CTkButton(frame, text="+ Adicionar", fg_color=self.verde_sucesso, width=100, corner_radius=20,
                          command=lambda: self.controller.operacao_certificado('CRIAR')).pack(side="right")

    def create_directories(self):
        for d in ["assets", "certificados", "dados_usuario"]:
            os.makedirs(d, exist_ok=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = ctk.CTk()
    app.geometry("1200x800")
    app_frame = UserProfileSystem(master=app, email_usuario="teste@senac.com")
    app_frame.pack(fill="both", expand=True) 
    app.mainloop()