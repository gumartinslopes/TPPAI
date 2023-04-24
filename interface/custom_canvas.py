import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.contrast_factor = 1.0

        self.slider = tk.Scale(
            self,
            from_=0.1,
            to=2.0,
            orient=tk.HORIZONTAL,
            resolution=0.1,
            length=200,
            command=self.set_contrast
        )
        self.slider.set(1.0)
        self.create_window(self.image.width // 2, self.image.height +
                           20, anchor=tk.CENTER, window=self.slider)

    def set_contrast(self, factor_1, factor_2):
        # Converte a ImageTk.PhotoImage para uma imagem do Pillow

        pil_img = self.image.copy()

        # Determina os valores mínimos e máximos da janela
        min_pixel = float(factor_1)
        max_pixel = float(factor_2)

        # Aplica o contraste por janelamento
        scale = 255 / (max_pixel - min_pixel)

        # Apply the scaling factor and shift the image
        new_img = pil_img.point(lambda x: (x - min_pixel) * scale)

        # Converte a imagem do Pillow de volta para ImageTk.PhotoImage
        self.photo_image = ImageTk.PhotoImage(new_img)
        self.itemconfig(self.find_all()[0], image=self.photo_image)
