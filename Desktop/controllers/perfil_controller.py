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

    # No seu controllers/perfil_controller.py, substitua esse método:
    def salvar_alteracoes_perfil(self, nome, sobrenome, bio, senha, caminho_foto_local=None):
        if not nome or not sobrenome:
            messagebox.showwarning("Campos Obrigatórios", "Nome e Sobrenome são necessários.")
            return

        try:
            imagem_para_banco = None

            # SE O USUÁRIO SELECIONOU UMA NOVA FOTO LOCAL
            # SE O USUÁRIO SELECIONOU UMA NOVA FOTO LOCAL
            if caminho_foto_local and os.path.exists(caminho_foto_local):
                import cloudinary
                import cloudinary.uploader
                
                # Resgata as 3 variáveis reais do seu arquivo .env mapeado
                cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
                api_key = os.getenv("CLOUDINARY_API_KEY")
                api_secret = os.getenv("CLOUDINARY_API_SECRET")
                
                # Validação preventiva para te avisar no terminal se faltar algo
                if not all([cloud_name, api_key, api_secret]):
                    print("[ERRO CLOUDINARY] Faltam credenciais (Key ou Secret) no seu arquivo .env!")
                
                # CONFIGURAÇÃO COMPLETA E OBRIGATÓRIA PARA UPLOADS SECURE
                cloudinary.config(
                    cloud_name=cloud_name,
                    api_key=api_key,
                    api_secret=api_secret,
                    secure=True
                )
                
                print(f"[CLOUDINARY] Iniciando envio seguro de: {caminho_foto_local}...")
                
                # Realiza o upload para a sua conta
                upload_result = cloudinary.uploader.upload(
                    caminho_foto_local,
                    folder="usuario_avatares"
                )
                
                # Captura o link HTTPS definitivo gerado pelo Cloudinary
                imagem_para_banco = upload_result.get("secure_url")
                print(f"[CLOUDINARY] Upload concluído com sucesso! URL: {imagem_para_banco}")

            # ATUALIZAÇÃO NO BANCO DE DADOS POSTGRES
            conn = conectar()
            with conn.cursor() as cursor:
                if imagem_para_banco:
                    # Se trocou a foto, atualiza os dados E a coluna da imagem (com aspas duplas por causa do Postgres)
                    sql = """
                        UPDATE usuario 
                        SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s, "Senha" = %s, "imagem_usuario" = %s
                        WHERE "Email" = %s
                    """
                    cursor.execute(sql, (nome, sobrenome, bio, senha, imagem_para_banco, self.email))
                else:
                    # Se NÃO trocou a foto, mantém a imagem atual e atualiza apenas os textos
                    sql = """
                        UPDATE usuario 
                        SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s, "Senha" = %s
                        WHERE "Email" = %s
                    """
                    cursor.execute(sql, (nome, sobrenome, bio, senha, self.email))
                
                conn.commit()
            
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso no banco de dados!")
            
            # Recarrega a tela com os dados atualizados vindos do banco
            if hasattr(self, 'inicializar_perfil'):
                self.inicializar_perfil()
                
        except Exception as e:
            print(f"[CONTROLLER ERRO GRAVAÇÃO] Erro ao salvar: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Falha ao salvar alterações: {e}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()

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