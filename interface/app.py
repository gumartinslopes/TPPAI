import customtkinter as ctk
from pages.initial_page import InitialPage
from pages.image_visualizer import ImageVisualizer
from tkinter import messagebox
from tkinter import filedialog as fd
import os

# setup do tema inicial
ctk.set_default_color_theme(
    f"{os.getcwd()}/interface/themes/flamingo.json")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._img_path = ""

        # inicializacoes do app
        self.setup_window()
        self.setup_container()
        self.setup_frames()

        # carregando página inicial
        self.show_initial_page()

    def setup_container(self):
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def setup_window(self):
        # geometria da janela
        self.width = 1200
        self.height = 600
        self.title("Trabalho de PAI")
        self.geometry(f'{self.width}x{self.height}')

        # bindings com o teclado e fullscreen
        self.bind('<F11>', self.toggle_fullscreen)
        self.fullscreen = False
        self.attributes('-fullscreen', self.fullscreen)

        self.center_window()

    def setup_frames(self):
        # inicializacao do frame inicial
        self.initial_page_frame = InitialPage(self.container, self)
        self.initial_page_frame.grid(row=0, column=0, sticky="nsew")

        # inicializacao do frame de visualizador de imagem
        self.image_visualizer_frame = ImageVisualizer(self.container, self)
        self.image_visualizer_frame.grid(row=0, column=0, sticky="nsew")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes('-fullscreen', self.fullscreen)
        self.center_window()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)

        # centralizacao da janela
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y-50))

    def set_img_path(self, path):
        self._img_path = path

    def select_file(self):
        filetypes = (('All files', '*.*'), ('text files', '*.txt'),)
        file_path = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )
        if (file_path == ""):
            messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada!")
        else:
            self.set_img_path(file_path)

    # mostrando cada página
    def show_initial_page(self):
        self.initial_page_frame.tkraise()

    def show_image_visualizer(self):
        self.image_visualizer_frame.tkraise()
        self.image_visualizer_frame.update_image(self._img_path)


app = App()
app.mainloop()
