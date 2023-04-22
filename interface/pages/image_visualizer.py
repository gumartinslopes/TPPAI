import customtkinter as ctk
import tkinter as tk

from tkinter import messagebox
from tkinter import filedialog as fd
from . utils.image_canvas import ImageCanvas

class ImageVisualizer(ctk.CTkFrame):
    def __init__(self, parent, controller):   
        ctk.CTkFrame.__init__(self,parent)

        # configurações do grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0), weight=1)

        # inicialização do label de imagem
        self.img_label = ctk.CTkLabel(self, text="")
        self.img_label.grid(row = 0, column = 1)
        
        self.img_path = controller._img_path
        self.setup_canvas()

        self.setup_sidebar()
    
    def update_image(self, path):
        self.img_path = path
        self.setup_canvas()
    
    # configurações iniciais da sidebar
    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Configurações", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, command=self.new_image, text="Selecionar uma nova Imagem")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
    
    def new_image(self):    
        filetypes = (('All files', '*.*'),('text files', '*.txt'),)
        file_path = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )
        if(file_path == ""):
            messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada!")
        else:   
            self.img_path = file_path     
            #substituição do canvas anterior
            self.img_canvas.destroy()
            self.setup_canvas()
    
    #altera o contraste da imagem
    def set_contrast(self, factor):
        self.windowing_label.configure(text = 'Escala de Tons de Cinza {0:.2f}'.format(factor))
        self.img_canvas.set_contrast(factor=factor)

    # criação de um novo canvas
    def setup_canvas(self):
       if(self.img_path != ""):
        # self.img_canvas = CanvasImage(self, self.img_path)
        # self.img_canvas.grid(row=0, column=1, pady = 10, padx = 10)
        self.img_canvas = ImageCanvas(self, self.img_path)
        self.img_canvas.grid(row=0, column=1, pady = 10, padx = 10)
        self.img_canvas.grid(sticky='nswe')  

        self.windowing_label = ctk.CTkLabel(self, text=f'Escala de Tons de Cinza: {0}')
        self.windowing_label.grid(row = 1, column = 1, pady = 10, padx = 10)
        self.windowing_slider = ctk.CTkSlider(master=self, from_=0.1, to=2.0, command=self.set_contrast)
        self.windowing_slider.grid(row = 2, column =1, pady = 10, padx = 10)