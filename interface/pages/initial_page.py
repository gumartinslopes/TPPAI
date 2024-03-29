import customtkinter as ctk
# Página inicial da aplicação
class InitialPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self,parent)
        label = ctk.CTkLabel(self, text="Select Image")
        label.pack(pady=10,padx=10)

        button = ctk.CTkButton(self, text="Selecionar Imagem",
                            command = self.switch_tabs)

        button.pack()
    
    # traca de página após selecionar uma imagem
    def switch_tabs(self):
        self.controller.select_file()
        self.controller.show_image_visualizer()
