import customtkinter as ctk
from PIL import Image
import os

# Configurar aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PerfilUsuario:
    def __init__(self, nome, foto_path=None, email="", curso="Ciência da Computação", biografia=""):
        self.nome = nome
        self.foto_path = foto_path
        self.email = email
        self.curso = curso
        self.biografia = biografia
        self.certificados = []
        self.projetos = []

class AppTurma(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Turma - Perfis dos Alunos")
        self.geometry("1200x700")
        
        # Criar dados de exemplo dos usuários
        self.usuarios = self.criar_usuarios_exemplo()
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="👥 Perfis da Turma - Ciência da Computação",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 30))
        
        # Frame SCROLLABLE para os cards
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5)
        
        # Criar cards dos usuários
        self.criar_cards_usuarios()
        
        # Frame para rodapé
        self.footer_frame = ctk.CTkFrame(self.main_frame, height=50, fg_color="transparent")
        self.footer_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        self.contador_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"Total de alunos: {len(self.usuarios)}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.contador_label.pack(side="left", padx=20)
        
        self.status_label = ctk.CTkLabel(
            self.footer_frame,
            text="Clique em 'Ver Perfil' para mais detalhes",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="right", padx=20)
    
    def criar_usuarios_exemplo(self):
        """Cria uma lista de usuários de exemplo"""
        usuarios = []
        
        # Certificados comuns
        certificados_base = [
            "Python Básico - 40 horas",
            "Introdução à Ciência de Dados",
            "Desenvolvimento Web com Django",
            "Banco de Dados SQL",
            "Git e Controle de Versão"
        ]
        
        # Projetos comuns
        projetos_base = [
            "Sistema de Gestão Escolar",
            "Aplicativo de Tarefas",
            "E-commerce com Django",
            "Análise de Dados com Pandas",
            "API RESTful"
        ]
        
        # Biografias de exemplo
        biografias = [
            """Sou apaixonada por tecnologia desde criança. Atualmente focada em Machine Learning e Ciência de Dados. Participo ativamente de maratonas de programação e hackathons.""",
            
            """Desenvolvedor full-stack com interesse em sistemas distribuídos e cloud computing. Gosto de compartilhar conhecimento através de blogs técnicos.""",
            
            """Especialista em front-end e UX/UI design. Busco sempre criar interfaces intuitivas e acessíveis para todos os usuários.""",
            
            """Foco em desenvolvimento back-end e arquitetura de software. Experiência com microserviços e APIs escaláveis.""",
            
            """Interessada em segurança da informação e criptografia. Participo de grupos de estudos sobre cybersecurity.""",
            
            """Engenheiro de dados com experiência em pipelines ETL. Trabalho com big data e análise de dados em larga escala.""",
            
            """Mobile developer especializada em React Native. Já publiquei 3 aplicativos na Play Store.""",
            
            """DevOps engineer com certificação AWS. Automatizo processos de deploy e monitoramento."""
        ]
        
        # Lista de usuários
        usuarios_info = [
            ("Ana Silva", "ana.silva@email.com", biografias[0]),
            ("Carlos Santos", "carlos.santos@email.com", biografias[1]),
            ("Mariana Oliveira", "mariana.oliveira@email.com", biografias[2]),
            ("Pedro Costa", "pedro.costa@email.com", biografias[3]),
            ("Juliana Fernandes", "juliana.fernandes@email.com", biografias[4]),
            ("Rafael Almeida", "rafael.almeida@email.com", biografias[5]),
            ("Fernanda Lima", "fernanda.lima@email.com", biografias[6]),
            ("Lucas Rodrigues", "lucas.rodrigues@email.com", biografias[7]),
        ]
        
        for i, (nome, email, biografia) in enumerate(usuarios_info):
            usuario = PerfilUsuario(nome, None, email, biografia=biografia)
            
            # Adicionar certificados (varia por usuário)
            usuario.certificados = certificados_base[:3 + (i % 3)]
            
            # Adicionar projetos (varia por usuário)
            usuario.projetos = projetos_base[:2 + (i % 4)]
            
            # Adicionar certificados/projetos específicos
            if i == 0:  # Ana Silva
                usuario.certificados.append("Machine Learning Básico")
                usuario.projetos.append("Reconhecimento Facial com OpenCV")
            elif i == 1:  # Carlos Santos
                usuario.certificados.append("Docker e Containers")
                usuario.projetos.append("Deploy com Kubernetes")
            elif i == 2:  # Mariana Oliveira
                usuario.certificados.append("React.js Avançado")
                usuario.projetos.append("Dashboard em Tempo Real")
            
            usuarios.append(usuario)
        
        return usuarios
    
    def criar_cards_usuarios(self):
        """Cria os cards para cada usuário"""
        # Configurar grid - 4 colunas
        num_colunas = 4
        
        for i, usuario in enumerate(self.usuarios):
            # Calcular posição na grid
            row = i // num_colunas
            col = i % num_colunas
            
            # Criar frame para o card
            card_frame = ctk.CTkFrame(
                self.scrollable_frame,
                width=200,
                height=320,
                corner_radius=15,
                
                fg_color= "#ffffff"
            )
            
            # Usar grid dentro do scrollable frame
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Configurar peso das colunas para centralizar
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
            
            # Criar imagem do perfil
            try:
                if usuario.foto_path and os.path.exists(usuario.foto_path):
                    img = Image.open(usuario.foto_path)
                else:
                    # Criar imagem padrão com cor sólida
                    img = Image.new('RGB', (140, 140), color=(70, 70, 70))
                    
                img = img.resize((140, 140), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(140, 140))
                
                imagem_label = ctk.CTkLabel(card_frame, image=photo, text="", corner_radius=70)
                imagem_label.image = photo
                imagem_label.pack(pady=(20, 15))
                
            except Exception as e:
                # Fallback: usar label com emoji
                emoji = "👩" if i % 2 == 0 else "👨"
                fallback_label = ctk.CTkLabel(
                    card_frame, 
                    text=emoji,
                    font=ctk.CTkFont(size=50),
                    width=140,
                    height=140,
                    corner_radius=70,
                    fg_color="#ffffff"
                )
                fallback_label.pack(pady=(20, 15))
            
            # Nome do usuário
            nome_label = ctk.CTkLabel(
                card_frame,
                text=usuario.nome,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            nome_label.pack(pady=(0, 15))
            
            # Contadores de certificados e projetos
            contadores_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            contadores_frame.pack(pady=(0, 10))
            
            # Certificados
            cert_frame = ctk.CTkFrame(contadores_frame, fg_color="transparent")
            cert_frame.pack(side="left", padx=(0, 15))
            
            cert_icon = ctk.CTkLabel(
                cert_frame,
                text="🏆",
                font=ctk.CTkFont(size=14)
            )
            cert_icon.pack(side="left")
            
            cert_label = ctk.CTkLabel(
                cert_frame,
                text=f"{len(usuario.certificados)}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            cert_label.pack(side="left", padx=(5, 0))
            
            # Projetos
            proj_frame = ctk.CTkFrame(contadores_frame, fg_color="transparent")
            proj_frame.pack(side="left")
            
            proj_icon = ctk.CTkLabel(
                proj_frame,
                text="🚀",
                font=ctk.CTkFont(size=14)
            )
            proj_icon.pack(side="left")
            
            proj_label = ctk.CTkLabel(
                proj_frame,
                text=f"{len(usuario.projetos)}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            proj_label.pack(side="left", padx=(5, 0))
            
            # Botão "Ver Perfil"
            ver_perfil_btn = ctk.CTkButton(
                card_frame,
                text="👤 VER PERFIL COMPLETO",
                command=lambda u=usuario: self.ver_perfil_detalhado(u),
                width=180,
                height=35,
                corner_radius=10,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#004a8d",
                hover_color="#003366"
            )
            ver_perfil_btn.pack(pady=(0, 20))
    
    def ver_perfil_detalhado(self, usuario):
        """Abre janela com detalhes do perfil com abas"""
        detalhes_window = ctk.CTkToplevel(self)
        detalhes_window.title(f"Perfil - {usuario.nome}")
        detalhes_window.geometry("700x650")
        detalhes_window.resizable(False, False)
        
        # Centralizar janela
        detalhes_window.transient(self)
        detalhes_window.grab_set()
        
        # Frame principal
        main_frame_detalhes = ctk.CTkFrame(detalhes_window, corner_radius=20)
        main_frame_detalhes.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo_label = ctk.CTkLabel(
            main_frame_detalhes,
            text=f"👤 {usuario.nome}",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo_label.pack(pady=(10, 20))
        
        # Frame da foto e info básica
        top_frame = ctk.CTkFrame(main_frame_detalhes, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Foto
        foto_frame = ctk.CTkFrame(top_frame, width=100, height=100, corner_radius=50)
        foto_frame.pack(side="left")
        foto_frame.pack_propagate(False)
        
        try:
            if usuario.foto_path and os.path.exists(usuario.foto_path):
                img = Image.open(usuario.foto_path)
            else:
                img = Image.new('RGB', (100, 100), color=(70, 70, 70))
                
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))
            
            imagem_label = ctk.CTkLabel(foto_frame, image=photo, text="", corner_radius=50)
            imagem_label.image = photo
            imagem_label.pack(expand=True)
            
        except:
            emoji = "👩" if self.usuarios.index(usuario) % 2 == 0 else "👨"
            fallback_label = ctk.CTkLabel(
                foto_frame, 
                text=emoji, 
                font=ctk.CTkFont(size=40),
                fg_color="#2b2b2b",
                corner_radius=50
            )
            fallback_label.pack(expand=True)
        
        # Info básica ao lado da foto (SEM MATRÍCULA)
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=20, fill="both", expand=True)
        
        campos_basicos = [
            ("📧 Email:", usuario.email),
            ("🎓 Curso:", usuario.curso),
        ]
        
        for label_text, valor in campos_basicos:
            campo_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            campo_frame.pack(fill="x", pady=3)
            
            label = ctk.CTkLabel(
                campo_frame,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=80,
                anchor="w"
            )
            label.pack(side="left")
            
            valor_label = ctk.CTkLabel(
                campo_frame,
                text=valor,
                font=ctk.CTkFont(size=12),
                text_color="#CCCCCC"
            )
            valor_label.pack(side="left", padx=(10, 0))
        
        # Abas para Certificados, Projetos e Biografia
        tabview = ctk.CTkTabview(main_frame_detalhes, corner_radius=15)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Aba 1: Certificados
        tabview.add("🏆 Certificados")
        self.criar_tab_certificados(tabview.tab("🏆 Certificados"), usuario)
        
        # Aba 2: Projetos
        tabview.add("🚀 Projetos")
        self.criar_tab_projetos(tabview.tab("🚀 Projetos"), usuario)
        
        # Aba 3: Biografia
        tabview.add("📖 Biografia")
        self.criar_tab_biografia(tabview.tab("📖 Biografia"), usuario)
        
        # Botão Fechar (SEM "Enviar Mensagem")
        botoes_frame = ctk.CTkFrame(main_frame_detalhes, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        fechar_btn = ctk.CTkButton(
            botoes_frame,
            text="Fechar",
            command=detalhes_window.destroy,
            width=100,
            height=35,
            corner_radius=10,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        fechar_btn.pack(side="right")
    
    def criar_tab_certificados(self, tab_frame, usuario):
        """Cria conteúdo da aba de certificados"""
        # Frame scrollable para certificados
        scroll_frame = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not usuario.certificados:
            sem_cert_label = ctk.CTkLabel(
                scroll_frame,
                text="Nenhum certificado registrado",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            sem_cert_label.pack(pady=50)
            return
        
        for i, certificado in enumerate(usuario.certificados):
            cert_frame = ctk.CTkFrame(
                scroll_frame,
                corner_radius=10,
                border_width=1,
                border_color="#3a3a3a",
                height=60
            )
            cert_frame.pack(fill="x", pady=5)
            cert_frame.pack_propagate(False)
            
            # Número do certificado
            num_label = ctk.CTkLabel(
                cert_frame,
                text=f"{i+1:02d}",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=30,
                anchor="center"
            )
            num_label.pack(side="left", padx=15)
            
            # Nome do certificado (SEM "Concluído")
            nome_label = ctk.CTkLabel(
                cert_frame,
                text=certificado,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            nome_label.pack(side="left", padx=(0, 20), fill="x", expand=True)
    
    def criar_tab_projetos(self, tab_frame, usuario):
        """Cria conteúdo da aba de projetos"""
        # Frame scrollable para projetos
        scroll_frame = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not usuario.projetos:
            sem_proj_label = ctk.CTkLabel(
                scroll_frame,
                text="Nenhum projeto registrado",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            sem_proj_label.pack(pady=50)
            return
        
        for i, projeto in enumerate(usuario.projetos):
            proj_frame = ctk.CTkFrame(
                scroll_frame,
                corner_radius=10,
                border_width=1,
                border_color="#3a3a3a",
                height=70
            )
            proj_frame.pack(fill="x", pady=5)
            proj_frame.pack_propagate(False)
            
            # Ícone do projeto
            icon_label = ctk.CTkLabel(
                proj_frame,
                text="🔨" if i % 3 == 0 else "📱" if i % 3 == 1 else "🌐",
                font=ctk.CTkFont(size=16)
            )
            icon_label.pack(side="left", padx=15)
            
            # Detalhes do projeto
            details_frame = ctk.CTkFrame(proj_frame, fg_color="transparent")
            details_frame.pack(side="left", padx=(0, 20), fill="both", expand=True)
            
            # Nome do projeto
            nome_label = ctk.CTkLabel(
                details_frame,
                text=projeto,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            nome_label.pack(anchor="w", pady=(10, 0))
            
            # Descrição simples
            desc_label = ctk.CTkLabel(
                details_frame,
                text="Projeto acadêmico",
                font=ctk.CTkFont(size=11),
                text_color="#CCCCCC"
            )
            desc_label.pack(anchor="w", pady=(2, 10))
    
    def criar_tab_biografia(self, tab_frame, usuario):
        """Cria conteúdo da aba de biografia"""
        # Frame scrollable para biografia
        scroll_frame = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if not usuario.biografia:
            sem_bio_label = ctk.CTkLabel(
                scroll_frame,
                text="Nenhuma biografia disponível",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            sem_bio_label.pack(pady=50)
            return
        
        # Título da biografia
        bio_title = ctk.CTkLabel(
            scroll_frame,
            text="Sobre mim",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        bio_title.pack(anchor="w", pady=(0, 15))
        
        # Texto da biografia
        bio_text = ctk.CTkLabel(
            scroll_frame,
            text=usuario.biografia,
            font=ctk.CTkFont(size=13),
            justify="left",
            wraplength=580
        )
        bio_text.pack(anchor="w", fill="x")
        
        # Separador
        separator = ctk.CTkFrame(scroll_frame, height=2, fg_color="#3a3a3a")
        separator.pack(fill="x", pady=30)
        
        # Interesses/Habilidades
        interesses_title = ctk.CTkLabel(
            scroll_frame,
            text="Interesses e Habilidades",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        interesses_title.pack(anchor="w", pady=(0, 15))
        
        # Tags de interesses
        tags_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        tags_frame.pack(anchor="w", fill="x")
        
        # Tags baseadas no perfil do usuário
        interesses_map = {
            0: ["Machine Learning", "Python", "Ciência de Dados", "IA"],
            1: ["Full-Stack", "Cloud", "DevOps", "APIs"],
            2: ["Front-End", "UI/UX", "React", "Design"],
            3: ["Back-End", "Arquitetura", "Microserviços", "Java"],
            4: ["Segurança", "Criptografia", "Cybersecurity"],
            5: ["Big Data", "ETL", "Data Engineering", "Spark"],
            6: ["Mobile", "React Native", "iOS/Android"],
            7: ["DevOps", "AWS", "Docker", "Kubernetes"]
        }
        
        idx = self.usuarios.index(usuario) % 8
        interesses = interesses_map.get(idx, ["Tecnologia", "Programação"])
        
        # Primeira linha de tags
        linha1_frame = ctk.CTkFrame(tags_frame, fg_color="transparent")
        linha1_frame.pack(anchor="w", pady=(0, 10))
        
        for tag in interesses[:2]:
            tag_label = ctk.CTkLabel(
                linha1_frame,
                text=tag,
                font=ctk.CTkFont(size=11, weight="bold"),
                padx=12,
                pady=6,
                corner_radius=15,
                fg_color="#2b2b2b",
                text_color="#4CC2FF"
            )
            tag_label.pack(side="left", padx=(0, 10))
        
        # Segunda linha de tags
        if len(interesses) > 2:
            linha2_frame = ctk.CTkFrame(tags_frame, fg_color="transparent")
            linha2_frame.pack(anchor="w", pady=(0, 10))
            
            for tag in interesses[2:4]:
                tag_label = ctk.CTkLabel(
                    linha2_frame,
                    text=tag,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    padx=12,
                    pady=6,
                    corner_radius=15,
                    fg_color="#2b2b2b",
                    text_color="#FF6B6B"
                )
                tag_label.pack(side="left", padx=(0, 10))

if __name__ == "__main__":
    app = AppTurma()
    app.mainloop()