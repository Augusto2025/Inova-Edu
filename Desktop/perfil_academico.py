import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps
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
        self.app.geometry("1350x700")
        self.app.resizable(True, True)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.menu_frame, self.botoes_menu = sidebar(self.app)
        
        self.main_content_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.user_data = self.load_user_data()
        
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
                {"nome": "Sistema de Gestão Acadêmica", "descricao": "Desenvolvimento de sistema web para gestão de estudantes"},
                {"nome": "App Mobile para Ensino", "descricao": "Aplicativo para auxílio no aprendizado de matemática"},
                {"nome": "API de Integração", "descricao": "API REST para integração entre sistemas"}
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
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")
            return False
    
    def create_default_avatar(self):
        """Criar avatar padrão - APENAS BORDA E ÍCONE SIMPLES"""
        try:
            # Criar diretório se não existir
            os.makedirs("assets", exist_ok=True)
            
            # Criar imagem com fundo TRANSPARENTE
            size = 200
            img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))  # Transparente
            d = ImageDraw.Draw(img)
            
            # Desenhar círculo externo (borda cinza)
            border_size = 3
            d.ellipse(
                [border_size, border_size, size - border_size, size - border_size],
                fill='#E0E0E0',  # Cinza claro para borda
                outline='#C0C0C0',
                width=2
            )
            
            # Desenhar ícone de usuário simplificado (sem fundo branco)
            # Cabeça (círculo)
            head_center = size // 2
            head_radius = 35
            d.ellipse(
                [head_center - head_radius, 50, head_center + head_radius, 120],
                fill='#A0A0A0',
                outline='#808080',
                width=1
            )
            
            # Corpo (retângulo arredondado)
            body_top = 120
            body_bottom = 160
            body_width = 70
            d.rounded_rectangle(
                [head_center - body_width//2, body_top, 
                 head_center + body_width//2, body_bottom],
                radius=15,
                fill='#A0A0A0',
                outline='#808080',
                width=1
            )
            
            # Salvar a imagem
            avatar_path = "assets/default_avatar.png"
            img.save(avatar_path)
            
            print(f"Avatar criado com sucesso em: {avatar_path}")
            self.user_data["foto"] = avatar_path
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar avatar: {e}")
            # Criar uma imagem simples de fallback
            try:
                img = Image.new('RGBA', (200, 200), color=(240, 240, 240, 255))  # Cinza claro
                d = ImageDraw.Draw(img)
                d.ellipse([10, 10, 190, 190], fill='#E0E0E0', outline='#C0C0C0', width=2)
                img.save("assets/default_avatar.png")
                self.user_data["foto"] = "assets/default_avatar.png"
                return True
            except:
                return False
    
    def create_circular_image(self, image_path, size=200):
        """Criar uma imagem circular a partir de uma imagem qualquer"""
        try:
            # Abrir a imagem original
            original_img = Image.open(image_path).convert("RGBA")
            
            # Redimensionar mantendo proporção
            original_img.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            # Criar uma máscara circular
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            # Aplicar a máscara
            result = Image.new('RGBA', (size, size))
            result.paste(original_img, (0, 0), mask)
            
            # Adicionar borda
            border_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(border_img)
            draw.ellipse((0, 0, size, size), outline='#E0E0E0', width=3)
            
            # Combinar a imagem com a borda
            result = Image.alpha_composite(result, border_img)
            
            return result
            
        except Exception as e:
            print(f"Erro ao criar imagem circular: {e}")
            return None
    
    def setup_ui(self):
        """Configurar interface principal"""
        title_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="👤 Meu Perfil Acadêmico",
            font=("Arial", 28, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        self.profile_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.profile_frame.pack(fill="both", expand=True)
        
        self.left_panel = ctk.CTkFrame(self.profile_frame, width=350, corner_radius=15)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20))
        self.left_panel.pack_propagate(False)
        
        self.right_panel = ctk.CTkFrame(self.profile_frame, corner_radius=15)
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        self.setup_left_panel()
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """Configurar painel esquerdo"""
        profile_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        profile_header.pack(pady=20)
        
        # Container da foto de perfil - SEM FUNDO
        self.photo_container = ctk.CTkFrame(
            profile_header, 
            width=180, 
            height=180, 
            corner_radius=90,
            fg_color="transparent",  # TRANSPARENTE
            border_color="#E0E0E0",
            border_width=2
        )
        self.photo_container.pack()
        self.photo_container.pack_propagate(False)
        
        # Carregar a foto de perfil
        self.load_profile_photo()
        
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
        
        info_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        info_frame.pack(pady=20, padx=20, fill="x")
        
        self.name_label = ctk.CTkLabel(
            info_frame,
            text=self.user_data["nome"],
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        )
        self.name_label.pack(pady=(0, 10))
        
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
        
        ctk.CTkLabel(
            info_frame,
            text="📝 Biografia",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.bio_text = ctk.CTkTextbox(
            info_frame,
            height=120,
            font=("Arial", 13),
            wrap="word",
            fg_color="#F8F9FA",
            border_color="#E0E0E0",
            border_width=1
        )
        self.bio_text.pack(fill="x", pady=(0, 10))
        self.bio_text.insert("1.0", self.user_data["bio"])
        self.bio_text.configure(state="disabled")
        
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
    
    def load_profile_photo(self):
        """Carregar foto de perfil na interface"""
        try:
            # Verificar se o arquivo existe
            foto_path = self.user_data["foto"]
            
            if not os.path.exists(foto_path):
                print(f"Arquivo não encontrado: {foto_path}")
                # Criar avatar padrão
                if self.create_default_avatar():
                    foto_path = self.user_data["foto"]
                else:
                    # Usar uma imagem de fallback
                    foto_path = "assets/default_avatar.png"
            
            # Se for o avatar padrão, carregar normalmente
            if "default_avatar" in foto_path:
                pil_image = Image.open(foto_path)
            else:
                # Para fotos reais, criar versão circular
                pil_image = self.create_circular_image(foto_path, 180)
                if pil_image is None:
                    # Fallback para carregamento normal
                    pil_image = Image.open(foto_path)
            
            # Criar CTkImage
            self.profile_img = ctk.CTkImage(
                light_image=pil_image,
                size=(176, 176)  # Um pouco menor para caber na borda
            )
            
            # Criar ou atualizar o label da foto
            if hasattr(self, 'photo_label'):
                self.photo_label.configure(image=self.profile_img)
            else:
                self.photo_label = ctk.CTkLabel(
                    self.photo_container,
                    image=self.profile_img,
                    text="",
                    fg_color="transparent"  # Fundo transparente
                )
                self.photo_label.pack(pady=0)  # Sem padding
            
            print(f"Foto carregada: {foto_path}")
            
        except Exception as e:
            print(f"Erro ao carregar foto: {e}")
            # Criar um label de texto como fallback
            if hasattr(self, 'photo_label'):
                self.photo_label.configure(
                    text="👤", 
                    image=None, 
                    font=("Arial", 64),
                    fg_color="transparent"
                )
            else:
                self.photo_label = ctk.CTkLabel(
                    self.photo_container,
                    text="👤",
                    font=("Arial", 64),
                    text_color="#808080",
                    fg_color="transparent"
                )
                self.photo_label.pack(pady=0)
    
    def setup_right_panel(self):
        """Configurar painel direito"""
        self.tabview = ctk.CTkTabview(self.right_panel)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tabview.add("📜 Certificados")
        self.setup_certificados_tab()
        
        self.tabview.add("🚀 Projetos")
        self.setup_projetos_tab()
        
        self.tabview.set("📜 Certificados")
    
    def setup_certificados_tab(self):
        """Configurar aba de certificados"""
        cert_tab = self.tabview.tab("📜 Certificados")
        
        header_frame = ctk.CTkFrame(cert_tab, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Meus Certificados",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
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
        
        self.cert_list_container = ctk.CTkFrame(cert_tab, fg_color="transparent")
        self.cert_list_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.update_certificates_display()
    
    def setup_projetos_tab(self):
        """Configurar aba de projetos"""
        projetos_tab = self.tabview.tab("🚀 Projetos")
        
        header_frame = ctk.CTkFrame(projetos_tab, fg_color="transparent")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="Projetos que Estou Participando",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        projetos_container = ctk.CTkScrollableFrame(projetos_tab, fg_color="#F8F9FA")
        projetos_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        for projeto in self.user_data["projetos"]:
            self.create_projeto_card(projetos_container, projeto)
    
    def create_projeto_card(self, parent, projeto):
        """Criar card de projeto"""
        card = ctk.CTkFrame(
            parent,
            height=100,
            corner_radius=12,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1
        )
        card.pack(fill="x", pady=8, padx=5)
        card.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text=projeto["nome"],
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        
        ctk.CTkLabel(
            content_frame,
            text=projeto["descricao"],
            font=("Arial", 13),
            text_color="#7F8C8D",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(8, 0))
    
    def update_display(self):
        """Atualizar todos os elementos da interface"""
        self.name_label.configure(text=self.user_data["nome"])
        self.course_label.configure(text=self.user_data["curso"])
        
        self.bio_text.configure(state="normal")
        self.bio_text.delete("1.0", "end")
        self.bio_text.insert("1.0", self.user_data["bio"])
        self.bio_text.configure(state="disabled")
        
        # Atualizar a foto
        self.load_profile_photo()
        
        self.update_certificates_display()
    
    def update_certificates_display(self):
        """Atualizar exibição de certificados"""
        for widget in self.cert_list_container.winfo_children():
            widget.destroy()
        
        if not self.user_data["certificados"]:
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
        
        cert_scroll_frame = ctk.CTkScrollableFrame(self.cert_list_container, fg_color="#F8F9FA")
        cert_scroll_frame.pack(fill="both", expand=True)
        
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
            
            main_info = ctk.CTkFrame(content_frame, fg_color="transparent")
            main_info.pack(side="left", fill="both", expand=True)
            
            icon_frame = ctk.CTkFrame(main_info, fg_color="transparent")
            icon_frame.pack(side="left")
            
            ctk.CTkLabel(
                icon_frame,
                text="📜",
                font=("Arial", 28)
            ).pack()
            
            details_frame = ctk.CTkFrame(main_info, fg_color="transparent")
            details_frame.pack(side="left", fill="both", expand=True, padx=15)
            
            ctk.CTkLabel(
                details_frame,
                text=cert["nome"],
                font=("Arial", 16, "bold"),
                text_color="#2C3E50"
            ).pack(anchor="w")
            
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
            
            btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            btn_frame.pack(side="right")
            
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
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            try:
                # Verificar se é uma imagem válida
                Image.open(file_path).verify()
                
                # Criar nome único para o arquivo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"profile_{timestamp}_{os.path.basename(file_path)}"
                new_path = f"assets/{filename}"
                
                # Garantir que o diretório existe
                os.makedirs("assets", exist_ok=True)
                
                # Copiar arquivo
                shutil.copy(file_path, new_path)
                
                # Atualizar dados
                self.user_data["foto"] = new_path
                
                # Atualizar a imagem na interface
                self.load_profile_photo()
                
                # Salvar dados
                self.save_user_data()
                messagebox.showinfo("Sucesso", "✅ Foto de perfil atualizada!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Não foi possível carregar a imagem.\n{str(e)}")
    
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
            messagebox.showinfo("Sucesso", "✅ Nome atualizado com sucesso!")
    
    def edit_bio(self):
        """Abrir editor de biografia"""
        edit_window = ctk.CTkToplevel(self.app)
        edit_window.title("Editar Biografia")
        edit_window.geometry("500x350")
        edit_window.resizable(False, False)
        edit_window.transient(self.app)
        edit_window.grab_set()
        
        ctk.CTkLabel(
            edit_window,
            text="Editar Biografia",
            font=("Arial", 20, "bold")
        ).pack(pady=15)
        
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
        btn_frame.pack(pady=15)
        
        def save_changes():
            new_bio = bio_editor.get("1.0", "end-1c")
            if new_bio != self.user_data["bio"]:
                self.user_data["bio"] = new_bio
                self.save_user_data()
                self.update_display()
                messagebox.showinfo("Sucesso", "✅ Biografia atualizada!")
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
        # Criar nova janela
        self.add_window = ctk.CTkToplevel(self.app)
        self.add_window.title("Adicionar Certificado")
        self.add_window.geometry("500x650")
        self.add_window.resizable(False, False)
        self.add_window.transient(self.app)
        self.add_window.grab_set()
        
        # Container principal
        main_container = ctk.CTkFrame(self.add_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_container,
            text="Adicionar Certificado",
            font=("Arial", 24, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(0, 20))
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        # Armazenar referências
        self.cert_entries = {}
        
        # Nome do Certificado
        ctk.CTkLabel(
            form_frame,
            text="Nome do Certificado:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.cert_entries['nome'] = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Curso de Python Avançado",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        self.cert_entries['nome'].pack(fill="x", pady=(0, 15))
        
        # Instituição
        ctk.CTkLabel(
            form_frame,
            text="Instituição:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.cert_entries['instituicao'] = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nome da instituição",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        self.cert_entries['instituicao'].pack(fill="x", pady=(0, 15))
        
        # Data de Conclusão
        ctk.CTkLabel(
            form_frame,
            text="Data de Conclusão:",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.cert_entries['data'] = ctk.CTkEntry(
            form_frame,
            placeholder_text="DD/MM/AAAA",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        self.cert_entries['data'].pack(fill="x", pady=(0, 15))
        
        # Carga Horária (opcional)
        ctk.CTkLabel(
            form_frame,
            text="Carga Horária (opcional):",
            font=("Arial", 14, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        self.cert_entries['horas'] = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: 40 horas",
            height=40,
            font=("Arial", 13),
            corner_radius=8
        )
        self.cert_entries['horas'].pack(fill="x", pady=(0, 15))
        
        # Upload de arquivo
        self.file_label = ctk.CTkLabel(
            form_frame,
            text="Nenhum arquivo selecionado",
            font=("Arial", 12),
            text_color="#7F8C8D"
        )
        self.file_label.pack(pady=(10, 5))
        
        ctk.CTkButton(
            form_frame,
            text="📎 Anexar Arquivo",
            command=self.select_certificate_file,
            width=150,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=(0, 20))
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x")
        
        # Botão Salvar
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 SALVAR CERTIFICADO",
            command=self.save_certificate_data,
            width=200,
            height=45,
            fg_color="#27AE60",
            hover_color="#229954",
            font=("Arial", 16, "bold")
        )
        save_btn.pack(side="left", padx=10, pady=5)
        
        # Botão Cancelar
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ CANCELAR",
            command=self.add_window.destroy,
            width=150,
            height=45,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=("Arial", 14, "bold")
        )
        cancel_btn.pack(side="right", padx=10, pady=5)
        
        # Variável para armazenar o arquivo
        self.selected_file = None
    
    def select_certificate_file(self):
        """Selecionar arquivo do certificado"""
        file_path = filedialog.askopenfilename(
            title="Selecione o certificado",
            filetypes=[
                ("PDF", "*.pdf"),
                ("Imagens", "*.png *.jpg *.jpeg"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.configure(
                text=f"✅ Arquivo: {os.path.basename(file_path)}",
                text_color="#27AE60"
            )
    
    def save_certificate_data(self):
        """Salvar os dados do certificado"""
        # Obter valores dos campos
        nome = self.cert_entries['nome'].get().strip()
        instituicao = self.cert_entries['instituicao'].get().strip()
        data = self.cert_entries['data'].get().strip()
        horas = self.cert_entries['horas'].get().strip()
        
        # Validar campos obrigatórios
        if not nome:
            messagebox.showwarning("Atenção", "O nome do certificado é obrigatório!")
            return
        
        if not data:
            messagebox.showwarning("Atenção", "A data de conclusão é obrigatória!")
            return
        
        if not self.selected_file:
            messagebox.showwarning("Atenção", "Selecione um arquivo para o certificado!")
            return
        
        try:
            # Criar objeto do certificado
            cert_data = {
                "nome": nome,
                "instituicao": instituicao,
                "data": data
            }
            
            # Adicionar carga horária se preenchida
            if horas:
                if "horas" not in horas.lower() and "h" not in horas.lower():
                    horas = f"{horas} horas"
                cert_data["carga_horaria"] = horas
            
            # Copiar arquivo
            arquivo_original = self.selected_file
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
            
            # Salvar dados
            if self.save_user_data():
                # Limpar variável
                self.selected_file = None
                
                # Fechar a janela
                self.add_window.destroy()
                
                # Atualizar a exibição
                self.update_display()
                
                messagebox.showinfo("Sucesso", "✅ Certificado adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", "❌ Não foi possível salvar o certificado.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Falha ao salvar certificado:\n{str(e)}")
    
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
        new_file_path = [None]
        
        def select_new_file():
            file_path = filedialog.askopenfilename(
                title="Selecione novo arquivo",
                filetypes=[
                    ("PDF", "*.pdf"),
                    ("Imagens", "*.png *.jpg *.jpeg")
                ]
            )
            if file_path:
                new_file_path[0] = file_path
                file_label.configure(
                    text=f"Novo arquivo: {os.path.basename(file_path)}",
                    text_color="#27AE60"
                )
        
        ctk.CTkButton(
            form_frame,
            text="📎 Trocar Arquivo",
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
                    if "horas" not in horas.lower() and "h" not in horas.lower():
                        horas = f"{horas} horas"
                    self.user_data["certificados"][index]["carga_horaria"] = horas
                elif "carga_horaria" in self.user_data["certificados"][index]:
                    del self.user_data["certificados"][index]["carga_horaria"]
                
                # Se novo arquivo selecionado
                if new_file_path[0]:
                    arquivo_original = new_file_path[0]
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nome_arquivo = os.path.basename(arquivo_original)
                    filename = f"cert_{timestamp}_{nome_arquivo}"
                    new_path = f"certificados/{filename}"
                    
                    os.makedirs("certificados", exist_ok=True)
                    shutil.copy2(arquivo_original, new_path)
                    self.user_data["certificados"][index]["arquivo"] = new_path
                
                self.save_user_data()
                self.update_display()
                
                edit_window.destroy()
                messagebox.showinfo("Sucesso", "✅ Certificado atualizado!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Falha ao atualizar:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Alterações",
            command=save_edits,
            width=180,
            height=40,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
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
                
                messagebox.showinfo("Sucesso", "✅ Certificado excluído!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Falha ao excluir:\n{str(e)}")
    
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