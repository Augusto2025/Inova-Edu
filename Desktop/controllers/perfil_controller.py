import os
from tkinter import messagebox
from models.perfil_model import PerfilModel 
from models.sessao import UsuarioSessao 
import customtkinter as ctk
from config.banco import conectar
import traceback

from dotenv import load_dotenv

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_env = os.path.join(diretorio_atual, '.env')

load_dotenv(caminho_env)
class ProfileController:
    def __init__(self, view, session_email=None):
        self.view = view
        self.model = PerfilModel()
        
        # Recuperação do email da sessão
        if session_email:
            self.email = session_email
        else:
            self.email = UsuarioSessao().email
            
        print(f"CONTROLLER RECUPEROU DA SESSÃO: {self.email}")
        
    def inicializar_perfil(self):
        if not self.email:
            print("ERRO CRÍTICO: E-mail da sessão está VAZIO!")
            return self.notificar_erro_sessao()

        conn = None
        try:
            # 1. BUSCA EXCLUSIVA DA FOTO VIA CONEXÃO DIRETA
            conn = conectar()
            url_imagem_completa = None
            with conn.cursor() as cursor:
                sql = """
                    SELECT "imagem_usuario" 
                    FROM usuario 
                    WHERE "Email" = %s
                """
                cursor.execute(sql, (self.email,))
                dado_foto = cursor.fetchone()
                
                if dado_foto and dado_foto[0]:
                    imagem_bruta = str(dado_foto[0]).strip()
                    
                    if imagem_bruta.startswith("http"):
                        url_imagem_completa = imagem_bruta
                    else:
                        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
                        
                        # TRATAMENTO ESPECIAL: Se o valor do banco não contiver a rota do Cloudinary,
                        # nós adicionamos o prefixo padrão 'image/upload/' que o Django CloudinaryField exige.
                        if "image/upload/" in imagem_bruta:
                            url_imagem_completa = f"https://res.cloudinary.com/{cloud_name}/{imagem_bruta}"
                        else:
                            url_imagem_completa = f"https://res.cloudinary.com/{cloud_name}/image/upload/{imagem_bruta}"
                            
                    print(f"[DEBUG URL GENERATED] URL Final Gerada: {url_imagem_completa}")

            # 2. BUSCA DOS DADOS COMPLETOS (TEXTOS, CERTIFICADOS) VIA MODEL
            dados = self.model.obter_dados_perfil(self.email)
            
            if not dados:
                messagebox.showwarning("Atenção", "Usuário não encontrado no banco de dados.")
                return

            u = dados['usuario']
            
            # 3. ENVIA OS DADOS PRINCIPAIS E A URL DA FOTO PARA A VIEW
            self.view.atualizar_dados_principais(
                nome=u.get('nome') or u.get('Nome'),
                sobrenome=u.get('sobrenome') or u.get('Sobrenome'),
                descricao=u.get('descricao') or u.get('Descricao'),
                turma_nome=dados.get('turma', 'Sem Turma'),
                url_foto=url_imagem_completa  # Passando a URL recuperada da nossa query direta
            )

            # 4. REINSTAURADO: Renderiza os certificados na View
            self.view.renderizar_certificados(dados.get('certificados', []))

            # 5. REINSTAURADO: Busca projetos DIRETO DO BANCO usando o ID do usuário
            id_usuario = u.get('idusuario') or u.get('idUsuario')
            projetos_usuario = self.model.listar_projetos_do_usuario(id_usuario)
            
            # Envia para a View renderizar os cards de projetos ativos
            self.view.renderizar_projetos(projetos_usuario)
            
            print(f"DEBUG: {len(projetos_usuario)} projetos e {len(dados.get('certificados', []))} certificados enviados para a view.")
            
        except Exception as e:
            print(f"[CONTROLLER PROFILE ERRO] Falha ao carregar perfil: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro de Carregamento", f"Erro ao processar dados do perfil: {e}")
        finally:
            if conn:
                conn.close()

    def salvar_alteracoes_perfil(self, nome, sobrenome, bio, senha):
        if not nome or not sobrenome:
            messagebox.showwarning("Campos Obrigatórios", "Nome e Sobrenome são necessários.")
            return

        try:
            sucesso = self.model.salvar_usuario(self.email, nome, sobrenome, bio, senha)
            if sucesso:
                messagebox.showinfo("Sucesso", "Perfil updated com sucesso!")
                if hasattr(self, 'inicializar_perfil'):
                    self.inicializar_perfil()
            else:
                messagebox.showerror("Erro", "Falha ao salvar no banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no Controller: {e}")

    def operacao_certificado(self, operacao, cert_id=None):
        try:
            perfil = self.model.obter_dados_perfil(self.email)
            id_usuario = perfil['usuario'].get('idusuario') or perfil['usuario'].get('idUsuario')

            if operacao == 'EXCLUIR':
                if messagebox.askyesno("Confirmar", "Deseja mesmo excluir este certificado?"):
                    self.model.excluir_certificado(cert_id, id_usuario)
            
            self.inicializar_perfil() 
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na operação: {e}")

    def notificar_erro_sessao(self):
        messagebox.showerror("Sessão Inválida", "Não foi possível identificar o usuário logado.")