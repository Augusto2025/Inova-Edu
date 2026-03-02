import sys
from tkinter import messagebox
import customtkinter as ctk
from controllers.login_controller import autenticar
import threading
from PIL import Image, ImageOps
import os
from assets.cores import *
from assets.fonts import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class tela_login(ctk.CTkFrame):  
    def __init__(self, master):  
        super().__init__(master)
        self.master = master

        # Cores Adicionais para Refinamento
        self.cor_fundo = "#F1F5F9"
        self.cor_borda = "#E2E8F0"
        self.cor_texto_secundario = "#94A3B8"

        self.configure(fg_color=self.cor_fundo) 
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")

        self.container.grid_columnconfigure(0, weight=1) 
        self.container.grid_columnconfigure(1, weight=1) 
        self.container.grid_rowconfigure(0, weight=1)

        # --- LADO ESQUERDO: Branding Experience ---
        self.left = ctk.CTkFrame(self.container, fg_color=azulEscuro, corner_radius=0)
        self.left.grid(row=0, column=0, sticky="nsew")

        # Overlay sutil para textura (Opcional)
        self.brand_content = ctk.CTkFrame(self.left, fg_color="transparent")
        self.brand_content.place(relx=0.5, rely=0.5, anchor="center")

        # Logo centralizado mais alto
        try:
            # Removido "Desktop/" e adicionado resource_path
            caminho_imagem = resource_path("assets/img/LOGOBRANCO.png")
            
            if os.path.exists(caminho_imagem):
                img_pil = Image.open(caminho_imagem)
                self.img_logo = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(180, 220))
                self.logo_label = ctk.CTkLabel(self.brand_content, image=self.img_logo, text="")
                self.logo_label.pack(pady=(0, 20))
            else:
                print(f"[LOGIN] Imagem não encontrada em: {caminho_imagem}")
        except Exception as e:
            print(f"[LOGIN ERRO IMAGEM] {e}")

        ctk.CTkLabel(
            self.brand_content, text="INOVA EDU", 
            font=ctk.CTkFont(family="Inter", size=48, weight="bold"), 
            text_color="white"
        ).pack()

        ctk.CTkFrame(self.brand_content, width=40, height=4, fg_color="#38BDF8").pack(pady=15)

        ctk.CTkLabel(
            self.brand_content, 
            text="Transformando a gestão acadêmica\ncom tecnologia de ponta.", 
            font=ctk.CTkFont(family="Inter", size=18, weight="normal"), 
            text_color="#CBD5E1",
            justify="center"
        ).pack()

        # --- LADO DIREITO: Clean Form ---
        self.right = ctk.CTkFrame(self.container, fg_color="white", corner_radius=0)
        self.right.grid(row=0, column=1, sticky="nsew")

        # Box do Formulário (Simulando um Card)
        self.form_card = ctk.CTkFrame(self.right, fg_color="white", width=400)
        self.form_card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.form_card, text="Bem-vindo de volta", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold"), 
            text_color=azulEscuro
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            self.form_card, text="Por favor, insira seus dados de acesso.", 
            font=ctk.CTkFont(family="Inter", size=14), 
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(5, 30))

        # Estilização dos Inputs
        input_kwargs = {
            "width": 360,
            "height": 52,
            "corner_radius": 10,
            "border_width": 1,
            "border_color": self.cor_borda,
            "fg_color": "#F8FAFC",
            "text_color": 'black',
            "font": (Fonte1, 14),
            "placeholder_text_color": "#94A3B8"
        }

        self.usuario = ctk.CTkEntry(self.form_card, placeholder_text="Usuário ou e-mail", **input_kwargs)
        self.usuario.pack(pady=10, padx=20)

        self.senha = ctk.CTkEntry(self.form_card, placeholder_text="Sua senha", show="*", **input_kwargs)
        self.senha.pack(pady=10, padx=20)

        # Link de "Esqueci minha senha" (Estético)
        # ctk.CTkLabel(
        #     self.form_card, text="Esqueceu a senha?", 
        #     font=ctk.CTkFont(size=12, weight="bold"), 
        #     text_color="#38BDF8", cursor="hand2"
        # ).pack(anchor="e", padx=25)

        self.erro = ctk.CTkLabel(self.form_card, text="", text_color=VermelhoErro, font=("Inter", 12))
        self.erro.pack(pady=5)

        # Botão com Design Robusto
        self.botao_entrar = ctk.CTkButton(
            self.form_card, 
            text="Entrar no Sistema", 
            width=360, height=55, 
            corner_radius=10, 
            font=ctk.CTkFont(family="Inter", size=16, weight="bold"), 
            fg_color=AzulPrimario, 
            hover_color=AzulHover, 
            command=self.autentificacao
        )
        self.botao_entrar.pack(pady=(20, 20), padx=20)

        # Binds
        self.usuario.bind("<Return>", self.autentificacao)
        self.senha.bind("<Return>", self.autentificacao)

    # --- LÓGICA MANTIDA ---
    def autentificacao(self, event=None):
        try:
            usuario = self.usuario.get()
            senha = self.senha.get()
            if not usuario or not senha:
                self.erro.configure(text="Preencha email e senha")
                return
            self.botao_entrar.configure(state="disabled", text="Autenticando...")
            self.erro.configure(text="")
            thread = threading.Thread(target=self._autenticar_thread, args=(usuario, senha), daemon=True)
            thread.start()
        except Exception as e:
            self.erro.configure(text=f"Erro: {str(e)}")
            self.botao_entrar.configure(state="normal", text="Entrar")

    def _autenticar_thread(self, usuario, senha):
        try:
            tipo = ""
            result = autenticar(usuario, senha, tipo)
            self.after(0, self._processar_resultado, result, usuario)
        except Exception as e:
            self.after(0, lambda: self._mostrar_erro(f"Erro: {str(e)}"))

    def _processar_resultado(self, result, usuario):
        try:
            self.botao_entrar.configure(state="normal", text="Acessar Sistema")
            if isinstance(result, tuple) and len(result) >= 2 and result[1]:
                tipo = result[0]
                self.destroy()
                if tipo in ["Aluno", "Professor"]:
                    from views.Aluno_e_Professor.home_view import Home
                    self.home_aluno_screen = Home(self.master)
                    self.home_aluno_screen.pack(expand=True, fill="both")
                elif tipo == "Coordenador":
                    from views.Coordenacao.HomeCoordenador import HomeCoordenador
                    self.home_coordenador_screen = HomeCoordenador(self.master)
                    self.home_coordenador_screen.pack(expand=True, fill="both")
            else:
                self._mostrar_erro(result[0] if isinstance(result, tuple) else str(result))
        except Exception as e:
            self._mostrar_erro(f"Erro: {str(e)}")

    def _mostrar_erro(self, mensagem):
        try:
            self.erro.configure(text=mensagem)
            self.botao_entrar.configure(state="normal", text="Acessar Sistema")
        except: pass