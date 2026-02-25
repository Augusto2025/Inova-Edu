import os
import customtkinter as ctk
from views.login_view import tela_login
import traceback
import sys
import tkinter as tk

ctk.set_appearance_mode("light")

def global_exception_handler(exc_type, exc_value, exc_traceback):
    print(f"\n[ERRO GLOBAL] {exc_type.__name__}: {exc_value}")
    print(f"[TRACEBACK] {traceback.format_exc()}")

sys.excepthook = global_exception_handler

# ESSA FUNÇÃO É OBRIGATÓRIA PARA O EXECUTÁVEL
def resource_path(relative_path):
    try:
        # Quando o .exe roda, ele cria uma pasta temporária em sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            caminho_icone = resource_path("Desktop/assets/img/LOGOBRANCO.png")
            
            if os.path.exists(caminho_icone):
                # 1. Carregamos a imagem
                img = tk.PhotoImage(file=caminho_icone)
                
                # 2. ESSENCIAL: Salva a referência no self para o Python não apagar
                self.logo_image = img 
                
                # 3. Aplica o ícone na janela (wm_iconphoto é mais estável)
                self.wm_iconphoto(False, self.logo_image)
                
                print(f"[MAIN] Ícone aplicado e referenciado: {caminho_icone}")
            else:
                print(f"[AVISO] Arquivo não encontrado: {caminho_icone}")

            self.title("Sistema Acadêmico - INOVA EDU")
            self.attributes("-fullscreen", True)
            
            self.login_screen = tela_login(self)
            self.login_screen.pack(expand=True, fill="both")
            print("[MAIN] App iniciada")
        except Exception as e:
            print(f"[MAIN ERRO] {str(e)}")
            traceback.print_exc()
            raise

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    try:
        app = main()
        app.mainloop()
    except Exception as e:
        print(f"[MAIN FATAL] {str(e)}")
        traceback.print_exc()