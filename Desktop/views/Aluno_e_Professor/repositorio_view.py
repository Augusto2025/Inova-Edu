import customtkinter as ctk
import os
import sys
from tkinter import messagebox, filedialog
import requests
import zipfile

# Ajuste de caminhos para imports (MVC) para que o EXE localize as pastas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from assets.cores import *
except ImportError:
    azulEscuro = "#1a237e"
    AzulPrimario = "#2196f3"
    AzulHover = "#1976d2"
    Branco = "#ffffff"
    CinzaFundo = "#f5f5f5"

from controllers.repositorio_controller import RepositorioController

class RepositorioDashboard(ctk.CTkFrame):
    def __init__(self, master, turma_id, nome_projeto="Repositório Principal", pasta_id=None):
        super().__init__(master)
        self.janela = master
        self.turma_id = turma_id
        self.pasta_atual_id = pasta_id
        self.nome_projeto_inicial = nome_projeto
        self.historico_pastas = [] # Guardará tuplas de (id, nome) para navegação por cliques
        
        self.controller = RepositorioController()
        self.configure(fg_color=CinzaFundo)
        self.pack(side="right", fill="both", expand=True)
        
        self.carregar_e_mostrar()

    def carregar_e_mostrar(self):
        """Limpa a interface e recarrega os dados do banco"""
        self.carregar_dados()
        self.criar_interface()

    def carregar_dados(self):
        """Busca pastas e arquivos filtrados pelo ID atual"""
        try:
            self.pastas, self.arquivos = self.controller.listar_conteudo(
                self.turma_id, 
                self.pasta_atual_id
            )
        except Exception as e:
            print(f"[ERRO VIEW]: Falha ao carregar dados do banco: {e}")
            self.pastas, self.arquivos = [], []

    def criar_interface(self):
        """Renderiza os componentes visuais no estilo Tabela/Lista Detalhada do Windows"""
        for widget in self.winfo_children():
            widget.destroy()

        # 1. HEADER FIXO
        from assets.header import HeaderPadrao
        header = HeaderPadrao(self, titulo="Repositório de Arquivos", comando_voltar=None)

        # Botão de Download Geral mantido no canto superior direito
        btn_zip = ctk.CTkButton(header, text="📦 Baixar Tudo (.zip)", fg_color="#10b981", 
                               text_color=Branco, width=160, height=35, 
                               font=ctk.CTkFont(weight="bold"),
                               command=self.baixar_tudo_zip)
        btn_zip.pack(side="right", padx=30)

        # 2. BARRA DE CAMINHO (Breadcrumb)
        self.criar_barra_caminho()

        # 3. ÁREA DE SCROLL PRINCIPAL (Fundo branco para simular a tabela)
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color=Branco, corner_radius=8, border_width=1, border_color="#e2e8f0")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # --- CABEÇALHO DA TABELA (Colunas Fixas) ---
        header_tabela = ctk.CTkFrame(self.main_scroll, fg_color="#f1f5f9", height=35, corner_radius=4)
        header_tabela.pack(fill="x", padx=5, pady=(5, 10))
        header_tabela.pack_propagate(False)

        # Definição das larguras e alinhamentos das colunas usando grid
        header_tabela.columnconfigure(0, weight=0, minsize=40)
        header_tabela.columnconfigure(1, weight=3, minsize=250)
        header_tabela.columnconfigure(2, weight=1, minsize=130)
        header_tabela.columnconfigure(3, weight=1, minsize=130)
        header_tabela.columnconfigure(4, weight=1, minsize=150)

        # Alterado: Removido o width=20 e adicionado padx igual ao do ícone abaixo
        ctk.CTkLabel(header_tabela, text="", font=("Arial", 18)).grid(row=0, column=0, sticky="w", padx=(10, 0))
        
        # Alinhados com sticky="w" para travar o início do texto na mesma reta
        ctk.CTkLabel(header_tabela, text="Nome", font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569", anchor="w").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ctk.CTkLabel(header_tabela, text="Data de modificação", font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569", anchor="w").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ctk.CTkLabel(header_tabela, text="Tipo", font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569", anchor="w").grid(row=0, column=3, sticky="w", padx=5, pady=5)
        ctk.CTkLabel(header_tabela, text="Quem enviou", font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569", anchor="w").grid(row=0, column=4, sticky="w", padx=5, pady=5)

        # Se o diretório estiver totalmente vazio
        if not self.pastas and not self.arquivos:
            ctk.CTkLabel(self.main_scroll, text="Esta pasta está vazia.", 
                         text_color="#64748b", font=("Arial", 14, "italic")).pack(pady=40)
            return

        # RENDERIZAR PASTAS PRIMEIRO
        for pasta in self.pastas:
            self.criar_linha_tabela(item=pasta, tipo_item="pasta")

        # RENDERIZAR ARQUIVOS LOGO EM SEGUIDA
        for arquivo in self.arquivos:
            self.criar_linha_tabela(item=arquivo, tipo_item="arquivo")

    def criar_linha_tabela(self, item, tipo_item):
        """Gera uma linha horizontal com colunas alinhadas perfeitamente com o cabeçalho"""
        cor_fundo_inicial = "#fef08a" if tipo_item == "pasta" else "transparent"
        linha = ctk.CTkFrame(self.main_scroll, fg_color="transparent", height=38, corner_radius=4)
        linha.pack(fill="x", padx=5, pady=1)
        linha.pack_propagate(False)

        # Espelhamento exato do grid do cabeçalho
        linha.columnconfigure(0, weight=0, minsize=40)
        linha.columnconfigure(1, weight=3, minsize=250)
        linha.columnconfigure(2, weight=1, minsize=130)
        linha.columnconfigure(3, weight=1, minsize=130)
        linha.columnconfigure(4, weight=1, minsize=150)

        # Efeito visual de seleção ao passar o mouse por cima da linha inteira
        linha.bind("<Enter>", lambda e: linha.configure(fg_color="#f8fafc"))
        linha.bind("<Leave>", lambda e: linha.configure(fg_color="transparent"))

        # Define as variáveis com base no tipo (Pasta ou Arquivo)
        if tipo_item == "pasta":
            icone = "📁"
            cor_texto = azulEscuro
            data = item.get('data', '--/--/----')
            tipo_extensao = "Pasta de arquivos"
            autor = item.get('autor', 'Sistema')
            linha.bind("<Double-1>", lambda e: self.entrar_na_pasta(item))
        else:
            icone = "📄"
            cor_texto = "#334155"
            data = item.get('data', '--/--/----')
            _, ext = os.path.splitext(item['nome'])
            tipo_extensao = f"Arquivo {ext.upper()}" if ext else "Arquivo"
            autor = item.get('autor', 'Não informado')
            linha.bind("<Double-1>", lambda e: self.baixar_arquivo(item))

        # --- INSERÇÃO DOS DADOS MILIMETRICAMENTE ALINHADOS ---
        
        # Col 0: Ícone (Mesmo padx do cabeçalho)
        if tipo_item == "pasta":
            # Usamos o emoji de pasta aberta que costuma ser mais dourado/amarelo nativamente
            lbl_icon = ctk.CTkLabel(linha, text="📂", font=("Arial", 18), text_color="#eab308") 
        else:
            lbl_icon = ctk.CTkLabel(linha, text="📄", font=("Arial", 18))
            
        lbl_icon.grid(row=0, column=0, sticky="w", padx=(10, 0))

        # Col 1: Nome do Item (Com limitador wraplength para não empurrar a coluna)
        lbl_nome = ctk.CTkLabel(linha, text=item['nome'], font=ctk.CTkFont(size=13), text_color=cor_texto, anchor="w", wraplength=240, justify="left")
        lbl_nome.grid(row=0, column=1, sticky="w", padx=5)

        # Col 2: Data de Modificação
        lbl_data = ctk.CTkLabel(linha, text=data, font=ctk.CTkFont(size=12), text_color="#64748b", anchor="w")
        lbl_data.grid(row=0, column=2, sticky="w", padx=5)

        # Col 3: Tipo do Elemento
        lbl_tipo = ctk.CTkLabel(linha, text=tipo_extensao, font=ctk.CTkFont(size=12), text_color="#64748b", anchor="w")
        lbl_tipo.grid(row=0, column=3, sticky="w", padx=5)

        # Col 4: Autor / Quem Enviou
        lbl_autor = ctk.CTkLabel(linha, text=autor, font=ctk.CTkFont(size=12), text_color="#64748b", anchor="w")
        lbl_autor.grid(row=0, column=4, sticky="w", padx=5)

        # Faz com que o clique nos textos repasse o evento de duplo clique para a linha pai
        for child in linha.winfo_children():
            if tipo_item == "pasta":
                child.bind("<Double-1>", lambda e, p=item: self.entrar_na_pasta(p))
            else:
                child.bind("<Double-1>", lambda e, a=item: self.baixar_arquivo(a))

    def criar_barra_caminho(self):
        """Cria uma barra simulando o topo do explorador de arquivos com cliques funcionais"""
        path_frame = ctk.CTkFrame(self, fg_color="#e2e8f0", height=32, corner_radius=4)
        path_frame.pack(fill="x", padx=30, pady=15)
        path_frame.pack_propagate(False)

        # Ícone de computador inicial
        ctk.CTkLabel(path_frame, text=" 💻 Este Computador ", font=("Arial", 12, "bold"), text_color="#475569").pack(side="left", padx=(5, 2))
        
        # Botão interativo para a Raiz
        btn_raiz = ctk.CTkButton(path_frame, text="Raiz", font=("Arial", 12), text_color=azulEscuro,
                                 fg_color="transparent", width=40, hover_color="#cbd5e1", command=self.voltar_raiz)
        btn_raiz.pack(side="left")

        # reconstrói os caminhos baseados no histórico para permitir cliques diretos no meio do caminho
        for idx, pasta_hist in enumerate(self.historico_pastas):
            ctk.CTkLabel(path_frame, text=">", text_color="#94a3b8", font=("Arial", 12)).pack(side="left", padx=2)
            btn_path = ctk.CTkButton(
                path_frame, 
                text=pasta_hist['nome'], 
                font=("Arial", 12),
                text_color=azulEscuro,
                fg_color="transparent",
                width=50,
                hover_color="#cbd5e1",
                command=lambda p=pasta_hist, i=idx: self.navegar_historico(p, i)
            )
            btn_path.pack(side="left")

    def criar_item_explorer(self, parent, item, tipo, index):
        """Gera um Card compacto de pasta ou arquivo mesclados no Grid geral"""
        card = ctk.CTkFrame(parent, fg_color="transparent", width=210, height=85, corner_radius=6)
        card.grid(row=index // 4, column=index % 4, padx=8, pady=8, sticky="nsew")
        card.grid_propagate(False)

        # Efeito de hover manual estilo Windows
        card.bind("<Enter>", lambda e: card.configure(fg_color="#f1f5f9"))
        card.bind("<Leave>", lambda e: card.configure(fg_color="transparent"))

        # Define visual com base no tipo
        if tipo == "pasta":
            icone = "📁"
            cor_titulo = azulEscuro
            # Duplo clique abre a pasta
            card.bind("<Double-1>", lambda e: self.entrar_na_pasta(item))
        else:
            icone = "📄"
            cor_titulo = "#334155"
            # Duplo clique baixa o arquivo
            card.bind("<Double-1>", lambda e: self.baixar_arquivo(item))

        # Layout interno do item (Ícone ao lado esquerdo, dados textuais ao lado)
        lbl_icon = ctk.CTkLabel(card, text=icone, font=("Arial", 28))
        lbl_icon.pack(side="left", padx=10)
        lbl_icon.bind("<Double-1>", lambda e: self.entrar_na_pasta(item) if tipo == "pasta" else self.baixar_arquivo(item))

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=12)

        lbl_nome = ctk.CTkLabel(info_frame, text=item['nome'], font=ctk.CTkFont(size=12, weight="bold"), 
                                text_color=cor_titulo, anchor="w", justify="left")
        lbl_nome.pack(fill="x")
        lbl_nome.bind("<Double-1>", lambda e: self.entrar_na_pasta(item) if tipo == "pasta" else self.baixar_arquivo(item))

        # Legenda menor descritiva
        sub_texto = "Pasta de Arquivos" if tipo == "pasta" else f"Por: {item.get('autor', 'Pref.')}"
        lbl_sub = ctk.CTkLabel(info_frame, text=sub_texto, font=ctk.CTkFont(size=10), text_color="#64748b", anchor="w")
        lbl_sub.pack(fill="x")

    # --- LÓGICA DE NAVEGAÇÃO REFEITA ---
    def entrar_na_pasta(self, pasta):
        """Atualiza a pasta atual e registra o rastro no histórico de navegação"""
        if {'id': pasta['id'], 'nome': pasta['nome']} not in self.historico_pastas:
            self.historico_pastas.append({'id': pasta['id'], 'nome': pasta['nome']})
        
        self.pasta_atual_id = pasta['id']
        self.carregar_e_mostrar()

    def navegar_historico(self, pasta, index):
        """Permite que o usuário clique em qualquer pasta anterior do caminho do topo"""
        self.historico_pastas = self.historico_pastas[:index + 1]
        self.pasta_atual_id = pasta['id']
        self.carregar_e_mostrar()

    def voltar_raiz(self):
        """Reseta de volta para o diretório de origem"""
        self.historico_pastas.clear()
        self.pasta_atual_id = None
        self.carregar_e_mostrar()

    # --- LÓGICA DE DOWNLOADS INTEGRADOS ---
    def baixar_arquivo(self, arquivo):
        url_file = arquivo.get('url')
        if not url_file:
            messagebox.showerror("Erro", "Este arquivo não possui uma URL válida na nuvem.")
            return

        local = filedialog.asksaveasfilename(initialfile=arquivo['nome'], title="Salvar Arquivo")
        if local:
            try:
                resposta = requests.get(url_file, timeout=20)
                if resposta.status_code == 200:
                    with open(local, 'wb') as f:
                        f.write(resposta.content)
                    messagebox.showinfo("Sucesso", f"O arquivo '{arquivo['nome']}' foi baixado!")
                else:
                    messagebox.showerror("Erro", f"Falha no servidor da nuvem (Status {resposta.status_code})")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha de conexão: {e}")

    def baixar_tudo_zip(self):
        if not self.arquivos:
            messagebox.showwarning("Aviso", "Não há arquivos para compactar nesta pasta.")
            return
        
        local_zip = filedialog.asksaveasfilename(defaultextension=".zip", 
                                                initialfile="repositorio.zip",
                                                title="Salvar Repositório Compactado")
        if local_zip:
            try:
                sucesso = 0
                with zipfile.ZipFile(local_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for arq in self.arquivos:
                        url_file = arq.get('url')
                        if url_file:
                            res = requests.get(url_file, timeout=15)
                            if res.status_code == 200:
                                zip_file.writestr(arq['nome'], res.content)
                                sucesso += 1
                if sucesso > 0:
                    messagebox.showinfo("ZIP", f"Compactado com sucesso! {sucesso} arquivos salvos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Houve um problema ao criar o .zip: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x800")
    root.title("Inova Edu - Explorer")
    app = RepositorioDashboard(root, turma_id=1) 
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()