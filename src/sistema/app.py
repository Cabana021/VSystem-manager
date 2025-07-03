import customtkinter as ctk
from typing import Optional
from sistema.config import settings
from sistema.ui.FontManager import FontManager
from sistema.core.database import initialize_core_database
from sistema.features.loja.database import initialize_loja_database
from sistema.features.escola.database import initialize_escola_database
from sistema.core.models import User
from sistema.ui.loading_screen import LoadingScreen
from sistema.ui.login_screen import LoginScreen
from sistema.ui.register_screen import RegisterScreen
from sistema.ui.main_screen import MainScreen
from sistema.ui.profile_screen import ProfileScreen
from sistema.features.loja.views.loja_screen import LojaDashboard
from sistema.features.escola.views.escola_screen import EscolaDashboard

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._initialize_services()
        self.title(settings.APP_NAME)
        self.geometry("1280x720")
        self.current_user: Optional[User] = None
        self.withdraw()
        LoadingScreen(self, on_close=self.show_login_screen)
    
    def _initialize_services(self):
        print("Inicializando aplicação...")
        FontManager.initialize()
        initialize_core_database()
        initialize_loja_database()
        initialize_escola_database()
        print("Inicialização completa.")

    def _clear_main_frame(self):
        for widget in self.winfo_children(): widget.destroy()

    def show_login_screen(self, logout: bool = False):
        self._clear_main_frame()
        if logout: self.current_user = None
        self.deiconify(); self.state('zoomed')
        login_frame = LoginScreen(master=self, on_login_success=self.show_main_app, on_show_register=self.show_register_screen)
        login_frame.pack(expand=True, fill="both")

    def show_register_screen(self):
        self._clear_main_frame()
        register_frame = RegisterScreen(master=self, on_show_login=self.show_login_screen)
        register_frame.pack(expand=True, fill="both")
    
    def show_main_app(self, user: User):
        self.current_user = user
        self.show_main_screen()

    def show_main_screen(self):
        self._clear_main_frame()
        if not self.current_user: self.show_login_screen(); return
        main_frame = MainScreen(master=self, user_full_name=self.current_user.full_name, subscription_type=self.current_user.subscription_type, logout_callback=lambda: self.show_login_screen(logout=True), show_loja_callback=self.show_loja_screen, show_profile_callback=self.show_profile_screen, show_escola_callback=self.show_escola_screen)
        main_frame.pack(expand=True, fill="both")

    def show_profile_screen(self):
        self._clear_main_frame()
        profile_frame = ProfileScreen(master=self, current_user=self.current_user, on_back=self.show_main_screen, on_delete_account=lambda: self.show_login_screen(logout=True))
        profile_frame.pack(expand=True, fill="both")
    
    def show_loja_screen(self):
        self._clear_main_frame()
        loja_frame = LojaDashboard(master=self, current_user=self.current_user, show_home_callback=self.show_main_screen)
        loja_frame.pack(expand=True, fill="both")

    def show_escola_screen(self):
        self._clear_main_frame()
        escola_frame = EscolaDashboard(master=self, current_user=self.current_user, show_home_callback=self.show_main_screen)
        escola_frame.pack(expand=True, fill="both")

def run_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()