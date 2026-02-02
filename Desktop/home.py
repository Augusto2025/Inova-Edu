import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class Home:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Cursos - Inova Edu")
        self.janela.geometry("1700x700")

        # cores
        self.cor_fundo = "#f5f7fb"
        self.janela.configure(fg_color=self.cor_fundo)

        # importar sidebar_AP de forma tardia (evita import circular)
        from sidebar_AP import sidebar
        sidebar(self.janela)

        self.criar_interface()

        # dados de exemplo
        self.cursos = [
            {
                "name": "Introdução à Programação",
                "description": "Conceitos básicos de lógica e algoritmos.",
                "image": "",
                "start_date": "2025-03-01"
            },
            {
                "name": "Desenvolvimento Web",
                "description": "HTML, CSS, JavaScript e frameworks modernos.",
                "image": "",
                "start_date": "2025-04-10"
            },
            {
                "name": "Inteligência Artificial",
                "description": "Fundamentos de ML e redes neurais.",
                "image": "",
                "start_date": "2025-02-20"
            },
        ]

        self.atualizar_cards()

    def criar_interface(self):
        # area de conteúdo (à direita do sidebar)
        self.conteudo = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.conteudo.pack(side="right", fill="both", expand=True)

        # Barra de pesquisa no topo
        pesquisa_frame = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        pesquisa_frame.pack(fill="x", padx=16, pady=(16, 8))

        ctk.CTkLabel(pesquisa_frame, text="🔍 Buscar:", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=6)
        self.nome_filter = ctk.CTkEntry(pesquisa_frame, width=350, placeholder_text="Digite o nome do curso...")
        self.nome_filter.pack(side="left", padx=(6, 12), fill="x", expand=True)
        self.nome_filter.bind("<Return>", lambda e: self.aplicar_filtros())

        # Botão para abrir modal de filtros
        filtros_btn = ctk.CTkButton(pesquisa_frame, text="⚙️ Filtros Avançados", width=150, command=self.abrir_modal_filtros)
        filtros_btn.pack(side="right", padx=6)

        # Área de cards (scrollable)
        self.scroll_area = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # container interno para grid de cards
        self.cards_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.cards_container.pack(expand=False, padx=8, pady=8)
        self.cards_container.grid_columnconfigure((0, 1), weight=1)

        # Variáveis para filtros
        self.data_inicio = None
        self.data_fim = None
        self.ordenar_var = ctk.StringVar(value="A-Z")

    def abrir_modal_filtros(self):
        """Abre janela modal com filtros avançados"""
        modal = ctk.CTkToplevel(self.janela)
        modal.title("Filtros Avançados")
        modal.geometry("550x420")
        modal.resizable(False, False)
        modal.grab_set()  # Modal em primeiro plano
        modal.configure(fg_color="#f5f7fb")

        # Cabeçalho do modal
        header = ctk.CTkFrame(modal, fg_color="#004A8D", corner_radius=0)
        header.pack(fill="x")
        
        titulo = ctk.CTkLabel(
            header, 
            text="⚙️ FILTROS AVANÇADOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        titulo.pack(padx=20, pady=16)

        # Frame principal com padding
        main_frame = ctk.CTkFrame(modal, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Data início
        ctk.CTkLabel(
            main_frame, 
            text="📅 Data de Início",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#004A8D"
        ).pack(anchor="w", pady=(0, 8))
        data_inicio_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Ex: 2025-03-01",
            height=40,
            border_width=2,
            border_color="#004A8D"
        )
        data_inicio_entry.pack(fill="x", pady=(0, 20))

        # Data fim
        ctk.CTkLabel(
            main_frame, 
            text="📅 Data de Fim",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#004A8D"
        ).pack(anchor="w", pady=(0, 8))
        data_fim_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Ex: 2025-12-31",
            height=40,
            border_width=2,
            border_color="#004A8D"
        )
        data_fim_entry.pack(fill="x", pady=(0, 24))

        # Ordenação
        ctk.CTkLabel(
            main_frame, 
            text="🔤 Ordenar por",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#004A8D"
        ).pack(anchor="w", pady=(0, 12))
        
        ordenar_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        ordenar_frame.pack(fill="x", pady=(0, 32))
        
        ctk.CTkRadioButton(
            ordenar_frame, 
            text="A-Z (Crescente)",
            variable=self.ordenar_var, 
            value="A-Z",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 30))
        ctk.CTkRadioButton(
            ordenar_frame, 
            text="Z-A (Decrescente)",
            variable=self.ordenar_var, 
            value="Z-A",
            font=ctk.CTkFont(size=12)
        ).pack(side="left")

        # Botões de ação
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x")

        def aplicar():
            self.data_inicio = data_inicio_entry.get().strip()
            self.data_fim = data_fim_entry.get().strip()
            self.aplicar_filtros()
            modal.destroy()

        def limpar():
            data_inicio_entry.delete(0, "end")
            data_fim_entry.delete(0, "end")
            self.ordenar_var.set("A-Z")

        ctk.CTkButton(
            botoes_frame, 
            text="✅ Aplicar",
            command=aplicar, 
            fg_color="#28a745",
            hover_color="#20c997",
            height=45,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 12), fill="x", expand=True)
        
        ctk.CTkButton(
            botoes_frame, 
            text="🔄 Limpar",
            command=limpar, 
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=45,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 12), fill="x", expand=True)
        
        ctk.CTkButton(
            botoes_frame, 
            text="❌ Fechar",
            command=modal.destroy, 
            fg_color="#dc3545",
            hover_color="#c82333",
            height=45,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="right", fill="x", expand=True)

    def aplicar_filtros(self):
        nome = self.nome_filter.get().strip().lower()
        inicio_txt = self.data_inicio if isinstance(self.data_inicio, str) else ""
        fim_txt = self.data_fim if isinstance(self.data_fim, str) else ""

        inicio = None
        fim = None
        try:
            if inicio_txt:
                inicio = datetime.strptime(inicio_txt, "%Y-%m-%d").date()
            if fim_txt:
                fim = datetime.strptime(fim_txt, "%Y-%m-%d").date()
        except Exception:
            inicio = None
            fim = None

        # filtrar
        filtrados = []
        for c in self.cursos:
            nome_ok = (not nome) or (nome in c["name"].lower())
            data_ok = True
            if inicio or fim:
                try:
                    sd = datetime.strptime(c["start_date"], "%Y-%m-%d").date()
                    if inicio and sd < inicio:
                        data_ok = False
                    if fim and sd > fim:
                        data_ok = False
                except Exception:
                    data_ok = False

            if nome_ok and data_ok:
                filtrados.append(c)

        # ordenar
        reverse = self.ordenar_var.get() == "Z-A"
        filtrados.sort(key=lambda x: x["name"].lower(), reverse=reverse)

        self.atualizar_cards(filtrados)

    def atualizar_cards(self, lista=None):
        # limpa container
        for w in self.cards_container.winfo_children():
            w.destroy()

        cursos = lista if lista is not None else self.cursos

        # criar cards em grade (2 colunas) com tamanho fixo - AUMENTADO
        CARD_WIDTH = 420
        CARD_HEIGHT = 420
        cols = 3
        
        for idx, curso in enumerate(cursos):
            r = idx // cols
            c = idx % cols
            card = ctk.CTkFrame(
                self.cards_container, 
                width=CARD_WIDTH, 
                height=CARD_HEIGHT,
                corner_radius=15, 
                fg_color="#ffffff",
                border_width=2,
                border_color="#e0e0e0"
            )
            card.grid(row=r, column=c, padx=16, pady=16, sticky="nsew")
            card.pack_propagate(False)  # Fixa o tamanho do card

            # imagem
            img_path = curso.get("image", "")
            pil = None
            try:
                if img_path and os.path.exists(img_path):
                    pil = Image.open(img_path).resize((CARD_WIDTH - 20, 170))
                else:
                    pil = Image.new("RGB", (CARD_WIDTH - 20, 170), (200, 200, 200))
            except Exception:
                pil = Image.new("RGB", (CARD_WIDTH - 20, 170), (200, 200, 200))

            img_ctk = ctk.CTkImage(light_image=pil, size=(CARD_WIDTH - 20, 170))
            img_lbl = ctk.CTkLabel(card, image=img_ctk, text="")
            img_lbl.pack(padx=10, pady=(10, 12))

            # nome
            nome_lbl = ctk.CTkLabel(
                card, 
                text=curso["name"], 
                font=ctk.CTkFont(size=15, weight="bold"),
                wraplength=CARD_WIDTH - 30,
                justify="left"
            )
            nome_lbl.pack(anchor="w", padx=14, pady=(0, 8))

            # descricao
            desc_lbl = ctk.CTkLabel(
                card, 
                text=curso["description"], 
                wraplength=CARD_WIDTH - 30, 
                justify="left",
                font=ctk.CTkFont(size=12)
            )
            desc_lbl.pack(anchor="w", padx=14, pady=(0, 14), fill="both", expand=True)

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = Home()
    app.run()
