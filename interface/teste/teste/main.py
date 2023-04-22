import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.image_path = image_path
        self.image = Image.open(image_path).convert('L')
        # keep original image for resetting contrast
        self.original_image = self.image.copy()
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.contrast_factor = 1.0
        self.scale_factor = 1.0

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
                           20, anchor=tk.NW, window=self.slider)

        self.bind("<Configure>", self.resize_image)
        self.bind("<MouseWheel>", self.on_mousewheel)
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag_image)

    def set_contrast(self, factor):
        self.contrast_factor = float(factor)
        enhanced_image = ImageEnhance.Contrast(
            self.original_image).enhance(self.contrast_factor)
        self.image = enhanced_image.convert('L')
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.itemconfig(self.find_all()[0], image=self.photo_image)

    def resize_image(self, event):
        self.scale_factor = min(
            event.width / self.image.width, event.height / self.image.height)
        new_size = (int(self.image.width * self.scale_factor),
                    int(self.image.height * self.scale_factor))
        resized_image = self.image.resize(new_size, Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.itemconfig(self.find_all()[0], image=self.photo_image)

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


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter Slider Example')
        self.geometry('600x400')

        canvas = CustomCanvas(self, 'imgs/batman.jpg')
        canvas.pack(fill=tk.BOTH, expand=True)

        self.bind("<MouseWheel>", canvas.on_mousewheel)


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
