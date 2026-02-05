import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

# Configurar aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ListaUsuarios:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Gestão de Usuários")
        
        # Obtém o tamanho da tela
        self.largura_tela = self.janela.winfo_screenwidth()
        self.altura_tela = self.janela.winfo_screenheight()
        
        # Configurar janela para ocupar toda a tela
        self.janela.geometry(f"{self.largura_tela}x{self.altura_tela}")
        self.janela.state('zoomed')  # Maximiza a janela
        
        # Configurar cores personalizadas
        self.cor_azul = "#004a8d"
        self.cor_azul_hover = "#003366"
        self.cor_branco = "#ffffff"
        self.cor_cinza_claro = "#f5f5f5"
        self.cor_cinza = "#e0e0e0"
        self.cor_texto = "#333333"
        self.cor_verde = "#28a745"
        self.cor_verde_hover = "#218838"
        self.cor_vermelho = "#dc3545"
        
        # Configurar pesos para redimensionamento
        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)
        
        # Aplicar cores de fundo
        self.janela.configure(fg_color=self.cor_branco)
        
        # Dados de exemplo baseados na imagem
        self.usuarios = [
            {"nome": "Augusto", "sobrenome": "Sousa", "email": "Augusto@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Felipe", "sobrenome": "Monteiro", "email": "Felip01@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Professor", "ativo": True},
            {"nome": "Jona", "sobrenome": "Costa", "email": "JonyMal@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Coordenador", "ativo": True},
            {"nome": "Kleber", "sobrenome": "Marques", "email": "Klebin@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Maria", "sobrenome": "Fernandes", "email": "maria.fernandes@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Professor", "ativo": True},
            {"nome": "João", "sobrenome": "Pereira", "email": "joao.pereira@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Paula", "sobrenome": "Mendes", "email": "paula.mendes@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Coordenador", "ativo": True},
            {"nome": "Ricardo", "sobrenome": "Oliveira", "email": "ricardo.oliveira@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Mariana", "sobrenome": "Silva", "email": "mariana.silva@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Carlos", "sobrenome": "Almeida", "email": "carlos.almeida@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Professor", "ativo": True},
            {"nome": "Ana", "sobrenome": "Santos", "email": "ana.santos@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Pedro", "sobrenome": "Lima", "email": "pedro.lima@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Professor", "ativo": True},
            {"nome": "Carla", "sobrenome": "Rodrigues", "email": "carla.rodrigues@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Coordenador", "ativo": True},
            {"nome": "Roberto", "sobrenome": "Fernandes", "email": "roberto.fernandes@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Aluno", "ativo": True},
            {"nome": "Fernanda", "sobrenome": "Alves", "email": "fernanda.alves@gmail.com", 
             "descricao": "🖼️", "imagem": "🔗", "tipo": "Professor", "ativo": True}
        ]
        
        self.criar_menu_lateral()
        self.criar_tela_lista()
        
        # Configurar redimensionamento responsivo
        self.janela.bind('<Configure>', self.on_window_resize)
        
    def criar_menu_lateral(self):
        # Frame do menu lateral
        self.menu_frame = ctk.CTkFrame(
            self.janela, 
            width=250,  # Largura fixa para menu
            corner_radius=0,
            fg_color=self.cor_azul
        )
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.grid_propagate(False)
        
        # Container para conteúdo do menu
        menu_container = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        menu_container.pack(fill="both", expand=True, padx=10, pady=20)
        
        # Título do menu
        titulo_label = ctk.CTkLabel(
            menu_container,
            text="MENU PRINCIPAL",
            font=ctk.CTkFont(size=18, weight="bold", family="Arial"),
            text_color=self.cor_branco
        )
        titulo_label.pack(pady=(0, 20))
        
        # Separador
        separador = ctk.CTkFrame(
            menu_container, 
            height=2,
            fg_color=self.cor_branco,
            bg_color=self.cor_azul
        )
        separador.pack(fill="x", pady=5)
        
        # Opções do menu
        opcoes_menu = [
            "📚 Cadastro de Cursos",
            "👥 Cadastro de Turmas",
            "👤 Lista de Usuários",
            "📊 Relatórios",
            "⚙️ Configurações"
        ]
        
        self.botoes_menu = []
        
        for opcao in opcoes_menu:
            botao = ctk.CTkButton(
                menu_container,
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
            botao.pack(fill="x", pady=3)
            self.botoes_menu.append(botao)
            
        # Espaço vazio para preencher
        espaco_vazio = ctk.CTkLabel(menu_container, text="")
        espaco_vazio.pack(fill="both", expand=True)
        
        # Botão Sair
        sair_btn = ctk.CTkButton(
            menu_container,
            text="🚪 Sair do Sistema",
            command=self.janela.quit,
            height=45,
            fg_color=self.cor_branco,
            hover_color=self.cor_cinza_claro,
            text_color=self.cor_azul,
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            corner_radius=8
        )
        sair_btn.pack(side="bottom", fill="x", pady=(10, 0))
        
    def criar_tela_lista(self):
        # Frame principal do conteúdo
        self.conteudo_frame = ctk.CTkFrame(
            self.janela,
            fg_color=self.cor_branco,
            corner_radius=0
        )
        self.conteudo_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        # Configurar pesos para redimensionamento
        self.conteudo_frame.grid_columnconfigure(0, weight=1)
        self.conteudo_frame.grid_rowconfigure(1, weight=1)  # Linha da tabela
        
        # Cabeçalho
        self.cabecalho_frame = ctk.CTkFrame(
            self.conteudo_frame,
            fg_color=self.cor_azul,
            height=70,
            corner_radius=0
        )
        self.cabecalho_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.cabecalho_frame.grid_columnconfigure(0, weight=1)
        
        # Container do cabeçalho
        cabecalho_container = ctk.CTkFrame(self.cabecalho_frame, fg_color="transparent")
        cabecalho_container.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Título da tela no cabeçalho
        self.titulo_label = ctk.CTkLabel(
            cabecalho_container,
            text="👤 LISTA DE USUÁRIOS",
            font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
            text_color=self.cor_branco
        )
        self.titulo_label.pack(side="left")
        
        # Botão + Cadastro
        self.cadastro_btn = ctk.CTkButton(
            cabecalho_container,
            text="+ Cadastro",
            height=40,
            width=120,
            fg_color=self.cor_branco,
            hover_color=self.cor_cinza_claro,
            text_color=self.cor_azul,
            font=ctk.CTkFont(size=14, weight="bold", family="Arial"),
            corner_radius=8,
            command=self.adicionar_usuario
        )
        self.cadastro_btn.pack(side="right")
        
        # Frame para conteúdo principal
        self.container = ctk.CTkFrame(self.conteudo_frame, fg_color=self.cor_branco)
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)  # Linha da tabela
        
        # Frame para barra de busca e filtros
        self.filtros_frame = ctk.CTkFrame(self.container, fg_color=self.cor_cinza_claro, height=60)
        self.filtros_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.filtros_frame.grid_columnconfigure(0, weight=1)
        
        filtros_container = ctk.CTkFrame(self.filtros_frame, fg_color="transparent")
        filtros_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Barra de busca
        busca_frame = ctk.CTkFrame(filtros_container, fg_color="transparent")
        busca_frame.pack(side="left", fill="y")
        
        busca_label = ctk.CTkLabel(
            busca_frame,
            text="🔍",
            font=ctk.CTkFont(size=16),
            text_color=self.cor_azul
        )
        busca_label.pack(side="left")
        
        self.busca_entry = ctk.CTkEntry(
            busca_frame,
            placeholder_text="Buscar usuário...",
            width=300,
            height=35,
            border_width=1,
            border_color=self.cor_cinza,
            fg_color=self.cor_branco
        )
        self.busca_entry.pack(side="left", padx=(10, 0))
        self.busca_entry.bind('<KeyRelease>', self.filtrar_usuarios)
        
        # Filtro por tipo
        filtro_frame = ctk.CTkFrame(filtros_container, fg_color="transparent")
        filtro_frame.pack(side="right", fill="y")
        
        filtro_label = ctk.CTkLabel(
            filtro_frame,
            text="Filtrar por:",
            font=ctk.CTkFont(size=13, family="Arial"),
            text_color=self.cor_texto
        )
        filtro_label.pack(side="left", padx=(0, 10))
        
        tipos = ["Todos", "Aluno", "Professor", "Coordenador"]
        self.tipo_filtro = ctk.StringVar(value="Todos")
        
        for tipo in tipos:
            btn = ctk.CTkRadioButton(
                filtro_frame,
                text=tipo,
                variable=self.tipo_filtro,
                value=tipo,
                font=ctk.CTkFont(size=12, family="Arial"),
                command=self.filtrar_usuarios,
                width=80
            )
            btn.pack(side="left", padx=5)
        
        # Frame para a tabela
        self.tabela_container = ctk.CTkFrame(
            self.container,
            fg_color=self.cor_branco
        )
        self.tabela_container.grid(row=1, column=0, sticky="nsew")
        self.tabela_container.grid_columnconfigure(0, weight=1)
        self.tabela_container.grid_rowconfigure(1, weight=1)  # Linha do conteúdo da tabela
        
        # Cabeçalho da tabela
        self.cabecalho_tabela = ctk.CTkFrame(
            self.tabela_container,
            fg_color=self.cor_azul,
            height=50
        )
        self.cabecalho_tabela.grid(row=0, column=0, sticky="ew")
        
        # Colunas do cabeçalho - ajustáveis
        self.colunas = ["Nome", "Sobrenome", "Email", "Descrição", "Imagem", "Tipo", "Ações"]
        self.criar_cabecalho_tabela()
        
        # Frame para o conteúdo da tabela (scrollable)
        self.tabela_conteudo = ctk.CTkScrollableFrame(
            self.tabela_container,
            fg_color=self.cor_branco
        )
        self.tabela_conteudo.grid(row=1, column=0, sticky="nsew")
        
        # Carregar usuários
        self.carregar_usuarios()
        
        # Estatísticas
        self.stats_frame = ctk.CTkFrame(self.container, fg_color=self.cor_cinza_claro, height=50)
        self.stats_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        self.atualizar_estatisticas()
        
        # Ajustar layout inicial
        self.ajustar_layout()
    
    def criar_cabecalho_tabela(self):
        # Limpar cabeçalho anterior
        for widget in self.cabecalho_tabela.winfo_children():
            widget.destroy()
        
        # Calcular larguras proporcionais
        largura_total = self.conteudo_frame.winfo_width() - 250  # Subtrair largura do menu
        if largura_total < 800:  # Largura mínima
            largura_total = 800
        
        # Percentuais para cada coluna (ajustáveis)
        percentuais = [0.15, 0.15, 0.25, 0.1, 0.1, 0.15, 0.1]
        
        for i, (coluna, percentual) in enumerate(zip(self.colunas, percentuais)):
            largura_col = int(largura_total * percentual)
            
            col_frame = ctk.CTkFrame(self.cabecalho_tabela, fg_color="transparent", width=largura_col)
            col_frame.pack(side="left", fill="y")
            col_frame.pack_propagate(False)
            
            if i < len(self.colunas) - 1:
                separador = ctk.CTkFrame(col_frame, fg_color=self.cor_branco, width=1)
                separador.pack(side="right", fill="y", padx=(0, 5))
            
            label = ctk.CTkLabel(
                col_frame,
                text=coluna,
                font=ctk.CTkFont(size=13, weight="bold", family="Arial"),
                text_color=self.cor_branco
            )
            label.pack(expand=True, fill="both", padx=10)
    
    def carregar_usuarios(self, usuarios_filtrados=None):
        # Limpar conteúdo atual
        for widget in self.tabela_conteudo.winfo_children():
            widget.destroy()
        
        # Usar lista filtrada ou todas
        lista_exibir = usuarios_filtrados if usuarios_filtrados else self.usuarios
        
        # Calcular larguras proporcionais
        largura_total = self.conteudo_frame.winfo_width() - 250
        if largura_total < 800:
            largura_total = 800
        
        percentuais = [0.15, 0.15, 0.25, 0.1, 0.1, 0.15, 0.1]
        
        # Carregar cada usuário
        for i, usuario in enumerate(lista_exibir):
            # Alternar cores das linhas
            cor_fundo = self.cor_branco if i % 2 == 0 else self.cor_cinza_claro
            
            linha = ctk.CTkFrame(
                self.tabela_conteudo,
                fg_color=cor_fundo,
                height=45
            )
            linha.pack(fill="x", pady=1)
            linha.pack_propagate(False)
            
            # Criar colunas com larguras proporcionais
            for j, (coluna, percentual) in enumerate(zip(self.colunas, percentuais)):
                largura_col = int(largura_total * percentual)
                
                if coluna == "Nome":
                    self.criar_coluna(linha, largura_col, usuario["nome"], "left", j == len(self.colunas)-1)
                elif coluna == "Sobrenome":
                    self.criar_coluna(linha, largura_col, usuario["sobrenome"], "left", j == len(self.colunas)-1)
                elif coluna == "Email":
                    self.criar_coluna(linha, largura_col, usuario["email"], "left", j == len(self.colunas)-1)
                elif coluna == "Descrição":
                    self.criar_coluna_botao(linha, largura_col, usuario["descricao"], 
                                           lambda u=usuario: self.ver_descricao(u), j == len(self.colunas)-1)
                elif coluna == "Imagem":
                    self.criar_coluna_botao(linha, largura_col, usuario["imagem"], 
                                           lambda u=usuario: self.ver_imagem(u), j == len(self.colunas)-1)
                elif coluna == "Tipo":
                    self.criar_coluna_tipo(linha, largura_col, usuario["tipo"], j == len(self.colunas)-1)
                elif coluna == "Ações":
                    self.criar_coluna_acoes(linha, largura_col, usuario, j == len(self.colunas)-1)
    
    def criar_coluna(self, parent, width, texto, anchor="center", ultima=False):
        col_frame = ctk.CTkFrame(parent, fg_color="transparent", width=width)
        col_frame.pack(side="left", fill="y")
        col_frame.pack_propagate(False)
        
        if not ultima:
            separador = ctk.CTkFrame(col_frame, fg_color=self.cor_cinza, width=1)
            separador.pack(side="right", fill="y", padx=(0, 5))
        
        label = ctk.CTkLabel(
            col_frame,
            text=texto,
            font=ctk.CTkFont(size=12, family="Arial"),
            text_color=self.cor_texto
        )
        label.pack(expand=True, fill="both", padx=10)
    
    def criar_coluna_botao(self, parent, width, texto, command, ultima=False):
        col_frame = ctk.CTkFrame(parent, fg_color="transparent", width=width)
        col_frame.pack(side="left", fill="y")
        col_frame.pack_propagate(False)
        
        if not ultima:
            separador = ctk.CTkFrame(col_frame, fg_color=self.cor_cinza, width=1)
            separador.pack(side="right", fill="y", padx=(0, 5))
        
        btn = ctk.CTkButton(
            col_frame,
            text=texto,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=self.cor_cinza,
            text_color=self.cor_azul,
            font=ctk.CTkFont(size=14),
            command=command
        )
        btn.pack(expand=True)
    
    def criar_coluna_tipo(self, parent, width, tipo, ultima=False):
        col_frame = ctk.CTkFrame(parent, fg_color="transparent", width=width)
        col_frame.pack(side="left", fill="y")
        col_frame.pack_propagate(False)
        
        if not ultima:
            separador = ctk.CTkFrame(col_frame, fg_color=self.cor_cinza, width=1)
            separador.pack(side="right", fill="y", padx=(0, 5))
        
        # Cor baseada no tipo
        cor_tipo = {
            "Aluno": "#28a745",
            "Professor": "#004a8d",
            "Coordenador": "#6f42c1"
        }.get(tipo, self.cor_texto)
        
        label = ctk.CTkLabel(
            col_frame,
            text=tipo,
            font=ctk.CTkFont(size=12, weight="bold", family="Arial"),
            text_color=cor_tipo
        )
        label.pack(expand=True, fill="both", padx=10)
    
    def criar_coluna_acoes(self, parent, width, usuario, ultima=False):
        col_frame = ctk.CTkFrame(parent, fg_color="transparent", width=width)
        col_frame.pack(side="left", fill="y")
        col_frame.pack_propagate(False)
        
        if not ultima:
            separador = ctk.CTkFrame(col_frame, fg_color=self.cor_cinza, width=1)
            separador.pack(side="right", fill="y", padx=(0, 5))
        
        acoes_frame = ctk.CTkFrame(col_frame, fg_color="transparent")
        acoes_frame.pack(expand=True)
        
        # Botão de status/ativo
        if usuario["ativo"]:
            status_btn = ctk.CTkButton(
                acoes_frame,
                text="✅",
                width=35,
                height=35,
                fg_color=self.cor_verde,
                hover_color=self.cor_verde_hover,
                text_color=self.cor_branco,
                font=ctk.CTkFont(size=14),
                command=lambda u=usuario: self.alterar_status(u)
            )
        else:
            status_btn = ctk.CTkButton(
                acoes_frame,
                text="❌",
                width=35,
                height=35,
                fg_color=self.cor_vermelho,
                hover_color="#c82333",
                text_color=self.cor_branco,
                font=ctk.CTkFont(size=14),
                command=lambda u=usuario: self.alterar_status(u)
            )
        status_btn.pack(side="left", padx=2)
        
        # Botão editar
        editar_btn = ctk.CTkButton(
            acoes_frame,
            text="✏️",
            width=35,
            height=35,
            fg_color=self.cor_azul,
            hover_color=self.cor_azul_hover,
            text_color=self.cor_branco,
            font=ctk.CTkFont(size=14),
            command=lambda u=usuario: self.editar_usuario(u)
        )
        editar_btn.pack(side="left", padx=2)
    
    def filtrar_usuarios(self, event=None):
        termo_busca = self.busca_entry.get().lower()
        tipo_filtro = self.tipo_filtro.get()
        
        usuarios_filtrados = []
        
        for usuario in self.usuarios:
            # Filtrar por busca
            busca_match = (
                termo_busca in usuario["nome"].lower() or
                termo_busca in usuario["sobrenome"].lower() or
                termo_busca in usuario["email"].lower()
            ) if termo_busca else True
            
            # Filtrar por tipo
            tipo_match = (
                usuario["tipo"] == tipo_filtro or
                tipo_filtro == "Todos"
            )
            
            if busca_match and tipo_match:
                usuarios_filtrados.append(usuario)
        
        self.carregar_usuarios(usuarios_filtrados)
        self.atualizar_estatisticas(usuarios_filtrados)
    
    def atualizar_estatisticas(self, usuarios_filtrados=None):
        # Limpar estatísticas anteriores
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        lista = usuarios_filtrados if usuarios_filtrados else self.usuarios
        
        total = len(lista)
        alunos = len([u for u in lista if u["tipo"] == "Aluno"])
        professores = len([u for u in lista if u["tipo"] == "Professor"])
        coordenadores = len([u for u in lista if u["tipo"] == "Coordenador"])
        
        stats_text = f"Total: {total} usuários | Alunos: {alunos} | Professores: {professores} | Coordenadores: {coordenadores}"
        
        if usuarios_filtrados is not None:
            stats_text += f" (Filtrados: {len(usuarios_filtrados)}/{len(self.usuarios)})"
        
        stats_label = ctk.CTkLabel(
            self.stats_frame,
            text=stats_text,
            font=ctk.CTkFont(size=13, family="Arial"),
            text_color=self.cor_azul
        )
        stats_label.pack(expand=True, padx=20, pady=10)
    
    def ver_descricao(self, usuario):
        messagebox.showinfo(
            f"Descrição - {usuario['nome']} {usuario['sobrenome']}",
            f"Visualização da descrição do usuário.\n\n"
            f"Em uma versão completa, aqui apareceria a descrição detalhada do usuário.",
            icon="info"
        )
    
    def ver_imagem(self, usuario):
        messagebox.showinfo(
            f"Imagem - {usuario['nome']} {usuario['sobrenome']}",
            f"Visualização da imagem do perfil.\n\n"
            f"Em uma versão completa, aqui apareceria a imagem do usuário.",
            icon="info"
        )
    
    def alterar_status(self, usuario):
        usuario["ativo"] = not usuario["ativo"]
        
        status = "ativado" if usuario["ativo"] else "desativado"
        messagebox.showinfo(
            "Status Alterado",
            f"Usuário {usuario['nome']} {usuario['sobrenome']} foi {status}.",
            icon="info"
        )
        
        # Recarregar tabela
        self.carregar_usuarios()
    
    def editar_usuario(self, usuario):
        messagebox.showinfo(
            "Editar Usuário",
            f"Editar usuário: {usuario['nome']} {usuario['sobrenome']}\n\n"
            f"Em uma versão completa, esta ação abriria um formulário de edição.",
            icon="info"
        )
    
    def adicionar_usuario(self):
        messagebox.showinfo(
            "Novo Cadastro",
            "Abrir formulário de cadastro de novo usuário.\n\n"
            "Em uma versão completa, esta ação abriria o formulário de cadastro.",
            icon="info"
        )
    
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
        
        print(f"Menu selecionado: {opcao}")
        
        if opcao != "👤 Lista de Usuários":
            messagebox.showinfo(
                "Navegação",
                f"Você selecionou: {opcao}\n\n"
                "Em uma aplicação completa, esta ação carregaria a tela correspondente.",
                icon="info"
            )
    
    def on_window_resize(self, event):
        # Só ajustar se a janela principal for redimensionada
        if event.widget == self.janela:
            self.ajustar_layout()
    
    def ajustar_layout(self):
        # Atualizar tamanhos dinamicamente
        largura_disponivel = self.conteudo_frame.winfo_width()
        
        # Ajustar fonte do título baseado no tamanho
        if largura_disponivel < 800:
            tamanho_fonte = 18
        elif largura_disponivel < 1200:
            tamanho_fonte = 20
        else:
            tamanho_fonte = 22
        
        self.titulo_label.configure(font=ctk.CTkFont(size=tamanho_fonte, weight="bold", family="Arial"))
        
        # Reconstruir cabeçalho da tabela
        self.criar_cabecalho_tabela()
        
        # Recarregar usuários para ajustar larguras
        self.carregar_usuarios()
    
    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = ListaUsuarios()
    app.run()