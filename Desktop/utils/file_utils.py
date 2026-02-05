import os
import shutil
from datetime import datetime

class FileUtils:
    @staticmethod
    def save_profile_image(file_path, destination_dir="assets"):
        """
        Salvar imagem de perfil com nome único
        """
        try:
            os.makedirs(destination_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"profile_{timestamp}_{os.path.basename(file_path)}"
            new_path = os.path.join(destination_dir, filename)
            
            shutil.copy(file_path, new_path)
            return new_path
            
        except Exception as e:
            print(f"Erro ao salvar imagem: {e}")
            return None
    
    @staticmethod
    def save_certificate_file(file_path, destination_dir="certificados"):
        """
        Salvar arquivo de certificado com nome único
        """
        try:
            os.makedirs(destination_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"cert_{timestamp}_{os.path.basename(file_path)}"
            new_path = os.path.join(destination_dir, filename)
            
            shutil.copy2(file_path, new_path)
            return new_path
            
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            return None