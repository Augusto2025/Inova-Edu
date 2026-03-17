import customtkinter as ctk
import os
import sys
from tkinter import messagebox, filedialog
import zipfile

# Ajuste de caminhos para imports (MVC) para que o EXE localize as pastas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Tenta importar as cores, com fallback caso o caminho mude no executável
try:
    from assets.cores import *
except ImportError:
    # Cores de fallback caso o arquivo assets/cores.py não seja carregado
    azulEscuro = "#1a237e"
    AzulPrimario = "#2196f3"
    AzulHover = "#1976d2"
    Branco = "#ffffff"
    CinzaFundo = "#f5f5f5"

from controllers.repositorio_controller import RepositorioController

class RepositorioDashboard(ctk.CTkFrame):
    def __init__(self, master, turma_id, pasta_id=None, nome_projeto="Repositório Principal"):
        super().__init__(master)
        self.janela = master
        self.turma_id = turma_id
        self.pasta_atual_id = pasta_id
        self.nome_projeto = nome_projeto
        
        # Instancia o controller que conversa com o Model (PostgreSQL)
        self.controller = RepositorioController()
        
        self.configure(fg_color=CinzaFundo)
        self.pack(side="right", fill="both", expand=True)
        
        # Inicia a interface e carrega os dados
        self.carregar_e_mostrar()

    def carregar_e_mostrar(self):
        """Limpa a interface e recarrega os dados do banco"""
        # 1. Busca os dados via Controller
        self.carregar_dados()
        # 2. Desenha os elementos na tela
        self.criar_interface()

    def carregar_dados(self):
        """Busca pastas e arquivos filtrados pelo ID atual"""
        try:
            # Chama o controller passando o ID da Turma/Projeto e a Pasta Atual
            self.pastas, self.arquivos = self.controller.listar_conteudo(
                self.turma_id, 
                self.pasta_atual_id
            )
            print(f"[DEBUG] Dados carregados: {len(self.pastas)} pastas, {len(self.arquivos)} arquivos.")
        except Exception as e:
            print(f"[ERRO VIEW]: Falha ao carregar dados do banco: {e}")
            self.pastas, self.arquivos = [], []

    def criar_interface(self):
        """Renderiza todos os componentes visuais"""
        # Limpa widgets existentes para evitar duplicidade na navegação
        for widget in self.winfo_children():
            widget.destroy()

        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=90, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Botão Voltar (aparece apenas se não estiver na raiz)
        if self.pasta_atual_id:
            btn_voltar = ctk.CTkButton(header, text="⬅ Voltar", width=90, height=35,
                                      fg_color="transparent", border_width=1, border_color=Branco,
                                      hover_color=AzulHover, command=self.voltar_raiz)
            btn_voltar.pack(side="left", padx=20)

        lbl_titulo = ctk.CTkLabel(header, text=self.nome_projeto, 
                                 font=ctk.CTkFont(size=22, weight="bold"), 
                                 text_color=Branco)
        lbl_titulo.pack(side="left", padx=20)

        # Botão de Download Geral
        btn_zip = ctk.CTkButton(header, text="📦 Baixar Tudo (.zip)", fg_color="#10b981", 
                               text_color=Branco, width=160, height=35, 
                               font=ctk.CTkFont(weight="bold"),
                               command=self.baixar_tudo_zip)
        btn_zip.pack(side="right", padx=30)

        # --- ÁREA DE SCROLL PRINCIPAL ---
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)

        # SEÇÃO: PASTAS
        self.renderizar_secao_pastas()

        # Separador Visual
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#e2e8f0").pack(fill="x", pady=25)

        # SEÇÃO: ARQUIVOS
        self.renderizar_secao_arquivos()

    def renderizar_secao_pastas(self):
        lbl_p = ctk.CTkLabel(self.main_scroll, text="Pastas", font=ctk.CTkFont(size=19, weight="bold"), 
                             text_color=azulEscuro)
        lbl_p.pack(anchor="w", pady=(0, 15))

        grid_pastas = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        grid_pastas.pack(fill="x")

        if not self.pastas:
            ctk.CTkLabel(grid_pastas, text="Nenhuma pasta encontrada nesta seção.", 
                         text_color="#64748b", font=("Arial", 13)).pack(pady=10)
        else:
            for i, pasta in enumerate(self.pastas):
                self.criar_card_pasta(grid_pastas, pasta, i)

    def renderizar_secao_arquivos(self):
        lbl_a = ctk.CTkLabel(self.main_scroll, text="Arquivos", font=ctk.CTkFont(size=19, weight="bold"), 
                             text_color=azulEscuro)
        lbl_a.pack(anchor="w", pady=(0, 15))

        if not self.arquivos:
            ctk.CTkLabel(self.main_scroll, text="Nenhum arquivo disponível aqui.", 
                         text_color="#64748b", font=("Arial", 13)).pack(pady=10)
        else:
            for arq in self.arquivos:
                self.criar_linha_arquivo(arq)

    def criar_card_pasta(self, parent, pasta, index):
        """Cria o card visual para cada pasta vinda do Postgres"""
        card = ctk.CTkFrame(parent, fg_color=Branco, width=280, height=130, 
                            corner_radius=12, border_width=1, border_color="#cbd5e1")
        card.grid(row=index//3, column=index%3, padx=10, pady=10)
        card.pack_propagate(False)

        lbl_icon = ctk.CTkLabel(card, text="📁", font=("Arial", 28))
        lbl_icon.pack(pady=(15, 0))

        # O RealDictCursor permite acessar por nome: pasta['nome']
        lbl_nome = ctk.CTkLabel(card, text=pasta['nome'], font=ctk.CTkFont(size=14, weight="bold"), 
                                text_color=azulEscuro)
        lbl_nome.pack()

        btn_abrir = ctk.CTkButton(card, text="Abrir Pasta", height=28, width=120,
                                 fg_color=AzulPrimario, hover_color=AzulHover,
                                 command=lambda p=pasta: self.entrar_na_pasta(p))
        btn_abrir.pack(side="bottom", pady=15)

    def criar_linha_arquivo(self, arquivo):
        """Cria uma linha horizontal para cada arquivo"""
        linha = ctk.CTkFrame(self.main_scroll, fg_color=Branco, height=65, 
                             corner_radius=10, border_width=1, border_color="#cbd5e1")
        linha.pack(fill="x", pady=5)
        linha.pack_propagate(False)

        ctk.CTkLabel(linha, text="📄", font=("Arial", 22)).pack(side="left", padx=20)

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=10)

        ctk.CTkLabel(info, text=arquivo['nome'], font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=azulEscuro, anchor="w").pack(fill="x")
        
        meta = f"Por: {arquivo['autor']}  •  Data: {arquivo['data']}"
        ctk.CTkLabel(info, text=meta, font=ctk.CTkFont(size=11), 
                     text_color="#64748b", anchor="w").pack(fill="x")

        btn_dl = ctk.CTkButton(linha, text="📥 Baixar", width=100, height=32,
                              fg_color="#f1f5f9", text_color=azulEscuro, hover_color="#e2e8f0",
                              command=lambda a=arquivo: self.baixar_arquivo(a))
        btn_dl.pack(side="right", padx=20)

    # --- LÓGICA DE NAVEGAÇÃO ---
    def entrar_na_pasta(self, pasta):
        """Atualiza o estado e recarrega a tela (evita abrir múltiplas janelas)"""
        self.pasta_atual_id = pasta['id']
        self.nome_projeto = pasta['nome']
        self.carregar_e_mostrar()

    def voltar_raiz(self):
        """Reseta para o diretório principal"""
        self.pasta_atual_id = None
        self.nome_projeto = "Repositório Principal"
        self.carregar_e_mostrar()

    # --- LÓGICA DE DOWNLOAD ---
    def baixar_arquivo(self, arquivo):
        local = filedialog.asksaveasfilename(initialfile=arquivo['nome'], title="Salvar Arquivo")
        if local:
            messagebox.showinfo("Download", f"O download de '{arquivo['nome']}' foi iniciado.")

    def baixar_tudo_zip(self):
        if not self.arquivos:
            messagebox.showwarning("Aviso", "Não há arquivos para compactar.")
            return
        
        local_zip = filedialog.asksaveasfilename(defaultextension=".zip", 
                                                initialfile=f"projeto_{self.turma_id}.zip")
        if local_zip:
            messagebox.showinfo("ZIP", "Arquivo compactado com sucesso!")

# --- BLOCO DE EXECUÇÃO (Teste) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x800")
    root.title("Inova Edu - Repositório")
    
    # IMPORTANTE: Passe um ID que exista no seu banco para testar!
    app = RepositorioDashboard(root, turma_id=1) 
    
    # Atalho para fechar o fullscreen se necessário
    root.bind("<Escape>", lambda e: root.destroy())
    
    root.mainloop()