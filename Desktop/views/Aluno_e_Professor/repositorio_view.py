import customtkinter as ctk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from assets.cores import *

class RepositorioDashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.configure(fg_color=CinzaFundo)
        
        # Dados simulados
        self.pastas = [
            {"id": 1, "nome": "Documentação Técnica", "autor": "Ana Silva", "data": "10/02/2026"},
            {"id": 2, "nome": "Assets de Design", "autor": "Carlos Lopes", "data": "05/02/2026"},
            {"id": 3, "nome": "Atas de Reunião", "autor": "Beatriz Silva", "data": "01/02/2026"},
            {"id": 4, "nome": "Códigos Fonte", "autor": "Diego Ramos", "data": "28/01/2026"},
        ]
        self.arquivos = [
            {"id": 101, "nome": "cronograma_projeto.pdf", "autor": "Ana Silva", "data": "12/02/2026", "tamanho": "1.2 MB"},
            {"id": 102, "nome": "logo_final_v2.png", "autor": "Carlos Lopes", "data": "11/02/2026", "tamanho": "450 KB"},
        ]

        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break
        if not sidebar_existente:
            sidebar(self.janela)

        self.pack(side="right", fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color=azulEscuro, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Repositório de Arquivos", 
                     font=ctk.CTkFont(size=24, weight="bold"), 
                     text_color=Branco).pack(side="left", padx=30)

        # Botões do Header
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=30)

        ctk.CTkButton(btn_frame, text="📁 Nova Pasta", fg_color="transparent", 
                      border_width=1, border_color=Branco, text_color=Branco,
                      width=130, height=35).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="📤 Enviar Arquivo", fg_color=Branco, 
                      text_color=azulEscuro,
                      width=140, height=35, font=ctk.CTkFont(weight="bold"),
                      hover_color=CinzaFundo).pack(side="left", padx=0)

        # --- ÁREA DE SCROLL ---
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=30, pady=20)

        # ==========================================
        # BLOCO 1: PASTAS
        # ==========================================
        self.renderizar_secao_pastas()

        # Separador Visual
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#e2e8f0").pack(fill="x", pady=30)

        # ==========================================
        # BLOCO 2: ARQUIVOS
        # ==========================================
        self.renderizar_secao_arquivos()

    def renderizar_secao_pastas(self):
        # Título
        title_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(title_frame, text="Pastas", font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color=azulEscuro).pack(side="left")

        # Grid Container
        grid_pastas = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        grid_pastas.pack(fill="x")

        if not self.pastas:
            ctk.CTkLabel(grid_pastas, text="Nenhuma pasta encontrada.", text_color=CinzaTexto).pack(pady=20)
        else:
            for i, pasta in enumerate(self.pastas):
                self.criar_card_pasta(grid_pastas, pasta, i)

    def criar_card_pasta(self, parent, pasta, index):
        # Card Container
        card = ctk.CTkFrame(parent, fg_color=Branco, width=300, height=140, 
                            corner_radius=12, border_width=1, border_color="#cbd5e1")
        card.grid(row=index//3, column=index%3, padx=10, pady=10)
        card.pack_propagate(False)

        # --- PARTE SUPERIOR (Info + Botão Editar) ---
        top_content = ctk.CTkFrame(card, fg_color="transparent")
        top_content.pack(fill="x", padx=15, pady=(15, 5))

        # Ícone de Pasta (Esquerda)
        ctk.CTkLabel(top_content, text="📁", font=("Arial", 30)).pack(side="left")
        
        # Textos (Centro-Esquerda)
        info_frame = ctk.CTkFrame(top_content, fg_color="transparent")
        info_frame.pack(side="left", padx=10, fill="x", expand=True)
        
        ctk.CTkLabel(info_frame, text=pasta["nome"], font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=azulEscuro, anchor="w").pack(anchor="w", fill="x")
        ctk.CTkLabel(info_frame, text=f"{pasta['data']}", font=ctk.CTkFont(size=11), 
                     text_color=CinzaTexto, anchor="w").pack(anchor="w", fill="x")

        # Botão Editar (Só Ícone - Direita Superior)
        btn_editar = ctk.CTkButton(top_content, text="🖊️", width=10, height=30,
                                   fg_color="transparent", text_color=azulEscuro, hover_color="#f1f5f9",
                                   command=lambda p=pasta: print(f"Editar nome da pasta: {p['nome']}"))
        btn_editar.pack(side="right", anchor="ne")

        # --- PARTE INFERIOR (Botões Grandes) ---
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(side="bottom", fill="x", padx=15, pady=15)

        # Botão Entrar (Azul - Ação Principal)
        btn_entrar = ctk.CTkButton(actions, text="📂 Entrar", fg_color=AzulPrimario, text_color=Branco,
                                   hover_color=AzulHover, width=100, height=32,
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   command=lambda p=pasta: print(f"Entrando em {p['nome']}"))
        btn_entrar.pack(side="left", expand=True, padx=(0, 5))

        # Botão Excluir (Vermelho - Ação Destrutiva)
        btn_excluir = ctk.CTkButton(actions, text="🗑️ Excluir", fg_color="#fee2e2", text_color=VermelhoErro,
                                    hover_color="#fecaca", width=100, height=32,
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    command=lambda p=pasta: print(f"Excluir {p['nome']}"))
        btn_excluir.pack(side="left", expand=True, padx=(5, 0))

    def renderizar_secao_arquivos(self):
        # Título
        title_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(title_frame, text="Arquivos", font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color=azulEscuro).pack(side="left")

        if not self.arquivos:
            ctk.CTkLabel(self.main_scroll, text="Nenhum arquivo disponível.", text_color=CinzaTexto).pack(pady=20)
        else:
            for arquivo in self.arquivos:
                self.criar_linha_arquivo(arquivo)

    def criar_linha_arquivo(self, arquivo):
        linha = ctk.CTkFrame(self.main_scroll, fg_color=Branco, height=60, 
                             corner_radius=10, border_width=1, border_color="#cbd5e1")
        linha.pack(fill="x", pady=5)
        linha.pack_propagate(False)

        ctk.CTkLabel(linha, text="📄", font=("Arial", 22)).pack(side="left", padx=(20, 15))

        info_frame = ctk.CTkFrame(linha, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=8)

        ctk.CTkLabel(info_frame, text=arquivo["nome"], font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=azulEscuro, anchor="w").pack(fill="x")
        
        meta_texto = f"Enviado por: {arquivo['autor']}  •  {arquivo['tamanho']}"
        ctk.CTkLabel(info_frame, text=meta_texto, font=ctk.CTkFont(size=11), 
                     text_color=CinzaTexto, anchor="w").pack(fill="x")

        # Botões Arquivo
        ctk.CTkButton(linha, text="📥 Baixar", fg_color="#f1f5f9", text_color=azulEscuro,
                      hover_color="#e2e8f0", width=100, height=32,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=lambda a=arquivo: print(f"Baixando {a['nome']}")).pack(side="right", padx=(5, 20))

        ctk.CTkButton(linha, text="🗑️ Excluir", fg_color="#fee2e2", text_color=VermelhoErro,
                      hover_color="#fecaca", width=100, height=32,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=lambda a=arquivo: print(f"Excluindo {a['nome']}")).pack(side="right", padx=5)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("1100x800")
    root.title("Inova Edu - Repositório")
    root.attributes("-fullscreen", True)
    app = RepositorioDashboard(root)
    root.mainloop()