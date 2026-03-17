import os
import customtkinter as ctk
from views.login_view import tela_login
import traceback
import sys

ctk.set_appearance_mode("light")

def resource_path(relative_path):
    """ Retorna o caminho absoluto para recursos dentro do .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    print(f"\n[ERRO GLOBAL] {exc_type.__name__}: {exc_value}")
    print(f"[TRACEBACK] {traceback.format_exc()}")

sys.excepthook = global_exception_handler

class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            # --- CONFIGURAÇÃO DA JANELA ---
            self.title("Sistema Acadêmico - INOVA EDU")
            self.attributes("-fullscreen", True)

            # --- CARREGAMENTO DO ÍCONE (.ico) ---
            # Removemos o "Desktop/" e deixamos o os.path.join resolver as barras
            caminho_ico = resource_path(os.path.join("assets", "img", "LOGOBRANCO.ico"))
            
            # Força o caminho a usar barras invertidas (\) padrão do Windows
            caminho_ico = os.path.normpath(caminho_ico)

            if os.path.exists(caminho_ico):
                # Usamos o método wm_iconbitmap que é mais direto no Tkinter
                self.wm_iconbitmap(caminho_ico)
                print(f"[MAIN] Ícone carregado com sucesso!")
            else:
                print(f"[AVISO] Arquivo não encontrado: {caminho_ico}")

            # --- INICIALIZAÇÃO DA INTERFACE ---
            self.login_screen = tela_login(self)
            self.login_screen.pack(expand=True, fill="both")
            print("[MAIN] App iniciada com tela de login")

        except Exception as e:
            print(f"[MAIN ERRO] {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    try:
        app = main()
        app.mainloop()
    except Exception as e:
        print(f"[MAIN FATAL] {str(e)}")
        traceback.print_exc()