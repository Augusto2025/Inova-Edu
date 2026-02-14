import customtkinter as ctk
import os
import sys

# Adicionar o diretório atual ao path para facilitar imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar o menu lateral
# from menu_com_perfil import sidebar

print("DEBUG: Iniciando perfil_academico.py")

class UserProfileSystem(ctk.CTkFrame):
    def __init__(self, master=None):
        # 1. Primeiro chamamos o super e definimos a janela
        super().__init__(master, fg_color="transparent")
        self.janela = master  # ESSA LINHA PRECISA VIR ANTES DE TUDO

        # 2. Agora o código de buscar a sidebar funciona
        from sidebar_AP import Sidebar, sidebar
        
        sidebar_existente = None
        # Agora o self.janela existe, então o loop abaixo não dará erro
        for widget in self.janela.winfo_children():
            if isinstance(widget, Sidebar):
                sidebar_existente = widget
                break

        if not sidebar_existente:
            sidebar_existente, _ = sidebar(self.janela)
        
        # 3. Frame principal colado na sidebar (side="left")
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # ... resto do seu código (create_directories, etc)
        
        # Criar diretórios necessários
        self.create_directories()
        
        # Inicializar controller
        try:
            print("DEBUG: Importando ProfileController...")
            from controllers.profile_controller import ProfileController
            print("DEBUG: ProfileController importado com sucesso!")
            
            # Inicializar controller
            self.controller = ProfileController(self.main_content_frame, sidebar_existente)
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

if __name__ == "__main__":
    ctk.set_appearance_mode("light") # ESSA LINHA É VITAL
    app = ctk.CTk()
    app.geometry("1200x800")
    # Garante que o container principal preencha a tela
    app_frame = UserProfileSystem(master=app)
    app_frame.pack(fill="both", expand=True) 
    app.mainloop()