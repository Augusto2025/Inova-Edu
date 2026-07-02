import customtkinter as ctk
from datetime import datetime, timedelta
import os
import sys

# Mantendo sua lógica de caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from assets.cores import *
from controllers.eventos_controller import EventosController

class CalendarioDesktopApp(ctk.CTkFrame):
    def __init__(self, master):  
        super().__init__(master)
        self.janela = master
        self.cor_fundo = "#f5f7fb"
        self.configure(fg_color=self.cor_fundo)

        # Instancia o controller para buscar dados reais
        self.controller = EventosController()

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

        # Agora carregamos os eventos do banco de dados
        self.eventos = self.carregar_eventos_banco()
        
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        
        self.criar_interface()
        self.atualizar_calendario()

    def carregar_eventos_banco(self):
        """Busca os eventos reais do banco através do Controller"""
        try:
            # O controller agora retorna uma lista de dicionários formatados
            return self.controller.obter_todos_eventos()
        except Exception as e:
            print(f"Erro ao carregar banco: {e}")
            return []

    def criar_interface(self):
        from assets.header import HeaderPadrao
        self.header = HeaderPadrao(self, titulo="Calendário de Eventos", comando_voltar=None)

        # SE FOR PROFESSOR: Renderiza o botão. SE FOR ALUNO: O botão simplesmente não existe na tela
        if self.controller.e_professor():
            self.btn_criar = ctk.CTkButton(self.header, text="➕ Criar Evento", width=140, 
                                           fg_color="#22c55e", hover_color="#16a34a", 
                                           font=ctk.CTkFont(weight="bold", size=14),
                                           command=self.abrir_modal_criar)
            self.btn_criar.pack(side="left", padx=10)

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

        # --- ÁREA DE CONTEÚDO ---
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

    def exibir_detalhes_embaixo(self, eventos):
        """Recebe uma lista de eventos daquele dia e renderiza todos em formato de cards"""
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()

        # Criamos um container rolável interno para suportar múltiplos eventos sem quebrar o layout
        scroll_container = ctk.CTkScrollableFrame(self.detalhes_frame, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True, padx=20, pady=20)

        for evento in eventos:
            # Card para cada evento individual
            card = ctk.CTkFrame(scroll_container, fg_color="#ffffff", border_width=1, border_color="#cbd5e1", corner_radius=12)
            card.pack(fill="x", pady=10, padx=10)

            # Linha Superior do Card (Título + Botões de Ação)
            titulo_row = ctk.CTkFrame(card, fg_color="transparent")
            titulo_row.pack(fill="x", padx=20, pady=(15, 5))

            ctk.CTkLabel(titulo_row, text=evento["nome"], 
                         font=ctk.CTkFont(size=22, weight="bold"), text_color="#1e293b").pack(side="left")

            # Validação de permissão do Professor Criador
            if evento.get("pode_gerenciar", False):
                acoes_frame = ctk.CTkFrame(titulo_row, fg_color="transparent")
                acoes_frame.pack(side="right")

                ctk.CTkButton(acoes_frame, text="✏️ Editar", width=80, fg_color="#3b82f6", hover_color="#2563eb",
                              font=ctk.CTkFont(weight="bold", size=12), command=lambda ev=evento: self.abrir_modal_editar(ev)).pack(side="left", padx=3)

                ctk.CTkButton(acoes_frame, text="🗑️ Excluir", width=80, fg_color="#ef4444", hover_color="#dc2626",
                              font=ctk.CTkFont(weight="bold", size=12), command=lambda ev_id=evento["id"]: self.confirmar_exclusao(ev_id)).pack(side="left", padx=3)

            # Linha de Informações (Horário e Local)
            info_row = ctk.CTkFrame(card, fg_color="transparent")
            info_row.pack(fill="x", padx=20, pady=5)

            h_f = ctk.CTkFrame(info_row, fg_color="#f1f5f9", corner_radius=8)
            h_f.pack(side="left", padx=(0, 10))
            ctk.CTkLabel(h_f, text=f"🕒 Horário: {evento['hora']}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#475569").pack(padx=10, pady=5)

            l_f = ctk.CTkFrame(info_row, fg_color="#f1f5f9", corner_radius=8)
            l_f.pack(side="left")
            ctk.CTkLabel(l_f, text=f"📍 Local: {evento['endereco']}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#475569").pack(padx=10, pady=5)

            # Descrição do Evento
            ctk.CTkLabel(card, text="SOBRE O EVENTO:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94a3b8").pack(anchor="w", padx=20, pady=(10, 2))
            
            # Usando Label dinâmico para a descrição dentro do card ficar mais fluido
            desc_lbl = ctk.CTkLabel(card, text=evento["descricao"], font=ctk.CTkFont(size=15), text_color="#334155", justify="left", anchor="w", wraplength=700)
            desc_lbl.pack(fill="x", padx=20, pady=(0, 15))

    def atualizar_calendario(self):
        self.eventos = self.carregar_eventos_banco()
        
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
            
            # MUDANÇA AQUI: Filtra TODOS os eventos deste dia específico em uma lista
            eventos_do_dia = [e for e in self.eventos if str(e["data"]) == dt_bloco.strftime('%Y-%m-%d')]

            dia_frame = ctk.CTkFrame(self.days_frame, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0")
            dia_frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            
            lbl = ctk.CTkLabel(dia_frame, text=str(dia), font=ctk.CTkFont(size=18, weight="bold"), text_color="#1e293b")
            lbl.pack(anchor="nw", padx=12, pady=8)

            # Se houver um ou mais eventos no dia
            if eventos_do_dia:
                dia_frame.configure(cursor="hand2", fg_color="#ffffff")
                
                # Exibe um contador sutil se houver mais de 1 evento
                if len(eventos_do_dia) > 1:
                    lbl_qtd = ctk.CTkLabel(dia_frame, text=f"{len(eventos_do_dia)} ev.", 
                                           font=ctk.CTkFont(size=11, weight="bold"), 
                                           text_color="#475569", fg_color="#e2e8f0", corner_radius=5)
                    lbl_qtd.pack(anchor="ne", padx=10, pady=5, side="top")

                cor = "#ef4444" if dt_bloco < hoje_dt else ("#facc15" if dt_bloco == hoje_dt else "#22c55e")
                ctk.CTkFrame(dia_frame, height=8, fg_color=cor, corner_radius=0).pack(side="bottom", fill="x")
                
                # Passa a lista completa de eventos para a função de clique
                dia_frame.bind("<Button-1>", lambda e, evs=eventos_do_dia: self.exibir_detalhes_embaixo(evs))
                lbl.bind("<Button-1>", lambda e, evs=eventos_do_dia: self.exibir_detalhes_embaixo(evs))

            if dt_bloco == hoje_dt:
                dia_frame.configure(border_color="#3b82f6", border_width=2)

    # --- MÉTODOS DE GERENCIAMENTO (POP-UPS DE FORMULÁRIOS) ---
    def abrir_modal_criar(self):
        if not self.controller.e_professor():
            return
        
        modal = ctk.CTkToplevel(self)
        modal.title("Criar Novo Evento")
        modal.geometry("500x550")
        modal.grab_set() # Foca apenas na janela pop-up
        modal.resizable(False, False)

        ctk.CTkLabel(modal, text="Novo Evento", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        ctk.CTkLabel(modal, text="Nome do Evento:").pack(anchor="w", padx=40)
        txt_nome = ctk.CTkEntry(modal, width=420)
        txt_nome.pack(pady=5)

        ctk.CTkLabel(modal, text="Data (AAAA-MM-DD):").pack(anchor="w", padx=40)
        txt_data = ctk.CTkEntry(modal, width=420)
        txt_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        txt_data.pack(pady=5)

        ctk.CTkLabel(modal, text="Horário (HH:MM):").pack(anchor="w", padx=40)
        txt_hora = ctk.CTkEntry(modal, width=420)
        txt_hora.insert(0, "14:00")
        txt_hora.pack(pady=5)

        ctk.CTkLabel(modal, text="Local / Endereço:").pack(anchor="w", padx=40)
        txt_local = ctk.CTkEntry(modal, width=420)
        txt_local.pack(pady=5)

        ctk.CTkLabel(modal, text="Descrição:").pack(anchor="w", padx=40)
        txt_desc = ctk.CTkTextbox(modal, width=420, height=100)
        txt_desc.pack(pady=5)

        def salvar():
            msg, sucesso = self.controller.criar_evento(
                txt_nome.get(), txt_hora.get(), txt_data.get(), txt_desc.get("0.0", "end"), txt_local.get()
            )
            if sucesso:
                modal.destroy()
                self.atualizar_calendario()
            else:
                print(f"Erro: {msg}")

        ctk.CTkButton(modal, text="Salvar Evento", fg_color="#22c55e", command=salvar).pack(pady=20)

    def abrir_modal_editar(self, evento):
        modal = ctk.CTkToplevel(self)
        modal.title("Editar Evento")
        modal.geometry("500x550")
        modal.grab_set()
        modal.resizable(False, False)

        ctk.CTkLabel(modal, text="Editar Evento", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        ctk.CTkLabel(modal, text="Nome do Evento:").pack(anchor="w", padx=40)
        txt_nome = ctk.CTkEntry(modal, width=420)
        txt_nome.insert(0, evento["nome"])
        txt_nome.pack(pady=5)

        ctk.CTkLabel(modal, text="Data (AAAA-MM-DD):").pack(anchor="w", padx=40)
        txt_data = ctk.CTkEntry(modal, width=420)
        txt_data.insert(0, str(evento["data"]))
        txt_data.pack(pady=5)

        ctk.CTkLabel(modal, text="Horário (HH:MM):").pack(anchor="w", padx=40)
        txt_hora = ctk.CTkEntry(modal, width=420)
        txt_hora.insert(0, str(evento["hora"]))
        txt_hora.pack(pady=5)

        ctk.CTkLabel(modal, text="Local / Endereço:").pack(anchor="w", padx=40)
        txt_local = ctk.CTkEntry(modal, width=420)
        txt_local.insert(0, evento["endereco"])
        txt_local.pack(pady=5)

        ctk.CTkLabel(modal, text="Descrição:").pack(anchor="w", padx=40)
        txt_desc = ctk.CTkTextbox(modal, width=420, height=100)
        txt_desc.insert("0.0", evento["descricao"])
        txt_desc.pack(pady=5)

        def salvar_alteracao():
            msg, sucesso = self.controller.atualizar_evento(
                evento["id"], txt_nome.get(), txt_hora.get(), txt_data.get(), txt_desc.get("0.0", "end"), txt_local.get()
            )
            if sucesso:
                modal.destroy()
                self.atualizar_calendario()
                
                # --- CORREÇÃO DO ERRO AQUI ---
                # Limpa tudo com segurança
                for widget in self.detalhes_frame.winfo_children(): 
                    widget.destroy()
                
                # Criamos um NOVO label de aviso na hora em vez de tentar usar o antigo que foi destruído
                aviso = ctk.CTkLabel(self.detalhes_frame, text="Selecione um evento para ver a descrição completa.", 
                                     font=ctk.CTkFont(size=20, slant="italic"), text_color="#94a3b8")
                aviso.place(relx=0.5, rely=0.5, anchor="center")
            else:
                print(f"Erro: {msg}")

        ctk.CTkButton(modal, text="Atualizar Dados", fg_color="#3b82f6", command=salvar_alteracao).pack(pady=20)

    def confirmar_exclusao(self, id_evento):
        msg, sucesso = self.controller.deletar_evento(id_evento)
        if sucesso:
            self.atualizar_calendario()
            
            # --- CORREÇÃO DO ERRO NA EXCLUSÃO TAMBÉM ---
            for widget in self.detalhes_frame.winfo_children(): 
                widget.destroy()
                
            aviso = ctk.CTkLabel(self.detalhes_frame, text="Selecione um evento para ver a descrição completa.", 
                                 font=ctk.CTkFont(size=20, slant="italic"), text_color="#94a3b8")
            aviso.place(relx=0.5, rely=0.5, anchor="center")

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