import os
from tkinter import messagebox
from models.perfil_model import PerfilModel 
from models.sessao import UsuarioSessao 
import customtkinter as ctk

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

        try:
            # 1. Busca os dados no banco
            dados = self.model.obter_dados_perfil(self.email)
            
            if not dados:
                messagebox.showwarning("Atenção", "Usuário não encontrado no banco de dados.")
                return

            u = dados['usuario']
            
            # 2. Atualiza os dados de texto na View
            self.view.atualizar_dados_principais(
                nome=u.get('nome') or u.get('Nome'),
                sobrenome=u.get('sobrenome') or u.get('Sobrenome'),
                descricao=u.get('descricao') or u.get('Descricao'),
                turma_nome=dados.get('turma', 'Sem Turma')
            )

            # 3. Renderiza os certificados na View
            self.view.renderizar_certificados(dados.get('certificados', []))

            # 4. Busca projetos DIRETO DO BANCO usando o ID do usuário
            u = dados['usuario']
            id_usuario = u.get('idusuario') or u.get('idUsuario')
            
            # Chama a função que criamos/ajustamos no Model
            projetos_usuario = self.model.listar_projetos_do_usuario(id_usuario)
            
            # Envia para a View renderizar os cards
            self.view.renderizar_projetos(projetos_usuario)
            
            print(f"DEBUG: {len(projetos_usuario)} projetos encontrados para o usuário.")
            
            print(f"DEBUG: Perfil de {self.email} carregado com sucesso.")
            
        except Exception as e:
            messagebox.showerror("Erro de Carregamento", f"Erro ao processar dados do perfil: {e}")

    def salvar_alteracoes_perfil(self, nome, sobrenome, bio):
        if not nome or not sobrenome:
            messagebox.showwarning("Campos Obrigatórios", "Nome e Sobrenome não podem estar vazios.")
            return

        try:
            sucesso = self.model.salvar_usuario(self.email, nome, sobrenome, bio)
            if sucesso:
                messagebox.showinfo("Sucesso", "Perfil atualizado!")
                self.inicializar_perfil()
            else:
                messagebox.showerror("Erro", "O banco de dados recusou a alteração.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

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