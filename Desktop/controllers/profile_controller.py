import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import os
import shutil
from datetime import datetime

print("DEBUG: Carregando ProfileController...")

class ProfileController:
    def __init__(self, main_content_frame, menu_frame):
        print("DEBUG: Inicializando ProfileController...")
        self.main_content_frame = main_content_frame
        self.menu_frame = menu_frame
        
        # Importar e inicializar Model
        try:
            from models.user_model import UserModel
            self.model = UserModel()
            print("DEBUG: Model carregado com sucesso!")
        except ImportError as e:
            print(f"DEBUG: Erro ao carregar model: {e}")
            # Criar model básico localmente
            self.model = self.create_basic_model()
        
        # Importar e inicializar View
        try:
            from views.profile_view import ProfileView
            self.view = ProfileView(main_content_frame, self)
            print("DEBUG: View carregada com sucesso!")
        except ImportError as e:
            print(f"DEBUG: Erro ao carregar view: {e}")
            # Criar view básica localmente
            self.view = self.create_basic_view()
        
        # Atualizar a view com dados do model
        self.update_view()
    
    def create_basic_model(self):
        """Criar um modelo básico se o import falhar"""
        print("DEBUG: Criando modelo básico...")
        
        class BasicModel:
            def __init__(self):
                self.user_data = {
                    "nome": "Alcides Miranda Neto",
                    "bio": "Estudante dedicado com interesse em tecnologia e aprendizado contínuo.",
                    "curso": "Ciência da Computação",
                    "foto": "assets/default_avatar.png",
                    "certificados": [],
                    "projetos": []
                }
            
            def get_user_data(self):
                return self.user_data.copy()
            
            def update_profile_field(self, field, value):
                if field in self.user_data:
                    self.user_data[field] = value
                    return True
                return False
            
            def add_certificate(self, certificate_data):
                if "certificados" not in self.user_data:
                    self.user_data["certificados"] = []
                self.user_data["certificados"].append(certificate_data)
                return True
            
            def delete_certificate(self, index):
                if "certificados" in self.user_data and 0 <= index < len(self.user_data["certificados"]):
                    self.user_data["certificados"].pop(index)
                    return True
                return False
        
        return BasicModel()
    
    def create_basic_view(self):
        """Criar uma view básica se o import falhar"""
        # Esta função não será usada se ProfileView existir
        pass
    
    def create_default_avatar(self):
        """Criar avatar padrão - APENAS BORDA E ÍCONE SIMPLES"""
        try:
            print("DEBUG: Criando avatar padrão...")
            
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
            
            print(f"DEBUG: Avatar criado com sucesso em: {avatar_path}")
            return avatar_path
            
        except Exception as e:
            print(f"DEBUG: Erro ao criar avatar: {e}")
            # Criar uma imagem simples de fallback
            try:
                img = Image.new('RGBA', (200, 200), color=(240, 240, 240, 255))  # Cinza claro
                d = ImageDraw.Draw(img)
                d.ellipse([10, 10, 190, 190], fill='#E0E0E0', outline='#C0C0C0', width=2)
                img.save("assets/default_avatar.png")
                return "assets/default_avatar.png"
            except:
                return None
    
    def create_circular_image(self, image_path, size=200):
        """Criar uma imagem circular a partir de uma imagem qualquer"""
        try:
            original_img = Image.open(image_path).convert("RGBA")
            original_img.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            result = Image.new('RGBA', (size, size))
            result.paste(original_img, (0, 0), mask)
            
            # Adicionar borda
            border_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(border_img)
            draw.ellipse((0, 0, size, size), outline='#E0E0E0', width=3)
            
            result = Image.alpha_composite(result, border_img)
            return result
            
        except Exception as e:
            print(f"DEBUG: Erro ao criar imagem circular: {e}")
            return None
    
    def load_profile_photo(self):
        """Carregar foto de perfil REAL"""
        try:
            foto_path = self.model.user_data.get("foto", "assets/default_avatar.png")
            
            print(f"DEBUG: Tentando carregar foto: {foto_path}")
            
            # Verificar se o arquivo existe
            if not os.path.exists(foto_path):
                print(f"DEBUG: Arquivo não encontrado. Criando avatar padrão...")
                # Criar avatar padrão
                new_path = self.create_default_avatar()
                if new_path:
                    foto_path = new_path
                    # Atualizar modelo com o novo caminho
                    self.model.update_profile_field("foto", foto_path)
                else:
                    # Fallback para ícone
                    self.view.photo_label.configure(
                        text="👤",
                        image=None,
                        font=("Arial", 64),
                        text_color="#808080"
                    )
                    return
            
            # Carregar imagem
            if "default_avatar" in foto_path:
                pil_image = Image.open(foto_path)
            else:
                # Tentar criar imagem circular para fotos reais
                pil_image = self.create_circular_image(foto_path, 180)
                if pil_image is None:
                    pil_image = Image.open(foto_path)
            
            # Converter para CTkImage
            profile_img = ctk.CTkImage(
                light_image=pil_image,
                size=(176, 176)  # Um pouco menor para caber na borda
            )
            
            # Atualizar view
            self.view.photo_label.configure(
                image=profile_img,
                text=""
            )
            
            print(f"DEBUG: Foto carregada com sucesso: {foto_path}")
                
        except Exception as e:
            print(f"DEBUG: Erro ao carregar foto: {e}")
            # Fallback para ícone
            self.view.photo_label.configure(
                text="👤",
                image=None,
                font=("Arial", 64),
                text_color="#808080"
            )
    
    def update_view(self):
        """Atualizar a view com dados do model"""
        print("DEBUG: Atualizando view...")
        try:
            user_data = self.model.get_user_data()
            print(f"DEBUG: Dados do usuário: {user_data['nome']}")
            
            # Atualizar informações do perfil
            self.view.update_profile_info(user_data)
            
            # Atualizar certificados
            certificates = user_data.get("certificados", [])
            print(f"DEBUG: {len(certificates)} certificados encontrados")
            self.view.update_certificates_display(certificates)
            
            # Atualizar projetos
            projects = user_data.get("projetos", [])
            print(f"DEBUG: {len(projects)} projetos encontrados")
            self.view.update_projects_display(projects)
            
            # Carregar foto de perfil
            self.load_profile_photo()
            
            print("DEBUG: View atualizada com sucesso!")
            
        except Exception as e:
            print(f"DEBUG: Erro ao atualizar view: {e}")
            import traceback
            traceback.print_exc()
    
    # ========== FUNCIONALIDADES REAIS ==========
    
    def change_photo(self):
        """Alterar foto de perfil - FUNCIONALIDADE REAL"""
        print("DEBUG: change_photo REAL chamado")
        
        file_path = filedialog.askopenfilename(
            title="Selecione uma foto",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Validar que é uma imagem
                Image.open(file_path).verify()
                
                # Criar nome único para o arquivo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"profile_{timestamp}_{os.path.basename(file_path)}"
                new_path = f"assets/{filename}"
                
                # Garantir que o diretório existe
                os.makedirs("assets", exist_ok=True)
                
                # Copiar arquivo
                shutil.copy(file_path, new_path)
                
                # Atualizar modelo
                self.model.update_profile_field("foto", new_path)
                
                # Atualizar view
                self.load_profile_photo()
                
                messagebox.showinfo("Sucesso", "✅ Foto de perfil atualizada com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Não foi possível carregar a imagem:\n{str(e)}")
    
    def edit_name(self):
        """Editar nome do usuário - FUNCIONALIDADE REAL"""
        print("DEBUG: edit_name REAL chamado")
        
        current_name = self.model.user_data.get("nome", "")
        
        dialog = ctk.CTkInputDialog(
            text=f"Digite seu novo nome (atual: {current_name}):",
            title="Editar Nome"
        )
        
        new_name = dialog.get_input()
        
        if new_name and new_name.strip() and new_name.strip() != current_name:
            if self.model.update_profile_field("nome", new_name.strip()):
                self.update_view()
                messagebox.showinfo("Sucesso", "✅ Nome atualizado com sucesso!")
    
    def edit_bio(self):
        """Abrir editor de biografia - FUNCIONALIDADE REAL"""
        print("DEBUG: edit_bio REAL chamado")
        
        user_data = self.model.get_user_data()
        current_bio = user_data.get("bio", "")
        
        edit_window = ctk.CTkToplevel(self.main_content_frame.winfo_toplevel())
        edit_window.title("Editar Biografia")
        edit_window.geometry("500x350")
        edit_window.resizable(False, False)
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
        bio_editor.insert("1.0", current_bio)
        
        btn_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        def save_changes():
            new_bio = bio_editor.get("1.0", "end-1c")
            if new_bio != current_bio:
                if self.model.update_profile_field("bio", new_bio):
                    self.update_view()
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
        """Adicionar novo certificado - FUNCIONALIDADE REAL"""
        print("DEBUG: add_certificate REAL chamado")
        
        # Criar janela para adicionar certificado
        self.show_add_certificate_dialog()
    
    def show_add_certificate_dialog(self):
        """Mostrar diálogo para adicionar certificado"""
        add_window = ctk.CTkToplevel(self.main_content_frame.winfo_toplevel())
        add_window.title("Adicionar Certificado")
        add_window.geometry("500x700")
        add_window.resizable(False, False)
        add_window.grab_set()
        
        main_container = ctk.CTkFrame(add_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            main_container,
            text="📜 Adicionar Certificado",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(0, 20))
        
        # Formulário
        form_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        # Nome do Certificado
        ctk.CTkLabel(
            form_frame,
            text="Nome do Certificado:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(10, 5))
        
        nome_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Curso de Python Avançado",
            height=40,
            font=("Arial", 13)
        )
        nome_entry.pack(fill="x", pady=(0, 15))
        
        # Instituição
        ctk.CTkLabel(
            form_frame,
            text="Instituição:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(10, 5))
        
        instituicao_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nome da instituição",
            height=40,
            font=("Arial", 13)
        )
        instituicao_entry.pack(fill="x", pady=(0, 15))
        
        # Data
        ctk.CTkLabel(
            form_frame,
            text="Data de Conclusão:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(10, 5))
        
        data_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="DD/MM/AAAA",
            height=40,
            font=("Arial", 13)
        )
        data_entry.pack(fill="x", pady=(0, 15))
        
        # Carga Horária
        ctk.CTkLabel(
            form_frame,
            text="Carga Horária (opcional):",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(10, 5))
        
        carga_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: 40 horas",
            height=40,
            font=("Arial", 13)
        )
        carga_entry.pack(fill="x", pady=(0, 15))
        
        # Arquivo
        self.selected_cert_file = None
        file_label = ctk.CTkLabel(
            form_frame,
            text="Nenhum arquivo selecionado",
            font=("Arial", 12),
            text_color="#7F8C8D"
        )
        file_label.pack(pady=(10, 5))
        
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
                self.selected_cert_file = file_path
                file_label.configure(
                    text=f"✅ {os.path.basename(file_path)}",
                    text_color="#27AE60"
                )
        
        ctk.CTkButton(
            form_frame,
            text="📎 Anexar Arquivo",
            command=select_file,
            width=150,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 13)
        ).pack(pady=(0, 20))
        
        # Botões
        btn_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x")
        
        def save_certificate():
            # Validar campos obrigatórios
            nome = nome_entry.get().strip()
            data = data_entry.get().strip()
            
            if not nome:
                messagebox.showwarning("Atenção", "O nome do certificado é obrigatório!")
                return
            
            if not data:
                messagebox.showwarning("Atenção", "A data de conclusão é obrigatória!")
                return
            
            if not self.selected_cert_file:
                messagebox.showwarning("Atenção", "Selecione um arquivo para o certificado!")
                return
            
            try:
                # Preparar dados do certificado
                cert_data = {
                    "nome": nome,
                    "instituicao": instituicao_entry.get().strip(),
                    "data": data
                }
                
                # Adicionar carga horária se preenchida
                carga = carga_entry.get().strip()
                if carga:
                    cert_data["carga_horaria"] = carga
                
                # Salvar arquivo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"cert_{timestamp}_{os.path.basename(self.selected_cert_file)}"
                new_path = f"certificados/{filename}"
                
                os.makedirs("certificados", exist_ok=True)
                shutil.copy2(self.selected_cert_file, new_path)
                cert_data["arquivo"] = new_path
                
                # Adicionar ao modelo
                if self.model.add_certificate(cert_data):
                    # Atualizar view
                    self.update_view()
                    add_window.destroy()
                    messagebox.showinfo("Sucesso", "✅ Certificado adicionado com sucesso!")
                else:
                    messagebox.showerror("Erro", "❌ Não foi possível salvar o certificado.")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar certificado:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Certificado",
            command=save_certificate,
            width=180,
            height=40,
            fg_color="#27AE60",
            hover_color="#229954",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=add_window.destroy,
            width=120,
            height=40,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=("Arial", 14)
        ).pack(side="right", padx=5)
    
    def view_certificate(self, cert):
        """Visualizar informações do certificado - FUNCIONALIDADE REAL"""
        print(f"DEBUG: Visualizando certificado: {cert['nome']}")
        
        # Criar janela de detalhes
        detail_window = ctk.CTkToplevel(self.main_content_frame.winfo_toplevel())
        detail_window.title(f"Certificado: {cert['nome']}")
        detail_window.geometry("500x400")
        detail_window.resizable(False, False)
        detail_window.grab_set()
        
        main_frame = ctk.CTkFrame(detail_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="📋 Detalhes do Certificado",
            font=("Arial", 22, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(0, 20))
        
        # Informações
        info_frame = ctk.CTkFrame(main_frame, fg_color="#F8F9FA", corner_radius=10)
        info_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        info_text = f"**Nome:** {cert['nome']}\n\n"
        
        if cert.get('instituicao'):
            info_text += f"**Instituição:** {cert['instituicao']}\n\n"
        
        info_text += f"**Data de Conclusão:** {cert['data']}\n\n"
        
        if cert.get('carga_horaria'):
            info_text += f"**Carga Horária:** {cert['carga_horaria']}\n\n"
        
        if cert.get('arquivo'):
            info_text += f"**Arquivo:** {os.path.basename(cert['arquivo'])}"
        
        # Usar CTkTextbox para melhor formatação
        text_widget = ctk.CTkTextbox(
            info_frame,
            height=200,
            font=("Arial", 14),
            wrap="word",
            fg_color="transparent",
            border_width=0
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")
        
        # Botões adicionais
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        # Botão para abrir arquivo se existir
        if cert.get('arquivo') and os.path.exists(cert['arquivo']):
            def open_file():
                try:
                    os.startfile(cert['arquivo'])  # Windows
                except:
                    try:
                        import subprocess
                        subprocess.run(['open', cert['arquivo']])  # Mac
                    except:
                        try:
                            subprocess.run(['xdg-open', cert['arquivo']])  # Linux
                        except:
                            messagebox.showinfo("Abrir Arquivo", 
                                              f"Caminho do arquivo:\n{cert['arquivo']}")
            
            ctk.CTkButton(
                btn_frame,
                text="📂 Abrir Arquivo",
                command=open_file,
                width=120,
                height=35,
                fg_color="#3498DB",
                hover_color="#2980B9",
                font=("Arial", 12)
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Fechar",
            command=detail_window.destroy,
            width=120,
            height=35,
            fg_color="#004A8D",
            hover_color="#003366",
            font=("Arial", 12)
        ).pack(side="left", padx=5)
    
    def edit_certificate(self, index):
        """Editar certificado existente - FUNCIONALIDADE REAL"""
        print(f"DEBUG: edit_certificate REAL chamado para índice {index}")
        
        # Obter certificado atual
        user_data = self.model.get_user_data()
        certificates = user_data.get("certificados", [])
        
        if 0 <= index < len(certificates):
            cert = certificates[index]
            
            # Mostrar mensagem de desenvolvimento
            messagebox.showinfo("Funcionalidade em Desenvolvimento", 
                              f"A edição de certificados está sendo desenvolvida.\n\n"
                              f"Certificado: {cert['nome']}\n"
                              f"Para editar, exclua e adicione um novo.")
        else:
            messagebox.showerror("Erro", "Certificado não encontrado!")
    
    def delete_certificate(self, index):
        """Excluir certificado - FUNCIONALIDADE REAL"""
        print(f"DEBUG: delete_certificate REAL chamado para índice {index}")
        
        user_data = self.model.get_user_data()
        certificates = user_data.get("certificados", [])
        
        if 0 <= index < len(certificates):
            cert = certificates[index]
            cert_name = cert['nome']
            
            resposta = messagebox.askyesno(
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o certificado:\n\n"
                f"**{cert_name}**\n"
                f"Data: {cert.get('data', 'N/A')}\n\n"
                f"Esta ação não pode ser desfeita!"
            )
            
            if resposta:
                try:
                    # Remover arquivo físico se existir
                    arquivo = cert.get('arquivo')
                    if arquivo and os.path.exists(arquivo):
                        os.remove(arquivo)
                        print(f"DEBUG: Arquivo removido: {arquivo}")
                    
                    # Remover do modelo
                    if self.model.delete_certificate(index):
                        # Atualizar view
                        self.update_view()
                        messagebox.showinfo("Sucesso", f"✅ Certificado '{cert_name}' excluído com sucesso!")
                    else:
                        messagebox.showerror("Erro", "❌ Não foi possível excluir o certificado.")
                        
                except Exception as e:
                    messagebox.showerror("Erro", f"❌ Erro ao excluir certificado:\n{str(e)}")
        else:
            messagebox.showerror("Erro", "❌ Certificado não encontrado!")