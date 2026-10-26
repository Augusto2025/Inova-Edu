import os
from tkinter import messagebox
from models.perfil_model import PerfilModel
from models.sessao import UsuarioSessao
import customtkinter as ctk
from config.banco import conectar
import traceback
from security.logger import get_logger
from security.file_validator import validate_image_upload

logger = get_logger(__name__)

# Carrega .env uma vez
from dotenv import load_dotenv
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_env = os.path.join(os.path.dirname(diretorio_atual), '.env')
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

        logger.info(f"ProfileController inicializado para: {self.email}")

    def inicializar_perfil(self):
        if not self.email:
            logger.error("E-mail da sessão está VAZIO!")
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

                        if "image/upload/" in imagem_bruta:
                            url_imagem_completa = f"https://res.cloudinary.com/{cloud_name}/{imagem_bruta}"
                        else:
                            url_imagem_completa = f"https://res.cloudinary.com/{cloud_name}/image/upload/{imagem_bruta}"

                    logger.debug(f"URL da foto gerada: {url_imagem_completa}")

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
                url_foto=url_imagem_completa
            )

            # 4. Renderiza os certificados na View
            self.view.renderizar_certificados(dados.get('certificados', []))

            # 5. Busca projetos DIRETO DO BANCO usando o ID do usuário
            id_usuario = u.get('idusuario') or u.get('idUsuario')
            projetos_usuario = self.model.listar_projetos_do_usuario(id_usuario)

            # Envia para a View renderizar os cards de projetos ativos
            self.view.renderizar_projetos(projetos_usuario)

            logger.info(f"Perfil carregado: {len(projetos_usuario)} projetos, {len(dados.get('certificados', []))} certificados")

        except Exception as e:
            logger.error(f"Falha ao carregar perfil: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro de Carregamento", "Erro ao processar dados do perfil.")
        finally:
            if conn:
                conn.close()

    def salvar_alteracoes_perfil(self, nome, sobrenome, bio, senha, caminho_foto_local=None):
        if not nome or not sobrenome:
            messagebox.showwarning("Campos Obrigatórios", "Nome e Sobrenome são necessários.")
            return

        try:
            estado_foto = "manter"
            imagem_para_banco = None

            # SE O USUÁRIO SELECIONOU UMA NOVA FOTO LOCAL
            if caminho_foto_local == "":
                estado_foto = "remover"
            elif caminho_foto_local and os.path.exists(caminho_foto_local):
                # Valida o arquivo antes do upload
                valido, erro = validate_image_upload(caminho_foto_local)
                if not valido:
                    messagebox.showerror("Erro de Arquivo", erro)
                    return

                estado_foto = "upload"

                import cloudinary
                import cloudinary.uploader

                cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
                api_key = os.getenv("CLOUDINARY_API_KEY")
                api_secret = os.getenv("CLOUDINARY_API_SECRET")

                if not all([cloud_name, api_key, api_secret]):
                    logger.error("Credenciais Cloudinary faltando no .env")
                    messagebox.showerror("Erro", "Configuração de armazenamento incompleta.")
                    return

                cloudinary.config(
                    cloud_name=cloud_name,
                    api_key=api_key,
                    api_secret=api_secret,
                    secure=True
                )

                logger.info(f"Enviando foto para Cloudinary: {caminho_foto_local}")

                upload_result = cloudinary.uploader.upload(
                    caminho_foto_local,
                    folder="usuario_avatares"
                )

                imagem_para_banco = upload_result.get("secure_url")
                logger.info(f"Upload concluído: {imagem_para_banco}")

            # ATUALIZAÇÃO NO BANCO DE DADOS POSTGRES
            conn = conectar()
            with conn.cursor() as cursor:
                if estado_foto == "upload" and imagem_para_banco:
                    sql = """
                        UPDATE usuario
                        SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s, "Senha" = %s, "imagem_usuario" = %s
                        WHERE "Email" = %s
                    """
                    cursor.execute(sql, (nome, sobrenome, bio, senha, imagem_para_banco, self.email))

                elif estado_foto == "remover":
                    sql = """
                        UPDATE usuario
                        SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s, "Senha" = %s, "imagem_usuario" = NULL
                        WHERE "Email" = %s
                    """
                    cursor.execute(sql, (nome, sobrenome, bio, senha, self.email))

                else:
                    sql = """
                        UPDATE usuario
                        SET "Nome" = %s, "Sobrenome" = %s, "Descricao" = %s, "Senha" = %s
                        WHERE "Email" = %s
                    """
                    cursor.execute(sql, (nome, sobrenome, bio, senha, self.email))

                conn.commit()

            logger.info(f"Perfil salvo com sucesso para: {self.email}")
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")

            # Recarrega a tela com os dados atualizados vindos do banco
            if hasattr(self, 'inicializar_perfil'):
                self.inicializar_perfil()

        except Exception as e:
            logger.error(f"Erro ao salvar perfil: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", "Falha ao salvar alterações.")
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    def operacao_certificado(self, operacao, cert_id=None):
        try:
            perfil = self.model.obter_dados_perfil(self.email)
            id_usuario = perfil['usuario'].get('idusuario') or perfil['usuario'].get('idUsuario')

            if operacao == 'EXCLUIR':
                if not cert_id:
                    messagebox.showwarning("Aviso", "Identificador do certificado não encontrado.")
                    return

                if messagebox.askyesno("Confirmar Exclusão", "Deseja mesmo excluir este certificado?"):
                    sucesso = self.model.excluir_certificado(cert_id, id_usuario)
                    if sucesso:
                        messagebox.showinfo("Sucesso", "Certificado excluído com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Falha ao excluir o certificado.")

            # Recarrega a interface com os certificados atualizados
            self.inicializar_perfil()
        except Exception as e:
            logger.error(f"Erro na operação certificado: {e}")
            messagebox.showerror("Erro", "Erro na operação.")

    def notificar_erro_sessao(self):
        messagebox.showerror("Sessão Inválida", "Não foi possível identificar o usuário logado.")