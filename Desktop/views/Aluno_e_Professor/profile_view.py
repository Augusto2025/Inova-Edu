from tkinter import messagebox

import customtkinter as ctk
import sys
import os
from models.sessao import UsuarioSessao
from controllers.perfil_controller import ProfileController

# Constantes de Estilo
AZUL_SENAC = "#004A8D"
BRANCO = "#FFFFFF"

class UserProfileSystem(ctk.CTkFrame):
    def __init__(self, master=None, email_usuario=None):
        super().__init__(master, fg_color="#F0F2F5") 
        self.janela = master
        
        # Gerenciamento de Identidade (Sessão Global ou Parâmetro)
        self.sessao = UsuarioSessao()
        self.email = email_usuario if email_usuario else self.sessao.email

        # 1. Instanciar o Controller (Ele é quem vai ao banco por você)
        self.controller = ProfileController(self, self.email)

        # 2. Garantir a Sidebar (Reutilizando sua lógica)
        self.configurar_sidebar()
        
        # 3. Construção da Interface
        self.render_header()
        
        self.main_content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.render_visual_profile()

        # 4. DISPARAR BUSCA NO BANCO
        # O controller vai buscar no banco e chamar 'atualizar_dados_principais'
        self.controller.inicializar_perfil()

    def configurar_sidebar(self):
        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break
        if not sidebar_existente:
            sidebar(self.janela)

    def render_header(self):
        self.header = ctk.CTkFrame(self, fg_color=AZUL_SENAC, height=80, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header, text="👤 Perfil Acadêmico", 
            font=ctk.CTkFont(size=22, weight="bold"), text_color=BRANCO
        ).pack(side="left", padx=30)

        # Botão de Refresh (Puxa do banco novamente)
        ctk.CTkButton(
            self.header, text="🔄 Atualizar", width=100, height=30,
            fg_color="#F7941D", hover_color="#E68510",
            command=self.controller.inicializar_perfil 
        ).pack(side="right", padx=30)

    def render_visual_profile(self):
        # Card Principal de Informações
        profile_card = ctk.CTkFrame(self.main_content_frame, fg_color=BRANCO, corner_radius=20)
        profile_card.pack(fill="x", pady=(0, 20))

        header_layout = ctk.CTkFrame(profile_card, fg_color="transparent")
        header_layout.pack(fill="x", padx=25, pady=25)

        # Foto (Apenas visual agora)
        self.lbl_foto = ctk.CTkLabel(
            header_layout, text="👤", font=("Arial", 50),
            width=100, height=100, fg_color="#F1F5F9", corner_radius=50
        )
        self.lbl_foto.pack(side="left")

        # Dados do Usuário
        info_frame = ctk.CTkFrame(header_layout, fg_color="transparent")
        info_frame.pack(side="left", padx=25, fill="both", expand=True)

        self.lbl_nome_usuario = ctk.CTkLabel(info_frame, text="Buscando no banco...", 
                                             font=("Roboto", 24, "bold"), text_color=AZUL_SENAC)
        self.lbl_nome_usuario.pack(anchor="w")

        self.lbl_badge_turma = ctk.CTkLabel(info_frame, text=" -- ", 
                                           fg_color="#94A3B8", text_color="white", 
                                           corner_radius=10, font=("Roboto", 11, "bold"))
        self.lbl_badge_turma.pack(anchor="w", pady=5)

        self.lbl_descricao_usuario = ctk.CTkLabel(info_frame, text="", 
                                                 font=("Roboto", 14), text_color="#64748B", 
                                                 wraplength=600, justify="left")
        self.lbl_descricao_usuario.pack(anchor="w", pady=5)

        # --- SEÇÕES DE CONTEÚDO ---
        self.create_section_title("🎓 Meus Certificados", show_add=True)
        self.cert_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.cert_container.pack(fill="x", pady=10) 

        self.create_section_title("📊 Projetos Ativos", show_add=False)
        self.proj_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.proj_container.pack(fill="x", pady=10)

    # --- MÉTODOS DE ATUALIZAÇÃO (CHAMADOS PELO CONTROLLER) ---

    def atualizar_dados_principais(self, nome, sobrenome, descricao, turma_nome):
        self.lbl_nome_usuario.configure(text=f"{nome} {sobrenome}")
        self.lbl_descricao_usuario.configure(text=descricao if descricao else "Estudante Senac")
        self.lbl_badge_turma.configure(text=f" {turma_nome} ", fg_color=AZUL_SENAC)

    def renderizar_certificados(self, certificados):
        """Limpa e recria a lista de certificados vinda do banco"""
        for widget in self.cert_container.winfo_children():
            widget.destroy()
        
        if not certificados:
            ctk.CTkLabel(self.cert_container, text="Nenhum certificado cadastrado.", 
                         text_color="#94A3B8").pack(pady=10)
            return

        for cert in certificados:
            # Tratamento para chaves do Postgres (minúsculas)
            nome = cert.get('nome') or cert.get('Nome')
            id_c = cert.get('idcertificado') or cert.get('idCertificado')

            card = ctk.CTkFrame(self.cert_container, fg_color=BRANCO, corner_radius=12, border_width=1, border_color="#E2E8F0")
            card.pack(side="left", padx=10, pady=10, ipadx=10, ipady=10)
            
            ctk.CTkLabel(card, text=f"📜 {nome}", font=("Roboto", 13, "bold")).pack(pady=5)
            
            ctk.CTkButton(
                card, text="Remover", fg_color="#FEE2E2", text_color="#EF4444", 
                hover_color="#FECACA", height=24, width=80,
                command=lambda c=id_c: self.controller.operacao_certificado('EXCLUIR', cert_id=c)
            ).pack(pady=5)

    def create_section_title(self, text, show_add=False):
        frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(20, 5), padx=5)
        ctk.CTkLabel(frame, text=text, font=("Roboto", 18, "bold"), text_color=AZUL_SENAC).pack(side="left")
        
        if show_add:
            ctk.CTkButton(
                frame, text="+ Novo", fg_color="#22C55E", hover_color="#16A34A",
                width=70, height=28, corner_radius=15,
                # AGORA CHAMA O MÉTODO LOCAL
                command=self.abrir_modal_cadastro 
            ).pack(side="right")

    def abrir_modal_cadastro(self):
        # 1. Pegar o ID do usuário (precisamos dele para o INSERT)
        dados = self.controller.model.obter_dados_perfil(self.email)
        if not dados:
            messagebox.showerror("Erro", "Não foi possível recuperar dados do usuário.")
            return
        
        usuario = dados['usuario']
        id_usuario = usuario.get('idusuario') or usuario.get('idUsuario')

        # 2. Criar a Janela Modal
        modal = ctk.CTkToplevel(self)
        modal.title("Novo Certificado")
        modal.geometry("400x500")
        modal.attributes("-topmost", True)
        modal.grab_set()

        ctk.CTkLabel(modal, text="📜 Cadastrar Certificado", font=("Roboto", 16, "bold")).pack(pady=20)

        # Campos
        ctk.CTkLabel(modal, text="Nome:").pack()
        ent_nome = ctk.CTkEntry(modal, width=250)
        ent_nome.pack(pady=5)

        ctk.CTkLabel(modal, text="Descrição:").pack()
        ent_desc = ctk.CTkEntry(modal, width=250)
        ent_desc.pack(pady=5)

        ctk.CTkLabel(modal, text="Início (AAAA-MM-DD):").pack()
        ent_ini = ctk.CTkEntry(modal, width=250, placeholder_text="2024-01-01")
        ent_ini.pack(pady=5)

        ctk.CTkLabel(modal, text="Fim (AAAA-MM-DD):").pack()
        ent_fim = ctk.CTkEntry(modal, width=250, placeholder_text="2024-12-31")
        ent_fim.pack(pady=5)

        def salvar():
            # Chamamos o model através do controller que já está instanciado
            sucesso = self.controller.model.salvar_certificado(
                ent_nome.get(), ent_desc.get(), 
                ent_ini.get(), ent_fim.get(), id_usuario
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Certificado Salvo!")
                modal.destroy()
                self.controller.inicializar_perfil() # Recarrega a tela
            else:
                messagebox.showerror("Erro", "Verifique os dados (especialmente a data).")

        ctk.CTkButton(modal, text="Confirmar", fg_color="#22C55E", command=salvar).pack(pady=20)

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x700")
    # Aqui o app_frame vai buscar os dados automaticamente no banco
    app_frame = UserProfileSystem(master=app) 
    app_frame.pack(fill="both", expand=True) 
    app.mainloop()