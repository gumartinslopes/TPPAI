import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk


class ImageCanvas(tk.Canvas):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.image_path = image_path
        self.image = Image.open(image_path).convert('L')

        self.original_image = self.image.copy()
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        # setup do fator de contraste e escala
        self.contrast_factor = 1.0
        self.scale_factor = 1.0

        self.config(background="#000000", highlightthickness=0, relief='ridge')
        self.setup_bindings()

    # Setup dos comandos do teclado
    def setup_bindings(self):
        self.bind("<Configure>", self.handle_resize_event)
        self.bind("<MouseWheel>", self.on_mousewheel)
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag_image)

    def set_contrast(self, factor_1, factor_2):

        # Converte a ImageTk.PhotoImage para uma imagem do Pillow
        pil_img = self.original_image.copy()

        # Determina os valores mínimos e máximos da janela
        min_pixel = float(factor_1)
        max_pixel = float(factor_2)

        # Aplica o contraste por janelamento
        scale = 255 / (max_pixel - min_pixel)

        # Apply the scaling factor and shift the image
        new_img = pil_img.point(lambda x: (x - min_pixel) * scale)

        self.image = new_img.convert('L')

        # Converte a imagem do Pillow de volta para ImageTk.PhotoImage
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.itemconfig(self.find_all()[0], image=self.photo_image)
        self.resize_image(self.winfo_width(), self.winfo_height())

    def resize_image(self, w, h):
        self.scale_factor = min(
            w / self.image.width, h / self.image.height)
        new_size = (int(self.image.width * self.scale_factor),
                    int(self.image.height * self.scale_factor))
        resized_image = self.image.resize(new_size, Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.itemconfig(self.find_all()[0], image=self.photo_image)

    def handle_resize_event(self, event):
        self.resize_image(event.width, event.height)

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.scale_factor = min(self.scale_factor + 0.1, 2.0)
        else:
            self.scale_factor = max(self.scale_factor - 0.1, 0.1)

        new_size = (int(self.image.width * self.scale_factor),
                    int(self.image.height * self.scale_factor))
        resized_image = self.image.resize(new_size, Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.itemconfig(self.find_all()[0], image=self.photo_image)

    def start_drag(self, event):
        self.scan_mark(event.x, event.y)
        self.previous_x = event.x
        self.previous_y = event.y

    def drag_image(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def reset_contrast(self):
        self.image = self.original_image.copy()
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.itemconfig(self.find_all()[0], image=self.photo_image)
        self.contrast_factor = 1.0
        self.slider.set(1.0)
