import customtkinter as ctk
from typing import Callable
from sistema.config import settings
from sistema.ui.FontManager import FontManager 
from sistema.utils.asset_loader import assets

class LoadingScreen(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk, on_close: Callable[[], None]):
        super().__init__(parent)
        self.on_close = on_close
        self.progress_value = 0
        self.geometry("500x350")
        self.overrideredirect(True)
        self.center_window()
        self._setup_ui()
        self.after(100, self._animate_step_1)

    def center_window(self):
        self.update_idletasks()
        width, height = 500, 350
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_ui(self):
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(expand=True, fill="both")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure((0, 4), weight=1)
        self.brand_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        
        # Usa o ícone do loader
        self.logo_label = ctk.CTkLabel(self.brand_container, text="", image=assets.cabana_logo_medium)
        self.title_label = ctk.CTkLabel(self.brand_container, text=settings.APP_NAME, font=FontManager.get("title_medium"))
        self.progressbar = ctk.CTkProgressBar(main_frame, mode='determinate', height=4)
        self.progressbar.set(0)
        self.status_label = ctk.CTkLabel(main_frame, text="", font=FontManager.get("small"), text_color=settings.TEXT_SUBTLE_COLOR)
        self.version_label = ctk.CTkLabel(main_frame, text=settings.APP_VERSION, font=FontManager.get("xsmall"), text_color="gray40")

    def _animate_step_1(self):
        self.brand_container.grid(row=1, column=0, pady=(10, 0), sticky="s")
        self.logo_label.pack(pady=(0, 20))
        self.after(500, self._animate_step_2)

    def _animate_step_2(self):
        self.title_label.pack()
        self.after(700, self._animate_step_3)

    def _animate_step_3(self):
        self.progressbar.grid(row=2, column=0, sticky="ew", padx=100, pady=20)
        self.status_label.grid(row=3, column=0)
        self.version_label.place(relx=0.98, rely=0.98, anchor="se")
        self.after(100, self._update_progress)

    def _update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            if self.progress_value < 30: self.status_label.configure(text="Inicializando módulos...")
            elif self.progress_value < 70: self.status_label.configure(text="Conectando ao banco de dados...")
            else: self.status_label.configure(text="Preparando interface...")
            self.progressbar.set(self.progress_value / 100)
            self.after(15, self._update_progress)
        else:
            self.status_label.configure(text="Tudo pronto!")
            self.after(500, self.on_close)