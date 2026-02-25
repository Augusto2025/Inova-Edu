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

class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            caminho_icone = "Desktop/assets/img/LOGOBRANCO.ico"
            
            if os.path.exists(caminho_icone):
                self.iconbitmap(caminho_icone)
                
                print(f"[MAIN] Ícone .ico aplicado: {caminho_icone}")
            else:
                print(f"[AVISO] Arquivo .ico não encontrado: {caminho_icone}")

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