import customtkinter as ctk
from controllers.login_controller import autenticar
import threading
import traceback
from tkinter import messagebox

class tela_login(ctk.CTkFrame):  # use CamelCase por convenção
    def __init__(self, master):  
        super().__init__(master)

        # este frame precisa ser adicionado à janela pelo chamador (pack/grid)
        # Ex.: no main.py: TelaLogin(root).pack(expand=True, fill="both")

        print("Tela de login iniciada")
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both")

        self.container.grid_columnconfigure((0, 1), weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.left = ctk.CTkFrame(self.container, fg_color="#1f6aa5")
        self.left.grid(row=0, column=0, sticky="nsew")

        # titulo do lado esquerdo
        ctk.CTkLabel(
            self.left, text="Bem-vindo!", font=("Arial", 34, "bold"), text_color="white"
        ).pack(pady=(120, 10))
        ctk.CTkLabel(
            self.left, text="Sistema Desktop\nProfinal", font=("Arial", 18), text_color="white"
        ).pack()
        ctk.CTkLabel(
            self.left, text="Faça login para continuar", font=("Arial", 14), text_color="white"
        ).pack(pady=10)

        self.right = ctk.CTkFrame(self.container, fg_color="white")
        self.right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            self.right, text="LOGIN", font=("Arial", 30, "bold"), text_color="#1f6aa5"
        ).pack(pady=(120, 30))

        self.usuario = ctk.CTkEntry(self.right, placeholder_text="Usuário", width=280, height=45)
        self.usuario.pack(pady=10)

        self.senha = ctk.CTkEntry(
            self.right, placeholder_text="Senha", show="*", width=280, height=45
        )
        self.senha.pack(pady=10)
        self.usuario.bind("<Return>", self.autentificacao)
        self.senha.bind("<Return>", self.autentificacao)

        self.erro = ctk.CTkLabel(self.right, text="", text_color="red")
        self.erro.pack()

        self.botao_entrar = ctk.CTkButton(
            self.right,
            text="Entrar",
            width=280,
            height=45,
            font=("Arial", 16),
            command=self.autentificacao,
        )
        self.botao_entrar.pack(pady=30)

    
    def autentificacao(self, event=None):
        """Executa autenticação em thread separada para não travar UI"""
        try:
            print("[LOGIN] Clicou Entrar")
            usuario = self.usuario.get()
            senha = self.senha.get()
            
            if not usuario or not senha:
                self.erro.configure(text="Preencha email e senha")
                return
            
            # Desabilita botão
            self.botao_entrar.configure(state="disabled", text="Autenticando...")
            self.erro.configure(text="")
            
            # Executa autenticação em thread separada
            thread = threading.Thread(target=self._autenticar_thread, args=(usuario, senha), daemon=True)
            thread.start()
        except Exception as e:
            print(f"[LOGIN ERRO] {str(e)}")
            self.erro.configure(text=f"Erro: {str(e)}")
            self.botao_entrar.configure(state="normal", text="Entrar")
    
    def _autenticar_thread(self, usuario, senha):
        """Executa a autenticação em thread"""
        try:
            print(f"[LOGIN THREAD] Autenticando {usuario}")
            tipo = ""
            
            print(f"[LOGIN THREAD] Chamando controller...")
            result = autenticar(usuario, senha, tipo)
            print(f"[LOGIN THREAD] Resultado: {result}")
            
            # Volta para a thread principal para atualizar UI
            self.after(0, self._processar_resultado, result, usuario)
        except Exception as e:
            print(f"[LOGIN THREAD ERRO] {str(e)}")
            print(f"[LOGIN THREAD TRACEBACK] {traceback.format_exc()}")
            self.after(0, lambda: self._mostrar_erro(f"Erro: {str(e)}"))
    
    def _processar_resultado(self, result, usuario):
        """Processa o resultado da autenticação (rodando na thread principal)"""
        try:
            self.botao_entrar.configure(state="normal", text="Entrar")
            
            if isinstance(result, tuple) and len(result) >= 2 and result[1]:
                # Autenticado!
                tipo = result[0]
                print(f"[LOGIN] Autenticado! Tipo: {tipo}")

                if tipo == "Aluno" or tipo == "Professor":
                    try:
                        print("[LOGIN] Abrindo Home...")
                        self.destroy()
                        
                        print("[LOGIN] Importando Home...")
                        from views.Aluno_e_Professor.home_view import Home
                        print("[LOGIN] Criando instância de Home...")
                        self.home_aluno_screen = Home(self.master)
                        print("[LOGIN] Empacotando Home...")
                        self.home_aluno_screen.pack(expand=True, fill="both")
                        print("[LOGIN] Home aberta com sucesso!")
                    except Exception as home_error:
                        print(f"[LOGIN HOME ERRO] {str(home_error)}")
                        print(f"[LOGIN HOME TRACEBACK] {traceback.format_exc()}")
                        self._mostrar_erro(f"Erro ao abrir home: {str(home_error)}")
                elif tipo == "Coordenador":
                    print("[LOGIN] Tipo Coordenador")
                    pass
            else:
                # Falha na autenticação
                mensagem = result[0] if isinstance(result, tuple) else str(result)
                print(f"[LOGIN] Falha na autenticacao: {mensagem}")
                self._mostrar_erro(mensagem)
        except Exception as e:
            print(f"[LOGIN PROCESSAR ERRO] {str(e)}")
            print(f"[LOGIN PROCESSAR TRACEBACK] {traceback.format_exc()}")
            self._mostrar_erro(f"Erro: {str(e)}")
    
    def _mostrar_erro(self, mensagem):
        """Mostra erro na UI (thread-safe)"""
        try:
            self.erro.configure(text=mensagem)
            self.botao_entrar.configure(state="normal", text="Entrar")
        except:
            print(f"[LOGIN MOSTRAR ERRO] Nao conseguiu atualizar label de erro")


    
    def autentificacao(self):
        tipo = ""
        result = autenticar(self.usuario.get(), self.senha.get(), tipo)
        print(result)
        if result[1]:  # Se o segundo valor da tupla é True (autenticado)
            tipo = result[0]  # O tipo de usuário retornado

            # Abre a HOME como nova janela
            if tipo == "Aluno" or tipo == "Professor":
                self.destroy()  # Fecha a tela de login
                
                from views.Aluno_e_Professor.home_view import Home
                self.home_aluno_screen = Home(self.master)
                self.home_aluno_screen.pack(expand=True, fill="both")
                
                # falta implementar a tela do coordenador
            elif tipo == "Coordenador":
                print("teste de tela iniciada da home")
                
                
                messagebox.showinfo(
                    "Em desenvolvimento",
                    "As telas da Coordenação ainda estão em processo de desenvolvimento."
                )
        else:
            # result é uma tupla (mensagem, False)
            mensagem, ok = result
            self.erro.configure(text=mensagem)

