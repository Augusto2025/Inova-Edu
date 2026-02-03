def __init__(self, main_content_frame, menu_frame):
    self.main_content_frame = main_content_frame
    self.menu_frame = menu_frame
    
    # Importar Model
    from models.user_model import UserModel
    from utils.image_utils import ImageUtils
    from utils.file_utils import FileUtils
    
    # Inicializar componentes
    self.model = UserModel()
    self.image_utils = ImageUtils
    self.file_utils = FileUtils
    
    # Importar Views
    from views.profile_view import ProfileView
    from views.certificates_view import CertificatesView
    from views.projects_view import ProjectsView
    
    # Inicializar Views
    self.profile_view = ProfileView(main_content_frame, self)
    self.certificates_view = CertificatesView(self)
    self.projects_view = ProjectsView(self)
    
    # Configurar as views nas abas
    self.setup_tab_views()
    
    # Atualizar views
    self.update_all_views()