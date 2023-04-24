import customtkinter as ctk
import tkinter as tk

from tkinter import messagebox
from tkinter import filedialog as fd
from . utils.image_canvas import ImageCanvas


class ImageVisualizer(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # configurações do grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0), weight=1)

        # inicialização do label de imagem
        self.img_label = ctk.CTkLabel(self, text="")
        self.img_label.grid(row=0, column=1)

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
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Configurações", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.sidebar_button_1 = ctk.CTkButton(
            self.sidebar_frame, command=self.new_image, text="Selecionar uma nova Imagem")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

    def new_image(self):
        filetypes = (('All files', '*.*'), ('text files', '*.txt'),)
        file_path = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )
        if (file_path == ""):
            messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada!")
        else:
            self.img_path = file_path
            # substituição do canvas anterior
            self.img_canvas.destroy()
            self.setup_canvas()

    # altera o contraste da imagem
    def set_contrast(self, factor_1=None, factor_2=None):
        if factor_1 is None:
            if (factor_2 > self.windowing_slider_2.get()):
                self.windowing_label_1.configure(
                    text='Limite Superior: {0:.0f}'.format(factor_2))
                self.img_canvas.set_contrast(
                    factor_1=self.windowing_slider_2.get(), factor_2=factor_2)
        if factor_2 is None:
            if (factor_1 < self.windowing_slider_1.get()):
                self.windowing_label_2.configure(
                    text='Limite Inferior: {0:.0f}'.format(factor_1))
                self.img_canvas.set_contrast(
                    factor_1=factor_1, factor_2=self.windowing_slider_1.get())

    # criação de um novo canvas
    def setup_canvas(self):
        if (self.img_path != ""):
            # self.img_canvas = CanvasImage(self, self.img_path)
            # self.img_canvas.grid(row=0, column=1, pady = 10, padx = 10)
            self.img_canvas = ImageCanvas(self, self.img_path)
            self.img_canvas.grid(row=0, column=1, pady=10, padx=10)
            self.img_canvas.grid(sticky='nswe')

            self.windowing_label_3 = ctk.CTkLabel(
                self, text=f'Contraste por Janelamento',
                width=120,
                height=25,
                fg_color=("white", "gray75"),
                text_color="black",
                corner_radius=8)
            self.windowing_label_3.grid(row=1, column=1, pady=10, padx=10)

            s1 = ctk.CTkSlider(master=self)
            s2 = ctk.CTkSlider(master=self)

            s1.configure(
                from_=0, to=255, hover=True, command=lambda e: self.set_contrast(factor_2=s1.get()))
            s1.grid(row=3, column=1, pady=10, padx=10)
            s1.set(255)

            s2.configure(
                from_=0, to=255, hover=True, command=lambda e: self.set_contrast(factor_1=s2.get()))
            s2.grid(row=5, column=1, pady=10, padx=10)
            s2.set(0)

            self.windowing_slider_1 = s1
            self.windowing_slider_2 = s2

            self.windowing_label_1 = ctk.CTkLabel(
                self, text='Limite Superior: {0:.0f}'.format(s1.get()))
            self.windowing_label_1.grid(row=2, column=1, pady=10, padx=10)

            self.windowing_label_2 = ctk.CTkLabel(
                self, text='Limite Inferior: {0:.0f}'.format(s2.get()))
            self.windowing_label_2.grid(row=4, column=1, pady=10, padx=10)
