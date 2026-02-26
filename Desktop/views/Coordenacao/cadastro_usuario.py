import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
# from controllers.usuario_controller import UsuarioController



# Configurar aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class CadastroUsuarios:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Cadastro de Usuários")
        self.janela.geometry("1100x800")
        self.janela.attributes("-fullscreen", True)  # TELA INTEIRA
        
        # Configurar cores personalizadas
        self.cor_azul = "#004a8d"
        self.cor_azul_hover = "#003366"
        self.cor_branco = "#ffffff"
        self.cor_cinza_claro = "#f5f5f5"
        self.cor_cinza = "#e0e0e0"
        self.cor_texto = "#333333"
        self.cor_vermelho = "#dc3545"
        self.cor_vermelho_hover = "#c82333"
        self.cor_verde = "#28a745"
        self.cor_verde_hover = "#218838"
        
        # Aplicar cores de fundo
        self.janela.configure(fg_color=self.cor_branco)

        # Importar o sidebar de forma tardia para evitar importação circular
        from Desktop.views.Coordenacao.sidebar_C import sidebar
        sidebar(self.janela)

        self.view_container = ctk.CTkFrame(self.janela, fg_color=self.cor_branco)
        self.view_container.pack(side="right", fill="both", expand=True)

        self.view_cadastro = ctk.CTkFrame(self.view_container, fg_color=self.cor_branco)

        self.criar_tela_cadastro(self.view_cadastro)

        self.view_cadastro.pack(fill="both", expand=True)
        
        
        
        

        
        
    def criar_tela_cadastro(self, parent):
        
        # Frame principal do conteúdo
        self.conteudo_frame = parent
        

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
            text="👤 CADASTRO DE USUÁRIOS",
            font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
            text_color=self.cor_branco
        )
        titulo.pack(side="left", padx=30, pady=20)
        
        # Frame para os campos
        container = ctk.CTkFrame(self.conteudo_frame, fg_color=self.cor_branco)
        container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Frame principal com rolagem
        main_scroll = ctk.CTkScrollableFrame(
            container,
            fg_color=self.cor_cinza_claro,
            corner_radius=15
        )
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame interno para organização
        campos_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
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
        
        # Linha 0: Nome
        nome_label = ctk.CTkLabel(
            campos_frame, 
            text="Nome: *",
            **estilo_label
        )
        nome_label.grid(row=0, column=0, padx=(30, 15), pady=(20, 15), sticky="w")
        
        self.nome_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Digite o primeiro nome...",
            **estilo_entry
        )
        self.nome_entry.grid(row=0, column=1, padx=(0, 30), pady=(20, 15), sticky="ew")
        
        # Linha 1: Sobrenome
        sobrenome_label = ctk.CTkLabel(
            campos_frame, 
            text="Sobrenome: *",
            **estilo_label
        )
        sobrenome_label.grid(row=1, column=0, padx=(30, 15), pady=15, sticky="w")
        
        self.sobrenome_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Digite o sobrenome...",
            **estilo_entry
        )
        self.sobrenome_entry.grid(row=1, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Linha 2: Email
        email_label = ctk.CTkLabel(
            campos_frame, 
            text="Email: *",
            **estilo_label
        )
        email_label.grid(row=2, column=0, padx=(30, 15), pady=15, sticky="w")
        
        self.email_entry = ctk.CTkEntry(
            campos_frame,
            placeholder_text="exemplo@email.com",
            **estilo_entry
        )
        self.email_entry.grid(row=2, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Linha 3: Tipo de Usuário
        tipo_label = ctk.CTkLabel(
            campos_frame, 
            text="Tipo de Usuário: *",
            **estilo_label
        )
        tipo_label.grid(row=3, column=0, padx=(30, 15), pady=15, sticky="w")
        
        # Frame para os botões de tipo
        tipo_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        tipo_frame.grid(row=3, column=1, padx=(0, 30), pady=15, sticky="w")
        
        # Variável para armazenar o tipo selecionado
        self.tipo_var = ctk.StringVar(value="Aluno")
        
        # Botões de opção para tipo
        tipos = ["Aluno", "Professor", "Coordenador"]
        for i, tipo in enumerate(tipos):
            btn = ctk.CTkRadioButton(
                tipo_frame,
                text=tipo,
                variable=self.tipo_var,
                value=tipo,
                font=ctk.CTkFont(size=13, family="Arial"),
                text_color=self.cor_texto
            )
            btn.pack(side="left", padx=(0, 20))
        
        # Linha 4: Imagem do Perfil
        imagem_label = ctk.CTkLabel(
            campos_frame, 
            text="Imagem do Perfil:",
            **estilo_label
        )
        imagem_label.grid(row=4, column=0, padx=(30, 15), pady=15, sticky="w")
        
        # Frame para imagem
        imagem_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        imagem_frame.grid(row=4, column=1, padx=(0, 30), pady=15, sticky="ew")
        
        # Campo para caminho da imagem
        self.imagem_entry = ctk.CTkEntry(
            imagem_frame,
            placeholder_text="Selecione uma imagem de perfil...",
            **estilo_entry
        )
        self.imagem_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botão para buscar imagem
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
        
        # Preview da imagem (opcional - espaço reservado)
        preview_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        preview_frame.grid(row=5, column=1, padx=(0, 30), pady=(5, 15), sticky="w")
        
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="🖼️ Pré-visualização da imagem aparecerá aqui",
            font=ctk.CTkFont(size=12, family="Arial"),
            text_color="#666666"
        )
        self.preview_label.pack()
        
        # Linha 6: Descrição
        descricao_label = ctk.CTkLabel(
            campos_frame, 
            text="Descrição:",
            **estilo_label
        )
        descricao_label.grid(row=6, column=0, padx=(30, 15), pady=15, sticky="nw")
        
        # Área de texto para descrição
        self.descricao_text = ctk.CTkTextbox(
            campos_frame,
            height=150,
            border_width=2,
            border_color=self.cor_cinza,
            fg_color=self.cor_branco,
            text_color=self.cor_texto,
            font=ctk.CTkFont(size=13, family="Arial"),
            corner_radius=8
        )
        self.descricao_text.grid(row=6, column=1, padx=(0, 30), pady=15, sticky="nsew")
        
        # Texto de exemplo na descrição
        exemplo_descricao = "Ex: Estudante do curso de Ciência da Computação, interessado em desenvolvimento web e inteligência artificial."
        self.descricao_text.insert("1.0", exemplo_descricao)
        
        # *******************************************
        # ÁREA DOS BOTÕES SALVAR E CANCELAR
        # *******************************************
        
        # Frame para os botões de ação
        botoes_frame = ctk.CTkFrame(
            campos_frame, 
            fg_color="transparent",
            height=100
        )
        botoes_frame.grid(row=7, column=0, columnspan=2, pady=(30, 20), sticky="ew")
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
            text="💾 SALVAR USUÁRIO",
            command=self.salvar_usuario,
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
        self.janela.bind('<Control-s>', lambda e: self.salvar_usuario())
        self.janela.bind('<Escape>', lambda e: self.cancelar_operacao())
        
        # Rodapé informativo
        rodape = ctk.CTkLabel(
            campos_frame,
            text="* Campos marcados com asterisco são obrigatórios | Atalhos: Ctrl+S (Salvar) | Esc (Cancelar)",
            font=ctk.CTkFont(size=11, family="Arial"),
            text_color="#666666"
        )
        rodape.grid(row=8, column=0, columnspan=2, pady=(10, 20))
    
    def buscar_imagem(self):
        """Abre o diálogo para selecionar uma imagem"""
        tipos_arquivos = [
            ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Todos os arquivos", "*.*")
        ]
        
        arquivo = filedialog.askopenfilename(
            title="Selecione uma imagem de perfil",
            filetypes=tipos_arquivos
        )
        
        if arquivo:
            self.imagem_entry.delete(0, "end")
            self.imagem_entry.insert(0, arquivo)
            
            # Atualizar preview
            nome_arquivo = arquivo.split('/')[-1]
            self.preview_label.configure(
                text=f"✅ Imagem selecionada: {nome_arquivo}",
                text_color=self.cor_verde
            )
    
    def validar_email(self, email):
        """Validação simples de email"""
        import re
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None
    
    def salvar_usuario(self):
        # Coletar dados dos campos
        nome = self.nome_entry.get()
        sobrenome = self.sobrenome_entry.get()
        email = self.email_entry.get()
        tipo = self.tipo_var.get()
        imagem = self.imagem_entry.get()
        descricao = self.descricao_text.get("1.0", "end-1c")
        
        # Validação
        erros = []
        
        if not nome:
            erros.append("O campo 'Nome' é obrigatório!")
            self.nome_entry.focus()
        
        if not sobrenome:
            erros.append("O campo 'Sobrenome' é obrigatório!")
        
        if not email:
            erros.append("O campo 'Email' é obrigatório!")
        elif not self.validar_email(email):
            erros.append("Email em formato inválido!")
        
        if not tipo:
            erros.append("Selecione um 'Tipo de Usuário'!")
        
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
            f"Deseja salvar o usuário '{nome} {sobrenome}'?\n\n"
            f"Detalhes:\n"
            f"• Email: {email}\n"
            f"• Tipo: {tipo}\n"
            f"• Imagem: {'Sim' if imagem else 'Não'}\n"
            f"• Descrição: {'Sim' if descricao.strip() else 'Não'}",
            icon="question"
        )
        
        if resposta:
            try:
                self.model.cadastrar(
                    imagem=imagem if imagem else None,
                    tipo=tipo,
                    nome=nome,
                    sobrenome=sobrenome,
                    email=email,
                    senha="123456",
                    descricao=descricao
                )

                messagebox.showinfo(
                    "Sucesso",
                    "✅ Usuário salvo com sucesso no banco!"
                )

                self.limpar_campos()

            except Exception as e:
                messagebox.showerror(
                    "Erro",
                    f"Erro ao salvar no banco:\n{e}"
                )

    
    def cancelar_operacao(self):
        """Função do botão Cancelar"""
        # Verificar se há dados não salvos
        tem_dados = (
            self.nome_entry.get() or
            self.sobrenome_entry.get() or
            self.email_entry.get() or
            self.imagem_entry.get() or
            self.descricao_text.get("1.0", "end-1c").strip() != 
            "Ex: Estudante do curso de Ciência da Computação, interessado em desenvolvimento web e inteligência artificial."
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
        self.nome_entry.delete(0, "end")
        self.sobrenome_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.tipo_var.set("Aluno")
        self.imagem_entry.delete(0, "end")
        
        # Limpar descrição e colocar texto de exemplo
        self.descricao_text.delete("1.0", "end")
        exemplo_descricao = "Ex: Estudante do curso de Ciência da Computação, interessado em desenvolvimento web e inteligência artificial."
        self.descricao_text.insert("1.0", exemplo_descricao)
        
        # Resetar preview
        self.preview_label.configure(
            text="🖼️ Pré-visualização da imagem aparecerá aqui",
            text_color="#666666"
        )
        
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
        
        print(f"Menu selecionado: {opcao}")
        
        # Aqui você implementaria a navegação entre telas
        if opcao != "👤 Cadastro de Usuários":
            messagebox.showinfo(
                "Navegação",
                f"Você selecionou: {opcao}\n\n"
                "Em uma aplicação completa, esta ação carregaria a tela correspondente.",
                icon="info"
            )
        
    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = CadastroUsuarios()
    app.run()
    
    
