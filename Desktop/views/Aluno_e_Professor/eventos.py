import customtkinter as ctk
from datetime import datetime, timedelta
# Adicionar sidebar
try:
    from sidebar_AP import Sidebar
except Exception:
    Sidebar = None

class CalendarioDesktopApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.attributes("-fullscreen", True)

        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Dados de exemplo
        self.eventos = self.carregar_eventos_exemplo()
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        self.dia_selecionado = None
        
        self.criar_widgets()
        self.atualizar_calendario()
        
    def carregar_eventos_exemplo(self):
        """Carrega eventos de exemplo para demonstração"""
        return [
            {
                "id": 1,
                "nome": "Reunião de Planejamento",
                "data": f"{datetime.now().year}-01-15",
                "hora": "14:00",
                "descricao": "Reunião para planejar as atividades do trimestre. Todos os coordenadores devem participar.",
                "endereco": "Sala 101 - Bloco A",
                "status": "agendado"
            },
            {
                "id": 2,
                "nome": "Workshop de Python",
                "data": f"{datetime.now().year}-01-20",
                "hora": "09:00",
                "descricao": "Workshop sobre desenvolvimento em Python para iniciantes. Traga seu notebook.",
                "endereco": "Laboratório de Informática",
                "status": "em_andamento"
            },
            {
                "id": 3,
                "nome": "Apresentação de Projetos",
                "data": f"{datetime.now().year}-01-25",
                "hora": "16:00",
                "descricao": "Apresentação dos projetos finais dos alunos de Engenharia.",
                "endereco": "Auditório Principal",
                "status": "finalizado"
            },
            {
                "id": 4,
                "nome": "Avaliação Bimestral",
                "data": f"{datetime.now().year}-01-10",
                "hora": "10:00",
                "descricao": "Avaliação do primeiro bimestre de Matemática.",
                "endereco": "Sala 205",
                "status": "finalizado"
            },
            {
                "id": 5,
                "nome": "Palestra sobre IA",
                "data": f"{datetime.now().year}-01-30",
                "hora": "19:00",
                "descricao": "Palestra sobre Inteligência Artificial aplicada à educação com convidado especial.",
                "endereco": "Auditório Central",
                "status": "agendado"
            }
        ]
    
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Container principal
        self.main_container = ctk.CTkFrame(self.root, fg_color="#f8fafc")
        self.main_container.pack(fill="both", expand=True)
        # Sidebar (se disponível)
        if Sidebar:
            try:
                self.sidebar = Sidebar(self.main_container)
                self.sidebar.pack(side="left", fill="y")
            except Exception as e:
                print(f"[EVENTOS] Falha ao carregar Sidebar: {e}")
        
        # Cabeçalho
        self.criar_cabecalho()
        
        # Painel de navegação superior
        self.criar_navegacao_superior()
        
        # Linha divisória
        ctk.CTkFrame(
            self.main_container,
            height=2,
            fg_color="#e2e8f0"
        ).pack(fill="x", pady=(10, 20))
        
        # Container do calendário (centralizado)
        self.calendario_container = ctk.CTkFrame(
            self.main_container,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#e2e8f0"
        )
        self.calendario_container.pack(fill="both", expand=True)
        
        # Cabeçalho dos dias da semana
        self.criar_cabecalho_dias_semana()
        
        # Frame para os dias do calendário
        self.days_container = ctk.CTkFrame(
            self.calendario_container,
            fg_color="transparent"
        )
        self.days_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Frame interno para os dias
        self.days_frame = ctk.CTkFrame(
            self.days_container,
            fg_color="transparent"
        )
        self.days_frame.pack(fill="both", expand=True)
    
    def criar_cabecalho(self):
        """Cria o cabeçalho da aplicação"""
        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título principal
        titulo = ctk.CTkLabel(
            header_frame,
            text="📅 Calendário Acadêmico",
            font=ctk.CTkFont(size=32, weight="bold", family="Arial"),
            text_color="#1e293b"
        )
        titulo.pack(side="left")
        
        # Botão criar evento
        btn_criar = ctk.CTkButton(
            header_frame,
            text="+ Novo Evento",
            command=self.criar_evento,
            width=120,
            height=40,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        btn_criar.pack(side="right")
    
    def criar_navegacao_superior(self):
        """Cria o painel de navegação acima do calendário"""
        nav_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        nav_frame.pack(fill="x", pady=(0, 15))
        
        # Controle de ano (esquerda)
        year_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        year_frame.pack(side="left")
        
        # Botão ano anterior
        btn_prev_year = ctk.CTkButton(
            year_frame,
            text="◀",
            width=40,
            height=40,
            command=lambda: self.alterar_ano(-1),
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            corner_radius=8
        )
        btn_prev_year.pack(side="left", padx=(0, 10))
        
        # Ano atual
        self.year_label = ctk.CTkLabel(
            year_frame,
            text=str(self.ano_atual),
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1e293b"
        )
        self.year_label.pack(side="left", padx=10)
        
        # Botão próximo ano
        btn_next_year = ctk.CTkButton(
            year_frame,
            text="▶",
            width=40,
            height=40,
            command=lambda: self.alterar_ano(1),
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            corner_radius=8
        )
        btn_next_year.pack(side="left")
        
        # Mês atual (centro)
        meses_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        meses_frame.pack(side="left", expand=True)
        
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        
        self.month_label = ctk.CTkLabel(
            meses_frame,
            text=meses[self.mes_atual - 1],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1e293b"
        )
        self.month_label.pack()
        
        # Botões de meses (direita)
        months_buttons_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        months_buttons_frame.pack(side="right")
        
        # Botão mês anterior
        btn_prev_month = ctk.CTkButton(
            months_buttons_frame,
            text="Mês Anterior",
            width=100,
            height=40,
            command=lambda: self.alterar_mes(-1),
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        btn_prev_month.pack(side="left", padx=(0, 10))
        
        # Botão próximo mês
        btn_next_month = ctk.CTkButton(
            months_buttons_frame,
            text="Próximo Mês",
            width=100,
            height=40,
            command=lambda: self.alterar_mes(1),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        btn_next_month.pack(side="left")
        
        # Botão mês atual
        btn_current_month = ctk.CTkButton(
            months_buttons_frame,
            text="Hoje",
            width=80,
            height=40,
            command=self.ir_para_mes_atual,
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        btn_current_month.pack(side="left", padx=(10, 0))
    
    def criar_cabecalho_dias_semana(self):
        """Cria o cabeçalho com os dias da semana"""
        weekdays_frame = ctk.CTkFrame(
            self.calendario_container,
            fg_color="transparent"
        )
        weekdays_frame.pack(fill="x", padx=20, pady=20)
        
        weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for day in weekdays:
            label = ctk.CTkLabel(
                weekdays_frame,
                text=day,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#475569",
                width=100
            )
            label.pack(side="left", expand=True)
    
    def atualizar_calendario(self):
        """Atualiza o grid de dias do calendário com tamanhos uniformes"""
        # Limpar dias anteriores
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # Configurar grid 6x7 com tamanhos FIXOS e UNIFORMES
        for row in range(6):
            self.days_frame.grid_rowconfigure(row, weight=1, minsize=100)  # Altura fixa maior
        for col in range(7):
            self.days_frame.grid_columnconfigure(col, weight=1, minsize=100)  # Largura fixa
        
        # Obter primeiro dia do mês
        primeiro_dia = datetime(self.ano_atual, self.mes_atual, 1)
        
        # Encontrar o primeiro domingo do calendário
        offset = (primeiro_dia.weekday() + 1) % 7
        
        # Preencher dias vazios iniciais
        for i in range(offset):
            empty_frame = ctk.CTkFrame(
                self.days_frame,
                fg_color="transparent"
            )
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
            
            # Frame para o dia (TAMANHO FIXO)
            dia_frame = ctk.CTkFrame(
                self.days_frame,
                corner_radius=8,
                border_width=1,
                border_color="#e2e8f0",
                fg_color="white"
            )
            dia_frame.grid(
                row=linha, 
                column=coluna, 
                sticky="nsew", 
                padx=1, 
                pady=1
            )
            
            # Configurar grid interno para conteúdo
            dia_frame.grid_rowconfigure(0, weight=1)
            dia_frame.grid_columnconfigure(0, weight=1)
            
            # Container interno para o conteúdo
            content_frame = ctk.CTkFrame(dia_frame, fg_color="transparent")
            content_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
            
            # Número do dia (topo à esquerda)
            dia_label = ctk.CTkLabel(
                content_frame,
                text=str(dia),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#1e293b"
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
            
            # Se houver eventos, mostrar indicadores e tornar clicável
            if eventos_dia:
                # Container para indicadores
                indicators_frame = ctk.CTkFrame(
                    content_frame,
                    fg_color="transparent"
                )
                indicators_frame.pack(side="bottom", fill="x", pady=(5, 0))
                
                # Um indicador por tipo de evento (máximo 3)
                tipos_eventos = {}
                for evento in eventos_dia:
                    status = evento["status"]
                    if status not in tipos_eventos:
                        tipos_eventos[status] = evento
                
                for status in list(tipos_eventos.values())[:3]:
                    cor = self.get_cor_status(status["status"])
                    indicator = ctk.CTkFrame(
                        indicators_frame,
                        height=6,
                        corner_radius=3,
                        fg_color=cor
                    )
                    indicator.pack(side="left", fill="x", expand=True, padx=1)
                
                # Tornar clicável para abrir modal
                dia_frame.configure(cursor="hand2")
                for widget in [dia_frame, content_frame, dia_label]:
                    widget.bind("<Button-1>", lambda e, d=dia, ed=eventos_dia: self.abrir_modal_eventos(d, ed))
                    
                # Efeito hover
                dia_frame.bind("<Enter>", lambda e, f=dia_frame: f.configure(fg_color="#f8fafc"))
                dia_frame.bind("<Leave>", lambda e, f=dia_frame: f.configure(fg_color="white"))
            
            # Destacar se for o dia selecionado
            if dia == self.dia_selecionado:
                dia_frame.configure(
                    fg_color="#eff6ff",
                    border_color="#3b82f6",
                    border_width=2
                )
    
    def get_cor_status(self, status):
        """Retorna a cor correspondente ao status"""
        cores = {
            "finalizado": "#ef4444",      # Vermelho
            "em_andamento": "#f59e0b",    # Amarelo/laranja
            "agendado": "#10b981"         # Verde
        }
        return cores.get(status, "#94a3b8")
    
    def alterar_ano(self, delta):
        """Altera o ano atual"""
        self.ano_atual += delta
        self.year_label.configure(text=str(self.ano_atual))
        self.atualizar_calendario()
    
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
        
        self.year_label.configure(text=str(self.ano_atual))
        
        # Atualizar label do mês
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        self.month_label.configure(text=meses[self.mes_atual - 1])
        
        self.atualizar_calendario()
    
    def ir_para_mes_atual(self):
        """Vai para o mês atual"""
        hoje = datetime.now()
        self.ano_atual = hoje.year
        self.mes_atual = hoje.month
        
        self.year_label.configure(text=str(self.ano_atual))
        
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        self.month_label.configure(text=meses[self.mes_atual - 1])
        
        self.atualizar_calendario()
    
    def abrir_modal_eventos(self, dia, eventos_dia):
        """Abre modal com os eventos do dia clicado"""
        modal = ctk.CTkToplevel(self.root)
        modal.title(f"Eventos - {dia:02d}/{self.mes_atual:02d}/{self.ano_atual}")
        modal.geometry("600x700")
        modal.transient(self.root)
        modal.grab_set()
        
        # Centralizar modal
        modal.update_idletasks()
        modal_width = modal.winfo_width()
        modal_height = modal.winfo_height()
        
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        x = root_x + (root_width - modal_width) // 2
        y = root_y + (root_height - modal_height) // 2
        
        modal.geometry(f"{modal_width}x{modal_height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(modal, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Cabeçalho do modal
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Data do dia
        data_str = f"{dia:02d}/{self.mes_atual:02d}/{self.ano_atual}"
        data_label = ctk.CTkLabel(
            header_frame,
            text=data_str,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1e293b"
        )
        data_label.pack(side="left")
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            header_frame,
            text="✕",
            command=modal.destroy,
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#f1f5f9",
            text_color="#64748b",
            font=ctk.CTkFont(size=18)
        )
        close_btn.pack(side="right")
        
        # Número de eventos
        eventos_count = len(eventos_dia)
        count_label = ctk.CTkLabel(
            header_frame,
            text=f"{eventos_count} evento{'s' if eventos_count != 1 else ''}",
            font=ctk.CTkFont(size=14),
            text_color="#64748b"
        )
        count_label.pack(side="left", padx=(15, 0), pady=(5, 0))
        
        # Separador
        ctk.CTkFrame(
            main_frame,
            height=2,
            fg_color="#e2e8f0"
        ).pack(fill="x", pady=(0, 20))
        
        # Frame scrollable para eventos
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="transparent",
            height=500
        )
        scroll_frame.pack(fill="both", expand=True)
        
        # Exibir cada evento
        for evento in eventos_dia:
            self.criar_card_evento_modal(scroll_frame, evento)
        
        # Se não houver eventos (não deveria acontecer, mas por segurança)
        if not eventos_dia:
            sem_eventos = ctk.CTkLabel(
                scroll_frame,
                text="Nenhum evento para este dia",
                text_color="#94a3b8",
                font=ctk.CTkFont(size=14)
            )
            sem_eventos.pack(pady=50)
    
    def criar_card_evento_modal(self, parent, evento):
        """Cria um card detalhado para evento no modal"""
        event_card = ctk.CTkFrame(
            parent,
            corner_radius=10,
            fg_color="white",
            border_width=1,
            border_color="#e2e8f0"
        )
        event_card.pack(fill="x", pady=8)
        
        # Conteúdo do evento
        content_frame = ctk.CTkFrame(event_card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho do evento
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Nome do evento
        nome_label = ctk.CTkLabel(
            header_frame,
            text=evento["nome"],
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w",
            text_color="#1e293b"
        )
        nome_label.pack(side="left", fill="x", expand=True)
        
        # Status
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        status_ponto = ctk.CTkFrame(
            status_frame,
            width=12,
            height=12,
            corner_radius=6,
            fg_color=self.get_cor_status(evento["status"])
        )
        status_ponto.pack(side="left", padx=(0, 8))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text=evento["status"].title(),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.get_cor_status(evento["status"])
        )
        status_label.pack(side="left")
        
        # Linha de informações principais
        info_main_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_main_frame.pack(fill="x", pady=(0, 15))
        
        # Horário
        hora_frame = ctk.CTkFrame(info_main_frame, fg_color="transparent")
        hora_frame.pack(side="left", padx=(0, 30))
        
        hora_icon = ctk.CTkLabel(
            hora_frame,
            text="🕒",
            font=ctk.CTkFont(size=14)
        )
        hora_icon.pack(side="left", padx=(0, 8))
        
        hora_label = ctk.CTkLabel(
            hora_frame,
            text=evento["hora"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#475569"
        )
        hora_label.pack(side="left")
        
        # Local
        local_frame = ctk.CTkFrame(info_main_frame, fg_color="transparent")
        local_frame.pack(side="left")
        
        local_icon = ctk.CTkLabel(
            local_frame,
            text="📍",
            font=ctk.CTkFont(size=14)
        )
        local_icon.pack(side="left", padx=(0, 8))
        
        local_label = ctk.CTkLabel(
            local_frame,
            text=evento["endereco"],
            font=ctk.CTkFont(size=14),
            text_color="#475569"
        )
        local_label.pack(side="left")
        
        # Descrição
        desc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        desc_frame.pack(fill="x", pady=(0, 20))
        
        desc_title = ctk.CTkLabel(
            desc_frame,
            text="Descrição:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#475569",
            anchor="w"
        )
        desc_title.pack(fill="x", pady=(0, 5))
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text=evento["descricao"],
            wraplength=500,
            justify="left",
            anchor="w",
            text_color="#64748b"
        )
        desc_label.pack(fill="x")
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        if evento["status"] == "agendado":
            btn_acao = ctk.CTkButton(
                btn_frame,
                text="Iniciar Evento",
                command=lambda e=evento: self.marcar_em_andamento(e["id"], parent.winfo_toplevel()),
                width=120,
                height=35,
                fg_color="#f59e0b",
                hover_color="#d97706",
                font=ctk.CTkFont(size=13),
                corner_radius=6
            )
            btn_acao.pack(side="left", padx=(0, 10))
        elif evento["status"] == "em_andamento":
            btn_acao = ctk.CTkButton(
                btn_frame,
                text="Finalizar Evento",
                command=lambda e=evento: self.marcar_finalizado(e["id"], parent.winfo_toplevel()),
                width=120,
                height=35,
                fg_color="#ef4444",
                hover_color="#dc2626",
                font=ctk.CTkFont(size=13),
                corner_radius=6
            )
            btn_acao.pack(side="left", padx=(0, 10))
        
        btn_editar = ctk.CTkButton(
            btn_frame,
            text="Editar",
            width=80,
            height=35,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            font=ctk.CTkFont(size=13),
            corner_radius=6
        )
        btn_editar.pack(side="left", padx=(0, 10))
        
        btn_excluir = ctk.CTkButton(
            btn_frame,
            text="Excluir",
            width=80,
            height=35,
            fg_color="#f1f5f9",
            hover_color="#fee2e2",
            text_color="#ef4444",
            font=ctk.CTkFont(size=13),
            corner_radius=6
        )
        btn_excluir.pack(side="left")
    
    def marcar_em_andamento(self, evento_id, modal):
        """Marca evento como em andamento"""
        for evento in self.eventos:
            if evento["id"] == evento_id:
                evento["status"] = "em_andamento"
                break
        
        modal.destroy()
        self.atualizar_calendario()
    
    def marcar_finalizado(self, evento_id, modal):
        """Marca evento como finalizado"""
        for evento in self.eventos:
            if evento["id"] == evento_id:
                evento["status"] = "finalizado"
                break
        
        modal.destroy()
        self.atualizar_calendario()
    
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