import customtkinter as ctk
import os
from PIL import Image
from config import settings
from config.settings import FontManager

class BrandingFrame(ctk.CTkFrame):
    """Um painel lateral reutilizável para exibir a marca da aplicação."""
    def __init__(self, master):
        super().__init__(master, fg_color=settings.BRANDING_BG_COLOR, corner_radius=0)

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 2), weight=1)
        
        # Ancora a imagem para evitar que seja coletada pelo garbage collector
        self.logo_image = ctk.CTkImage(
            Image.open(os.path.join(settings.ASSETS_PATH, "cabana_icon.png")),
            size=(128, 128)
        )
        
        logo_label = ctk.CTkLabel(self, text="", image=self.logo_image)
        logo_label.grid(row=0, column=0, sticky="s", pady=(0, 20))
        
        brand_title = ctk.CTkLabel(self, text=settings.APP_NAME, font=FontManager.get("normal_bold"))
        brand_title.grid(row=1, column=0, sticky="n")