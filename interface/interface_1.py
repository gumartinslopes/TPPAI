import customtkinter
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image
from canvas_image import CanvasImage

from tkinter.messagebox import showinfo
customtkinter.set_appearance_mode("System") 
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()       
        self.width = 1200
        self.height = 600
        self.title("Trabalho de PAI")
        self.geometry(f'{self.width}x{self.height}')

        self.bind('<F11>', self.toggle_fullscreen)        
        self.fullscreen = False
        self.attributes('-fullscreen', self.fullscreen)
        self.center_window()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # inicialização do label de imagem
        self.img_label = customtkinter.CTkLabel(self, text="")
        self.img_label.grid(row = 0, column = 1)

        image_path = "C:/Users/gumar/faculdade/Estudos/EstudosPython/customTkinter/image_zoom/batman.jpg"
        self.img_canvas = CanvasImage(self, image_path)
        self.img_canvas.grid(row=0, column=1, pady = 10, padx = 10)  # show widge

        self.configure_sidebar()

    #Criação da sidebar e todos os seus frames
    def configure_sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Configurações", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.load_img_file, text="Selecionar Imagem")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes('-fullscreen', self.fullscreen)
        self.center_window()
        
    def center_window(self):
        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y-50))
    
    def load_img_file(self):
        filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt'),
        )

        file_path = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        self.open_img(file_path)

    
    def open_img(self, file_path):
        self.img_canvas.update_img(file_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()