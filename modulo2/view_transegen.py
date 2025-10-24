import tkinter as tk
from tkinter import ttk

class TransSegenView:
    """Vista para el módulo Trans-Segen"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor Trans-Segen")
        self.root.geometry("1000x700")  # Ventana más grande
        self.root.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura todos los elementos de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="Extractor de Datos Trans-Segen (OCR)",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # Nota sobre OCR
        note_label = ttk.Label(
            main_frame,
            text="⚠️ Este módulo usa OCR para PDFs escaneados. El proceso puede tardar más.",
            font=('Arial', 10),
            foreground='#FF6B35'
        )
        note_label.pack(pady=5)
        
        # Separador
        separator1 = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator1.pack(fill=tk.X, pady=10)
        
        # Frame de botones (VERTICAL)
        self._create_button_frame(main_frame)
        
        # Frame de lista de archivos
        self._create_file_list_frame(main_frame)
        
        # Frame de vista previa
        self._create_preview_frame(main_frame)
        
        # Barra de estado
        self.status_label = ttk.Label(
            main_frame, 
            text="Listo", 
            relief=tk.SUNKEN,
            padding=(5, 2)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    def _create_button_frame(self, parent):
        """Crea el frame con los botones en posición vertical"""
        # Frame contenedor para botones
        button_container = ttk.LabelFrame(parent, text="Acciones", padding="10")
        button_container.pack(fill=tk.X, pady=10)
        
        # Frame interno para los botones
        button_frame = ttk.Frame(button_container)
        button_frame.pack(fill=tk.X)
        
        # Botón 1: Cargar PDFs
        self.btn_load = ttk.Button(
            button_frame, 
            text="📁 Cargar PDFs",
            width=25
        )
        self.btn_load.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botón 2: Extraer con OCR
        self.btn_extract = ttk.Button(
            button_frame, 
            text="🔍 Extraer con OCR",
            width=25
        )
        self.btn_extract.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botón 3: Generar Excel
        self.btn_generate = ttk.Button(
            button_frame, 
            text="📊 Generar Excel",
            width=25
        )
        self.btn_generate.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botón 4: Debug OCR
        self.btn_debug = ttk.Button(
            button_frame, 
            text="🔧 Debug OCR",
            width=25
        )
        self.btn_debug.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botón 5: Limpiar
        self.btn_clear = ttk.Button(
            button_frame, 
            text="🗑️ Limpiar Todo",
            width=25
        )
        self.btn_clear.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
    
    def _create_file_list_frame(self, parent):
        """Crea el frame con la lista de archivos"""
        list_frame = ttk.LabelFrame(parent, text="Archivos Cargados", padding="10")
        list_frame.pack(fill=tk.X, pady=10)
        
        # Scrollbar y Listbox
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.X)
        
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL)
        self.file_listbox = tk.Listbox(
            list_container,
            yscrollcommand=scrollbar.set,
            height=6,
            font=('Arial', 9)
        )
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_preview_frame(self, parent):
        """Crea el frame con la vista previa de datos"""
        preview_frame = ttk.LabelFrame(
            parent,
            text="Vista Previa de Datos Extraídos",
            padding="10"
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para mostrar datos
        tree_container = ttk.Frame(preview_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        
        # Scrollbar horizontal
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        
        self.data_tree = ttk.Treeview(
            tree_container,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            height=12
        )
        
        v_scrollbar.config(command=self.data_tree.yview)
        h_scrollbar.config(command=self.data_tree.xview)
        
        # Configurar columnas
        self.data_tree['columns'] = ('nombres', 'transegen')
        
        self.data_tree.column('#0', width=60, minwidth=60, anchor=tk.CENTER)
        self.data_tree.column('nombres', width=400, minwidth=200)
        self.data_tree.column('transegen', width=300, minwidth=150)
        
        self.data_tree.heading('#0', text='#', anchor=tk.CENTER)
        self.data_tree.heading('nombres', text='Nombres y Apellidos')
        self.data_tree.heading('transegen', text='Nro Trans-Segen')
        
        # Grid layout para el treeview y scrollbars
        self.data_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configurar expansión
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
    
    def update_file_list(self, file_names):
        """Actualiza la lista de archivos"""
        self.file_listbox.delete(0, tk.END)
        for name in file_names:
            self.file_listbox.insert(tk.END, name)
    
    def clear_data_tree(self):
        """Limpia la vista previa"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
    
    def add_data_to_tree(self, index, nombres, nro_transegen):
        """Agrega una fila de datos"""
        self.data_tree.insert(
            '', 
            tk.END, 
            text=str(index),
            values=(nombres, nro_transegen)
        )
    
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update()
    
    def create_debug_window(self, pdf_name, text_content):
        """Crea ventana de debug con texto OCR"""
        debug_window = tk.Toplevel(self.root)
        debug_window.title(f"Debug OCR: {pdf_name}")
        debug_window.geometry("900x700")
        
        # Frame principal
        frame = ttk.Frame(debug_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(
            frame,
            text=f"Texto extraído con OCR de: {pdf_name}",
            font=('Arial', 12, 'bold')
        )
        title.pack(pady=5)
        
        # Frame con scrollbar
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=('Courier', 9)
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert('1.0', text_content)
        text_widget.config(state=tk.DISABLED)
    
    def set_button_commands(self, load_cmd, extract_cmd, generate_cmd, debug_cmd, clear_cmd):
        """Configura los comandos de los botones"""
        self.btn_load.config(command=load_cmd)
        self.btn_extract.config(command=extract_cmd)
        self.btn_generate.config(command=generate_cmd)
        self.btn_debug.config(command=debug_cmd)
        self.btn_clear.config(command=clear_cmd)
    def show_loading(self, message="Procesando..."):
        """Muestra un mensaje de carga"""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Procesando")
        self.loading_window.geometry("300x100")
        self.loading_window.transient(self.root)  # Mantener sobre la ventana principal
        self.loading_window.grab_set()  # Modal
        self.loading_window.resizable(False, False)
        
        # Centrar la ventana de carga
        self.loading_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 50
        self.loading_window.geometry(f"+{x}+{y}")
        
        # Contenido de la ventana de carga
        frame = ttk.Frame(self.loading_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        loading_label = ttk.Label(
            frame, 
            text=message,
            font=('Arial', 10)
        )
        loading_label.pack(pady=5)
        
        # Barra de progreso indeterminada
        self.progress_bar = ttk.Progressbar(
            frame, 
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)  # Iniciar animación
        
        self.loading_window.update()

    def hide_loading(self):
        """Oculta el mensaje de carga"""
        if hasattr(self, 'loading_window') and self.loading_window:
            self.progress_bar.stop()
            self.loading_window.destroy()
            self.loading_window = None