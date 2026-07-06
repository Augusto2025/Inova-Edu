import customtkinter as ctk
import os
import sys
from tkinter import messagebox
from PIL import Image
import requests
from io import BytesIO

# Ajuste de caminhos para imports (MVC)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *

class ProjetosDesktopDashboard(ctk.CTkFrame):
    def __init__(self, master, id_turma, nome_turma, tipo_usuario, controller):
        super().__init__(master)
        self.janela = master
        self.id_turma = id_turma
        self.nome_turma = nome_turma
        self.controller = controller
        
        self.configure(fg_color="#f8fafc") # Slate 50 clean
        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        from assets.header import HeaderPadrao
        header = HeaderPadrao(self, titulo=f"Projetos da Turma: {self.nome_turma}", comando_voltar=self.voltar_turma)

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)
        self.carregar_projetos()

    def voltar_turma(self):
        from views.Aluno_e_Professor.turma_view import TurmasDesktopDashboard
        self.pack_forget() 
        
        tela_turma = TurmasDesktopDashboard(
            master=self.janela, 
            id_curso=self.id_turma,    
            nome_curso=self.nome_turma, 
        )
        tela_turma.pack(side="right", fill="both", expand=True)

    def carregar_projetos(self):
        # Limpa a tela antes de carregar
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        # Chama seu Controller passando o ID da turma
        projetos = self.controller.listar_projetos(self.id_turma)
        print(f"DEBUG: Projetos encontrados -> {projetos}")
        
        if not projetos:
            ctk.CTkLabel(self.main_scroll, text="Nenhum projeto encontrado para esta turma.",
                         font=ctk.CTkFont(size=15), text_color="#64748b").pack(pady=50)
            return

        # Agora usamos uma lista simples de empilhamento vertical
        for p in projetos:
            self.criar_card_projeto(p)

    def criar_card_projeto(self, projeto):
        from PIL import Image
        import requests
        from io import BytesIO
        from dotenv import load_dotenv

        load_dotenv() 

        # Card em formato de Linha Larga (Altura fixa em 140 para ficar grande e imponente, largura se ajusta)
        card = ctk.CTkFrame(self.main_scroll, fg_color=Branco, corner_radius=15, 
                            height=140, border_width=1, border_color="#e2e8f0")
        card.pack(fill="x", pady=10, padx=10)
        card.pack_propagate(False)

        # ==========================================
        # 1. IMAGEM DO CLOUDINARY (LADO DIREITO)
        # ==========================================
        img_frame = ctk.CTkFrame(card, fg_color="#ebf0f5", width=200, height=110, corner_radius=10)
        img_frame.pack(side="left", padx=15, pady=15)
        img_frame.pack_propagate(False)

        url_imagem = projeto.get("imagem") 
        imagem_carregada = False

        if url_imagem:
            url_imagem = str(url_imagem).strip()
            if url_imagem and not url_imagem.startswith(("http://", "https://")):
                
                # ⬇️ PEGA O NOME DA CONTA AUTOMATICAMENTE DO SEU ARQUIVO .ENV ⬇️
                cloud_name = os.getenv("CLOUD_NAME")
                
                if not cloud_name:
                    print("[ERRO] CLOUD_NAME não configurado no arquivo .env!")
                
                if url_imagem.startswith("/"):
                    url_imagem = url_imagem[1:]
                url_imagem = f"https://res.cloudinary.com/{cloud_name}/{url_imagem}"

            try:
                resposta = requests.get(url_imagem, timeout=7)
                if resposta.status_code == 200:
                    img_data = Image.open(BytesIO(resposta.content))
                    ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(200, 110))
                    
                    lbl_img = ctk.CTkLabel(img_frame, image=ctk_img, text="")
                    lbl_img.image = ctk_img  
                    lbl_img.pack(fill="both", expand=True)
                    imagem_carregada = True
            except Exception as e:
                print(f"[AVISO] Erro ao baixar imagem: {e}")

        if not imagem_carregada:
            ctk.CTkLabel(img_frame, text="🚀", font=ctk.CTkFont(size=45)).place(relx=0.5, rely=0.5, anchor="center")

        # ==========================================
        # 2. BOTÃO DE ENTRAR NO REPOSITÓRIO (FINAL - EXTREMA DIREITA ANTES DA IMAGEM)
        # ==========================================
        btn_acessar = ctk.CTkButton(
            card, 
            text="📂 Abrir Repositório", 
            fg_color=azulEscuro, 
            hover_color="#2c3e50",
            width=160,
            height=40, 
            corner_radius=8, 
            font=ctk.CTkFont(weight="bold"),
            command=lambda p=projeto: self.abrir_repositorio(p)
        )
        # Empurra para o lado direito da linha, dando um respiro da imagem
        btn_acessar.pack(side="right", padx=(10, 20), pady=50)

        # ==========================================
        # 3. TEXTOS E INFORMAÇÕES (LADO ESQUERDO)
        # ==========================================
        # Frame invisível para alinhar os textos verticalmente à esquerda
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        # Nome do Projeto
        ctk.CTkLabel(info_frame, text=projeto["nome_projeto"], font=ctk.CTkFont(size=18, weight="bold"), 
                     text_color="#1e293b", anchor="w").pack(fill="x", pady=(0, 2))
        
        # Data de Criação
        ctk.CTkLabel(info_frame, text=f"Criado em: {projeto['data']}", font=ctk.CTkFont(size=11), 
                     text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 6))

        # Descrição (Ocupa o espaço restante até bater nos botões da direita)
        descricao_original = projeto.get("descricao") or "Nenhuma descrição fornecida para este projeto."
        # Como a linha é larga, podemos exibir mais caracteres (aumentei para 180)
        desc_tratada = descricao_original[:180] + "..." if len(descricao_original) > 180 else descricao_original
        
        lbl_desc = ctk.CTkLabel(info_frame, text=desc_tratada, font=ctk.CTkFont(size=13), text_color="#64748b", 
                                wraplength=500, justify="left", anchor="w")
        lbl_desc.pack(fill="x")

    def abrir_repositorio(self, projeto):
        try:
            from views.Aluno_e_Professor.repositorio_view import RepositorioDashboard
            self.pack_forget() 
            
            # Instancia o Repositorio respeitando a ordem correta dos parâmetros obrigatórios
            tela_repo = RepositorioDashboard(
                master=self.janela, 
                turma_id=projeto["idprojeto"],       # Puxa o 'idprojeto' formatado pelo Controller
                nome_projeto=projeto["nome_projeto"], # Envia o nome exato do projeto clicado
                pasta_id=None                        # Opcional por último
            )
            tela_repo.pack(side="right", fill="both", expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir repositório: {e}")
            print(f"ERRO CRÍTICO ao abrir repositório: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x700")
    root.mainloop()