import fitz  # PyMuPDF
import re
from pathlib import Path


class PDFDataModel:
    """Modelo que maneja la lógica de negocio y datos"""
    
    def __init__(self):
        self.pdf_files = []
        self.extracted_data = []
    
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
    
    def extract_text_from_pdf(self, pdf_path):
        """Extrae texto de las primeras páginas y última página del PDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            # Extraer texto de las primeras 2 páginas para datos personales
            for page_num in range(min(len(doc), 2)):
                page = doc[page_num]
                text += page.get_text() + "\n\n"
            
            # Extraer texto de la ÚLTIMA página para el nivel de riesgo
            if len(doc) > 0:
                last_page = doc[-1]
                text += "\n\n=== ÚLTIMA PÁGINA ===\n\n"
                text += last_page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Error al leer {Path(pdf_path).name}: {str(e)}")
    
    def extract_data_from_text(self, text, pdf_name):
        """Extrae los datos específicos del texto del PDF"""
        data = {
            'archivo': pdf_name,
            'nombres': '',
            'dni': '',
            'nivel_riesgo': ''
        }
        
        # Extraer Nombres y Apellidos
        nombre_match = re.search(r'Nombres\s+y\s+apellidos\s*:?\s*([^\n]+)', text, re.IGNORECASE)
        if nombre_match:
            data['nombres'] = nombre_match.group(1).strip()
        
        # Extraer DNI (8 dígitos)
        dni_match = re.search(r'DNI\s*:?\s*(\d{8})', text, re.IGNORECASE)
        if dni_match:
            data['dni'] = dni_match.group(1).strip()
        
        # Extraer Nivel de Riesgo Social
        lines = text.split('\n')
        
        # Buscar la sección "Nivel de Riesgo Social"
        for i, line in enumerate(lines):
            if 'Nivel de Riesgo Social' in line:
                # Buscar en las siguientes 10 líneas
                for j in range(i, min(i + 10, len(lines))):
                    current_line = lines[j].strip()
                    next_line = lines[j + 1].strip() if j + 1 < len(lines) else ""
                    next_next_line = lines[j + 2].strip() if j + 2 < len(lines) else ""
                    
                    # Verificar Alto
                    if re.match(r'^Alto\s*$', current_line, re.IGNORECASE):
                        if 'X' in current_line or 'x' in current_line:
                            data['nivel_riesgo'] = 'Alto'
                            break
                        elif next_line == 'X' or next_line == 'x':
                            data['nivel_riesgo'] = 'Alto'
                            break
                        elif next_next_line == 'X' or next_next_line == 'x':
                            data['nivel_riesgo'] = 'Alto'
                            break
                    
                    # Verificar Medio
                    elif re.match(r'^Medio\s*$', current_line, re.IGNORECASE):
                        if 'X' in current_line or 'x' in current_line:
                            data['nivel_riesgo'] = 'Medio'
                            break
                        elif next_line == 'X' or next_line == 'x':
                            data['nivel_riesgo'] = 'Medio'
                            break
                        elif next_next_line == 'X' or next_next_line == 'x':
                            data['nivel_riesgo'] = 'Medio'
                            break
                    
                    # Verificar Bajo
                    elif re.match(r'^Bajo\s*$', current_line, re.IGNORECASE):
                        if 'X' in current_line or 'x' in current_line:
                            data['nivel_riesgo'] = 'Bajo'
                            break
                        elif next_line == 'X' or next_line == 'x':
                            data['nivel_riesgo'] = 'Bajo'
                            break
                        elif next_next_line == 'X' or next_next_line == 'x':
                            data['nivel_riesgo'] = 'Bajo'
                            break
                    
                    # Verificar Ninguno
                    elif re.match(r'^Ninguno\s*$', current_line, re.IGNORECASE):
                        if 'X' in current_line or 'x' in current_line:
                            data['nivel_riesgo'] = 'Ninguno'
                            break
                        elif next_line == 'X' or next_line == 'x':
                            data['nivel_riesgo'] = 'Ninguno'
                            break
                        elif next_next_line == 'X' or next_next_line == 'x':
                            data['nivel_riesgo'] = 'Ninguno'
                            break
                
                if data['nivel_riesgo']:
                    break
        
        return data
    
    def process_all_pdfs(self):
        """Procesa todos los PDFs cargados y extrae sus datos"""
        self.extracted_data = []
        
        for pdf_path in self.pdf_files:
            try:
                text = self.extract_text_from_pdf(pdf_path)
                if text:
                    data = self.extract_data_from_text(text, Path(pdf_path).name)
                    self.extracted_data.append(data)
            except Exception as e:
                # Agregar datos vacíos con el error
                self.extracted_data.append({
                    'archivo': Path(pdf_path).name,
                    'nombres': '',
                    'dni': '',
                    'nivel_riesgo': '',
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