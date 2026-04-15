import os
from tkinter import messagebox, filedialog
# Certifique-se de que o caminho de importação está correto para sua estrutura
from models.perfil_model import PerfilModel 

class ProfileController:
    def __init__(self, view, session_email):
        self.view = view
        self.email = session_email
        self.model = PerfilModel()
        
    def inicializar_perfil(self):
        """
        Lógica unificada para carregar tudo o que o perfil precisa.
        Substitui o def perfil(request) do Django.
        """
        if not self.email:
            return self.notificar_erro_sessao()

        try:
            # 1. Busca os dados completos no banco (Model)
            dados = self.model.obter_dados_perfil(self.email)
            
            if not dados:
                messagebox.showwarning("Atenção", "Usuário não encontrado.")
                return

            usuario = dados['usuario']
            turma_nome = dados['turma']
            certificados = dados['certificados']

            # 2. Atualiza os textos básicos da View
            self.view.atualizar_dados_principais(
                nome=usuario['Nome'],
                sobrenome=usuario['Sobrenome'],
                descricao=usuario['Descricao'],
                turma_nome=turma_nome
            )

            # 3. Renderiza a lista de certificados dinamicamente
            self.view.renderizar_certificados(certificados)
            
            # 4. Projetos (Pode ser expandido conforme seu model de projetos)
            # id_turma = self.model.obter_id_turma_usuario(usuario['idUsuario'])
            # projetos = self.model.listar_projetos_por_turma(id_turma) if id_turma else []
            # self.view.renderizar_projetos(projetos)

            print(f"DEBUG: Perfil de {self.email} carregado com sucesso.")
            
        except Exception as e:
            messagebox.showerror("Erro de Carregamento", f"Não foi possível carregar os dados: {e}")

    def salvar_alteracoes_perfil(self, nome, sobrenome, bio):
        """
        Persiste as mudanças no banco.
        """
        if not nome or not sobrenome:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha Nome e Sobrenome.")
            return

        try:
            # Chama o Model para fazer o UPDATE
            sucesso = self.model.salvar_usuario(self.email, nome, sobrenome, bio)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "As alterações foram salvas!")
                self.inicializar_perfil() # Refresh automático na tela
            else:
                messagebox.showerror("Erro", "Não foi possível salvar no banco de dados.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def gerenciar_foto_perfil(self):
        """
        Abre o seletor de arquivos e salva a referência da imagem.
        """
        caminho_local = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        
        if caminho_local:
            try:
                # Aqui você chamaria o model para salvar o caminho ou fazer upload
                # self.model.atualizar_foto_usuario(self.email, caminho_local)
                
                print(f"DEBUG: Nova foto selecionada: {caminho_local}")
                # Se tiver lógica de exibição de imagem na View, chame aqui:
                # self.view.atualizar_foto_exibicao(caminho_local)
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar imagem: {e}")

    def operacao_certificado(self, operacao, cert_id=None, dados_cert=None):
        """
        Centraliza CRUD de certificados.
        """
        try:
            # Pega o ID do usuário para garantir que ele só mexa no dele
            perfil = self.model.obter_dados_perfil(self.email)
            id_usuario = perfil['usuario']['idUsuario']

            if operacao == 'EXCLUIR':
                if messagebox.askyesno("Confirmar Exclusão", "Deseja remover este certificado?"):
                    self.model.excluir_certificado(cert_id, id_usuario)
            
            elif operacao == 'CRIAR':
                # Aqui você abriria um modal para pegar dados_cert
                # self.model.salvar_certificado(dados_cert['nome'], ..., id_usuario)
                pass

            self.inicializar_perfil() # Atualiza a lista na tela
            
        except Exception as e:
            messagebox.showerror("Erro no Certificado", f"Erro: {e}")

    def notificar_erro_sessao(self):
        messagebox.showerror("Sessão Inválida", "Usuário não autenticado.")