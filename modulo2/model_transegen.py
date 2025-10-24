import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import re
from pathlib import Path


class TransSegenModel:
    """Modelo para extracción de datos Trans-Segen usando OCR"""
    
    def __init__(self):
        self.pdf_files = []
        self.extracted_data = []
        
        # Configurar Tesseract (ajusta la ruta según tu instalación)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\70995003\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    
    def add_pdf_files(self, files):
        """Agrega archivos PDF a la lista"""
        self.pdf_files.extend(files)
        return len(self.pdf_files)
    
    def get_pdf_files(self):
        """Retorna la lista de archivos PDF"""
        return self.pdf_files
    
    def get_pdf_names(self):
        """Retorna solo los nombres de los archivos"""
        return [Path(pdf).name for pdf in self.pdf_files]
    
    def clear_files(self):
        """Limpia todos los datos"""
        self.pdf_files = []
        self.extracted_data = []
    
    def extract_text_from_pdf_ocr(self, pdf_path):
        """Extrae texto de un PDF escaneado usando OCR"""
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            
            # Procesar solo las primeras 2 páginas
            for page_num in range(min(len(doc), 2)):
                page = doc[page_num]
                
                # Primero intentar extraer texto normal
                page_text = page.get_text()
                
                # Si no hay texto o es muy poco, usar OCR
                if len(page_text.strip()) < 50:
                    # Convertir página a imagen
                    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Aplicar OCR con configuración en español
                    page_text = pytesseract.image_to_string(
                        img, 
                        lang='spa',
                        config='--psm 6'
                    )
                
                full_text += page_text + "\n\n"
            
            doc.close()
            return full_text
        
        except Exception as e:
            raise Exception(f"Error al procesar {Path(pdf_path).name}: {str(e)}")
    
    def extract_data_from_text(self, text, pdf_name):
        """Extrae datos específicos del texto (Trans-Segen)"""
        data = {
            'archivo': pdf_name,
            'nombres': '',
            'nro_transegen': ''
        }
        
        # Extraer Nro Trans-Segen del encabezado
        # Patrón: TRANS-SEGEN-UPCH-2025-CU-XXXX
        transegen_match = re.search(
            r'TRANS[-\s]?SEGEN[-\s]?UPCH[-\s]?\d{4}[-\s]?CU[-\s]?\d{4}',
            text,
            re.IGNORECASE
        )
        
        if transegen_match:
            # Normalizar el formato eliminando espacios extras
            nro_raw = transegen_match.group(0)
            nro_normalized = re.sub(r'\s+', '-', nro_raw.strip())
            data['nro_transegen'] = nro_normalized
        
        # Extraer Nombre después de "CONSIDERANDO:" y "Que,"
        # Buscar el patrón: CONSIDERANDO: ... Que, NOMBRE APELLIDO
        considerando_section = re.search(
            r'CONSIDERANDO:.*?Que,?\s+([A-ZÁÉÍÓÚÑ\s]+(?:,\s*[A-ZÁÉÍÓÚÑ\s]+)?)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if considerando_section:
            nombre_raw = considerando_section.group(1).strip()
            # Limpiar el nombre (tomar solo hasta 'es estudiante' o similar)
            nombre_clean = re.split(
                r',?\s+es\s+estudiante|,?\s+de\s+acuerdo',
                nombre_raw,
                flags=re.IGNORECASE
            )[0].strip()
            
            # Convertir a formato Title Case para mejor legibilidad
            data['nombres'] = ' '.join(word.capitalize() for word in nombre_clean.split())
        
        return data
    
    def process_all_pdfs(self):
        """Procesa todos los PDFs cargados y extrae sus datos"""
        self.extracted_data = []
        
        for pdf_path in self.pdf_files:
            try:
                text = self.extract_text_from_pdf_ocr(pdf_path)
                if text:
                    data = self.extract_data_from_text(text, Path(pdf_path).name)
                    self.extracted_data.append(data)
            except Exception as e:
                self.extracted_data.append({
                    'archivo': Path(pdf_path).name,
                    'nombres': '',
                    'nro_transegen': '',
                    'error': str(e)
                })
        
        return self.extracted_data
    
    def get_extracted_data(self):
        """Retorna los datos extraídos"""
        return self.extracted_data
    
    def has_data(self):
        """Verifica si hay datos extraídos"""
        return len(self.extracted_data) > 0
    
    def has_files(self):
        """Verifica si hay archivos cargados"""
        return len(self.pdf_files) > 0