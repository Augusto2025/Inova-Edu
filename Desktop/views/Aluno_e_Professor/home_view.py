# views/Aluno_e_Professor/home_view.py
import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime, date
from models.cursos_model import CursosModel
from controllers.cursos_controllers import obter_cursos 
from assets.cores import *


class Home(ctk.CTkFrame):
    def __init__(self, master):  
        super().__init__(master)

        self.janela = master

        # cores
        self.cor_fundo = "#f5f7fb"
        self.janela.configure(fg_color=self.cor_fundo)

        # Configurar este frame para expandir
        self.configure(fg_color=self.cor_fundo)
        self.pack(fill="both", expand=True)

        # Criar um container principal dentro do frame Home
        self.container_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.container_principal.pack(fill="both", expand=True, side="left")
        
        # Importar sidebar (OOP) de forma tardia (evita import circular)
        from sidebar_AP import sidebar
        
        # Criar sidebar - passa self (frame Home) como master
        sidebar(self.container_principal)
        
        # Agora criar o conteúdo dentro do mesmo container
        self.criar_interface()

        # --- Carrega cursos de forma robusta (evita ValueError de unpack) ---
        cursos_data = CursosModel().exibirCursos()
        self.cursos = []

        def _to_str_date(value):
            """Normaliza datas para string YYYY-MM-DD sem quebrar se já for str."""
            if isinstance(value, datetime):
                return value.date().isoformat()
            if isinstance(value, date):
                return value.isoformat()
            return (str(value) if value is not None else "")[:10]

        for row in cursos_data:
            try:
                if isinstance(row, dict):
                    # Quando o model retorna dicts
                    nome_curso      = row.get("nome") or row.get("name") or row.get("titulo") or ""
                    imagem_curso    = row.get("imagem") or row.get("image") or ""
                    descricao_curso = row.get("descricao") or row.get("description") or ""
                    # data_inicio     = _to_str_date(row.get("data_inicio") or row.get("start_date"))
                    # data_final      = _to_str_date(row.get("data_final") or row.get("end_date"))
                else:
                    # Quando o model retorna tuplas/listas com 5+ colunas
                    # Ajuste os índices conforme seu SELECT real.
                    # Aqui assumimos: (nome, imagem, descricao, data_inicio, data_final, *extras)
                    nome_curso      = row[0] if len(row) > 0 else ""
                    imagem_curso    = row[1] if len(row) > 1 else ""
                    descricao_curso = row[2] if len(row) > 2 else ""
                    # data_inicio     = _to_str_date(row[3] if len(row) > 3 else "")
                    # data_final      = _to_str_date(row[4] if len(row) > 4 else "")
            except Exception as e:
                print(f"DEBUG: falha ao ler linha do cursos_data: {e} | row={row}")
                continue

            curso = {
                "name": str(nome_curso or "").strip(),
                "image": str(imagem_curso or "").strip(),
                "description": str(descricao_curso or "").strip(),
                # "start_date": data_inicio or "",
                # "end_date": data_final or ""
            }
            self.cursos.append(curso)
    
        print(f"Carregados {len(self.cursos)} cursos")

        self.atualizar_cards()

    def criar_interface(self):
        # area de conteúdo (à direita do sidebar)
        # Agora o conteúdo está dentro do mesmo container que a sidebar
        self.conteudo = ctk.CTkFrame(self.container_principal, fg_color="transparent")
        self.conteudo.pack(side="left", fill="both", expand=True)

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

        # Área de cards (scrollable) - OBRIGATÓRIO: precisa expandir para preencher espaço
        self.scroll_area = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # container interno para grid de cards
        self.cards_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.cards_container.pack(expand=True, fill="both", padx=8, pady=8)  # IMPORTANTE: expand=True aqui também
        
        # Configurar grid de cards (3 colunas)
        self.cards_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

        # Variáveis para filtros
        # self.data_inicio = None
        # self.data_fim = None
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
        self.data_inicio_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Ex: 2025-03-01",
            height=40,
            border_width=2,
            border_color="#004A8D"
        )
        self.data_inicio_entry.pack(fill="x", pady=(0, 20))

        # Data fim
        ctk.CTkLabel(
            main_frame, 
            text="📅 Data de Fim",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#004A8D"
        ).pack(anchor="w", pady=(0, 8))
        self.data_fim_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Ex: 2025-12-31",
            height=40,
            border_width=2,
            border_color="#004A8D"
        )
        self.data_fim_entry.pack(fill="x", pady=(0, 24))

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
            self.data_inicio = self.data_inicio_entry.get().strip()
            self.data_fim = self.data_fim_entry.get().strip()
            self.aplicar_filtros()
            modal.destroy()

        def limpar():
            self.data_inicio_entry.delete(0, "end")
            self.data_fim_entry.delete(0, "end")
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
            
            # Lógica do filtro de data
            data_ok = True
            
            if inicio or fim:
                try:
                    data_inicio_curso = datetime.strptime(c["start_date"], "%Y-%m-%d").date() if c.get("start_date") else None
                    data_fim_curso    = datetime.strptime(c["end_date"], "%Y-%m-%d").date()   if c.get("end_date") else None
                    
                    if inicio and fim:
                        # Curso deve estar dentro do intervalo [inicio, fim]
                        if (data_inicio_curso and data_inicio_curso < inicio) or (data_fim_curso and data_fim_curso > fim):
                            data_ok = False
                    elif inicio and not fim:
                        if data_inicio_curso and data_inicio_curso < inicio:
                            data_ok = False
                    elif fim and not inicio:
                        if data_fim_curso and data_fim_curso > fim:
                            data_ok = False
                            
                except Exception as e:
                    print(f"Erro ao processar datas do curso {c.get('name', '')}: {e}")
                    data_ok = False

            if nome_ok and data_ok:
                filtrados.append(c)

        # ordenar
        reverse = self.ordenar_var.get() == "Z-A"
        filtrados.sort(key=lambda x: x["name"].lower(), reverse=reverse)

        print(f"Filtrados {len(filtrados)} cursos")
        self.atualizar_cards(filtrados)

    def entrar_no_curso(self, curso):
        """Função chamada quando clica no botão 'Entrar' do curso"""
        print(f"Entrando no curso: {curso['name']}")
        from tkinter import messagebox
        messagebox.showinfo("Curso", f"Você entrou no curso: {curso['name']}")

    def atualizar_cards(self, lista=None):
        # limpa container
        for w in self.cards_container.winfo_children():
            w.destroy()

        cursos = lista if lista is not None else self.cursos

        # criar cards em grade (3 colunas) com tamanho fixo
        CARD_WIDTH = 420
        CARD_HEIGHT = 470
        cols = 3
        
        for idx, curso in enumerate(cursos):
            r = idx // cols
            c = idx % cols
            
            # Card com layout vertical centralizado
            card = ctk.CTkFrame(
                self.cards_container, 
                width=CARD_WIDTH, 
                height=CARD_HEIGHT,
                corner_radius=20,
                fg_color="#ffffff",
                border_width=1,
                border_color="#e0e0e0"
            )
            card.grid(row=r, column=c, padx=16, pady=16, sticky="nsew")
            card.pack_propagate(False)
            
            # CONTAINER PRINCIPAL - Centraliza tudo verticalmente
            main_container = ctk.CTkFrame(card, fg_color="transparent")
            main_container.pack(expand=True, fill="both", padx=20, pady=20)
            
            # 1. IMAGEM (topo) - Centralizada
            img_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=150)
            img_frame.pack(fill="x", pady=(0, 15))
            
            img_path = curso.get("image", "")
            pil = None
            try:
                if img_path and os.path.exists(img_path):
                    pil = Image.open(img_path).resize((CARD_WIDTH - 60, 140))
                else:
                    # Placeholder mais bonito
                    from PIL import ImageDraw, ImageFont
                    pil = Image.new("RGB", (CARD_WIDTH - 60, 140), (52, 152, 219))
                    draw = ImageDraw.Draw(pil)
                    # Adiciona um ícone/texto no placeholder
                    try:
                        # Tenta adicionar texto
                        font = ImageFont.load_default()
                        draw.text((50, 50), "🎓", font=font, fill="white")
                    except:
                        pass
            except Exception:
                pil = Image.new("RGB", (CARD_WIDTH - 60, 140), (52, 152, 219))

            img_ctk = ctk.CTkImage(light_image=pil, size=(CARD_WIDTH - 60, 140))
            img_lbl = ctk.CTkLabel(img_frame, image=img_ctk, text="", fg_color="transparent")
            img_lbl.image = img_ctk
            img_lbl.pack(expand=True)
            
            # 2. NOME DO CURSO - Centralizado
            nome_lbl = ctk.CTkLabel(
                main_container,
                text=curso["name"],
                font=ctk.CTkFont(size=16, weight="bold"),
                wraplength=CARD_WIDTH - 80,
                justify="center",
                text_color="#2c3e50"
            )
            nome_lbl.pack(pady=(0, 10))
            
            # 3. DESCRIÇÃO - Centralizada
            desc_lbl = ctk.CTkLabel(
                main_container, 
                text=curso["description"][:100] + "..." if len(curso["description"]) > 100 else curso["description"],
                wraplength=CARD_WIDTH - 80, 
                justify="center",
                font=ctk.CTkFont(size=12),
                text_color="#34495e"
            )
            desc_lbl.pack(pady=(0, 15), fill="x", expand=True)
            
            # 4. DATAS - Centralizadas em coluna
            # datas_frame = ctk.CTkFrame(main_container, fg_color="transparent")
            # datas_frame.pack(pady=(0, 15))
            
            # Data de início
            # inicio_frame = ctk.CTkFrame(datas_frame, fg_color="transparent")
            # inicio_frame.pack(pady=2)
            
            # ctk.CTkLabel(
            #     inicio_frame,
            #     text="📅",
            #     font=ctk.CTkFont(size=12),
            #     text_color="#3498db"
            # ).pack(side="left", padx=(0, 8))
            
            # ctk.CTkLabel(
            #     inicio_frame,
            #     text=f"Início: {curso.get('start_date', 'Não definido')}",
            #     font=ctk.CTkFont(size=11),
            #     text_color="#7f8c8d"
            # ).pack(side="left")
            
            # Data de término (se houver)
            # if curso.get("end_date"):
            #     termino_frame = ctk.CTkFrame(datas_frame, fg_color="transparent")
            #     termino_frame.pack(pady=2)
                
            #     ctk.CTkLabel(
            #         termino_frame,
            #         text="⏱️",
            #         font=ctk.CTkFont(size=12),
            #         text_color="#e74c3c"
            #     ).pack(side="left", padx=(0, 8))
                
            #     ctk.CTkLabel(
            #         termino_frame,
            #         text=f"Término: {curso['end_date']}",
            #         font=ctk.CTkFont(size=11),
            #         text_color="#7f8c8d"
            #     ).pack(side="left")
            
            # 5. BOTÃO - Centralizado na parte inferior
            btn_entrar = ctk.CTkButton(
                main_container,
                text="🎓 Acessar Curso",
                command=lambda c=curso: self.entrar_no_curso(c),
                fg_color="#3498db",
                hover_color="#2980b9",
                height=45,
                width=CARD_WIDTH - 80,
                font=ctk.CTkFont(size=14, weight="bold"),
                corner_radius=10,
                border_width=0
            )
            btn_entrar.pack(side="bottom", pady=(15, 0))