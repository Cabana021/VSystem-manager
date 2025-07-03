import customtkinter as ctk
from PIL import Image
from sistema.utils.helpers import resource_path

class AssetLoader:
    def __init__(self):
        
        # --- Logo ---
        self.cabana_logo_large = self._load_image(resource_path("assets/icons/logo/cabana_icon.png"), size=(128, 128))
        self.cabana_logo_medium = self._load_image(resource_path("assets/icons/logo/cabana_icon.png"), size=(80, 80))
        self.cabana_logo_small = self._load_image(resource_path("assets/icons/logo/cabana_icon.png"), size=(32, 32))

        # --- Ícones Gerais ---
        self.user_icon = self._load_image(resource_path("assets/icons/geral/user_icon.png"), size=(20, 20))
        self.lock_icon = self._load_image(resource_path("assets/icons/geral/lock_icon.png"))
        self.eye_opened_icon = self._load_image(resource_path("assets/icons/geral/eye_opened.png"))
        self.eye_closed_icon = self._load_image(resource_path("assets/icons/geral/eye_closed.png"))
        self.back_arrow_icon = self._load_image(resource_path("assets/icons/geral/back_arrow_icon.png"), size=(20, 20))
        self.logout_icon = self._load_image(resource_path("assets/icons/geral/logout_icon.png"), size=(20, 20))
        self.edit_icon_geral = self._load_image(resource_path("assets/icons/geral/edit_icon.png"), size=(20, 20))
        self.delete_icon_geral = self._load_image(resource_path("assets/icons/geral/delete_icon.png"), size=(20, 20))
        self.info_icon = self._load_image(resource_path("assets/icons/geral/info_icon.png"), size=(20, 20))
        
        # --- Ícones de Módulos ---
        self.store_module_icon = self._load_image(resource_path("assets/icons/módulos/store_icon.png"), size=(96, 96))
        self.school_module_icon = self._load_image(resource_path("assets/icons/módulos/school_icon.png"), size=(96, 96))
        self.complete_module_icon = self._load_image(resource_path("assets/icons/módulos/complete_icon.png"), size=(64, 64))

        # --- Ícones da Loja ---
        self.edit_icon_loja = self._load_image(resource_path("assets/icons/loja/edit_icon.png"))
        self.delete_icon_loja = self._load_image(resource_path("assets/icons/loja/delete_icon.png"))
        self.sell_icon = self._load_image(resource_path("assets/icons/loja/sell_icon.png"))

    def _load_image(self, path, size=(24, 24)):
        try:
            return ctk.CTkImage(Image.open(path), size=size)
        except FileNotFoundError:
            print(f"AVISO: Asset não encontrado em: {path}")
            return None

assets = AssetLoader()