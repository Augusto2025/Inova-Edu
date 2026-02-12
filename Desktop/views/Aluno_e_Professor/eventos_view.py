import customtkinter as ctk
from datetime import datetime, timedelta
import os
import sys

# Mantendo sua lógica de caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *

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
            sidebar(self.janela)
        
        self.pack(side="right", fill="both", expand=True)

        self.eventos = self.carregar_eventos_exemplo()
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        
        self.criar_interface()
        self.atualizar_calendario()

    def carregar_eventos_exemplo(self):
        hoje = datetime.now().date()
        return [
            {
                "Nome_do_evento": "Reunião de Alinhamento PI",
                "Hora_do_evento": "10:00",
                "Data_do_evento": (hoje - timedelta(days=1)).strftime('%Y-%m-%d'),
                "Descricao": "Discussão técnica sobre a arquitetura do projeto PI. Foco em banco de dados e interface.",
                "Endereco": "Sala Virtual 02"
            },
            {
                "Nome_do_evento": "Apresentação INOVA EDU",
                "Hora_do_evento": "14:30",
                "Data_do_evento": hoje.strftime('%Y-%m-%d'),
                "Descricao": "Apresentação final do sistema de calendário para a banca examinadora. Teste de todas as funcionalidades ao vivo.",
                "Endereco": "Auditório Central - Campus I"
            }
        ]

    def criar_interface(self):
        # --- HEADER (Cabeçalho Azul) ---
        self.header = ctk.CTkFrame(self, fg_color=azulEscuro, height=100, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Título dentro da Header
        ctk.CTkLabel(self.header, text="Calendário de Eventos", 
                     font=ctk.CTkFont(size=26, weight="bold"), 
                     text_color=Branco).pack(side="left", padx=30)

        # Container de Navegação dentro da Header (Direita)
        self.nav_bar = ctk.CTkFrame(self.header, fg_color="transparent")
        self.nav_bar.pack(side="right", padx=30)

        # Ano
        self.ano_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        self.ano_frame.pack(side="left", padx=10)
        ctk.CTkButton(self.ano_frame, text="«", width=30, fg_color="transparent", border_width=1, border_color=Branco, text_color=Branco, hover_color="#283593", command=lambda: self.alterar_ano(-1)).pack(side="left", padx=2)
        self.ano_label_widget = ctk.CTkLabel(self.ano_frame, text=str(self.ano_atual), font=ctk.CTkFont(size=18, weight="bold"), text_color=Branco)
        self.ano_label_widget.pack(side="left", padx=10)
        ctk.CTkButton(self.ano_frame, text="»", width=30, fg_color="transparent", border_width=1, border_color=Branco, text_color=Branco, hover_color="#283593", command=lambda: self.alterar_ano(1)).pack(side="left", padx=2)

        # Mês
        self.mes_frame = ctk.CTkFrame(self.nav_bar, fg_color="transparent")
        self.mes_frame.pack(side="left", padx=20)
        ctk.CTkButton(self.mes_frame, text="◀", width=35, fg_color="transparent", border_width=1, border_color=Branco, text_color=Branco, hover_color="#283593", command=lambda: self.alterar_mes(-1)).pack(side="left")
        self.month_label = ctk.CTkLabel(self.mes_frame, text="", font=ctk.CTkFont(size=20, weight="bold"), width=140, text_color=Branco)
        self.month_label.pack(side="left", padx=10)
        ctk.CTkButton(self.mes_frame, text="▶", width=35, fg_color="transparent", border_width=1, border_color=Branco, text_color=Branco, hover_color="#283593", command=lambda: self.alterar_mes(1)).pack(side="left")

        # Botão Hoje
        ctk.CTkButton(self.nav_bar, text="Hoje", width=70, fg_color=Branco, text_color=azulEscuro, font=ctk.CTkFont(weight="bold"), hover_color="#e0e0e0", command=self.ir_para_mes_atual).pack(side="left", padx=10)

        # --- ÁREA DE CONTEÚDO (Calendário e Detalhes) ---
        self.conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True, padx=25, pady=20)

        # CALENDÁRIO
        self.calendar_container = ctk.CTkFrame(self.conteudo, fg_color="#ffffff", corner_radius=15, border_width=1, border_color="#e2e8f0")
        self.calendar_container.pack(fill="x", side="top")
        
        self.days_frame = ctk.CTkFrame(self.calendar_container, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True, padx=10, pady=10)
        for i in range(7): self.days_frame.grid_columnconfigure(i, weight=1, uniform="dia")

        # ÁREA DE INFORMAÇÕES
        self.detalhes_frame = ctk.CTkFrame(self.conteudo, fg_color="#ffffff", corner_radius=15, border_width=1, border_color="#e2e8f0")
        self.detalhes_frame.pack(fill="both", expand=True, pady=(20, 0))

        self.label_aviso = ctk.CTkLabel(self.detalhes_frame, text="Selecione um evento para ver a descrição completa.", 
                                        font=ctk.CTkFont(size=20, slant="italic"), text_color="#94a3b8")
        self.label_aviso.place(relx=0.5, rely=0.5, anchor="center")

    def exibir_detalhes_embaixo(self, evento):
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.detalhes_frame, text=evento["Nome_do_evento"], 
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="#1e293b").pack(anchor="w", padx=40, pady=(25, 10))

        info_row = ctk.CTkFrame(self.detalhes_frame, fg_color="transparent")
        info_row.pack(fill="x", padx=40, pady=5)

        h_f = ctk.CTkFrame(info_row, fg_color="#f1f5f9", corner_radius=10)
        h_f.pack(side="left", padx=(0, 15))
        ctk.CTkLabel(h_f, text=f"🕒 Horário: {evento['Hora_do_evento']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#475569").pack(padx=15, pady=10)

        l_f = ctk.CTkFrame(info_row, fg_color="#f1f5f9", corner_radius=10)
        l_f.pack(side="left")
        ctk.CTkLabel(l_f, text=f"📍 Local: {evento['Endereco']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#475569").pack(padx=15, pady=10)

        ctk.CTkLabel(self.detalhes_frame, text="SOBRE O EVENTO", font=ctk.CTkFont(size=13, weight="bold"), text_color="#94a3b8").pack(anchor="w", padx=40, pady=(20, 5))
        
        desc_box = ctk.CTkTextbox(self.detalhes_frame, fg_color="transparent", font=ctk.CTkFont(size=18), text_color="#334155", border_width=0, wrap="word", height=150)
        desc_box.pack(fill="both", expand=True, padx=35, pady=(0, 20))
        desc_box.insert("0.0", evento["Descricao"])
        desc_box.configure(state="disabled")

    def atualizar_calendario(self):
        for widget in self.days_frame.winfo_children(): widget.destroy()

        dias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for i, d in enumerate(dias):
            ctk.CTkLabel(self.days_frame, text=d, font=ctk.CTkFont(size=14, weight="bold"), text_color="#94a3b8").grid(row=0, column=i, pady=5)

        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.month_label.configure(text=meses[self.mes_atual - 1])
        self.ano_label_widget.configure(text=str(self.ano_atual))

        primeiro_dia = datetime(self.ano_atual, self.mes_atual, 1)
        offset = (primeiro_dia.weekday() + 1) % 7
        ultimo_dia = (datetime(self.ano_atual, self.mes_atual + 1, 1) if self.mes_atual < 12 else datetime(self.ano_atual + 1, 1, 1)) - timedelta(days=1)
        hoje_dt = datetime.now().date()

        for r in range(1, 7): self.days_frame.grid_rowconfigure(r, minsize=100) 

        for dia in range(1, ultimo_dia.day + 1):
            pos = offset + dia - 1
            row, col = (pos // 7) + 1, pos % 7
            dt_bloco = datetime(self.ano_atual, self.mes_atual, dia).date()
            evento = next((e for e in self.eventos if e["Data_do_evento"] == dt_bloco.strftime('%Y-%m-%d')), None)

            dia_frame = ctk.CTkFrame(self.days_frame, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0")
            dia_frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            
            lbl = ctk.CTkLabel(dia_frame, text=str(dia), font=ctk.CTkFont(size=18, weight="bold"), text_color="#1e293b")
            lbl.pack(anchor="nw", padx=12, pady=8)

            if evento:
                dia_frame.configure(cursor="hand2", fg_color="#ffffff")
                cor = "#ef4444" if dt_bloco < hoje_dt else ("#facc15" if dt_bloco == hoje_dt else "#22c55e")
                ctk.CTkFrame(dia_frame, height=8, fg_color=cor, corner_radius=0).pack(side="bottom", fill="x")
                dia_frame.bind("<Button-1>", lambda e, ev=evento: self.exibir_detalhes_embaixo(ev))
                lbl.bind("<Button-1>", lambda e, ev=evento: self.exibir_detalhes_embaixo(ev))

            if dt_bloco == hoje_dt:
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
        h = datetime.now()
        self.ano_atual, self.mes_atual = h.year, h.month
        self.atualizar_calendario()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.attributes("-fullscreen", True)
    app = CalendarioDesktopApp(root)
    root.mainloop()