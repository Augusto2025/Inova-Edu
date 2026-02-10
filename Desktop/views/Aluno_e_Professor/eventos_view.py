# views/Aluno_e_Professor/eventos_view.py
import customtkinter as ctk
from controllers.eventos_controller import EventosController
from assets.cores import *
import traceback

class Eventos(ctk.CTkFrame):
    def __init__(self, master, id_usuario=None):
        super().__init__(master)
        self.controller = EventosController()
        self.id_usuario = id_usuario
        self.eventos_data = []
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
        
        # Importar e criar sidebar
        try:
            from sidebar_AP import Sidebar
            self.sidebar = Sidebar(self.container_principal)
            self.sidebar.pack(side="left", fill="y")
        except Exception as e:
            print(f"[VIEW EVENTOS] Erro ao carregar sidebar: {str(e)}")
        
        # Criar conteúdo principal
        self.content_frame = ctk.CTkFrame(self.container_principal, fg_color=self.cor_fundo)
        self.content_frame.pack(side="left", fill="both", expand=True)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        print("[VIEW EVENTOS] Inicializando tela de eventos...")
        
        try:
            self.setup_ui()
            self.carregar_eventos()
        except Exception as e:
            print(f"[VIEW EVENTOS ERRO] {str(e)}")
            print(f"[VIEW EVENTOS TRACEBACK] {traceback.format_exc()}")
    
    def setup_ui(self):
        """Cria a interface da tela de eventos"""
        # HEADER
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="#1f6aa5")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        ctk.CTkLabel(
            header_frame, 
            text="Eventos", 
            font=("Arial", 24, "bold"), 
            text_color="white"
        ).pack(pady=10, padx=10)
        
        # BOTÃO CRIAR EVENTO
        botoes_frame = ctk.CTkFrame(header_frame, fg_color="#1f6aa5")
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            botoes_frame,
            text="+ Novo Evento",
            command=self.abrir_criar_evento,
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes_frame,
            text="↻ Atualizar",
            command=self.carregar_eventos,
            fg_color="#1976D2",
            hover_color="#1565C0"
        ).pack(side="left", padx=5)
        
        # CONTEÚDO
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # LABEL INFO
        self.info_label = ctk.CTkLabel(
            self.scroll_frame, 
            text="Carregando eventos...", 
            text_color="gray"
        )
        self.info_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def carregar_eventos(self):
        """Carrega e exibe os eventos"""
        try:
            print("[VIEW EVENTOS] Carregando eventos...")
            # Se tiver ID de usuário, busca apenas seus eventos; senão busca todos
            if self.id_usuario:
                self.eventos_data = self.controller.obter_eventos_do_usuario(self.id_usuario)
            else:
                self.eventos_data = self.controller.obter_todos_eventos()
            
            self.exibir_eventos()
        except Exception as e:
            print(f"[VIEW EVENTOS ERRO AO CARREGAR] {str(e)}")
            self.info_label.configure(text=f"Erro ao carregar eventos: {str(e)}")
    
    def exibir_eventos(self):
        """Exibe a lista de eventos"""
        # Limpa frame anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not self.eventos_data:
            self.info_label = ctk.CTkLabel(
                self.scroll_frame, 
                text="Nenhum evento encontrado", 
                text_color="gray"
            )
            self.info_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            return
        
        # Exibe cada evento
        for idx, evento in enumerate(self.eventos_data):
            self.criar_card_evento(evento, idx)
    
    def criar_card_evento(self, evento, idx):
        """Cria um card para exibir um evento"""
        id_evento, nome, hora, data, descricao, endereco, id_usuario = evento
        
        card_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#ffffff")
        card_frame.grid(row=idx, column=0, sticky="ew", padx=5, pady=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # CABEÇALHO DO CARD
        header_card = ctk.CTkFrame(card_frame, fg_color="#1f6aa5")
        header_card.grid(row=0, column=0, sticky="ew")
        header_card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_card,
            text=nome,
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=10, pady=5)
        
        # DETALHES
        detalhes_frame = ctk.CTkFrame(card_frame, fg_color="white")
        detalhes_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        detalhes_frame.grid_columnconfigure(0, weight=1)
        
        info_text = f"""
📅 Data: {data}
🕐 Hora: {hora}
📍 Local: {endereco}
📝 {descricao}
        """.strip()
        
        ctk.CTkLabel(
            detalhes_frame,
            text=info_text,
            text_color="#333",
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=10)
        
        # BOTÕES
        botoes_card = ctk.CTkFrame(card_frame, fg_color="white")
        botoes_card.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(
            botoes_card,
            text="Editar",
            width=60,
            command=lambda: self.abrir_editar_evento(id_evento),
            fg_color="#1976D2",
            hover_color="#1565C0",
            font=("Arial", 10)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botoes_card,
            text="Deletar",
            width=60,
            command=lambda: self.deletar_evento(id_evento),
            fg_color="#C62828",
            hover_color="#B71C1C",
            font=("Arial", 10)
        ).pack(side="left", padx=5)
    
    def abrir_criar_evento(self):
        """Abre diálogo para criar novo evento"""
        print("[VIEW EVENTOS] Abrindo criar evento...")
        
        dialog = ctk.CTkToplevel(self.janela)
        dialog.title("Novo Evento")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        
        # CAMPOS
        campo_frame = ctk.CTkFrame(dialog)
        campo_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        labels_placeholders = [
            ("Nome do Evento", "nome_evento"),
            ("Data (YYYY-MM-DD)", "data_evento"),
            ("Hora (HH:MM:SS)", "hora_evento"),
            ("Endereço", "endereco"),
            ("Descrição", "descricao"),
        ]
        
        campos = {}
        for label_text, chave in labels_placeholders:
            ctk.CTkLabel(campo_frame, text=label_text, font=("Arial", 11)).pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(campo_frame, width=300)
            entry.pack(pady=5, fill="x")
            campos[chave] = entry
        
        # BOTÕES
        def salvar():
            try:
                nome = campos["nome_evento"].get()
                data = campos["data_evento"].get()
                hora = campos["hora_evento"].get()
                endereco = campos["endereco"].get()
                descricao = campos["descricao"].get()
                
                result = self.controller.criar_evento(nome, hora, data, descricao, endereco, self.id_usuario or 1)
                if result[1]:
                    print("[VIEW EVENTOS] Evento criado com sucesso")
                    dialog.destroy()
                    self.carregar_eventos()
                else:
                    print(f"[VIEW EVENTOS] Erro ao criar: {result[0]}")
            except Exception as e:
                print(f"[VIEW EVENTOS ERRO CRIAR] {str(e)}")
        
        botoes = ctk.CTkFrame(campo_frame)
        botoes.pack(pady=20, fill="x")
        
        ctk.CTkButton(botoes, text="Salvar", command=salvar, fg_color="#2E7D32").pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="Cancelar", command=dialog.destroy, fg_color="#757575").pack(side="left", padx=5)
    
    def abrir_editar_evento(self, id_evento):
        """Abre diálogo para editar evento (placeholder)"""
        print(f"[VIEW EVENTOS] Editando evento {id_evento}")
        # TODO: Implementar edição
    
    def deletar_evento(self, id_evento):
        """Deleta um evento com confirmação"""
        try:
            print(f"[VIEW EVENTOS] Deletando evento {id_evento}...")
            result = self.controller.deletar_evento(id_evento)
            if result[1]:
                self.carregar_eventos()
        except Exception as e:
            print(f"[VIEW EVENTOS ERRO DELETE] {str(e)}")


def run(master):
    """Função para integração com a sidebar"""
    return Eventos(master)
