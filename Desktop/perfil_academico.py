import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
from datetime import datetime

# Importar o menu lateral
from menu_com_perfil import sidebar

class UserProfileSystem:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Sistema de Perfil Acadêmico - INOVA EDU")
        self.app.geometry("1350x700")  # Aumentado para acomodar o menu
        self.app.resizable(True, True)
        
        # Configurar aparência
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Adicionar menu lateral
        self.menu_frame, self.botoes_menu = sidebar(self.app)
        
        # Frame principal para o conteúdo do perfil
        self.main_content_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Carregar dados
        self.user_data = self.load_user_data()
        
        # Configurar interface do perfil
        self.setup_ui()
        self.update_display()
        
    def load_user_data(self):
        """Carregar dados do usuário"""
        default_data = {
            "nome": "Aluno Exemplo",
            "bio": "Estudante dedicado com interesse em tecnologia e aprendizado contínuo.",
            "curso": "Ciência da Computação",
            "foto": "assets/default_avatar.png",
            "certificados": [],
            "projetos": [
                {"nome": "Sistema de Gestão Acadêmica", "status": "Em andamento", "descricao": "Desenvolvimento de sistema web para gestão de estudantes"},
                {"nome": "App Mobile para Ensino", "status": "Planejamento", "descricao": "Aplicativo para auxílio no aprendizado de matemática"},
                {"nome": "API de Integração", "status": "Concluído", "descricao": "API REST para integração entre sistemas"}
            ]
        }
        
        try:
            if os.path.exists("perfil_usuario.json"):
                with open("perfil_usuario.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key in default_data:
                        if key not in data:
                            data[key] = default_data[key]
                    return data
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
        
        return default_data
    
    def save_user_data(self):
        """Salvar dados do usuário"""
        os.makedirs("assets", exist_ok=True)
        os.makedirs("certificados", exist_ok=True)
        
        try:
            with open("perfil_usuario.json", "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")
    
    def create_default_avatar(self):
        """Criar avatar padrão"""
        from PIL import Image, ImageDraw
        
        img = Image.new('RGB', (200, 200), color='#4A90E2')
        d = ImageDraw.Draw(img)
        d.ellipse([10, 10, 190, 190], fill='#357ABD')
        
        os.makedirs("assets", exist_ok=True)
        img.save("assets/default_avatar.png")
        self.user_data["foto"] = "assets/default_avatar.png"
    
    def setup_ui(self):
        """Configurar interface principal do perfil"""
        # Título da página
        title_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="👤 Meu Perfil Acadêmico",
            font=("Arial", 28, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Layout principal do perfil
        self.profile_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.profile_frame.pack(fill="both", expand=True)
        
        # Layout em duas colunas
        self.left_panel = ctk.CTkFrame(self.profile_frame, width=350, corner_radius=15)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20))
        self.left_panel.pack_propagate(False)
        
        self.right_panel = ctk.CTkFrame(self.profile_frame, corner_radius=15)
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        self.setup_left_panel()
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """Configurar painel esquerdo (perfil simplificado)"""
        profile_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        profile_header.pack(pady=30)
        
        # Foto de perfil
        self.photo_container = ctk.CTkFrame(profile_header, width=180, height=180, corner_radius=90)
        self.photo_container.pack()
        
        try:
            self.profile_img = ctk.CTkImage(
                light_image=Image.open(self.user_data["foto"]),
                size=(160, 160)
            )
        except:
            self.create_default_avatar()
            self.profile_img = ctk.CTkImage(
                light_image=Image.open(self.user_data["foto"]),
                size=(160, 160)
            )
        
        self.photo_label = ctk.CTkLabel(
            self.photo_container,
            image=self.profile_img,
            text=""
        )
        self.photo_label.pack(pady=10)
        
        # Botão para alterar foto
        ctk.CTkButton(
            profile_header,
            text="📷 Alterar Foto",
            command=self.change_photo,
            width=180,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14)
        ).pack(pady=10)
        
        # Informações do usuário
        info_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        info_frame.pack(pady=20, padx=20, fill="x")
        
        # Nome do usuário
        self.name_label = ctk.CTkLabel(
            info_frame,
            text=self.user_data["nome"],
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        )
        self.name_label.pack(pady=(0, 10))
        
        # Botão para editar nome
        ctk.CTkButton(
            info_frame,
            text="✏️ Editar Nome",
            command=self.edit_name,
            width=180,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=(0, 20))
        
        # Curso (apenas visualização)
        course_frame = ctk.CTkFrame(info_frame, fg_color="#F0F7FF", corner_radius=8)
        course_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            course_frame,
            text="🎓 Curso Atual",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(10, 5))
        
        self.course_label = ctk.CTkLabel(
            course_frame,
            text=self.user_data["curso"],
            font=("Arial", 15),
            text_color="#3498DB"
        )
        self.course_label.pack(pady=(0, 10))
        
        # Biografia
        ctk.CTkLabel(
            info_frame,
            text="📝 Biografia",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.bio_text = ctk.CTkTextbox(
            info_frame,
            height=150,
            font=("Arial", 13),
            wrap="word",
            fg_color="#F8F9FA",
            border_color="#E0E0E0",
            border_width=1
        )
        self.bio_text.pack(fill="x", pady=(0, 10))
        self.bio_text.insert("1.0", self.user_data["bio"])
        self.bio_text.configure(state="disabled")
        
        # Botão para editar biografia
        ctk.CTkButton(
            info_frame,
            text="✏️ Editar Biografia",
            command=self.edit_bio,
            width=180,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=5)
    
    def setup_right_panel(self):
        """Configurar painel direito (certificados e projetos)"""
        # Container com tabs para alternar entre certificados e projetos
        self.tabview = ctk.CTkTabview(self.right_panel)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Aba de Certificados
        self.tabview.add("📜 Certificados")
        self.setup_certificados_tab()
        
        # Aba de Projetos
        self.tabview.add("🚀 Projetos")
        self.setup_projetos_tab()
        
        # Definir aba padrão
        self.tabview.set("📜 Certificados")
    
    def setup_certificados_tab(self):
        """Configurar aba de certificados"""
        cert_tab = self.tabview.tab("📜 Certificados")
        
        # Cabeçalho da aba
        header_frame = ctk.CTkFrame(cert_tab, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Meus Certificados",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Botão para adicionar certificado
        ctk.CTkButton(
            header_frame,
            text="+ Adicionar Certificado",
            command=self.add_certificate,
            width=200,
            height=40,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14, "bold")
        ).pack(side="right")
        
        # Container para lista de certificados
        self.cert_list_container = ctk.CTkFrame(cert_tab, fg_color="transparent")
        self.cert_list_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Atualizar lista
        self.update_certificates_display()
    
    def setup_projetos_tab(self):
        """Configurar aba de projetos"""
        projetos_tab = self.tabview.tab("🚀 Projetos")
        
        # Cabeçalho da aba
        header_frame = ctk.CTkFrame(projetos_tab, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Projetos que Estou Participando",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Container para lista de projetos
        projetos_container = ctk.CTkScrollableFrame(projetos_tab, fg_color="#F8F9FA")
        projetos_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Adicionar projetos
        for projeto in self.user_data["projetos"]:
            self.create_projeto_card(projetos_container, projeto)
    
    def create_projeto_card(self, parent, projeto):
        """Criar card de projeto"""
        card = ctk.CTkFrame(
            parent,
            height=120,
            corner_radius=12,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1
        )
        card.pack(fill="x", pady=8, padx=5)
        card.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Cabeçalho do projeto
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        # Nome do projeto
        ctk.CTkLabel(
            header_frame,
            text=projeto["nome"],
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        # Status do projeto
        status_color = "#2ECC71" if projeto["status"] == "Concluído" else "#F39C12" if projeto["status"] == "Em andamento" else "#3498DB"
        status_bg_color = "#E8F8EF" if projeto["status"] == "Concluído" else "#FEF5E7" if projeto["status"] == "Em andamento" else "#EBF5FB"
        
        status_frame = ctk.CTkFrame(header_frame, fg_color=status_bg_color, corner_radius=6)
        status_frame.pack(side="right", padx=(10, 0))
        
        ctk.CTkLabel(
            status_frame,
            text=projeto["status"],
            font=("Arial", 11, "bold"),
            text_color=status_color,
            padx=10,
            pady=3
        ).pack()
        
        # Descrição do projeto
        ctk.CTkLabel(
            content_frame,
            text=projeto["descricao"],
            font=("Arial", 13),
            text_color="#7F8C8D",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(10, 0))
    
    def update_display(self):
        """Atualizar todos os elementos da interface"""
        self.name_label.configure(text=self.user_data["nome"])
        self.course_label.configure(text=self.user_data["curso"])
        
        self.bio_text.configure(state="normal")
        self.bio_text.delete("1.0", "end")
        self.bio_text.insert("1.0", self.user_data["bio"])
        self.bio_text.configure(state="disabled")
        
        self.update_certificates_display()
    
    def update_certificates_display(self):
        """Atualizar exibição de certificados"""
        # Limpar container atual
        for widget in self.cert_list_container.winfo_children():
            widget.destroy()
        
        if not self.user_data["certificados"]:
            # Mensagem quando não há certificados
            empty_frame = ctk.CTkFrame(self.cert_list_container, fg_color="transparent", height=250)
            empty_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(
                empty_frame,
                text="📄",
                font=("Arial", 64),
                text_color="#BDC3C7"
            ).pack(pady=(40, 20))
            
            ctk.CTkLabel(
                empty_frame,
                text="Nenhum certificado adicionado",
                font=("Arial", 18),
                text_color="#7F8C8D"
            ).pack()
            
            ctk.CTkLabel(
                empty_frame,
                text="Clique em 'Adicionar Certificado' para adicionar seu primeiro certificado",
                font=("Arial", 14),
                text_color="#BDC3C7"
            ).pack(pady=(10, 0))
            
            return
        
        # Lista rolável para certificados
        cert_scroll_frame = ctk.CTkScrollableFrame(self.cert_list_container, fg_color="#F8F9FA")
        cert_scroll_frame.pack(fill="both", expand=True)
        
        # Adicionar cada certificado
        for idx, cert in enumerate(self.user_data["certificados"]):
            cert_card = ctk.CTkFrame(
                cert_scroll_frame,
                height=100,
                corner_radius=12,
                fg_color="white",
                border_color="#E0E0E0",
                border_width=1
            )
            cert_card.pack(fill="x", pady=8, padx=5)
            cert_card.pack_propagate(False)
            
            content_frame = ctk.CTkFrame(cert_card, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=25, pady=15)
            
            # Ícone e informações principais
            main_info = ctk.CTkFrame(content_frame, fg_color="transparent")
            main_info.pack(side="left", fill="both", expand=True)
            
            # Ícone
            icon_frame = ctk.CTkFrame(main_info, fg_color="transparent")
            icon_frame.pack(side="left")
            
            ctk.CTkLabel(
                icon_frame,
                text="📜",
                font=("Arial", 28)
            ).pack()
            
            # Detalhes do certificado
            details_frame = ctk.CTkFrame(main_info, fg_color="transparent")
            details_frame.pack(side="left", fill="both", expand=True, padx=15)
            
            # Nome do certificado
            ctk.CTkLabel(
                details_frame,
                text=cert["nome"],
                font=("Arial", 16, "bold"),
                text_color="#2C3E50"
            ).pack(anchor="w")
            
            # Informações secundárias
            info_text = f"📅 {cert['data']}"
            if cert.get('instituicao'):
                info_text += f"  •  🏛️ {cert['instituicao']}"
            if cert.get('carga_horaria'):
                info_text += f"  •  ⏱️ {cert['carga_horaria']}"
            
            ctk.CTkLabel(
                details_frame,
                text=info_text,
                font=("Arial", 13),
                text_color="#7F8C8D"
            ).pack(anchor="w", pady=(5, 0))
            
            # Botões de ação
            btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            btn_frame.pack(side="right")
            
            # Botão visualizar
            ctk.CTkButton(
                btn_frame,
                text="👁️ Ver",
                command=lambda c=cert: self.view_certificate(c),
                width=80,
                height=32,
                fg_color="#004A8D",
                hover_color="#003366",
                font=("Arial", 12)
            ).pack(side="left", padx=3)
            
            # Botão editar
            ctk.CTkButton(
                btn_frame,
                text="✏️ Editar",
                command=lambda i=idx: self.edit_certificate(i),
                width=80,
                height=32,
                fg_color="#004A8D",
                hover_color="#003366",
                font=("Arial", 12)
            ).pack(side="left", padx=3)
            
            # Botão excluir
            ctk.CTkButton(
                btn_frame,
                text="🗑️ Excluir",
                command=lambda i=idx: self.delete_certificate(i),
                width=80,
                height=32,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                font=("Arial", 12)
            ).pack(side="left", padx=3)
    
    def change_photo(self):
        """Alterar foto de perfil"""
        file_path = filedialog.askopenfilename(
            title="Selecione uma foto",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            try:
                Image.open(file_path).verify()
                filename = f"profile_{os.path.basename(file_path)}"
                new_path = f"assets/{filename}"
                shutil.copy(file_path, new_path)
                self.user_data["foto"] = new_path
                
                new_image = ctk.CTkImage(
                    light_image=Image.open(new_path),
                    size=(160, 160)
                )
                self.photo_label.configure(image=new_image)
                self.profile_img = new_image
                
                self.save_user_data()
                messagebox.showinfo("Sucesso", "Foto de perfil atualizada!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar a imagem.\n{str(e)}")
    
    def edit_name(self):
        """Editar nome do usuário"""
        dialog = ctk.CTkInputDialog(
            text="Digite seu novo nome:",
            title="Editar Nome"
        )
        
        new_name = dialog.get_input()
        
        if new_name and new_name.strip():
            self.user_data["nome"] = new_name.strip()
            self.save_user_data()
            self.update_display()
            messagebox.showinfo("Sucesso", "Nome atualizado com sucesso!")
    
    def edit_bio(self):
        """Abrir editor de biografia"""
        edit_window = ctk.CTkToplevel(self.app)
        edit_window.title("Editar Biografia")
        edit_window.geometry("500x400")
        edit_window.resizable(False, False)
        edit_window.transient(self.app)
        edit_window.grab_set()
        
        ctk.CTkLabel(
            edit_window,
            text="Editar Biografia",
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        
        text_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        bio_editor = ctk.CTkTextbox(
            text_frame,
            font=("Arial", 14),
            wrap="word"
        )
        bio_editor.pack(fill="both", expand=True)
        bio_editor.insert("1.0", self.user_data["bio"])
        
        btn_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        def save_changes():
            new_bio = bio_editor.get("1.0", "end-1c")
            if new_bio != self.user_data["bio"]:
                self.user_data["bio"] = new_bio
                self.save_user_data()
                self.update_display()
                messagebox.showinfo("Sucesso", "Biografia atualizada!")
            edit_window.destroy()
        
        ctk.CTkButton(
            btn_frame,
            text="Salvar",
            command=save_changes,
            width=120,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=edit_window.destroy,
            width=120,
            height=35,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
    
    def add_certificate(self):
        """Adicionar novo certificado"""
        add_window = ctk.CTkToplevel(self.app)
        add_window.title("Adicionar Certificado")
        add_window.geometry("500x600")
        add_window.resizable(False, False)
        add_window.transient(self.app)
        add_window.grab_set()
        
        # Container principal
        main_container = ctk.CTkFrame(add_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Título principal
        ctk.CTkLabel(
            main_container,
            text="Adicionar Certificado",
            font=("Arial", 24, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(0, 30))
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        # Nome do Certificado
        ctk.CTkLabel(
            form_frame,
            text="Nome do Certificado:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        cert_name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Curso de Python Avançado",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        cert_name_entry.pack(fill="x", pady=(0, 20))
        
        # Instituição
        ctk.CTkLabel(
            form_frame,
            text="Instituição:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        inst_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nome da instituição",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        inst_entry.pack(fill="x", pady=(0, 20))
        
        # Data de Conclusão
        ctk.CTkLabel(
            form_frame,
            text="Data de Conclusão:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        date_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="DD/MM/AAAA",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        date_entry.pack(fill="x", pady=(0, 20))
        
        # Carga Horária (opcional)
        ctk.CTkLabel(
            form_frame,
            text="Carga Horária (opcional):",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        hours_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: 40 horas",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        hours_entry.pack(fill="x", pady=(0, 25))
        
        # Upload de arquivo
        new_cert_file = [None]  # Usar lista para permitir modificação
        
        def select_file():
            file_path = filedialog.askopenfilename(
                title="Selecione o certificado",
                filetypes=[
                    ("PDF", "*.pdf"),
                    ("Imagens", "*.png *.jpg *.jpeg"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            if file_path:
                new_cert_file[0] = file_path
                file_label.configure(
                    text=f"Arquivo selecionado: {os.path.basename(file_path)}",
                    text_color="#27AE60"
                )
        
        file_btn = ctk.CTkButton(
            form_frame,
            text="Anexar Arquivo",
            command=select_file,
            width=150,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        )
        file_btn.pack(pady=(10, 5))
        
        file_label = ctk.CTkLabel(
            form_frame,
            text="Nenhum arquivo selecionado",
            font=("Arial", 12),
            text_color="#7F8C8D"
        )
        file_label.pack()
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        def save_certificate():
            # Validar campos obrigatórios
            nome = cert_name_entry.get().strip()
            data = date_entry.get().strip()
            
            if not nome:
                messagebox.showwarning("Atenção", "O nome do certificado é obrigatório!")
                return
            
            if not data:
                messagebox.showwarning("Atenção", "A data de conclusão é obrigatória!")
                return
            
            if not new_cert_file[0]:
                messagebox.showwarning("Atenção", "Selecione um arquivo para o certificado!")
                return
            
            try:
                # Criar objeto do certificado
                cert_data = {
                    "nome": nome,
                    "instituicao": inst_entry.get().strip(),
                    "data": data
                }
                
                # Adicionar carga horária se preenchida
                horas = hours_entry.get().strip()
                if horas:
                    # Adicionar "horas" se não estiver especificado
                    if not "horas" in horas.lower():
                        horas = f"{horas} horas"
                    cert_data["carga_horaria"] = horas
                
                # Copiar arquivo
                arquivo_original = new_cert_file[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nome_arquivo = os.path.basename(arquivo_original)
                filename = f"cert_{timestamp}_{nome_arquivo}"
                new_path = f"certificados/{filename}"
                
                # Garantir que o diretório existe
                os.makedirs("certificados", exist_ok=True)
                
                # Copiar arquivo
                shutil.copy2(arquivo_original, new_path)
                cert_data["arquivo"] = new_path
                
                # Adicionar à lista
                self.user_data["certificados"].append(cert_data)
                self.save_user_data()
                self.update_display()
                
                add_window.destroy()
                messagebox.showinfo("Sucesso", "Certificado adicionado com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar certificado:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="Salvar Certificado",
            command=save_certificate,
            width=180,
            height=40,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=add_window.destroy,
            width=120,
            height=40,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
    
    def edit_certificate(self, index):
        """Editar certificado existente"""
        cert = self.user_data["certificados"][index]
        
        edit_window = ctk.CTkToplevel(self.app)
        edit_window.title("Editar Certificado")
        edit_window.geometry("500x600")
        edit_window.resizable(False, False)
        edit_window.transient(self.app)
        edit_window.grab_set()
        
        main_container = ctk.CTkFrame(edit_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        ctk.CTkLabel(
            main_container,
            text="Editar Certificado",
            font=("Arial", 24, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(0, 30))
        
        form_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        # Nome do Certificado
        ctk.CTkLabel(
            form_frame,
            text="Nome do Certificado:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        cert_name_entry = ctk.CTkEntry(
            form_frame,
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        cert_name_entry.pack(fill="x", pady=(0, 20))
        cert_name_entry.insert(0, cert["nome"])
        
        # Instituição
        ctk.CTkLabel(
            form_frame,
            text="Instituição:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        inst_entry = ctk.CTkEntry(
            form_frame,
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        inst_entry.pack(fill="x", pady=(0, 20))
        inst_entry.insert(0, cert.get("instituicao", ""))
        
        # Data de Conclusão
        ctk.CTkLabel(
            form_frame,
            text="Data de Conclusão:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        date_entry = ctk.CTkEntry(
            form_frame,
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        date_entry.pack(fill="x", pady=(0, 20))
        date_entry.insert(0, cert["data"])
        
        # Carga Horária (opcional)
        ctk.CTkLabel(
            form_frame,
            text="Carga Horária (opcional):",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(15, 5))
        
        hours_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: 40 horas",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        hours_entry.pack(fill="x", pady=(0, 20))
        
        carga_horaria = cert.get("carga_horaria", "")
        if carga_horaria:
            # Limpar formatação
            horas = carga_horaria.replace('h', '').replace('horas', '').strip()
            hours_entry.insert(0, horas)
        
        # Informação do arquivo atual
        current_file = os.path.basename(cert.get("arquivo", "Nenhum"))
        ctk.CTkLabel(
            form_frame,
            text=f"Arquivo atual: {current_file}",
            font=("Arial", 12, "bold"),
            text_color="#3498DB"
        ).pack(anchor="w", pady=(15, 10))
        
        # Opção para trocar arquivo
        edit_cert_file = [None]
        
        def select_new_file():
            file_path = filedialog.askopenfilename(
                title="Selecione novo arquivo",
                filetypes=[
                    ("PDF", "*.pdf"),
                    ("Imagens", "*.png *.jpg *.jpeg")
                ]
            )
            if file_path:
                edit_cert_file[0] = file_path
                file_label.configure(
                    text=f"Novo arquivo: {os.path.basename(file_path)}",
                    text_color="#27AE60"
                )
        
        ctk.CTkButton(
            form_frame,
            text="Trocar Arquivo",
            command=select_new_file,
            width=150,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=(0, 10))
        
        file_label = ctk.CTkLabel(
            form_frame,
            text="Clique para selecionar novo arquivo",
            font=("Arial", 12),
            text_color="#7F8C8D"
        )
        file_label.pack()
        
        # Botões
        btn_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        def save_edits():
            nome = cert_name_entry.get().strip()
            data = date_entry.get().strip()
            
            if not nome:
                messagebox.showwarning("Atenção", "O nome do certificado é obrigatório!")
                return
            
            if not data:
                messagebox.showwarning("Atenção", "A data de conclusão é obrigatória!")
                return
            
            try:
                # Atualizar dados básicos
                self.user_data["certificados"][index]["nome"] = nome
                self.user_data["certificados"][index]["instituicao"] = inst_entry.get().strip()
                self.user_data["certificados"][index]["data"] = data
                
                # Atualizar carga horária
                horas = hours_entry.get().strip()
                if horas:
                    # Adicionar "horas" se não estiver especificado
                    if not "horas" in horas.lower():
                        horas = f"{horas} horas"
                    self.user_data["certificados"][index]["carga_horaria"] = horas
                elif "carga_horaria" in self.user_data["certificados"][index]:
                    del self.user_data["certificados"][index]["carga_horaria"]
                
                # Se novo arquivo selecionado
                if edit_cert_file[0]:
                    arquivo_original = edit_cert_file[0]
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nome_arquivo = os.path.basename(arquivo_original)
                    filename = f"cert_{timestamp}_{nome_arquivo}"
                    new_path = f"certificados/{filename}"
                    
                    # Garantir que o diretório existe
                    os.makedirs("certificados", exist_ok=True)
                    
                    # Copiar arquivo
                    shutil.copy2(arquivo_original, new_path)
                    self.user_data["certificados"][index]["arquivo"] = new_path
                
                self.save_user_data()
                self.update_display()
                
                edit_window.destroy()
                messagebox.showinfo("Sucesso", "Certificado atualizado!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao atualizar:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="Salvar Alterações",
            command=save_edits,
            width=180,
            height=40,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=edit_window.destroy,
            width=120,
            height=40,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
    
    def delete_certificate(self, index):
        """Excluir certificado"""
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir este certificado?\nEsta ação não pode ser desfeita."
        )
        
        if resposta:
            try:
                # Remover arquivo físico se existir
                cert = self.user_data["certificados"][index]
                arquivo = cert.get("arquivo")
                if arquivo and os.path.exists(arquivo):
                    os.remove(arquivo)
                
                # Remover da lista
                self.user_data["certificados"].pop(index)
                self.save_user_data()
                self.update_display()
                
                messagebox.showinfo("Sucesso", "Certificado excluído!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir:\n{str(e)}")
    
    def view_certificate(self, cert):
        """Visualizar informações do certificado"""
        info_text = f"📋 **Certificado**\n\n"
        info_text += f"**Nome:** {cert['nome']}\n"
        
        if cert.get('instituicao'):
            info_text += f"**Instituição:** {cert['instituicao']}\n"
        
        info_text += f"**Data:** {cert['data']}\n"
        
        if cert.get('carga_horaria'):
            info_text += f"**Carga Horária:** {cert['carga_horaria']}\n"
        
        arquivo = cert.get('arquivo', 'Não especificado')
        info_text += f"\n**Arquivo:** {os.path.basename(arquivo)}"
        
        messagebox.showinfo("Detalhes do Certificado", info_text)
    
    def run(self):
        """Executar aplicação"""
        self.app.mainloop()

def main():
    """Função principal"""
    os.makedirs("assets", exist_ok=True)
    os.makedirs("certificados", exist_ok=True)
    
    app = UserProfileSystem()
    app.run()

if __name__ == "__main__":
    main()