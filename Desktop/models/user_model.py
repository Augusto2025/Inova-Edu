import json
import os

print("DEBUG: Carregando UserModel...")

class UserModel:
    def __init__(self, data_file="perfil_usuario.json"):
        print("DEBUG: Inicializando UserModel...")
        self.data_file = data_file
        self.user_data = self.load_user_data()
    
    def load_user_data(self):
        """
        Carregar dados do usuário
        """
        default_data = {
            "nome": "Alcides Miranda Neto",
            "bio": "Estudante dedicado com interesse em tecnologia e aprendizado contínuo. Apaixonado por desenvolvimento de software e inovação educacional.",
            "curso": "Ciência da Computação",
            "foto": "assets/default_avatar.png",
            "certificados": [
                {
                    "nome": "Curso de Python Avançado",
                    "instituicao": "INOVA EDU",
                    "data": "15/10/2024",
                    "carga_horaria": "40 horas",
                    "arquivo": "certificados/python_avancado.pdf"
                },
                {
                    "nome": "Desenvolvimento Web Full Stack",
                    "instituicao": "Digital Innovation One",
                    "data": "20/09/2024",
                    "carga_horaria": "60 horas",
                    "arquivo": "certificados/web_fullstack.pdf"
                },
                {
                    "nome": "Inteligência Artificial Aplicada",
                    "instituicao": "Google AI",
                    "data": "05/11/2024",
                    "carga_horaria": "80 horas",
                    "arquivo": "certificados/ia_google.pdf"
                }
            ],
            "projetos": [
                {
                    "nome": "Sistema de Gestão Acadêmica",
                    "descricao": "Desenvolvimento de sistema web completo para gestão de estudantes, professores e disciplinas. Tecnologias: Django, React, PostgreSQL."
                },
                {
                    "nome": "App Mobile para Ensino de Matemática",
                    "descricao": "Aplicativo Android/iOS para auxílio no aprendizado de matemática básica. Com jogos educativos e exercícios interativos."
                },
                {
                    "nome": "API de Integração de Sistemas Educacionais",
                    "descricao": "API REST para integração entre diferentes sistemas acadêmicos. Implementado com FastAPI e autenticação JWT."
                },
                {
                    "nome": "Plataforma de Cursos Online",
                    "descricao": "Desenvolvimento de plataforma E-learning com videoaulas, quizzes e certificados automáticos."
                }
            ]
        }
        
        try:
            if os.path.exists(self.data_file):
                print(f"DEBUG: Carregando dados de {self.data_file}")
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Garantir que todos os campos padrão existem
                    for key in default_data:
                        if key not in data:
                            data[key] = default_data[key]
                    
                    print(f"DEBUG: Dados carregados: {data['nome']}")
                    return data
            else:
                print(f"DEBUG: Arquivo {self.data_file} não encontrado. Usando dados padrão.")
                
        except Exception as e:
            print(f"DEBUG: Erro ao carregar dados: {e}")
        
        return default_data
    
    def save_user_data(self):
        """
        Salvar dados do usuário
        """
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            print(f"DEBUG: Dados salvos em {self.data_file}")
            return True
        except Exception as e:
            print(f"DEBUG: Erro ao salvar dados: {e}")
            return False
    
    def get_user_data(self):
        """
        Obter todos os dados do usuário
        """
        return self.user_data.copy()
    
    def update_profile_field(self, field, value):
        """
        Atualizar campo do perfil
        """
        if field in self.user_data:
            self.user_data[field] = value
            success = self.save_user_data()
            print(f"DEBUG: Campo '{field}' atualizado: {success}")
            return success
        print(f"DEBUG: Campo '{field}' não encontrado")
        return False
    
    def get_certificates(self):
        """
        Obter certificados
        """
        return self.user_data.get("certificados", []).copy()
    
    def get_projects(self):
        """
        Obter projetos
        """
        return self.user_data.get("projetos", []).copy()
    
    # ... (código anterior permanece) ...

def add_certificate(self, certificate_data):
    """
    Adicionar certificado
    """
    try:
        if "certificados" not in self.user_data:
            self.user_data["certificados"] = []
        
        self.user_data["certificados"].append(certificate_data)
        success = self.save_user_data()
        print(f"DEBUG: Certificado adicionado: {success}")
        return success
        
    except Exception as e:
        print(f"DEBUG: Erro ao adicionar certificado: {e}")
        return False

def delete_certificate(self, index):
    """
    Excluir certificado pelo índice
    """
    try:
        if "certificados" in self.user_data and 0 <= index < len(self.user_data["certificados"]):
            removed_cert = self.user_data["certificados"].pop(index)
            success = self.save_user_data()
            print(f"DEBUG: Certificado excluído ({removed_cert['nome']}): {success}")
            return success
        return False
        
    except Exception as e:
        print(f"DEBUG: Erro ao excluir certificado: {e}")
        return False

def update_certificate(self, index, certificate_data):
    """
    Atualizar certificado pelo índice
    """
    try:
        if "certificados" in self.user_data and 0 <= index < len(self.user_data["certificados"]):
            self.user_data["certificados"][index] = certificate_data
            success = self.save_user_data()
            print(f"DEBUG: Certificado atualizado: {success}")
            return success
        return False
        
    except Exception as e:
        print(f"DEBUG: Erro ao atualizar certificado: {e}")
        return False