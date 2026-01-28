import customtkinter as ctk
from tkinter import messagebox

# Configurar aparência
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")

class CadastroCursos:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Cadastro de Cursos")
        self.janela.geometry("1000x600")
        
        # Configurar cores personalizadas
        self.cor_azul = "#004a8d"
        self.cor_azul_hover = "#003366"
        self.cor_branco = "#ffffff"
        self.cor_cinza_claro = "#f5f5f5"
        self.cor_cinza = "#e0e0e0"
        self.cor_texto = "#333333"
        
        # Aplicar cores de fundo
        self.janela.configure(fg_color=self.cor_branco)
        
        self.criar_menu_lateral()
        self.criar_tela_cadastro()
        
    def criar_menu_lateral(self):
        # Frame do menu lateral
        self.menu_frame = ctk.CTkFrame(
            self.janela, 
            width=220, 
            corner_radius=0,
            fg_color=self.cor_azul
        )
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)
        
        # Título do menu
        titulo_label = ctk.CTkLabel(
            self.menu_frame,
            text="MENU PRINCIPAL",
            font=ctk.CTkFont(size=18, weight="bold", family="Arial"),
            text_color=self.cor_branco
        )
        titulo_label.pack(pady=(30, 20))
        
        # Separador
        separador = ctk.CTkFrame(
            self.menu_frame, 
            height=2,
            fg_color=self.cor_branco,
            bg_color=self.cor_azul
        )
        separador.pack(fill="x", padx=20, pady=5)
        
        # Opções do menu
        opcoes_menu = [
            "📚 Cadastro de Cursos",
            "",
            "",
            "",
            "",
            ""
        ]
        
        self.botoes_menu = []
        
        for opcao in opcoes_menu:
            botao = ctk.CTkButton(
                self.menu_frame,
                text=opcao,
                command=lambda o=opcao: self.selecionar_menu(o),
                height=45,
                anchor="w",
                fg_color="transparent",
                hover_color=self.cor_azul_hover,
                text_color=self.cor_branco,
                font=ctk.CTkFont(size=14, family="Arial"),
                corner_radius=5,
                border_width=0
            )
            botao.pack(fill="x", padx=15, pady=3)
            self.botoes_menu.append(botao)
            
        # Espaço vazio para preencher
        espaco_vazio = ctk.CTkLabel(self.menu_frame, text="", height=20)
        espaco_vazio.pack(fill="x", expand=True)
        
        # Botão Sair
        sair_btn = ctk.CTkButton(
            self.menu_frame,
            text="🚪 Sair do Sistema",
            command=self.janela.quit,
            height=45,
            fg_color=self.cor_branco,
            hover_color=self.cor_cinza_claro,
            text_color=self.cor_azul,
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            corner_radius=8
        )
        sair_btn.pack(side="bottom", fill="x", padx=15, pady=20)
        
    def criar_tela_cadastro(self):
        # Frame principal do conteúdo
        self.conteudo_frame = ctk.CTkFrame(
            self.janela,
            fg_color=self.cor_branco,
            corner_radius=0
        )
        self.conteudo_frame.pack(side="right", fill="both", expand=True)
        
        # Cabeçalho
        cabecalho_frame = ctk.CTkFrame(
            self.conteudo_frame,
            fg_color=self.cor_azul,
            height=80,
            corner_radius=0
        )
        cabecalho_frame.pack(fill="x")
        cabecalho_frame.pack_propagate(False)
        
        # Título da tela no cabeçalho
        titulo = ctk.CTkLabel(
            cabecalho_frame,
            text="📝 CADASTRO DE CURSOS",
            font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
            text_color=self.cor_branco
        )
        titulo.pack(side="left", padx=30, pady=20)
        
        # Frame para os campos (com scroll se necessário)
        container = ctk.CTkFrame(self.conteudo_frame, fg_color=self.cor_branco)
        container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Frame para os campos
        campos_frame = ctk.CTkFrame(
            container,
            fg_color=self.cor_cinza_claro,
            corner_radius=15
        )
        campos_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar grid para os campos
        campos_frame.grid_columnconfigure(1, weight=1)
        
        # Estilo comum para labels
        estilo_label = {
            "font": ctk.CTkFont(size=14, weight="bold", family="Arial"),
            "text_color": self.cor_azul
        }
        
        # Estilo comum para entries
        estilo_entry = {
            "height": 40,
            "border_width": 2,
            "border_color": self.cor_cinza,
            "fg_color": self.cor_branco,
            "text_color": self.cor_texto,
            "font": ctk.CTkFont(size=13, family="Arial"),
            "corner_radius": 8
        }
        
        # Campo Nome
        nome_label = ctk.CTkLabel(
            campos_frame, 
            text="Nome do Curso: *",
            **estilo_label
        )
        nome_label.grid(row=0, column=0, padx=(30, 15), pady=(30, 15), sticky="w")
        
        self.nome_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Digite o nome do curso...",
            width=400,
            **estilo_entry
        )
        self.nome_entry.grid(row=0, column=1, padx=(0, 30), pady=(30, 15), sticky="ew")
        
        # Campo Data de Início
        inicio_label = ctk.CTkLabel(
            campos_frame, 
            text="Data de Início:",
            **estilo_label
        )
        inicio_label.grid(row=1, column=0, padx=(30, 15), pady=15, sticky="w")
        
        self.inicio_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="DD/MM/AAAA",
            **estilo_entry
        )
        self.inicio_entry.grid(row=1, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Campo Data de Término
        termino_label = ctk.CTkLabel(
            campos_frame, 
            text="Data de Término:",
            **estilo_label
        )
        termino_label.grid(row=2, column=0, padx=(30, 15), pady=15, sticky="w")
        
        self.termino_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="DD/MM/AAAA",
            **estilo_entry
        )
        self.termino_entry.grid(row=2, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Campo Imagem
        imagem_label = ctk.CTkLabel(
            campos_frame, 
            text="Imagem:",
            **estilo_label
        )
        imagem_label.grid(row=3, column=0, padx=(30, 15), pady=15, sticky="w")
        
        imagem_frame = ctk.CTkFrame(
            campos_frame,
            fg_color="transparent"
        )
        imagem_frame.grid(row=3, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        self.imagem_entry = ctk.CTkEntry(
            imagem_frame,
            placeholder_text="Selecione uma imagem...",
            **estilo_entry
        )
        self.imagem_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.buscar_btn = ctk.CTkButton(
            imagem_frame,
            text="📁 Buscar",
            width=100,
            height=40,
            fg_color=self.cor_azul,
            hover_color=self.cor_azul_hover,
            text_color=self.cor_branco,
            font=ctk.CTkFont(size=13, weight="bold", family="Arial"),
            corner_radius=8,
            command=self.buscar_imagem
        )
        self.buscar_btn.pack(side="right")
        
        # Campo Descrição
        descricao_label = ctk.CTkLabel(
            campos_frame, 
            text="Descrição:",
            **estilo_label
        )
        descricao_label.grid(row=4, column=0, padx=(30, 15), pady=15, sticky="nw")
        
        self.descricao_text = ctk.CTkTextbox(
            campos_frame,
            height=120,
            border_width=2,
            border_color=self.cor_cinza,
            fg_color=self.cor_branco,
            text_color=self.cor_texto,
            font=ctk.CTkFont(size=13, family="Arial"),
            corner_radius=8
        )
        self.descricao_text.grid(row=4, column=1, padx=(0, 30), pady=15, sticky="nsew")
        
        # Frame para os botões de ação
        botoes_frame = ctk.CTkFrame(
            campos_frame, 
            fg_color="transparent",
            height=80
        )
        botoes_frame.grid(row=5, column=0, columnspan=2, pady=(20, 30), sticky="ew")
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)
        
        # Botão Limpar (à esquerda)
        self.limpar_btn = ctk.CTkButton(
            botoes_frame,
            text="🔄 LIMPAR CAMPOS",
            command=self.limpar_campos,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            fg_color=self.cor_cinza,
            hover_color="#cccccc",
            text_color=self.cor_texto,
            corner_radius=10,
            border_width=0
        )
        self.limpar_btn.grid(row=0, column=0, padx=(30, 10), sticky="ew")
        
        # Botão Salvar (à direita)
        self.salvar_btn = ctk.CTkButton(
            botoes_frame,
            text="💾 SALVAR CURSO",
            command=self.salvar_curso,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            fg_color=self.cor_azul,
            hover_color=self.cor_azul_hover,
            text_color=self.cor_branco,
            corner_radius=10,
            border_width=0
        )
        self.salvar_btn.grid(row=0, column=1, padx=(10, 30), sticky="ew")
        
        # Rodapé informativo
        rodape = ctk.CTkLabel(
            campos_frame,
            text="* Campos marcados com asterisco são obrigatórios",
            font=ctk.CTkFont(size=11, family="Arial"),
            text_color="#666666"
        )
        rodape.grid(row=6, column=0, columnspan=2, pady=(0, 20))
        
    def buscar_imagem(self):
        # Em uma aplicação real, você implementaria o filedialog aqui
        messagebox.showinfo(
            "Buscar Imagem", 
            "Funcionalidade para selecionar imagem.\n\nEm uma versão completa, um filedialog seria aberto para escolher o arquivo.",
            icon="info"
        )
        
    def salvar_curso(self):
        # Coletar dados dos campos
        nome = self.nome_entry.get()
        inicio = self.inicio_entry.get()
        termino = self.termino_entry.get()
        imagem = self.imagem_entry.get()
        descricao = self.descricao_text.get("1.0", "end-1c")
        
        # Validação
        if not nome:
            messagebox.showwarning(
                "Atenção", 
                "O campo 'Nome do Curso' é obrigatório!",
                icon="warning"
            )
            self.nome_entry.focus()
            return
            
        # Aqui você normalmente salvaria no banco de dados
        dados = {
            "Nome": nome,
            "Início": inicio if inicio else "Não informado",
            "Término": termino if termino else "Não informado",
            "Imagem": imagem if imagem else "Não selecionada",
            "Descrição": descricao if descricao else "Sem descrição"
        }
        
        # Mostrar mensagem de sucesso
        messagebox.showinfo(
            "Sucesso!", 
            f"Curso '{nome}' salvo com sucesso!\n\n"
            f"Os dados foram processados e estão prontos para serem armazenados no banco de dados.",
            icon="info"
        )
        
        # Limpar campos após salvar (opcional)
        # self.limpar_campos()
        
    def limpar_campos(self):
        # Limpar todos os campos
        self.nome_entry.delete(0, "end")
        self.inicio_entry.delete(0, "end")
        self.termino_entry.delete(0, "end")
        self.imagem_entry.delete(0, "end")
        self.descricao_text.delete("1.0", "end")
        
        # Focar no primeiro campo
        self.nome_entry.focus()
        
    def selecionar_menu(self, opcao):
        # Destacar o botão selecionado
        for botao in self.botoes_menu:
            if botao.cget("text") == opcao:
                botao.configure(
                    fg_color=self.cor_azul_hover,
                    text_color=self.cor_branco
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    text_color=self.cor_branco
                )
        
        # Aqui você implementaria a troca de telas
        print(f"Menu selecionado: {opcao}")
        
        # Exemplo de feedback visual
        if opcao != "📚 Cadastro de Cursos":
            messagebox.showinfo(
                "Navegação",
                f"Você selecionou: {opcao}\n\n"
                "Em uma versão completa, esta ação carregaria a tela correspondente.",
                icon="info"
            )
        
    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = CadastroCursos()
    app.run()