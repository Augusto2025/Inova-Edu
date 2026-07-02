import customtkinter as ctk
from tkinter import filedialog, messagebox
from models.sessao import UsuarioSessao 

# --- IMPORTS PARA TRATAMENTO DE IMAGEM DA WEB E LOCAL ---
from PIL import Image
import urllib.request
import io
import threading
import os

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
        # Variável temporária para armazenar o caminho local do novo arquivo de foto selecionado
        self.caminho_nova_foto_local = None

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
        
        # Dispara a busca automática da foto atual do banco de dados de forma assíncrona
        self.inicializar_foto_atual()

    def render_header(self):
        from assets.header import HeaderPadrao
        self.header = HeaderPadrao(self, titulo="Editar Perfil Acadêmico", comando_voltar=self.voltar_perfil)

    def render_tela(self):
        self.main_content = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.main_content.pack(pady=40, padx=50, fill="x")

        # --- SEÇÃO FOTO INTEGRADA COM BOTÃO ---
        foto_section = ctk.CTkFrame(self.main_content, fg_color="transparent")
        foto_section.pack(fill="x", pady=(0, 40))
        
        self.borda_foto = ctk.CTkFrame(foto_section, width=180, height=180, corner_radius=90, fg_color=AZUL_SENAC)
        self.borda_foto.pack(side="left", padx=(0, 30))
        self.borda_foto.pack_propagate(False)
        
        self.lbl_foto = ctk.CTkLabel(self.borda_foto, text="👤", font=("Arial", 75), width=172, height=172, fg_color=CINZA_CLARO, corner_radius=86)
        self.lbl_foto.place(relx=0.5, rely=0.5, anchor="center")

        # Container dos botões do lado da foto
        botoes_foto_frame = ctk.CTkFrame(foto_section, fg_color="transparent")
        botoes_foto_frame.pack(side="left", fill="y", expand=True, pady=10)
        
        ctk.CTkLabel(botoes_foto_frame, text="Foto de Perfil", font=("Roboto", 16, "bold"), text_color=AZUL_SENAC).pack(anchor="w")
        ctk.CTkLabel(botoes_foto_frame, text="Escolha uma imagem quadrada JPG ou PNG.", font=("Roboto", 12), text_color="#64748B").pack(anchor="w", pady=(0, 15))
        
        self.btn_alterar_foto = ctk.CTkButton(
            botoes_foto_frame, text="📁 Selecionar Nova Imagem", fg_color=AZUL_SENAC, hover_color="#003566",
            height=35, font=("Roboto", 13, "bold"), command=self.escolher_imagem
        )
        self.btn_alterar_foto.pack(anchor="w")

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

    # --- LÓGICA DE CARREGAMENTO ASSÍNCRONO DA FOTO ATUAL ---
    def inicializar_foto_atual(self):
        """Monta o link com base no que está salvo na base e inicia o download da imagem atual"""
        u = self.dados_banco
        imagem_bruta = u.get('imagem') or u.get('imagem_usuario') or u.get('Imagem')
        
        if imagem_bruta:
            imagem_str = str(imagem_bruta).strip()
            if imagem_str.startswith("http"):
                url_final = imagem_str
            else:
                # Carrega o .env localizado em controllers/
                from dotenv import load_dotenv
                diretorio_atual = os.path.dirname(os.path.abspath(__file__))
                # Ajusta o caminho se esta view estiver em views/Aluno_e_Professor/
                caminho_controllers_env = os.path.join(os.path.dirname(diretorio_atual), '..', 'controllers', '.env')
                load_dotenv(caminho_controllers_env)
                
                cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME") or "dw0pxfap3"
                url_final = f"https://res.cloudinary.com/{cloud_name}/image/upload/{imagem_str}" if "image/upload/" not in imagem_str else f"https://res.cloudinary.com/{cloud_name}/{imagem_str}"
            
            # Executa a thread para baixar a foto atual
            def thread_task():
                try:
                    with urllib.request.urlopen(url_final) as resposta:
                        dados = resposta.read()
                    img_pil = Image.open(io.BytesIO(dados))
                    ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(172, 172))
                    self.janela.after(0, lambda: self.aplicar_foto_na_lbl(ctk_img))
                except Exception as e:
                    print(f"[EDIT PERFIL] Falha ao carregar imagem atual: {e}")

            threading.Thread(target=thread_task, daemon=True).start()

    def aplicar_foto_na_lbl(self, ctk_img):
        """Aplica a foto com segurança checando se o widget ainda existe na memória"""
        try:
            if self.winfo_exists() and hasattr(self, 'lbl_foto') and self.lbl_foto.winfo_exists():
                self.lbl_foto.configure(image=ctk_img, text="")
                self.lbl_foto._image = ctk_img
        except Exception as e:
            print(f"[EDIT] Download concluído após o fechamento da tela: {e}")

    # --- LÓGICA DE SELEÇÃO DE IMAGEM LOCAL ---
    def escolher_imagem(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
        if caminho_arquivo:
            self.caminho_nova_foto_local = caminho_arquivo
            
            # Carrega a imagem local no preview redondo imediatamente
            try:
                img_pil = Image.open(caminho_arquivo)
                ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(172, 172))
                self.aplicar_foto_na_lbl(ctk_img)
                self.btn_alterar_foto.configure(text="✅ Foto Selecionada", fg_color="#22c55e")
            except Exception as e:
                messagebox.showerror("Erro de Imagem", f"Não foi possível abrir o arquivo: {e}")

    def abrir_modal_senha(self):
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Alteração de Segurança")
        modal.geometry("500x420")
        modal.grab_set()
        modal.configure(fg_color="#f5f7fb")
        modal.resizable(False, False)
        modal.after(10, lambda: modal.focus_force())

        m_header = ctk.CTkFrame(modal, fg_color=AZUL_SENAC, corner_radius=0, height=60)
        m_header.pack(fill="x")
        ctk.CTkLabel(m_header, text="🔒 Alterar Senha de Acesso", font=ctk.CTkFont(size=16, weight="bold"), text_color=BRANCO).pack(pady=15)

        content = ctk.CTkFrame(modal, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(content, text="Nova Senha:", font=ctk.CTkFont(weight="bold"), text_color=AZUL_SENAC).pack(anchor="w", pady=(5, 5))
        txt_nova = ctk.CTkEntry(content, fg_color=BRANCO, border_color=CINZA_SENAC, border_width=2, height=40, corner_radius=8, show="*")
        txt_nova.pack(fill="x", pady=(0, 15))

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
                
            self.nova_senha_definida = senha
            self.btn_senha_modal.configure(text="✅ Senha Alterada (Pronta)", fg_color="#22c55e", hover_color="#16a34a")
            modal.destroy()

        ctk.CTkButton(modal, text="Confirmar Nova Senha", fg_color=AZUL_SENAC, hover_color="#003566", text_color=BRANCO, height=45, font=("Roboto", 14, "bold"),
                      command=validar_e_aplicar).pack(fill="x", padx=40, pady=(0, 25))

    def salvar_alteracoes(self):
        nome = self.ent_nome.get()
        sobrenome = self.ent_sobrenome.get()
        bio = self.txt_desc.get("0.0", "end").strip()
        
        # Busca a senha que veio direto do banco de dados (respeitando maiúsculo/minúsculo do seu Model)
        senha_atual_banco = self.dados_banco.get('senha') or self.dados_banco.get('Senha')

        # Se o usuário definiu uma nova no modal, usa a nova. Se não, mantém a atual do banco.
        senha_final = self.nova_senha_definida if self.nova_senha_definida else senha_atual_banco
        
        # --- PASSO IMPORTANTE: ---
        # Enviamos o caminho local do arquivo (self.caminho_nova_foto_local) para o seu Controller.
        # Caso o usuário não tenha selecionado uma imagem nova, ele passará None.
        if hasattr(self.controller, 'salvar_alteracoes_perfil_com_foto'):
            self.controller.salvar_alteracoes_perfil_com_foto(nome, sobrenome, bio, senha_final, self.caminho_nova_foto_local)
        else:
            # Fallback seguro caso você opte por adicionar o argumento direto na função antiga
            try:
                self.controller.salvar_alteracoes_perfil(nome, sobrenome, bio, senha_final, self.caminho_nova_foto_local)
            except TypeError:
                self.controller.salvar_alteracoes_perfil(nome, sobrenome, bio, senha_final)

        self.sessao.nome = nome
        self.sessao.sobrenome = sobrenome
        self.sessao.senha = senha_final
        self.sessao.descricao = bio

        self.voltar_perfil()

    def voltar_perfil(self):
        from views.Aluno_e_Professor.profile_view import UserProfileSystem
    
        for widget in list(self.janela.winfo_children()):
            if widget.__class__.__name__ in ["EditarPerfilView", "UserProfileSystem"]:
                widget.pack_forget()
                widget.destroy()
        
        email_sessao = self.sessao.email
        tela_perfil = UserProfileSystem(master=self.janela, email_usuario=email_sessao)
        tela_perfil.pack(side="right", fill="both", expand=True)