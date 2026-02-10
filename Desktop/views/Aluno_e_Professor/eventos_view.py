# eventos_view.py - CORRIGIDO
import customtkinter as ctk
from datetime import datetime, timedelta
from assets.cores import *

class CalendarioDesktopApp(ctk.CTkFrame):
    def __init__(self, master):  
        super().__init__(master)

        self.janela = master

        # cores
        self.cor_fundo = "#f5f7fb"
        self.janela.configure(fg_color=self.cor_fundo)

        # Configurar este frame para expandir
        self.configure(fg_color=self.cor_fundo)
        self.pack(fill="both", expand=True)

        # Criar um container principal
        self.container_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.container_principal.pack(fill="both", expand=True, side="left")
        
        # Importar sidebar
        from sidebar_AP import sidebar
        sidebar(self.container_principal)
        
        # INICIALIZAR VARIÁVEIS ANTES DE CRIAR A INTERFACE
        self.eventos = self.carregar_eventos_exemplo()
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        self.dia_selecionado = None
        
        # Agora criar a interface
        self.criar_interface()
        self.atualizar_calendario()

    def criar_interface(self):
        """Cria interface"""
        # area de conteúdo (à direita do sidebar)
        self.conteudo = ctk.CTkFrame(self.container_principal, fg_color="transparent")
        self.conteudo.pack(side="left", fill="both", expand=True)

        # Barra de pesquisa no topo
        pesquisa_frame = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        pesquisa_frame.pack(fill="x", padx=16, pady=(16, 8))

        ctk.CTkLabel(pesquisa_frame, text="🔍 Buscar Evento:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=6)
        
        self.nome_filter = ctk.CTkEntry(pesquisa_frame, width=350, 
                                       placeholder_text="Digite o nome do evento...")
        self.nome_filter.pack(side="left", padx=(6, 12), fill="x", expand=True)
        self.nome_filter.bind("<Return>", lambda e: self.aplicar_filtros())

        # Botão para criar novo evento
        criar_btn = ctk.CTkButton(pesquisa_frame, text="➕ Novo Evento", 
                                 width=150, command=self.criar_evento,
                                 fg_color="#28a745", hover_color="#20c997")
        criar_btn.pack(side="right", padx=6)

        # Área do calendário (scrollable)
        self.scroll_area = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Container do calendário
        self.calendario_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.calendario_container.pack(expand=True, fill="both", padx=8, pady=8)

        # Frame para navegação (mês/ano)
        self.nav_frame = ctk.CTkFrame(self.calendario_container, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=(0, 20))

        # Navegação do calendário
        self.criar_navegacao()

        # Frame para dias da semana
        self.criar_dias_semana()

        # Frame para os dias do calendário
        self.days_frame = ctk.CTkFrame(self.calendario_container, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True)

    def criar_navegacao(self):
        """Cria navegação do calendário"""
        # Botão mês anterior
        btn_prev = ctk.CTkButton(
            self.nav_frame, text="◀", width=40, height=40,
            command=lambda: self.alterar_mes(-1),
            fg_color="#f1f5f9", hover_color="#e2e8f0",
            text_color="#475569", corner_radius=8
        )
        btn_prev.pack(side="left", padx=(0, 10))
        
        # Mês e ano atual - AGORA self.mes_atual e self.ano_atual JÁ EXISTEM
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        # Criar label para mês/ano
        self.month_label = ctk.CTkLabel(
            self.nav_frame,
            text=f"{meses[self.mes_atual - 1]} {self.ano_atual}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1e293b"
        )
        self.month_label.pack(side="left", padx=10)
        
        # Botão próximo mês
        btn_next = ctk.CTkButton(
            self.nav_frame, text="▶", width=40, height=40,
            command=lambda: self.alterar_mes(1),
            fg_color="#f1f5f9", hover_color="#e2e8f0",
            text_color="#475569", corner_radius=8
        )
        btn_next.pack(side="left", padx=(10, 0))
        
        # Botão "Hoje"
        btn_today = ctk.CTkButton(
            self.nav_frame, text="Hoje", width=80, height=40,
            command=self.ir_para_mes_atual,
            fg_color="#3b82f6", hover_color="#2563eb",
            corner_radius=8, font=ctk.CTkFont(size=13)
        )
        btn_today.pack(side="right")

    def criar_dias_semana(self):
        """Cria cabeçalho com dias da semana"""
        weekdays_frame = ctk.CTkFrame(self.calendario_container, fg_color="transparent")
        weekdays_frame.pack(fill="x", pady=(0, 10))
        
        weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for day in weekdays:
            label = ctk.CTkLabel(
                weekdays_frame,
                text=day,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#475569"
            )
            label.pack(side="left", expand=True)

    def carregar_eventos_exemplo(self):
        """Carrega eventos de exemplo"""
        return [
            {
                "id": 1,
                "nome": "Reunião de Planejamento",
                "data": f"{datetime.now().year}-{datetime.now().month:02d}-15",
                "hora": "14:00",
                "descricao": "Reunião para planejar as atividades do trimestre.",
                "endereco": "Sala 101 - Bloco A",
                "status": "agendado"
            },
            {
                "id": 2,
                "nome": "Workshop de Python",
                "data": f"{datetime.now().year}-{datetime.now().month:02d}-20",
                "hora": "09:00",
                "descricao": "Workshop sobre desenvolvimento em Python.",
                "endereco": "Laboratório de Informática",
                "status": "em_andamento"
            },
            {
                "id": 3,
                "nome": "Apresentação de Projetos",
                "data": f"{datetime.now().year}-{datetime.now().month:02d}-25",
                "hora": "16:00",
                "descricao": "Apresentação dos projetos finais dos alunos.",
                "endereco": "Auditório Principal",
                "status": "finalizado"
            }
        ]

    def atualizar_calendario(self):
        """Atualiza o grid de dias do calendário"""
        # Limpar dias anteriores
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # Configurar grid 6x7
        for row in range(6):
            self.days_frame.grid_rowconfigure(row, weight=1, minsize=100)
        for col in range(7):
            self.days_frame.grid_columnconfigure(col, weight=1, minsize=100)
        
        # Obter primeiro dia do mês
        primeiro_dia = datetime(self.ano_atual, self.mes_atual, 1)
        
        # Encontrar o primeiro domingo do calendário
        offset = (primeiro_dia.weekday() + 1) % 7
        
        # Preencher dias vazios iniciais
        for i in range(offset):
            empty_frame = ctk.CTkFrame(self.days_frame, fg_color="transparent")
            empty_frame.grid(row=i//7, column=i%7, sticky="nsew", padx=1, pady=1)
        
        # Obter último dia do mês
        ultimo_dia = (datetime(self.ano_atual, self.mes_atual + 1, 1) 
                     if self.mes_atual < 12 
                     else datetime(self.ano_atual + 1, 1, 1)) - timedelta(days=1)
        num_dias = ultimo_dia.day
        
        # Preencher dias do mês
        for dia in range(1, num_dias + 1):
            posicao = offset + dia - 1
            linha = posicao // 7
            coluna = posicao % 7
            
            # Frame para o dia
            dia_frame = ctk.CTkFrame(
                self.days_frame,
                corner_radius=8,
                border_width=1,
                border_color="#e0e0e0",
                fg_color="#ffffff"
            )
            dia_frame.grid(row=linha, column=coluna, sticky="nsew", padx=1, pady=1)
            
            # Container interno
            content_frame = ctk.CTkFrame(dia_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Número do dia
            dia_label = ctk.CTkLabel(
                content_frame,
                text=str(dia),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#2c3e50"
            )
            dia_label.pack(anchor="nw")
            
            # Verificar se é hoje
            hoje = datetime.now()
            if (self.ano_atual == hoje.year and 
                self.mes_atual == hoje.month and 
                dia == hoje.day):
                dia_frame.configure(border_color="#3b82f6", border_width=2)
                dia_label.configure(text_color="#3b82f6")
            
            # Verificar eventos do dia
            data_str = f"{self.ano_atual}-{self.mes_atual:02d}-{dia:02d}"
            eventos_dia = [e for e in self.eventos if e["data"] == data_str]
            
            # Se houver eventos, mostrar indicadores
            if eventos_dia:
                indicators_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                indicators_frame.pack(side="bottom", fill="x", pady=(5, 0))
                
                # Mostrar até 3 indicadores
                for evento in eventos_dia[:3]:
                    cor = self.get_cor_status(evento["status"])
                    indicator = ctk.CTkFrame(
                        indicators_frame,
                        height=6,
                        corner_radius=3,
                        fg_color=cor
                    )
                    indicator.pack(side="left", fill="x", expand=True, padx=1)

    def get_cor_status(self, status):
        """Retorna a cor correspondente ao status"""
        cores = {
            "finalizado": "#ef4444",      # Vermelho
            "em_andamento": "#f59e0b",    # Amarelo/laranja
            "agendado": "#10b981"         # Verde
        }
        return cores.get(status, "#94a3b8")

    def alterar_mes(self, delta):
        """Altera o mês atual"""
        novo_mes = self.mes_atual + delta
        novo_ano = self.ano_atual
        
        if novo_mes > 12:
            novo_mes = 1
            novo_ano += 1
        elif novo_mes < 1:
            novo_mes = 12
            novo_ano -= 1
        
        self.ano_atual = novo_ano
        self.mes_atual = novo_mes
        
        # Atualizar label do mês
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.month_label.configure(text=f"{meses[self.mes_atual - 1]} {self.ano_atual}")
        
        self.atualizar_calendario()

    def ir_para_mes_atual(self):
        """Vai para o mês atual"""
        hoje = datetime.now()
        self.ano_atual = hoje.year
        self.mes_atual = hoje.month
        
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.month_label.configure(text=f"{meses[self.mes_atual - 1]} {self.ano_atual}")
        
        self.atualizar_calendario()

    def aplicar_filtros(self):
        """Aplica filtros de busca"""
        nome = self.nome_filter.get().strip().lower()
        if nome:
            print(f"Buscando eventos com: {nome}")
        else:
            print("Digite um termo para buscar")

    def criar_evento(self):
        """Cria novo evento"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Novo Evento",
            "Funcionalidade de criar novo evento.\n"
            "Aqui você implementaria um formulário para adicionar novos eventos."
        )
