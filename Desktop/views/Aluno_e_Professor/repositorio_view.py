import customtkinter as ctk
import os
import sys
from tkinter import messagebox, filedialog
import zipfile

# Ajuste de caminhos para imports (MVC)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from assets.cores import *
from controllers.repositorio_controller import RepositorioController

class RepositorioDashboard(ctk.CTkFrame):
    def __init__(self, master, turma_id, pasta_id=None, nome_projeto="Repositório Principal"):
        super().__init__(master)
        self.janela = master
        self.turma_id = turma_id
        self.pasta_atual_id = pasta_id 
        self.nome_projeto = nome_projeto
        
        self.controller = RepositorioController()
        
        self.configure(fg_color=CinzaFundo)
        self.pack(side="right", fill="both", expand=True)
        
        self.carregar_dados()
        self.criar_interface()

    def carregar_dados(self):
        """Busca os dados do MySQL via Controller"""
        try:
            self.pastas, self.arquivos = self.controller.listar_conteudo(
                self.turma_id, 
                self.pasta_atual_id
            )
            print(f"DEBUG: Pastas carregadas da Turma {self.turma_id}: {self.pastas}")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.pastas, self.arquivos = [], []


    def criar_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        # --- HEADER (Azul Escuro) ---
        header = ctk.CTkFrame(self.container_principal, fg_color=azulEscuro, height=100, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        if self.pasta_atual_id:
            ctk.CTkButton(header, text="⬅", width=40, fg_color="transparent", 
                          hover_color="#334155", command=self.voltar_raiz).pack(side="left", padx=(20, 0))
        # else:
        #     ctk.CTkButton(header, text="⬅ Projetos", width=100, text_color=Branco, fg_color=azulEscuro, hover='transparent', command=self.voltar_projetos).pack(side="left", padx=(20, 0)),

        ctk.CTkLabel(header, text=self.nome_projeto, 
                     font=ctk.CTkFont(size=24, weight="bold"), 
                     text_color=Branco).pack(side="left", padx=30)

        # Botão ZIP (Verde)
        ctk.CTkButton(header, text="📦 Baixar Tudo (.zip)", fg_color="#10b981", 
                      text_color=Branco, width=160, height=35, 
                      font=ctk.CTkFont(weight="bold"),
                      command=self.baixar_tudo_zip).pack(side="right", padx=30)

        # --- ÁREA DE SCROLL ---
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)

        # ==========================================
        # BLOCO 1: PASTAS (Design de Cards)
        # ==========================================
        title_pastas = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        title_pastas.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(title_pastas, text="Pastas", font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color=azulEscuro).pack(side="left")

        grid_pastas = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        grid_pastas.pack(fill="x")

        if not self.pastas:
            ctk.CTkLabel(grid_pastas, text="Nenhuma pasta encontrada.", text_color="#64748b").pack(pady=10)
        else:
            for i, pasta in enumerate(self.pastas):
                self.criar_card_pasta(grid_pastas, pasta, i)

        # Separador Visual
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#e2e8f0").pack(fill="x", pady=30)

        # ==========================================
        # BLOCO 2: ARQUIVOS (Design de Linhas)
        # ==========================================
        ctk.CTkLabel(self.main_scroll, text="Arquivos", font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color=azulEscuro, anchor="w").pack(fill="x", pady=(0, 15))

        if not self.arquivos:
            ctk.CTkLabel(self.main_scroll, text="Nenhum arquivo nesta pasta.", text_color="#64748b").pack(pady=10)
        else:
            for arq in self.arquivos:
                self.criar_linha_arquivo(arq)

    # def voltar_projetos(self):
    #     from views.Aluno_e_Professor.projetos_view import ProjetosDesktopDashboard
    
    #     self.pack_forget() 
        
    #     tela_projetos = ProjetosDesktopDashboard(
    #         master=self.janela, 
    #         id_turma=self.turma_id,    # ID que veio da tela de turmas
    #         nome_turma=self.nome_projeto, # Nome que veio da tela de turmas
    #         tipo_usuario=None,  # Você pode passar o tipo de usuário se necessário
    #         controller1=self.controller1  # Passa o controller para manter a consistência
    #     )
    #     tela_projetos.pack(side="right", fill="both", expand=True)

    def criar_card_pasta(self, parent, pasta, index):
        # Card igual ao seu design original
        card = ctk.CTkFrame(parent, fg_color=Branco, width=300, height=140, 
                            corner_radius=12, border_width=1, border_color="#cbd5e1")
        card.grid(row=index//3, column=index%3, padx=10, pady=10)
        card.pack_propagate(False)

        top_content = ctk.CTkFrame(card, fg_color="transparent")
        top_content.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(top_content, text="📁", font=("Arial", 30)).pack(side="left")
        
        info_frame = ctk.CTkFrame(top_content, fg_color="transparent")
        info_frame.pack(side="left", padx=10, fill="x", expand=True)
        
        ctk.CTkLabel(info_frame, text=pasta["nome"], font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=azulEscuro, anchor="w").pack(anchor="w", fill="x")
        ctk.CTkLabel(info_frame, text=f"{pasta['data']}", font=ctk.CTkFont(size=11), 
                     text_color="#64748b", anchor="w").pack(anchor="w", fill="x")

        # Botão Entrar (Ação Principal)
        btn_entrar = ctk.CTkButton(card, text="📂 Entrar", fg_color=AzulPrimario, text_color=Branco,
                                   hover_color=AzulHover, width=250, height=32,
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   command=lambda p=pasta: self.entrar_na_pasta(p))
        btn_entrar.pack(side="bottom", pady=15)

    def criar_linha_arquivo(self, arquivo):
        # Linha detalhada igual ao seu design original
        linha = ctk.CTkFrame(self.main_scroll, fg_color=Branco, height=60, 
                             corner_radius=10, border_width=1, border_color="#cbd5e1")
        linha.pack(fill="x", pady=5)
        linha.pack_propagate(False)

        ctk.CTkLabel(linha, text="📄", font=("Arial", 22)).pack(side="left", padx=(20, 15))

        info_frame = ctk.CTkFrame(linha, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=8)

        ctk.CTkLabel(info_frame, text=arquivo["nome"], font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=azulEscuro, anchor="w").pack(fill="x")
        
        # 'autor' e 'tamanho' vêm do seu Controller/Model
        meta_texto = f"Enviado por: {arquivo['autor']}  •  {arquivo['data']}"
        ctk.CTkLabel(info_frame, text=meta_texto, font=ctk.CTkFont(size=11), 
                     text_color="#64748b", anchor="w").pack(fill="x")

        # Botão Baixar
        ctk.CTkButton(linha, text="📥 Baixar", fg_color="#f1f5f9", text_color=azulEscuro,
                      hover_color="#e2e8f0", width=120, height=32,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=lambda a=arquivo: self.baixar_arquivo(a)).pack(side="right", padx=20)

    def entrar_na_pasta(self, pasta):
        self.pack_forget()
        RepositorioDashboard(self.janela, self.turma_id, pasta['id'], pasta['nome'])

    def voltar_raiz(self):
        self.pack_forget()
        RepositorioDashboard(self.janela, self.turma_id, None, "Repositório Principal")

    def baixar_arquivo(self, arquivo):
        local_destino = filedialog.asksaveasfilename(defaultextension=".dat", initialfile=arquivo['nome'])
        if local_destino:
            messagebox.showinfo("Download", f"Arquivo {arquivo['nome']} pronto para transferência.")

    def baixar_tudo_zip(self):
        local_zip = filedialog.asksaveasfilename(defaultextension=".zip", initialfile=f"repositorio_{self.nome_projeto}.zip")
        if local_zip:
            try:
                with zipfile.ZipFile(local_zip, 'w') as zip_arq:
                    for arq in self.arquivos:
                        zip_arq.writestr(arq['nome'], "Conteúdo recuperado do MySQL")
                messagebox.showinfo("Sucesso", "Repositório compactado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao gerar ZIP: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x800")
    root.title("Inova Edu - Repositório")
    root.attributes("-fullscreen", True)
    app = RepositorioDashboard(root)
    root.mainloop()