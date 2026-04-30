from tkinter import messagebox
import customtkinter as ctk
import sys
import os
from views.Aluno_e_Professor.editar_view import EditarPerfilView
from models.sessao import UsuarioSessao
from controllers.perfil_controller import ProfileController

# Constantes de Estilo
AZUL_SENAC = "#004A8D"
LARANJA_SENAC = "#F7941D"
BRANCO = "#FFFFFF"
CINZA_FUNDO = "#F0F2F5"

class UserProfileSystem(ctk.CTkFrame):
    def __init__(self, master=None, email_usuario=None):
        super().__init__(master, fg_color=CINZA_FUNDO) 
        self.janela = master
        
        self.sessao = UsuarioSessao()
        self.email = email_usuario if email_usuario else self.sessao.email

        self.controller = ProfileController(self, self.email)
        self.configurar_sidebar()
        
        self.render_header()
        
        self.main_content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.render_visual_profile()

        # Controle de estado do Acordeão
        self.form_aberto = False 

        self.render_visual_sections()
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
            self.header, text="Perfil Acadêmico", 
            font=("Roboto", 22, "bold"), text_color=BRANCO
        ).pack(side="left", padx=30)

        # SUBSTITUÍDO: Botão Atualizar -> Botão Editar Perfil
        ctk.CTkButton(
            self.header, 
            text="✏️ Editar Perfil", # Texto alterado
            width=140, 
            height=35,
            fg_color=AZUL_SENAC, 
            hover_color="#107FE7",
            border_width=1,
            border_color=BRANCO,
            font=("Roboto", 13, "bold"),
            command=self.ir_para_edicao # Comando alterado para a nova função
        ).pack(side="right", padx=30)

    def ir_para_edicao(self):
        """Esconde o perfil atual e abre a tela de edição."""
        # Obtemos os dados atuais do usuário através do model/controller
        dados_completos = self.controller.model.obter_dados_perfil(self.email)
        
        # Formatamos um dicionário simples para a tela de edição
        usuario = dados_completos.get('usuario', {})
        dados_formatados = {
            "nome": usuario.get('nome') or usuario.get('Nome') or "",
            "sobrenome": usuario.get('sobrenome') or usuario.get('Sobrenome') or "",
            "email": self.email,
            "descricao": usuario.get('descricao') or usuario.get('Descricao') or ""
        }

        self.pack_forget() # Esconde a tela de perfil
        
        # Instancia a EditarPerfilView (aquela que fizemos baseada no seu Django)
        # Ela será renderizada dentro do mesmo master (self.janela)
        EditarPerfilView(self.janela, dados_formatados, self.controller)

    def render_visual_profile(self):
        profile_card = ctk.CTkFrame(self.main_content_frame, fg_color=BRANCO, corner_radius=20)
        profile_card.pack(fill="x", pady=(0, 20))

        header_layout = ctk.CTkFrame(profile_card, fg_color="transparent")
        header_layout.pack(fill="x", padx=25, pady=25)

        self.lbl_foto = ctk.CTkLabel(header_layout, text="👤", font=("Arial", 50),
                                     width=100, height=100, fg_color="#F1F5F9", corner_radius=50)
        self.lbl_foto.pack(side="left")

        info_frame = ctk.CTkFrame(header_layout, fg_color="transparent")
        info_frame.pack(side="left", padx=25, fill="both", expand=True)

        self.lbl_nome_usuario = ctk.CTkLabel(info_frame, text="Buscando...", font=("Roboto", 24, "bold"), text_color=AZUL_SENAC)
        self.lbl_nome_usuario.pack(anchor="w")

        self.lbl_badge_turma = ctk.CTkLabel(info_frame, text=" -- ", fg_color="#94A3B8", text_color="white", corner_radius=10, font=("Roboto", 11, "bold"))
        self.lbl_badge_turma.pack(anchor="w", pady=5)

        self.lbl_descricao_usuario = ctk.CTkLabel(info_frame, text="", font=("Roboto", 14), text_color="#64748B", wraplength=600, justify="left")
        self.lbl_descricao_usuario.pack(anchor="w", pady=5)

    def render_visual_sections(self):
        self.create_section_title("🎓 Meus Certificados", is_accordion=True)
        
        self.form_frame = ctk.CTkFrame(self.main_content_frame, fg_color="#E2E8F0", corner_radius=15)
        
        self.cert_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.cert_container.pack(fill="x", pady=10) 

        self.create_section_title("📊 Projetos Ativos", is_accordion=False)
        self.proj_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.proj_container.pack(fill="x", pady=10)

    # --- NOVOS MÉTODOS DE RENDERIZAÇÃO DE PROJETOS ---

    def renderizar_projetos(self, projetos):
        """Renderiza os cards de repositórios/projetos no container."""
        for widget in self.proj_container.winfo_children():
            widget.destroy()
        
        if not projetos:
            ctk.CTkLabel(
                self.proj_container, 
                text="Você ainda não participa de nenhum projeto.", 
                text_color="#94A3B8", 
                font=("Roboto", 13, "italic")
            ).pack(pady=20)
            return

        grid_projetos = ctk.CTkFrame(self.proj_container, fg_color="transparent")
        grid_projetos.pack(fill="x", padx=5)
        grid_projetos.columnconfigure((0, 1, 2), weight=1)

        for i, proj in enumerate(projetos):
            # LÓGICA DE CAPTURA SEGURA:
            # Tenta pegar 'nome_projeto' (alias da query), 'Nome_projeto' (banco) ou 'nome' (fallback)
            nome_exibir = proj.get('nome_projeto') or proj.get('Nome_projeto') or proj.get('nome') or "Projeto Sem Nome"
            id_projeto = proj.get('idprojeto') or proj.get('idProjeto') or proj.get('id')

            card = ctk.CTkFrame(
                grid_projetos, 
                fg_color=BRANCO, 
                height=130, 
                corner_radius=12, 
                border_width=1, 
                border_color="#CBD5E1"
            )
            card.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
            card.pack_propagate(False)

            # Rótulo do Nome do Projeto
            lbl_nome = ctk.CTkLabel(
                card, 
                text=nome_exibir, # Variável tratada acima
                font=("Roboto", 15, "bold"), 
                text_color=AZUL_SENAC,
                wraplength=180
            )
            lbl_nome.pack(expand=True, pady=(10, 0))

            btn_entrar = ctk.CTkButton(
                card, 
                text="Entrar no Repositório", 
                height=32, 
                fg_color=AZUL_SENAC, 
                hover_color="#003566",
                font=("Roboto", 12, "bold"),
                command=lambda p=id_projeto, n=nome_exibir: self.abrir_repositorio(p, n)
            )
            btn_entrar.pack(side="bottom", fill="x", padx=15, pady=15)

    def abrir_repositorio(self, id_projeto, nome_projeto):
        """Navega para a tela do repositório selecionado."""
        from views.Aluno_e_Professor.repositorio_view import RepositorioDashboard
        
        # Esconde o frame de perfil para mostrar o repositório
        self.pack_forget()
        
        # Instancia a nova tela no mesmo master
        RepositorioDashboard(self.janela, turma_id=id_projeto, nome_projeto=nome_projeto)

    # --- FIM DOS NOVOS MÉTODOS ---

    def toggle_formulario(self):
        if not self.form_aberto:
            self.render_campos_formulario()
            self.form_frame.pack(fill="x", padx=10, pady=10, before=self.cert_container)
            self.btn_toggle.configure(text="✕ Fechar", fg_color="#EF4444", hover_color="#DC2626")
            self.form_aberto = True
        else:
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            self.form_frame.pack_forget()
            self.btn_toggle.configure(text="+ Novo", fg_color="#22C55E", hover_color="#16A34A")
            self.form_aberto = False

    def render_campos_formulario(self):
        self.form_frame.columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(self.form_frame, text="Cadastrar Novo Certificado", 
                     font=("Roboto", 16, "bold"), text_color=AZUL_SENAC).grid(row=0, column=0, columnspan=2, pady=(15, 10), padx=20, sticky="w")

        self.ent_nome = self.criar_input(self.form_frame, "Nome do Curso:", 1, 0)
        self.ent_desc = self.criar_input(self.form_frame, "Descrição:", 1, 1)
        self.ent_ini = self.criar_input(self.form_frame, "Data Início (AAAA-MM-DD):", 2, 0)
        self.ent_fim = self.criar_input(self.form_frame, "Data Fim (AAAA-MM-DD):", 2, 1)

        btn_salvar = ctk.CTkButton(self.form_frame, text="SALVAR CERTIFICADO", 
                                   fg_color=LARANJA_SENAC, hover_color="#E68510",
                                   font=("Roboto", 13, "bold"), height=40, command=self.salvar_pelo_acordeao)
        btn_salvar.grid(row=3, column=1, columnspan=1, pady=20, padx=20, sticky="ew")

    def criar_input(self, master, label, r, c):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.grid(row=r, column=c, padx=20, pady=5, sticky="ew")
        ctk.CTkLabel(f, text=label, font=("Roboto", 11, "bold"), text_color="#475569").pack(anchor="w")
        entry = ctk.CTkEntry(f, height=35, fg_color=BRANCO, border_color="#CBD5E1")
        entry.pack(fill="x", pady=2)
        return entry

    def salvar_pelo_acordeao(self):
        dados = self.controller.model.obter_dados_perfil(self.email)
        id_u = dados['usuario'].get('idusuario') or dados['usuario'].get('idUsuario')
        
        if not self.ent_nome.get() or not self.ent_ini.get():
            messagebox.showwarning("Aviso", "Nome e Data de Início são obrigatórios.")
            return

        sucesso = self.controller.model.salvar_certificado(
            self.ent_nome.get(), self.ent_desc.get(), self.ent_ini.get(), self.ent_fim.get(), id_u
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Certificado Adicionado!")
            self.toggle_formulario() 
            self.controller.inicializar_perfil() 
        else:
            messagebox.showerror("Erro", "Falha ao salvar. Verifique o formato da data.")

    def renderizar_certificados(self, certificados):
        for widget in self.cert_container.winfo_children(): widget.destroy()
        
        if not certificados:
            ctk.CTkLabel(self.cert_container, text="Nenhum certificado cadastrado.", 
                         text_color="#94A3B8", font=("Roboto", 13, "italic")).pack(pady=20)
            return

        grid = ctk.CTkFrame(self.cert_container, fg_color="transparent")
        grid.pack(fill="x")
        grid.columnconfigure((0, 1, 2), weight=1)

        for i, cert in enumerate(certificados):
            nome = cert.get('nome') or cert.get('Nome')
            desc = cert.get('descricao') or "Sem descrição disponível"
            inicio = cert.get('data_inicio') or "--"
            fim = cert.get('data_final') or "--"
            id_c = cert.get('idcertificado') or cert.get('idCertificado')
            
            card = ctk.CTkFrame(grid, fg_color=BRANCO, corner_radius=15, border_width=1, border_color="#E2E8F0")
            card.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")

            accent_bar = ctk.CTkFrame(card, fg_color=LARANJA_SENAC, width=4)
            accent_bar.pack(side="left", fill="y")
            
            inner_content = ctk.CTkFrame(card, fg_color="transparent")
            inner_content.pack(side="left", fill="both", expand=True, padx=15, pady=15)
            
            ctk.CTkLabel(inner_content, text="CERTIFICADO", font=("Roboto", 10, "bold"), 
                         text_color=LARANJA_SENAC).pack(anchor="w")
            
            ctk.CTkLabel(inner_content, text=nome, font=("Roboto", 15, "bold"), 
                         text_color=AZUL_SENAC, wraplength=200, justify="left").pack(anchor="w", pady=(2, 0))
            
            ctk.CTkLabel(inner_content, text=desc, font=("Roboto", 12), 
                         text_color="#64748B", wraplength=200, justify="left").pack(anchor="w", pady=5)
            
            footer = ctk.CTkFrame(inner_content, fg_color="#F8FAFC", corner_radius=5)
            footer.pack(fill="x", pady=5)
            ctk.CTkLabel(footer, text=f"📅 {inicio} • {fim}", font=("Roboto", 11), 
                         text_color="#475569").pack(padx=5, pady=2)
            
            ctk.CTkButton(inner_content, text="Remover", fg_color="transparent", text_color="#EF4444", 
                          hover_color="#FEE2E2", height=20, width=60, font=("Roboto", 11, "bold"),
                          command=lambda c=id_c: self.controller.operacao_certificado('EXCLUIR', cert_id=c)).pack(anchor="e", pady=(5,0))

    def create_section_title(self, text, is_accordion=False):
        frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(20, 5), padx=5)
        ctk.CTkLabel(frame, text=text, font=("Roboto", 18, "bold"), text_color=AZUL_SENAC).pack(side="left")
        
        if is_accordion:
            self.btn_toggle = ctk.CTkButton(frame, text="+ Novo", fg_color="#22C55E", hover_color="#16A34A", 
                                            width=80, height=28, corner_radius=15, command=self.toggle_formulario)
            self.btn_toggle.pack(side="right")

    def atualizar_dados_principais(self, nome, sobrenome, descricao, turma_nome):
        self.lbl_nome_usuario.configure(text=f"{nome} {sobrenome}")
        self.lbl_descricao_usuario.configure(text=descricao if descricao else "Estudante Senac")
        self.lbl_badge_turma.configure(text=f" {turma_nome} ", fg_color=AZUL_SENAC)

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x700")
    UserProfileSystem(master=app).pack(fill="both", expand=True) 
    app.mainloop()