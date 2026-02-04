from PIL import Image, ImageDraw
import os

class ImageUtils:
    @staticmethod
    def create_default_avatar():
        """
        Criar avatar padrão
        """
        try:
            os.makedirs("assets", exist_ok=True)
            
            size = 200
            img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            
            border_size = 3
            d.ellipse(
                [border_size, border_size, size - border_size, size - border_size],
                fill='#E0E0E0',
                outline='#C0C0C0',
                width=2
            )
            
            head_center = size // 2
            head_radius = 35
            d.ellipse(
                [head_center - head_radius, 50, head_center + head_radius, 120],
                fill='#A0A0A0',
                outline='#808080',
                width=1
            )
            
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
            
            avatar_path = "assets/default_avatar.png"
            img.save(avatar_path)
            return avatar_path
            
        except Exception as e:
            print(f"Erro ao criar avatar: {e}")
            return None
    
    @staticmethod
    def create_circular_image(image_path, size=200):
        """
        Criar uma imagem circular a partir de uma imagem qualquer
        """
        try:
            original_img = Image.open(image_path).convert("RGBA")
            original_img.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            result = Image.new('RGBA', (size, size))
            result.paste(original_img, (0, 0), mask)
            
            border_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(border_img)
            draw.ellipse((0, 0, size, size), outline='#E0E0E0', width=3)
            
            result = Image.alpha_composite(result, border_img)
            return result
            
        except Exception as e:
            print(f"Erro ao criar imagem circular: {e}")
            return None