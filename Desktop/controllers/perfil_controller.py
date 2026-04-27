import os
from tkinter import messagebox, filedialog
from models.perfil_model import PerfilModel 
from models.sessao import UsuarioSessao  # Importamos a caixa de memória

class ProfileController:
    def __init__(self, view, session_email=None):
        self.view = view
        self.model = PerfilModel()
        
        # Se não veio e-mail por "mão em mão", pegamos da "caixa global"
        if session_email:
            self.email = session_email
        else:
            self.email = UsuarioSessao().email
            
        print(f"CONTROLLER RECUPEROU DA SESSÃO: {self.email}")
        
    def inicializar_perfil(self):
        if not self.email:
            # Se cair aqui, é porque o Passo 2 falhou ou não foi executado
            print("ERRO CRÍTICO: E-mail da sessão está VAZIO!")
            return self.notificar_erro_sessao()

        try:
            # 1. Busca os dados completos no banco (Model)
            dados = self.model.obter_dados_perfil(self.email)
            
            if not dados:
                messagebox.showwarning("Atenção", "Usuário não encontrado no banco de dados.")
                return

            # IMPORTANTE: No Postgres com RealDictCursor, 
            # as chaves podem vir todas em minúsculo.
            u = dados['usuario']
            
            # 2. Atualiza a View (Tratando possíveis nomes de colunas do banco)
            self.view.atualizar_dados_principais(
                nome=u.get('nome') or u.get('Nome'),
                sobrenome=u.get('sobrenome') or u.get('Sobrenome'),
                descricao=u.get('descricao') or u.get('Descricao'),
                turma_nome=dados.get('turma', 'Sem Turma')
            )

            # 3. Renderiza os certificados
            self.view.renderizar_certificados(dados.get('certificados', []))
            
            print(f"DEBUG: Perfil de {self.email} carregado com sucesso.")
            
        except Exception as e:
            messagebox.showerror("Erro de Carregamento", f"Erro ao processar dados do perfil: {e}")

    def salvar_alteracoes_perfil(self, nome, sobrenome, bio):
        """Atualiza os dados textuais do usuário."""
        if not nome or not sobrenome:
            messagebox.showwarning("Campos Obrigatórios", "Nome e Sobrenome não podem estar vazios.")
            return

        try:
            sucesso = self.model.salvar_usuario(self.email, nome, sobrenome, bio)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Perfil atualizado!")
                self.inicializar_perfil() # Recarrega a tela com os novos dados
            else:
                messagebox.showerror("Erro", "O banco de dados recusou a alteração.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def operacao_certificado(self, operacao, cert_id=None, dados_cert=None):
        """Gerencia o CRUD de certificados."""
        try:
            # Precisamos do ID interno do usuário para qualquer operação de certificado
            perfil = self.model.obter_dados_perfil(self.email)
            u = perfil['usuario']
            id_usuario = u.get('idusuario') or u.get('idUsuario')

            if operacao == 'EXCLUIR':
                if messagebox.askyesno("Confirmar", "Deseja mesmo excluir este certificado?"):
                    # Aqui você deve ter o método excluir_certificado no seu PerfilModel
                    self.model.excluir_certificado(cert_id, id_usuario)
            
            elif operacao == 'CRIAR':
                # Lógica para abrir janela de novo certificado...
                pass

            self.inicializar_perfil() # Refresh na lista
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na operação de certificado: {e}")

    def notificar_erro_sessao(self):
        messagebox.showerror("Sessão Inválida", "Não foi possível identificar o usuário logado.")