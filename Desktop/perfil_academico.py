import customtkinter as ctk
import os
import sys

# Adicionar o diretório atual ao path para facilitar imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar o menu lateral
from menu_com_perfil import sidebar

print("DEBUG: Iniciando perfil_academico.py")

class UserProfileSystem:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Sistema de Perfil Acadêmico - INOVA EDU")
        self.app.geometry("1350x700")
        self.app.resizable(True, True)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Menu lateral
        print("DEBUG: Criando menu lateral...")
        self.menu_frame, self.botoes_menu = sidebar(self.app)
        
        # Frame principal
        self.main_content_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Criar diretórios necessários
        self.create_directories()
        
        # Inicializar controller
        try:
            print("DEBUG: Importando ProfileController...")
            from controllers.profile_controller import ProfileController
            print("DEBUG: ProfileController importado com sucesso!")
            
            # Inicializar controller
            self.controller = ProfileController(self.main_content_frame, self.menu_frame)
            print("DEBUG: Controller inicializado com sucesso!")
            
        except ImportError as e:
            print(f"DEBUG: Erro ao importar: {e}")
            # Fallback: mostrar interface básica
            self.show_basic_interface()
    
    def create_directories(self):
        """
        Criar diretórios necessários
        """
        os.makedirs("assets", exist_ok=True)
        os.makedirs("certificados", exist_ok=True)
        os.makedirs("dados_usuario", exist_ok=True)
        print("DEBUG: Diretórios criados/verificados")
    
    def show_basic_interface(self):
        """
        Mostrar interface básica se o MVC falhar
        """
        error_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        error_frame.pack(fill="both", expand=True, pady=100)
        
        ctk.CTkLabel(
            error_frame,
            text="👤 Meu Perfil Acadêmico",
            font=("Arial", 28, "bold"),
            text_color="#2C3E50"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            error_frame,
            text="⚠️ Erro ao carregar módulos MVC",
            font=("Arial", 18),
            text_color="#E74C3C"
        ).pack(pady=20)
    
    def run(self):
        """
        Executar aplicação
        """
        print("DEBUG: Iniciando mainloop...")
        self.app.mainloop()

def main():
    """
    Função principal
    """
    print("DEBUG: Executando main()...")
    app = UserProfileSystem()
    app.run()

if __name__ == "__main__":
    main()