import customtkinter as ctk
from tkinter import messagebox

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
        self.cor_cinza = "#e0e0e0"
        self.cor_texto = "#333333"
        self.cor_vermelho = "#dc3545"
        self.cor_vermelho_hover = "#c82333"
        self.cor_verde = "#28a745"
        self.cor_verde_hover = "#218838"
        # Aplicar cor de fundo
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
        
    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = CadastroTurmas()
    app.run()