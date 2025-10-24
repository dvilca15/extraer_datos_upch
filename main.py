import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# Agregar las carpetas de módulos al path
sys.path.insert(0, str(Path(__file__).parent / "modulo1"))
sys.path.insert(0, str(Path(__file__).parent / "modulo2"))

# Importar los módulos
from modulo1.model import PDFDataModel
from modulo1.view import PDFExtractorView
from modulo1.controller import PDFExtractorController

from modulo2.model_transegen import TransSegenModel
from modulo2.view_transegen import TransSegenView
from modulo2.controller_transegen import TransSegenController


class MainMenu:
    """Menú principal para seleccionar el módulo de extracción"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Extracción de Datos PDF")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura la interfaz del menú principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Sistema de Extracción de Datos PDF",
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Seleccione el módulo que desea utilizar:",
            font=('Arial', 11)
        )
        subtitle_label.pack(pady=10)
        
        # Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
        # Botón Módulo 1: Datos de Estudiantes
        btn_estudiantes = ttk.Button(
            button_frame,
            text="📚 Módulo 1: Informe Socioeconómico",
            command=self.open_estudiantes_module,
            width=40
        )
        btn_estudiantes.pack(pady=10, ipady=20)
        
        # Botón Módulo 2: Trans-Segen
        btn_transegen = ttk.Button(
            button_frame,
            text="📋 Módulo 2: Trans-Segen",
            command=self.open_transegen_module,
            width=40
        )
        btn_transegen.pack(pady=10, ipady=20)
        
        # Información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(side=tk.BOTTOM, pady=10)
        
        info_label = ttk.Label(
            info_frame,
            text="Desarrollado para extracción automática de datos desde PDFs",
            font=('Arial', 8),
            foreground='gray'
        )
        info_label.pack()
    
    def open_estudiantes_module(self):
        """Abre el módulo de datos de estudiantes"""
        # Crear nueva ventana
        estudiantes_window = tk.Toplevel(self.root)
        
        # Ocultar el menú principal
        self.root.withdraw()
        
        # Configurar el cierre del módulo
        def on_closing():
            estudiantes_window.destroy()
            self.root.deiconify()  # Mostrar menú principal nuevamente
        
        estudiantes_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Crear el modelo, vista y controlador
        model = PDFDataModel()
        view = PDFExtractorView(estudiantes_window)
        controller = PDFExtractorController(model, view)
    
    def open_transegen_module(self):
        """Abre el módulo de Trans-Segen"""
        # Crear nueva ventana
        transegen_window = tk.Toplevel(self.root)
        
        # Ocultar el menú principal
        self.root.withdraw()
        
        # Configurar el cierre del módulo
        def on_closing():
            transegen_window.destroy()
            self.root.deiconify()  # Mostrar menú principal nuevamente
        
        transegen_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Crear el modelo, vista y controlador
        model = TransSegenModel()
        view = TransSegenView(transegen_window)
        controller = TransSegenController(model, view)


def main():
    """Punto de entrada de la aplicación"""
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()