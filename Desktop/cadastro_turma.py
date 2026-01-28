import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

# Configurar aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class CadastroTurmas:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Cadastro de Turmas")
        self.janela.geometry("1000x650")
        
        # Configurar cores personalizadas
        self.cor_azul = "#004a8d"
        self.cor_azul_hover = "#003366"
        self.cor_branco = "#ffffff"
        self.cor_cinza_claro = "#f5f5f5"
        self.cor_cinza = "#b9b9b9"
        self.cor_texto = "#333333"
        self.cor_vermelho = "#dc3545"
        self.cor_vermelho_hover = "#c82333"
        self.cor_verde = "#28a745"
        self.cor_verde_hover = "#218838"
        
        # Dados de exemplo
        self.cursos = [
            "Ciência da Computação",
            "Engenharia de Software",
            "Sistemas de Informação",
            "Análise e Desenvolvimento de Sistemas",
            "Redes de Computadores"
        ]
        
        self.usuarios = [
            "João Silva",
            "Maria Santos",
            "Pedro Oliveira",
            "Ana Costa",
            "Carlos Rodrigues",
            "Juliana Ferreira"
        ]
        
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
            "👥 Cadastro de Turmas",
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
            text="👥 CADASTRO DE TURMAS",
            font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
            text_color=self.cor_branco
        )
        titulo.pack(side="left", padx=30, pady=20)
        
        # Frame para os campos
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
        
        # Campo Código da Turma
        codigo_label = ctk.CTkLabel(
            campos_frame, 
            text="Código da Turma: *",
            **estilo_label
        )
        codigo_label.grid(row=0, column=0, padx=(30, 15), pady=(30, 15), sticky="w")
        
        self.codigo_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Ex: TURMA2023-001",
            width=400,
            **estilo_entry
        )
        self.codigo_entry.grid(row=0, column=1, padx=(0, 30), pady=(30, 15), sticky="ew")
        
        # Campo Turno
        turno_label = ctk.CTkLabel(
            campos_frame, 
            text="Turno: *",
            **estilo_label
        )
        turno_label.grid(row=1, column=0, padx=(30, 15), pady=15, sticky="w")
        
        # Frame para os botões de turno
        turno_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        turno_frame.grid(row=1, column=1, padx=(0, 30), pady=15, sticky="w")
        
        # Variável para armazenar o turno selecionado
        self.turno_var = ctk.StringVar(value="Matutino")
        
        # Botões de opção para turno
        turnos = ["Matutino", "Vespertino", "Noturno", "Integral"]
        for i, turno in enumerate(turnos):
            btn = ctk.CTkRadioButton(
                turno_frame,
                text=turno,
                variable=self.turno_var,
                value=turno,
                font=ctk.CTkFont(size=13, family="Arial"),
                text_color=self.cor_texto
            )
            btn.pack(side="left", padx=(0, 20))
        
        # Campo Ano
        ano_label = ctk.CTkLabel(
            campos_frame, 
            text="Ano: *",
            **estilo_label
        )
        ano_label.grid(row=2, column=0, padx=(30, 15), pady=15, sticky="w")
        
        # Combobox para ano
        self.ano_combobox = ctk.CTkComboBox(
            campos_frame,
            values=[str(ano) for ano in range(2020, 2031)],
            state="readonly",
            height=40,
            border_width=2,
            border_color=self.cor_cinza,
            fg_color=self.cor_branco,
            text_color=self.cor_texto,
            font=ctk.CTkFont(size=13, family="Arial"),
            corner_radius=8,
            dropdown_font=ctk.CTkFont(size=13, family="Arial")
        )
        self.ano_combobox.set("2024")  # Valor padrão
        self.ano_combobox.grid(row=2, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Campo Curso
        curso_label = ctk.CTkLabel(
            campos_frame, 
            text="Curso: *",
            **estilo_label
        )
        curso_label.grid(row=3, column=0, padx=(30, 15), pady=15, sticky="w")
        
        # Combobox para curso
        self.curso_combobox = ctk.CTkComboBox(
            campos_frame,
            values=self.cursos,
            state="readonly",
            height=40,
            border_width=2,
            border_color=self.cor_cinza,
            fg_color=self.cor_branco,
            text_color=self.cor_texto,
            font=ctk.CTkFont(size=13, family="Arial"),
            corner_radius=8,
            dropdown_font=ctk.CTkFont(size=13, family="Arial")
        )
        self.curso_combobox.set(self.cursos[0])  # Valor padrão
        self.curso_combobox.grid(row=3, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Campo Usuários
        usuarios_label = ctk.CTkLabel(
            campos_frame, 
            text="Usuários (Alunos/Professores): *",
            **estilo_label
        )
        usuarios_label.grid(row=4, column=0, padx=(30, 15), pady=15, sticky="nw")
        
        # Frame para a lista de usuários
        usuarios_frame = ctk.CTkFrame(campos_frame, fg_color=self.cor_branco, corner_radius=8)
        usuarios_frame.grid(row=4, column=1, padx=(0, 30), pady=15, sticky="nsew")
        
        # Lista de usuários selecionáveis
        self.usuarios_selecionados = {}
        
        # Scrollable frame para os checkboxes
        usuarios_scroll = ctk.CTkScrollableFrame(
            usuarios_frame,
            height=150,
            fg_color=self.cor_branco
        )
        usuarios_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Criar checkboxes para cada usuário
        for usuario in self.usuarios:
            var = ctk.BooleanVar(value=False)
            self.usuarios_selecionados[usuario] = var
            
            checkbox = ctk.CTkCheckBox(
                usuarios_scroll,
                text=usuario,
                variable=var,
                font=ctk.CTkFont(size=13, family="Arial"),
                text_color=self.cor_texto
            )
            checkbox.pack(anchor="w", padx=5, pady=3)
        
        # Botões de seleção rápida
        selecao_frame = ctk.CTkFrame(usuarios_frame, fg_color="transparent")
        selecao_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(
            selecao_frame,
            text="Selecionar Todos",
            width=120,
            height=30,
            font=ctk.CTkFont(size=12, family="Arial"),
            fg_color=self.cor_azul,
            hover_color=self.cor_azul_hover,
            command=self.selecionar_todos_usuarios
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            selecao_frame,
            text="Deselecionar Todos",
            width=120,
            height=30,
            font=ctk.CTkFont(size=12, family="Arial"),
            fg_color=self.cor_cinza,
            hover_color="#e9e7e7",
            command=self.deselecionar_todos_usuarios
        ).pack(side="left")
        
        # *******************************************
        # ÁREA DOS BOTÕES SALVAR E CANCELAR
        # *******************************************
        
        # Frame para os botões de ação
        botoes_frame = ctk.CTkFrame(
            campos_frame, 
            fg_color="transparent",
            height=100
        )
        botoes_frame.grid(row=5, column=0, columnspan=2, pady=(30, 20), sticky="ew")
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)
        
        # Botão Cancelar (à esquerda) - VERMELHO
        self.cancelar_btn = ctk.CTkButton(
            botoes_frame,
            text="❌ CANCELAR",
            command=self.cancelar_operacao,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold", family="Arial"),
            fg_color=self.cor_vermelho,
            hover_color=self.cor_vermelho_hover,
            text_color=self.cor_branco,
            corner_radius=10,
            border_width=0
        )
        self.cancelar_btn.grid(row=0, column=0, padx=(30, 15), sticky="ew")
        
        # Botão Salvar (à direita) - AZUL
        self.salvar_btn = ctk.CTkButton(
            botoes_frame,
            text="💾 SALVAR TURMA",
            command=self.salvar_turma,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold", family="Arial"),
            fg_color=self.cor_azul,
            hover_color=self.cor_azul_hover,
            text_color=self.cor_branco,
            corner_radius=10,
            border_width=0
        )
        self.salvar_btn.grid(row=0, column=1, padx=(15, 30), sticky="ew")
        
        # Adicionar atalhos de teclado
        self.janela.bind('<Control-s>', lambda e: self.salvar_turma())
        self.janela.bind('<Escape>', lambda e: self.cancelar_operacao())
        
        # Rodapé informativo
        rodape = ctk.CTkLabel(
            campos_frame,
            text="* Campos marcados com asterisco são obrigatórios | Atalhos: Ctrl+S (Salvar) | Esc (Cancelar)",
            font=ctk.CTkFont(size=11, family="Arial"),
            text_color="#666666"
        )
        rodape.grid(row=6, column=0, columnspan=2, pady=(10, 20))
    
    def selecionar_todos_usuarios(self):
        """Seleciona todos os usuários"""
        for var in self.usuarios_selecionados.values():
            var.set(True)
    
    def deselecionar_todos_usuarios(self):
        """Deseleciona todos os usuários"""
        for var in self.usuarios_selecionados.values():
            var.set(False)
    
    def salvar_turma(self):
        # Coletar dados dos campos
        codigo = self.codigo_entry.get()
        turno = self.turno_var.get()
        ano = self.ano_combobox.get()
        curso = self.curso_combobox.get()
        
        # Obter usuários selecionados
        usuarios_selecionados = []
        for usuario, var in self.usuarios_selecionados.items():
            if var.get():
                usuarios_selecionados.append(usuario)
        
        # Validação
        erros = []
        
        if not codigo:
            erros.append("O campo 'Código da Turma' é obrigatório!")
            self.codigo_entry.focus()
        
        if not ano:
            erros.append("O campo 'Ano' é obrigatório!")
        
        if not curso:
            erros.append("O campo 'Curso' é obrigatório!")
        
        if not usuarios_selecionados:
            erros.append("Selecione pelo menos um usuário!")
        
        if erros:
            messagebox.showwarning(
                "Validação", 
                "\n".join(erros),
                icon="warning"
            )
            return
        
        # Mostrar confirmação
        resposta = messagebox.askyesno(
            "Confirmar Cadastro",
            f"Deseja salvar a turma '{codigo}'?\n\n"
            f"Detalhes:\n"
            f"• Turno: {turno}\n"
            f"• Ano: {ano}\n"
            f"• Curso: {curso}\n"
            f"• Usuários selecionados: {len(usuarios_selecionados)}",
            icon="question"
        )
        
        if resposta:
            # Aqui você normalmente salvaria no banco de dados
            dados = {
                "Código": codigo,
                "Turno": turno,
                "Ano": ano,
                "Curso": curso,
                "Usuários": usuarios_selecionados,
                "Total de Usuários": len(usuarios_selecionados)
            }
            
            # Mostrar mensagem de sucesso com detalhes
            messagebox.showinfo(
                "Sucesso!", 
                f"✅ Turma '{codigo}' salva com sucesso!\n\n"
                f"📋 Detalhes:\n"
                f"• Código: {codigo}\n"
                f"• Turno: {turno}\n"
                f"• Ano: {ano}\n"
                f"• Curso: {curso}\n"
                f"• Total de usuários: {len(usuarios_selecionados)}",
                icon="info"
            )
            
            # Limpar campos após salvar
            self.limpar_campos()
    
    def cancelar_operacao(self):
        """Função do botão Cancelar"""
        # Verificar se há dados não salvos
        tem_dados = (
            self.codigo_entry.get() or
            any(var.get() for var in self.usuarios_selecionados.values())
        )
        
        if tem_dados:
            resposta = messagebox.askyesno(
                "Cancelar Operação",
                "Existem dados não salvos no formulário.\nDeseja realmente cancelar e perder as alterações?",
                icon="warning"
            )
            
            if resposta:
                self.limpar_campos()
                messagebox.showinfo(
                    "Operação Cancelada", 
                    "✅ Cadastro cancelado. Todos os campos foram limpos.",
                    icon="info"
                )
        else:
            messagebox.showinfo(
                "Cancelar", 
                "Não há dados para cancelar.\nOs campos já estão vazios.",
                icon="info"
            )
    
    def limpar_campos(self):
        """Função auxiliar para limpar campos"""
        self.codigo_entry.delete(0, "end")
        self.turno_var.set("Matutino")
        self.ano_combobox.set("2024")
        self.curso_combobox.set(self.cursos[0])
        
        # Desmarcar todos os usuários
        for var in self.usuarios_selecionados.values():
            var.set(False)
        
        # Focar no primeiro campo
        self.codigo_entry.focus()
        
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
        
        # Aqui você implementaria a navegação entre telas
        if opcao != "👥 Cadastro de Turmas":
            messagebox.showinfo(
                "Navegação",
                f"Você selecionou: {opcao}\n\n"
                "Em uma aplicação completa, esta ação carregaria a tela correspondente.",
                icon="info"
            )
        
    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = CadastroTurmas()
    app.run()