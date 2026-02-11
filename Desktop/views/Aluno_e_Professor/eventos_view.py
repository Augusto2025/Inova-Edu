import customtkinter as ctk
from datetime import datetime, timedelta
import os
import sys

# Mantendo sua lógica de caminho para testes individuais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from assets.cores import *
except ImportError:
    # Cores de segurança caso o arquivo não seja encontrado no teste
    Branco = "#ffffff"
    azulEscuro = "#1a237e"

class CalendarioDesktopApp(ctk.CTkFrame):
    def __init__(self, master):  
        super().__init__(master)
        self.janela = master
        self.cor_fundo = "#f5f7fb"
        self.configure(fg_color=self.cor_fundo)

        # --- INTEGRAÇÃO COM A SIDEBAR ---
        from sidebar_AP import Sidebar, sidebar
        sidebar_existente = None
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break

        if not sidebar_existente:
            sidebar_existente, _ = sidebar(self.janela)
        
        self.pack(side="right", fill="both", expand=True)

        # 2. Inicialização de Variáveis e Dados (Simulando sua Tabela 'eventos')
        self.eventos = self.carregar_eventos_exemplo()
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        
        self.criar_interface()
        self.atualizar_calendario()

    def carregar_eventos_exemplo(self):
        """
        Retorna dados simulando a Tabela: eventos
        Columns: Nome_do_evento, Hora_do_evento, Data_do_evento, Descricao, Endereco, status
        """
        hoje = datetime.now().date()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=2)
        
        return [
            {
                "Nome_do_evento": "Reunião de Ontem",
                "Hora_do_evento": "10:00",
                "Data_do_evento": ontem.strftime('%Y-%m-%d'),
                "Descricao": "Discussão sobre o projeto PI que já ocorreu.",
                "Endereco": "Sala Virtual",
                "status": "Finalizado"
            },
            {
                "Nome_do_evento": "Apresentação PI",
                "Hora_do_evento": "14:30",
                "Data_do_evento": hoje.strftime('%Y-%m-%d'),
                "Descricao": "Apresentação do Desktop App para os professores.",
                "Endereco": "Auditório Central",
                "status": "Urgente"
            },
            {
                "Nome_do_evento": "Workshop Python",
                "Hora_do_evento": "09:00",
                "Data_do_evento": amanha.strftime('%Y-%m-%d'),
                "Descricao": "Aula prática de CustomTkinter e banco de dados.",
                "Endereco": "Laboratório 05",
                "status": "Agendado"
            }
        ]

    def abrir_modal_detalhes(self, evento):
        """Abre uma janela flutuante com as informações da tabela eventos"""
        modal = ctk.CTkToplevel(self)
        modal.title(f"Detalhes: {evento['Nome_do_evento']}")
        modal.geometry("450x450")
        modal.attributes("-topmost", True) # Mantém na frente
        modal.grab_set() # Bloqueia interação com a tela de trás
        modal.configure(fg_color="#ffffff")

        # Título do Modal
        ctk.CTkLabel(modal, text="📋 Detalhes do Evento", 
                     font=ctk.CTkFont(size=22, weight="bold"), text_color="#1e293b").pack(pady=20)

        container_info = ctk.CTkFrame(modal, fg_color="transparent")
        container_info.pack(fill="both", expand=True, padx=30)

        # Função auxiliar para exibir campos
        def info_row(label, texto):
            row = ctk.CTkFrame(container_info, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=f"{label}:", font=ctk.CTkFont(weight="bold"), text_color="#64748b").pack(side="left")
            ctk.CTkLabel(row, text=f" {texto}", text_color="#1e293b").pack(side="left")

        info_row("Evento", evento["Nome_do_evento"])
        info_row("Data", evento["Data_do_evento"])
        info_row("Hora", evento["Hora_do_evento"])
        info_row("Local", evento["Endereco"])
        info_row("Status", evento["status"])

        # Descrição (em uma caixa de texto)
        ctk.CTkLabel(container_info, text="Descrição:", font=ctk.CTkFont(weight="bold"), text_color="#64748b").pack(anchor="w", pady=(10, 0))
        txt_desc = ctk.CTkTextbox(container_info, height=100, border_width=1, fg_color="#f8fafc")
        txt_desc.pack(fill="x", pady=5)
        txt_desc.insert("0.0", evento["Descricao"])
        txt_desc.configure(state="disabled")

        ctk.CTkButton(modal, text="Fechar", command=modal.destroy, fg_color="#3b82f6").pack(pady=20)

    def criar_interface(self):
        self.conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True, padx=25, pady=20)

        # TÍTULO
        self.header_frame = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 25))
        ctk.CTkLabel(self.header_frame, text="Calendário de Eventos", 
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="#1e293b").pack(side="left")

        # NAVEGAÇÃO
        self.nav_bar = ctk.CTkFrame(self.conteudo, fg_color="transparent", height=50)
        self.nav_bar.pack(fill="x", pady=(0, 15))
        self.nav_bar.pack_propagate(False)

        # Ano (Esquerda)
        self.ano_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        self.ano_frame.pack(side="left")
        ctk.CTkButton(self.ano_frame, text="«", width=35, command=lambda: self.alterar_ano(-1), 
                      fg_color="#e2e8f0", text_color="#475569").pack(side="left", padx=2)
        self.ano_label_widget = ctk.CTkLabel(self.ano_frame, text=str(self.ano_atual), font=ctk.CTkFont(size=18, weight="bold"))
        self.ano_label_widget.pack(side="left", padx=12)
        ctk.CTkButton(self.ano_frame, text="»", width=35, command=lambda: self.alterar_ano(1), 
                      fg_color="#e2e8f0", text_color="#475569").pack(side="left", padx=2)

        # Mês (Centro)
        self.mes_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        self.mes_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkButton(self.mes_frame, text="◀", width=40, command=lambda: self.alterar_mes(-1)).pack(side="left", padx=15)
        self.month_label = ctk.CTkLabel(self.mes_frame, text="", font=ctk.CTkFont(size=22, weight="bold"), width=140)
        self.month_label.pack(side="left")
        ctk.CTkButton(self.mes_frame, text="▶", width=40, command=lambda: self.alterar_mes(1)).pack(side="left", padx=15)

        # Ações (Direita)
        self.acoes_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        self.acoes_frame.pack(side="right")
        ctk.CTkButton(self.acoes_frame, text="Hoje", width=80, command=self.ir_para_mes_atual).pack(side="left", padx=5)
        ctk.CTkButton(self.acoes_frame, text="➕ Novo Evento", width=140, fg_color="#28a745", command=self.criar_evento).pack(side="left", padx=5)

        # ÁREA DO CALENDÁRIO
        self.scroll_area = ctk.CTkScrollableFrame(self.conteudo, fg_color="#ffffff", corner_radius=15, border_width=1, border_color="#e2e8f0")
        self.scroll_area.pack(fill="both", expand=True)
        self.days_frame = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(7):
            self.days_frame.grid_columnconfigure(i, weight=1, uniform="dia")

    def atualizar_calendario(self):
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for i, day in enumerate(weekdays):
            ctk.CTkLabel(self.days_frame, text=day, font=ctk.CTkFont(size=14, weight="bold"), text_color="#94a3b8").grid(row=0, column=i, pady=10)

        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.month_label.configure(text=meses[self.mes_atual - 1])
        self.ano_label_widget.configure(text=str(self.ano_atual))

        primeiro_dia = datetime(self.ano_atual, self.mes_atual, 1)
        offset = (primeiro_dia.weekday() + 1) % 7
        ultimo_dia = (datetime(self.ano_atual, self.mes_atual + 1, 1) if self.mes_atual < 12 else datetime(self.ano_atual + 1, 1, 1)) - timedelta(days=1)
        
        hoje_dt = datetime.now().date()

        for dia in range(1, ultimo_dia.day + 1):
            pos = offset + dia - 1
            row, col = (pos // 7) + 1, pos % 7
            
            # BLOCOS MAIORES (Height=160)
            data_atual_bloco = datetime(self.ano_atual, self.mes_atual, dia).date()
            data_str = data_atual_bloco.strftime('%Y-%m-%d')
            
            # Busca se existe evento para este dia na lista
            evento_encontrado = next((e for e in self.eventos if e["Data_do_evento"] == data_str), None)

            dia_frame = ctk.CTkFrame(self.days_frame, height=160, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0")
            dia_frame.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            dia_frame.grid_propagate(False)
            
            lbl = ctk.CTkLabel(dia_frame, text=str(dia), font=ctk.CTkFont(size=16, weight="bold"))
            lbl.pack(anchor="nw", padx=12, pady=10)

            if evento_encontrado:
                # Muda cursor para indicar que é clicável
                dia_frame.configure(cursor="hand2")
                
                # LÓGICA DE CORES DA BARRA
                if data_atual_bloco < hoje_dt:
                    cor_barra = "#ef4444" # Vermelho
                elif data_atual_bloco == hoje_dt:
                    cor_barra = "#facc15" # Amarelo
                else:
                    cor_barra = "#22c55e" # Verde

                barra_evento = ctk.CTkFrame(dia_frame, height=8, fg_color=cor_barra, corner_radius=0)
                barra_evento.pack(side="bottom", fill="x")
                
                # BIND DE CLIQUE: Abre o modal ao clicar no bloco ou no número
                dia_frame.bind("<Button-1>", lambda e, ev=evento_encontrado: self.abrir_modal_detalhes(ev))
                lbl.bind("<Button-1>", lambda e, ev=evento_encontrado: self.abrir_modal_detalhes(ev))
                barra_evento.bind("<Button-1>", lambda e, ev=evento_encontrado: self.abrir_modal_detalhes(ev))

            if data_atual_bloco == hoje_dt:
                dia_frame.configure(border_color="#3b82f6", border_width=2)

    def alterar_mes(self, delta):
        self.mes_atual += delta
        if self.mes_atual > 12: self.mes_atual = 1; self.ano_atual += 1
        elif self.mes_atual < 1: self.mes_atual = 12; self.ano_atual -= 1
        self.atualizar_calendario()

    def alterar_ano(self, delta):
        self.ano_atual += delta
        self.atualizar_calendario()

    def ir_para_mes_atual(self):
        hoje = datetime.now()
        self.ano_atual, self.mes_atual = hoje.year, hoje.month
        self.atualizar_calendario()

    def criar_evento(self):
        print("Novo evento acionado")

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x850")
    app = CalendarioDesktopApp(root)
    root.mainloop()