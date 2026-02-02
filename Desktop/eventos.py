import customtkinter as ctk
from datetime import datetime, timedelta

class CalendarioDesktopApp:
    def __init__(self):
        self.root = ctk.CTk()
        # self.root.title("Eventos - Calendário")
        # self.root.geometry("1400x800")
        self.root.attributes("-fullscreen", True)

        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Dados de exemplo
        self.eventos = self.carregar_eventos_exemplo()
        self.ano_atual = 2025
        self.mes_atual = 1  # Janeiro
        self.dia_selecionado = None
        self.botoes_meses = {}  # Para armazenar referências dos botões dos meses
        
        self.criar_widgets()
        self.atualizar_calendario()
        self.exibir_eventos_mes()  # Mostrar eventos do mês inicial
        
    def carregar_eventos_exemplo(self):
        """Carrega eventos de exemplo para demonstração"""
        return [
            {
                "id": 1,
                "nome": "Reunião de Planejamento",
                "data": "2025-01-15",
                "hora": "14:00",
                "descricao": "Reunião para planejar as atividades do trimestre",
                "endereco": "Sala 101 - Bloco A",
                "status": "agendado"
            },
            {
                "id": 2,
                "nome": "Workshop de Python",
                "data": "2025-01-20",
                "hora": "09:00",
                "descricao": "Workshop sobre desenvolvimento em Python",
                "endereco": "Laboratório de Informática",
                "status": "em_andamento"
            },
            {
                "id": 3,
                "nome": "Apresentação de Projetos",
                "data": "2025-01-25",
                "hora": "16:00",
                "descricao": "Apresentação dos projetos finais",
                "endereco": "Auditório Principal",
                "status": "finalizado"
            },
            {
                "id": 4,
                "nome": "Avaliação Bimestral",
                "data": "2025-01-10",
                "hora": "10:00",
                "descricao": "Avaliação do primeiro bimestre",
                "endereco": "Sala 205",
                "status": "finalizado"
            },
            {
                "id": 5,
                "nome": "Palestra sobre IA",
                "data": "2025-01-30",
                "hora": "19:00",
                "descricao": "Palestra sobre Inteligência Artificial aplicada à educação",
                "endereco": "Auditório Central",
                "status": "agendado"
            },
            {
                "id": 6,
                "nome": "Fevereiro - Evento 1",
                "data": "2025-02-05",
                "hora": "13:00",
                "descricao": "Primeiro evento de fevereiro",
                "endereco": "Sala 301",
                "status": "agendado"
            },
            {
                "id": 7,
                "nome": "Fevereiro - Evento 2",
                "data": "2025-02-15",
                "hora": "15:00",
                "descricao": "Segundo evento de fevereiro",
                "endereco": "Laboratório B",
                "status": "em_andamento"
            },
            {
                "id": 8,
                "nome": "Março - Evento 1",
                "data": "2025-03-10",
                "hora": "11:00",
                "descricao": "Primeiro evento de março",
                "endereco": "Sala 102",
                "status": "agendado"
            }
        ]
    
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Container principal
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Container do calendário
        self.calendar_frame = ctk.CTkFrame(self.main_container)
        self.calendar_frame.pack(fill="both", expand=True)
        
        # Painel esquerdo - Controle de ano e meses
        self.criar_painel_esquerdo()
        
        # Painel central - Calendário (com tamanho fixo)
        self.criar_painel_central()
        
        # Painel direito - Lista de eventos
        self.criar_painel_direito()
    
    def criar_painel_esquerdo(self):
        """Cria o painel esquerdo com controle de ano e lista de meses"""
        left_panel = ctk.CTkFrame(self.calendar_frame, width=250)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Título do painel
        panel_title = ctk.CTkLabel(
            left_panel,
            text="Controle",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        panel_title.pack(pady=(20, 10))
        
        # Controle de ano
        year_frame = ctk.CTkFrame(left_panel)
        year_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_prev_year = ctk.CTkButton(
            year_frame,
            text="◀",
            width=40,
            command=lambda: self.alterar_ano(-1)
        )
        btn_prev_year.pack(side="left")
        
        self.year_label = ctk.CTkLabel(
            year_frame,
            text=str(self.ano_atual),
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.year_label.pack(side="left", expand=True)
        
        btn_next_year = ctk.CTkButton(
            year_frame,
            text="▶",
            width=40,
            command=lambda: self.alterar_ano(1)
        )
        btn_next_year.pack(side="right")
        
        # Label meses
        months_label = ctk.CTkLabel(
            left_panel,
            text="Meses",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        months_label.pack(pady=(10, 5))
        
        # Lista de meses
        months_frame = ctk.CTkFrame(left_panel)
        months_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        
        # Limpar dicionário de botões
        self.botoes_meses = {}
        
        for i, mes in enumerate(meses):
            btn_mes = ctk.CTkButton(
                months_frame,
                text=mes,
                command=lambda m=i+1: self.selecionar_mes(m),
                fg_color="transparent",
                hover_color=("gray85", "gray25"),
                text_color=("gray10", "gray90"),
                anchor="w",
                height=35
            )
            btn_mes.pack(fill="x", padx=5, pady=1)
            
            # Armazenar referência do botão
            self.botoes_meses[i+1] = btn_mes
            
            # Destacar mês atual
            if i + 1 == self.mes_atual:
                btn_mes.configure(
                    fg_color=("#3B8ED0", "#1F6AA5"),
                    text_color=("white", "white")
                )
        
        # Botão criar evento
        btn_criar = ctk.CTkButton(
            left_panel,
            text="+ Criar Evento",
            command=self.criar_evento,
            height=40,
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        )
        btn_criar.pack(pady=20, padx=20, fill="x")
    
    def criar_painel_central(self):
        """Cria o painel central com o calendário"""
        center_panel = ctk.CTkFrame(self.calendar_frame, width=700, height=600)
        center_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
        center_panel.pack_propagate(False)  # Impede que o tamanho mude
        
        # Cabeçalho do mês
        header_frame = ctk.CTkFrame(center_panel)
        header_frame.pack(fill="x", padx=10, pady=(15, 10))
        
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        
        self.month_label = ctk.CTkLabel(
            header_frame,
            text=meses[self.mes_atual - 1],
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.month_label.pack()
        
        # Container para grid de dias (com tamanho fixo)
        calendar_container = ctk.CTkFrame(center_panel)
        calendar_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para dias da semana (fixo no topo)
        weekdays_frame = ctk.CTkFrame(calendar_container, height=40)
        weekdays_frame.pack(fill="x")
        weekdays_frame.pack_propagate(False)
        
        weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for day in weekdays:
            label = ctk.CTkLabel(
                weekdays_frame,
                text=day,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            label.pack(side="left", expand=True, pady=5)
        
        # Frame principal para os dias (com altura fixa)
        self.days_container = ctk.CTkFrame(calendar_container, height=480)
        self.days_container.pack(fill="both", expand=True)
        self.days_container.pack_propagate(False)
        
        # Frame interno para os dias (que será atualizado)
        self.days_frame = ctk.CTkFrame(self.days_container)
        self.days_frame.pack(fill="both", expand=True)
        
        # Legenda de status (fixa na parte inferior)
        self.criar_legenda(center_panel)
    
    def criar_painel_direito(self):
        """Cria o painel direito com lista de eventos"""
        right_panel = ctk.CTkFrame(self.calendar_frame, width=350)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Título com contador de eventos
        self.eventos_title_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        self.eventos_title_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.eventos_count_label = ctk.CTkLabel(
            self.eventos_title_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.eventos_count_label.pack(side="right")
        
        self.eventos_label = ctk.CTkLabel(
            self.eventos_title_frame,
            text="Eventos do Mês",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.eventos_label.pack(side="left")
        
        # Scrollable frame para eventos
        self.scrollable_frame = ctk.CTkScrollableFrame(
            right_panel,
            width=330,
            height=550
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def criar_legenda(self, parent):
        """Cria a legenda de status dos eventos"""
        legend_frame = ctk.CTkFrame(parent, height=60)
        legend_frame.pack(fill="x", padx=10, pady=(0, 10))
        legend_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            legend_frame,
            text="Status dos Eventos",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title.pack(pady=(10, 5))
        
        # Linha com cores
        colors_frame = ctk.CTkFrame(legend_frame, fg_color="transparent")
        colors_frame.pack()
        
        status_info = [
            ("#FF5252", "Finalizado"),
            ("#FFB74D", "Em andamento"),
            ("#4CAF50", "Agendado")
        ]
        
        for color, text in status_info:
            item_frame = ctk.CTkFrame(colors_frame, fg_color="transparent")
            item_frame.pack(side="left", expand=True)
            
            # Ponto colorido
            point = ctk.CTkFrame(
                item_frame,
                width=12,
                height=12,
                corner_radius=6,
                fg_color=color
            )
            point.pack(side="left", padx=(0, 5))
            
            label = ctk.CTkLabel(item_frame, text=text)
            label.pack(side="left")
    
    def atualizar_calendario(self):
        """Atualiza o grid de dias do calendário"""
        # Limpar dias anteriores
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # Configurar grid 6x7 com proporções fixas
        for row in range(6):
            self.days_frame.grid_rowconfigure(row, weight=1, minsize=80)
        for col in range(7):
            self.days_frame.grid_columnconfigure(col, weight=1, minsize=100)
        
        # Obter primeiro dia do mês
        primeiro_dia = datetime(self.ano_atual, self.mes_atual, 1)
        
        # Encontrar o primeiro domingo do calendário
        offset = (primeiro_dia.weekday() + 1) % 7
        
        # Preencher dias vazios iniciais
        for i in range(offset):
            empty_frame = ctk.CTkFrame(self.days_frame)
            empty_frame.grid(
                row=i//7, 
                column=i%7, 
                sticky="nsew", 
                padx=1, 
                pady=1
            )
        
        # Obter último dia do mês
        if self.mes_atual == 12:
            proximo_mes = 1
            proximo_ano = self.ano_atual + 1
        else:
            proximo_mes = self.mes_atual + 1
            proximo_ano = self.ano_atual
        
        ultimo_dia = datetime(proximo_ano, proximo_mes, 1) - timedelta(days=1)
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
                border_color="#E0E0E0"
            )
            dia_frame.grid(
                row=linha, 
                column=coluna, 
                sticky="nsew", 
                padx=1, 
                pady=1
            )
            
            # Configurar grid interno para centralizar conteúdo
            dia_frame.grid_rowconfigure(0, weight=1)
            dia_frame.grid_columnconfigure(0, weight=1)
            
            # Container interno para o conteúdo
            content_frame = ctk.CTkFrame(dia_frame, fg_color="transparent")
            content_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            # Número do dia
            dia_label = ctk.CTkLabel(
                content_frame,
                text=str(dia),
                font=ctk.CTkFont(size=14, weight="bold")
            )
            dia_label.pack(anchor="nw", pady=(2, 0))
            
            # Verificar eventos do dia
            data_str = f"{self.ano_atual}-{self.mes_atual:02d}-{dia:02d}"
            eventos_dia = [e for e in self.eventos if e["data"] == data_str]
            
            # Adicionar pontos para eventos
            if eventos_dia:
                dots_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                dots_frame.pack(anchor="center", pady=(5, 0))
                
                for evento in eventos_dia[:3]:  # Máximo 3 pontos
                    cor = self.get_cor_status(evento["status"])
                    ponto = ctk.CTkFrame(
                        dots_frame,
                        width=6,
                        height=6,
                        corner_radius=3,
                        fg_color=cor
                    )
                    ponto.pack(side="left", padx=1)
            
            # Destacar se for o dia selecionado
            if dia == self.dia_selecionado:
                dia_frame.configure(border_width=2, border_color="#3B8ED0")
            
            # Tornar clicável
            dia_frame.bind("<Button-1>", lambda e, d=dia: self.selecionar_dia(d))
            dia_frame.bind("<Enter>", lambda e, f=dia_frame: f.configure(border_color="#90CAF9"))
            dia_frame.bind("<Leave>", lambda e, f=dia_frame, d=dia: 
                          f.configure(border_color="#3B8ED0" if d == self.dia_selecionado else "#E0E0E0"))
            
            for child in dia_frame.winfo_children():
                child.bind("<Button-1>", lambda e, d=dia: self.selecionar_dia(d))
    
    def get_cor_status(self, status):
        """Retorna a cor correspondente ao status"""
        cores = {
            "finalizado": "#FF5252",
            "em_andamento": "#FFB74D",
            "agendado": "#4CAF50"
        }
        return cores.get(status, "#808080")
    
    def alterar_ano(self, delta):
        """Altera o ano atual"""
        self.ano_atual += delta
        self.year_label.configure(text=str(self.ano_atual))
        self.atualizar_calendario()
        self.exibir_eventos_mes()  # Atualizar eventos do mês
        self.dia_selecionado = None
        
        # Resetar cor do dia selecionado
        self.selecionar_dia(None)
    
    def selecionar_mes(self, mes):
        """Seleciona um mês específico"""
        # Resetar cor do mês anterior
        if self.mes_atual in self.botoes_meses:
            self.botoes_meses[self.mes_atual].configure(
                fg_color="transparent",
                text_color=("gray10", "gray90")
            )
        
        # Definir novo mês
        self.mes_atual = mes
        self.dia_selecionado = None
        
        # Atualizar interface
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        self.month_label.configure(text=meses[mes-1])
        
        # Destacar botão do mês selecionado
        if mes in self.botoes_meses:
            self.botoes_meses[mes].configure(
                fg_color=("#3B8ED0", "#1F6AA5"),
                text_color=("white", "white")
            )
        
        self.atualizar_calendario()
        self.exibir_eventos_mes()  # Atualizar eventos do mês
    
    def selecionar_dia(self, dia):
        """Seleciona um dia no calendário"""
        self.dia_selecionado = dia
        self.atualizar_calendario()
        
        # Se clicar em um dia, mostrar eventos desse dia
        if dia:
            self.exibir_eventos_dia(dia)
    
    def exibir_eventos_mes(self):
        """Exibe todos os eventos do mês atual"""
        # Limpar lista anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filtrar eventos do mês atual
        eventos_mes = []
        for evento in self.eventos:
            try:
                evento_ano = int(evento["data"].split("-")[0])
                evento_mes = int(evento["data"].split("-")[1])
                if evento_ano == self.ano_atual and evento_mes == self.mes_atual:
                    eventos_mes.append(evento)
            except:
                continue
        
        # Ordenar eventos por data e hora
        eventos_mes.sort(key=lambda x: (x["data"], x["hora"]))
        
        # Atualizar contador
        total_eventos = len(eventos_mes)
        self.eventos_count_label.configure(
            text=f"{total_eventos} evento{'s' if total_eventos != 1 else ''}"
        )
        
        if not eventos_mes:
            sem_eventos = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Nenhum evento agendado para {self.month_label.cget('text')}.",
                text_color="gray",
                wraplength=300
            )
            sem_eventos.pack(pady=30)
            return
        
        # Agrupar eventos por data
        eventos_por_data = {}
        for evento in eventos_mes:
            data = evento["data"]
            if data not in eventos_por_data:
                eventos_por_data[data] = []
            eventos_por_data[data].append(evento)
        
        # Exibir eventos agrupados por data
        for data in sorted(eventos_por_data.keys()):
            # Converter data para formato brasileiro
            ano, mes, dia = data.split("-")
            data_formatada = f"{int(dia):02d}/{int(mes):02d}/{ano}"
            
            # Header da data
            data_header = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#E3F2FD",
                corner_radius=6,
                height=35
            )
            data_header.pack(fill="x", pady=(10, 5), padx=5)
            data_header.pack_propagate(False)
            
            data_label = ctk.CTkLabel(
                data_header,
                text=data_formatada,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#1565C0"
            )
            data_label.pack(side="left", padx=10, pady=8)
            
            # Eventos desta data
            for evento in eventos_por_data[data]:
                self.criar_card_evento(evento)
    
    def exibir_eventos_dia(self, dia):
        """Exibe os eventos do dia selecionado"""
        # Limpar lista anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        data_str = f"{self.ano_atual}-{self.mes_atual:02d}-{dia:02d}"
        data_formatada = f"{dia:02d}/{self.mes_atual:02d}/{self.ano_atual}"
        eventos_dia = [e for e in self.eventos if e["data"] == data_str]
        
        # Atualizar contador
        total_eventos = len(eventos_dia)
        self.eventos_count_label.configure(
            text=f"{total_eventos} evento{'s' if total_eventos != 1 else ''}"
        )
        
        # Header do dia
        data_header = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#E3F2FD",
            corner_radius=6,
            height=35
        )
        data_header.pack(fill="x", pady=(0, 10), padx=5)
        data_header.pack_propagate(False)
        
        data_label = ctk.CTkLabel(
            data_header,
            text=data_formatada,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1565C0"
        )
        data_label.pack(side="left", padx=10, pady=8)
        
        if not eventos_dia:
            sem_eventos = ctk.CTkLabel(
                self.scrollable_frame,
                text="Nenhum evento para este dia.",
                text_color="gray"
            )
            sem_eventos.pack(pady=20)
            return
        
        for evento in eventos_dia:
            self.criar_card_evento(evento)
    
    def criar_card_evento(self, evento):
        """Cria um card para exibir um evento"""
        event_card = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=10,
            border_width=1,
            border_color=self.get_cor_status(evento["status"])
        )
        event_card.pack(fill="x", pady=5, padx=5)
        
        # Conteúdo do evento
        content_frame = ctk.CTkFrame(event_card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Nome do evento
        nome_label = ctk.CTkLabel(
            content_frame,
            text=evento["nome"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        nome_label.pack(fill="x", pady=(0, 8))
        
        # Horário e status
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 5))
        
        horario_label = ctk.CTkLabel(
            info_frame,
            text=f"⏰ {evento['hora']}",
            text_color="gray"
        )
        horario_label.pack(side="left")
        
        # Status
        status_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        status_ponto = ctk.CTkFrame(
            status_frame,
            width=8,
            height=8,
            corner_radius=4,
            fg_color=self.get_cor_status(evento["status"])
        )
        status_ponto.pack(side="left", padx=(0, 5))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text=evento["status"].title(),
            font=ctk.CTkFont(size=11)
        )
        status_label.pack(side="left")
        
        # Endereço
        endereco_label = ctk.CTkLabel(
            content_frame,
            text=f"📍 {evento['endereco']}",
            text_color="gray",
            anchor="w"
        )
        endereco_label.pack(fill="x")
        
        # Descrição (curta)
        descricao = evento["descricao"]
        if len(descricao) > 60:
            descricao = descricao[:57] + "..."
        
        desc_label = ctk.CTkLabel(
            content_frame,
            text=descricao,
            wraplength=280,
            justify="left",
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(8, 0))
        
        # Botão para ver detalhes
        btn_detalhes = ctk.CTkButton(
            content_frame,
            text="Ver Detalhes",
            command=lambda e=evento: self.exibir_detalhes_evento(e),
            width=80,
            height=25,
            font=ctk.CTkFont(size=11)
        )
        btn_detalhes.pack(anchor="e", pady=(10, 0))

    def exibir_detalhes_evento(self, evento):
        """Exibe modal com detalhes completos do evento"""
        modal = ctk.CTkToplevel(self.root)
        modal.title("Detalhes do Evento")
        modal.geometry("500x500")
        modal.transient(self.root)
        modal.grab_set()
        
        # Centralizar modal
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        modal_width = 500
        modal_height = 500
        
        x = root_x + (root_width - modal_width) // 2
        y = root_y + (root_height - modal_height) // 2
        
        modal.geometry(f"{modal_width}x{modal_height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            main_frame,
            text="✕",
            command=modal.destroy,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=16)
        )
        close_btn.pack(anchor="ne")
        
        # Título do evento
        titulo = ctk.CTkLabel(
            main_frame,
            text=evento["nome"],
            font=ctk.CTkFont(size=22, weight="bold"),
            wraplength=450
        )
        titulo.pack(pady=(0, 20))
        
        # Informações do evento
        infos = [
            ("📅 Data:", evento["data"]),
            ("⏰ Horário:", evento["hora"]),
            ("📍 Endereço:", evento["endereco"]),
            ("📋 Status:", evento["status"].title()),
            ("📝 Descrição:", evento["descricao"])
        ]
        
        for icone_label, valor in infos:
            info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            info_frame.pack(fill="x", pady=8)
            
            label = ctk.CTkLabel(
                info_frame,
                text=icone_label,
                font=ctk.CTkFont(weight="bold")
            )
            label.pack(anchor="w")
            
            # Para descrição, usar wraplength
            if icone_label == "📝 Descrição:":
                valor_label = ctk.CTkLabel(
                    info_frame,
                    text=valor,
                    wraplength=450,
                    justify="left",
                    anchor="w"
                )
                valor_label.pack(anchor="w", padx=(10, 0), pady=(5, 0))
            else:
                valor_label = ctk.CTkLabel(
                    info_frame,
                    text=valor,
                    anchor="w"
                )
                valor_label.pack(anchor="w", padx=(10, 0))
        
        # Botão de ação
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(20, 0))
        
        if evento["status"] == "agendado":
            btn_acao = ctk.CTkButton(
                action_frame,
                text="Marcar como em andamento",
                fg_color="#FFB74D",
                hover_color="#FF9800",
                command=lambda: self.marcar_em_andamento(evento["id"], modal)
            )
            btn_acao.pack(side="left", padx=5)
        elif evento["status"] == "em_andamento":
            btn_acao = ctk.CTkButton(
                action_frame,
                text="Marcar como finalizado",
                fg_color="#FF5252",
                hover_color="#FF0000",
                command=lambda: self.marcar_finalizado(evento["id"], modal)
            )
            btn_acao.pack(side="left", padx=5)
        
        btn_fechar = ctk.CTkButton(
            action_frame,
            text="Fechar",
            command=modal.destroy
        )
        btn_fechar.pack(side="right", padx=5)
    
    def marcar_em_andamento(self, evento_id, modal):
        """Marca evento como em andamento"""
        for evento in self.eventos:
            if evento["id"] == evento_id:
                evento["status"] = "em_andamento"
                break
        
        modal.destroy()
        self.atualizar_calendario()
        self.exibir_eventos_mes()  # Atualizar lista de eventos do mês
        
    def marcar_finalizado(self, evento_id, modal):
        """Marca evento como finalizado"""
        for evento in self.eventos:
            if evento["id"] == evento_id:
                evento["status"] = "finalizado"
                break
        
        modal.destroy()
        self.atualizar_calendario()
        self.exibir_eventos_mes()  # Atualizar lista de eventos do mês
    
    def criar_evento(self):
        """Função para criar novo evento"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Criar Evento",
            "Funcionalidade de criar novo evento.\n"
            "Aqui você implementaria um formulário para adicionar novos eventos."
        )
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CalendarioDesktopApp()
    app.run()