import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

# Configuração do tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TelaCadastro:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Cadastro")
        self.janela.geometry("800x600")
        self.janela.resizable(False, False)
        
        # Caminho da foto selecionada
        self.caminho_foto = None
        
        self.criar_widgets()
        
    def criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self.janela, width=700, height=500)
        frame_principal.pack(pady=50, padx=50, fill="both", expand=True)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="CADASTRO DE USUÁRIO",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)
        
        # Frame para os campos
        frame_campos = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_campos.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Linha 1: Nome e Sobrenome
        frame_linha1 = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_linha1.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_linha1, text="Nome:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.entry_nome = ctk.CTkEntry(frame_linha1, width=250, placeholder_text="Digite seu nome")
        self.entry_nome.pack(side="left", padx=(0, 50))
        
        ctk.CTkLabel(frame_linha1, text="Sobrenome:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.entry_sobrenome = ctk.CTkEntry(frame_linha1, width=250, placeholder_text="Digite seu sobrenome")
        self.entry_sobrenome.pack(side="left")
        
        # Linha 2: Email
        frame_linha2 = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_linha2.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_linha2, text="Email:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.entry_email = ctk.CTkEntry(frame_linha2, width=550, placeholder_text="exemplo@email.com")
        self.entry_email.pack(side="left")
        
        # Linha 3: Senha
        frame_linha3 = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_linha3.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_linha3, text="Senha:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.entry_senha = ctk.CTkEntry(frame_linha3, width=550, show="•", placeholder_text="Digite sua senha")
        self.entry_senha.pack(side="left")
        
        # Linha 4: Foto e Tipo de Usuário
        frame_linha4 = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_linha4.pack(fill="x", pady=10)
        
        # Subframe para foto
        frame_foto = ctk.CTkFrame(frame_linha4, fg_color="transparent")
        frame_foto.pack(side="left", padx=(0, 50))
        
        ctk.CTkLabel(frame_foto, text="Foto:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        
        self.botao_foto = ctk.CTkButton(
            frame_foto,
            text="Selecionar Foto",
            width=200,
            height=40,
            command=self.selecionar_foto
        )
        self.botao_foto.pack(pady=5)
        
        self.label_foto = ctk.CTkLabel(frame_foto, text="Nenhuma foto selecionada", text_color="gray")
        self.label_foto.pack()
        
        # Subframe para tipo de usuário
        frame_tipo = ctk.CTkFrame(frame_linha4, fg_color="transparent")
        frame_tipo.pack(side="left")
        
        ctk.CTkLabel(frame_tipo, text="Tipo de Usuário:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 10))
        
        self.tipo_usuario = ctk.StringVar(value="Aluno")
        
        radio_aluno = ctk.CTkRadioButton(
            frame_tipo,
            text="Aluno",
            variable=self.tipo_usuario,
            value="Aluno"
        )
        radio_aluno.pack(anchor="w", pady=5)
        
        radio_professor = ctk.CTkRadioButton(
            frame_tipo,
            text="Professor",
            variable=self.tipo_usuario,
            value="Professor"
        )
        radio_professor.pack(anchor="w", pady=5)
        
        radio_coordenacao = ctk.CTkRadioButton(
            frame_tipo,
            text="Coordenação",
            variable=self.tipo_usuario,
            value="Coordenação"
        )
        radio_coordenacao.pack(anchor="w", pady=5)
        
        # Botões de ação
        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.pack(pady=30)
        
        self.botao_cadastrar = ctk.CTkButton(
            frame_botoes,
            text="CADASTRAR",
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.cadastrar
        )
        self.botao_cadastrar.pack(side="left", padx=20)
        
        self.botao_limpar = ctk.CTkButton(
            frame_botoes,
            text="LIMPAR",
            width=200,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="gray",
            hover_color="darkgray",
            command=self.limpar_campos
        )
        self.botao_limpar.pack(side="left", padx=20)
        
        # Label para mensagens
        self.label_mensagem = ctk.CTkLabel(frame_principal, text="", text_color="green")
        self.label_mensagem.pack(pady=10)
    
    def selecionar_foto(self):
        """Abre uma janela para selecionar uma imagem"""
        caminho = filedialog.askopenfilename(
            title="Selecionar Foto",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"), ("Todos os arquivos", "*.*")]
        )
        
        if caminho:
            self.caminho_foto = caminho
            nome_arquivo = os.path.basename(caminho)
            self.label_foto.configure(text=f"Foto: {nome_arquivo}")
    
    def validar_email(self, email):
        """Validação básica de email"""
        return '@' in email and '.' in email
    
    def cadastrar(self):
        """Processa o cadastro do usuário"""
        nome = self.entry_nome.get().strip()
        sobrenome = self.entry_sobrenome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        tipo = self.tipo_usuario.get()
        
        # Validação dos campos
        if not nome or not sobrenome:
            self.label_mensagem.configure(text="Por favor, preencha nome e sobrenome", text_color="red")
            return
            
        if not email:
            self.label_mensagem.configure(text="Por favor, preencha o email", text_color="red")
            return
            
        if not self.validar_email(email):
            self.label_mensagem.configure(text="Email inválido", text_color="red")
            return
            
        if not senha:
            self.label_mensagem.configure(text="Por favor, preencha a senha", text_color="red")
            return
            
        if len(senha) < 6:
            self.label_mensagem.configure(text="A senha deve ter pelo menos 6 caracteres", text_color="red")
            return
        
        # Montando dados do cadastro
        dados_cadastro = {
            "nome": nome,
            "sobrenome": sobrenome,
            "nome_completo": f"{nome} {sobrenome}",
            "email": email,
            "senha": senha,
            "tipo_usuario": tipo,
            "foto": self.caminho_foto if self.caminho_foto else "Nenhuma"
        }
        
        # Aqui você normalmente enviaria os dados para um banco de dados
        # Por enquanto, apenas mostra os dados no console
        print("=" * 50)
        print("DADOS DO CADASTRO:")
        print(f"Nome: {dados_cadastro['nome_completo']}")
        print(f"Email: {dados_cadastro['email']}")
        print(f"Tipo de Usuário: {dados_cadastro['tipo_usuario']}")
        print(f"Foto: {dados_cadastro['foto']}")
        print("=" * 50)
        
        # Mensagem de sucesso
        self.label_mensagem.configure(
            text=f"Usuário {nome} cadastrado com sucesso como {tipo}!",
            text_color="green"
        )
        
        # Aqui você pode adicionar a lógica para salvar no banco de dados
        # Por exemplo:
        # salvar_no_banco(dados_cadastro)
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, 'end')
        self.entry_sobrenome.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.tipo_usuario.set("Aluno")
        self.caminho_foto = None
        self.label_foto.configure(text="Nenhuma foto selecionada")
        self.label_mensagem.configure(text="")
    
    def executar(self):
        """Inicia a aplicação"""
        self.janela.mainloop()

if __name__ == "__main__":
    app = TelaCadastro()
    app.executar()