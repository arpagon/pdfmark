import numpy as np
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
import io
from pathlib import Path
import math

def create_rainbow_gradient(width: int, height: int) -> Image.Image:
    """Create a rainbow gradient image."""
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    for x in range(width):
        # Create rainbow hue based on position
        hue = (x / width) * 360
        # Convert HSV to RGB
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        for y in range(height):
            image.putpixel((x, y), (r, g, b, 255))
    
    return image

def create_wave_text_lines(width: int, height: int, frequency: int = 3, text: str = "WATERMARK") -> Image.Image:
    """Create continuous wave lines made of repeating text using improved algorithm."""
    from PIL import ImageFont
    
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    try:
        # Dynamic font size based on dimensions
        font_size = max(8, min(width, height) // 60)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Improved spacing calculation
    vertical_spacing = font_size + 5
    wave_amplitude = font_size // 2
    wave_frequency = 0.01 + (frequency * 0.005)  # More controlled frequency
    
    # Create text lines with proper wave distribution
    for y in range(0, height + vertical_spacing, vertical_spacing):
        # Create extended text string
        full_text = text
        text_width = draw.textlength(full_text, font=font)
        while text_width < width * 1.5:
            full_text += text
            text_width = draw.textlength(full_text, font=font)
        
        # Phase shift for each line
        phase_shift = y / 5
        
        # Draw each character with wave transformation
        char_x = 0
        for i, char in enumerate(full_text):
            if char_x > width + font_size:
                break
                
            # Calculate wave position
            wave_y = y + math.sin(char_x * wave_frequency) * wave_amplitude
            
            # Calculate rotation angle based on wave slope
            angle = math.atan(wave_frequency * wave_amplitude * math.cos(char_x * wave_frequency))
            angle_degrees = math.degrees(angle)
            
            # Create rotated character
            if abs(angle_degrees) > 1:
                temp_size = font_size * 3
                char_img = Image.new('L', (temp_size, temp_size), 0)
                char_draw = ImageDraw.Draw(char_img)
                char_draw.text((temp_size//2, temp_size//2), char, font=font, fill=255, anchor="mm")
                char_img = char_img.rotate(-angle_degrees, expand=False)
                
                # Paste rotated character
                paste_x = int(char_x - temp_size//2 - phase_shift)
                paste_y = int(wave_y - temp_size//2)
                
                if paste_x > -temp_size and paste_x < width and paste_y > -temp_size and paste_y < height:
                    # Efficient paste using PIL's paste method with mask
                    try:
                        mask.paste(char_img, (paste_x, paste_y), char_img)
                    except:
                        # Fallback to pixel-by-pixel for edge cases
                        for dy in range(temp_size):
                            for dx in range(temp_size):
                                src_x, src_y = paste_x + dx, paste_y + dy
                                if 0 <= src_x < width and 0 <= src_y < height:
                                    char_alpha = char_img.getpixel((dx, dy))
                                    if char_alpha > 0:
                                        current = mask.getpixel((src_x, src_y))
                                        new_alpha = min(255, current + char_alpha//3)  # Blend more subtly
                                        mask.putpixel((src_x, src_y), new_alpha)
            else:
                # Draw straight character
                draw.text((char_x - phase_shift, wave_y), char, font=font, fill=255)  # Full opacity
            
            # Advance character position
            char_x += draw.textlength(char, font=font)
    
    return mask

def create_watermark_image(width: int, height: int, wave_frequency: int, opacity: float, text: str = "WATERMARK") -> Image.Image:
    """Create the complete watermark image with rainbow gradient only where text appears."""
    # Create rainbow gradient
    gradient = create_rainbow_gradient(width, height)
    
    # Create wave text lines mask
    wave_mask = create_wave_text_lines(width, height, wave_frequency, text)
    
    # Create transparent image
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Apply gradient only where text mask exists
    for y in range(height):
        for x in range(width):
            mask_alpha = wave_mask.getpixel((x, y))
            if mask_alpha > 0:
                # Get gradient color at this position
                gradient_color = gradient.getpixel((x, y))
                # Apply opacity to the mask alpha - ensure minimum visibility
                final_alpha = int(min(255, max(20, mask_alpha * opacity * 2)))
                # Set pixel with gradient color and computed alpha
                result.putpixel((x, y), gradient_color[:3] + (final_alpha,))
    
    return result

def add_watermark(input_path: Path, output_path: Path, opacity: float = 0.3, wave_frequency: int = 3, text: str = "WATERMARK"):
    """Add wave pattern watermark to PDF."""
    
    # Read input PDF
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    
    for page_num, page in enumerate(reader.pages):
        # Get page dimensions
        page_box = page.mediabox
        page_width = float(page_box.width)
        page_height = float(page_box.height)
        
        # Create watermark image
        watermark_img = create_watermark_image(
            int(page_width), 
            int(page_height), 
            wave_frequency, 
            opacity,
            text
        )
        
        # Save watermark to bytes
        img_bytes = io.BytesIO()
        watermark_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Create PDF with watermark
        watermark_pdf = io.BytesIO()
        c = canvas.Canvas(watermark_pdf, pagesize=(page_width, page_height))
        c.drawImage(ImageReader(img_bytes), 0, 0, width=page_width, height=page_height)
        c.save()
        
        # Merge watermark with original page
        watermark_pdf.seek(0)
        watermark_reader = PdfReader(watermark_pdf)
        watermark_page = watermark_reader.pages[0]
        
        # Merge pages - put watermark under original content
        watermark_page.merge_page(page)
        writer.add_page(watermark_page)
    
    # Write output PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)