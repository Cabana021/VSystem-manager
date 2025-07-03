import customtkinter as ctk
from typing import Callable
from sistema.config import settings
from sistema.ui.FontManager import FontManager
from sistema.core.service import AuthService     
from sistema.utils.asset_loader import assets
from sistema.core.models import User             

class LoginScreen(ctk.CTkFrame):
    """Tela de login centralizada para autenticação do usuário."""

    def __init__(self, master: ctk.CTk, *, on_login_success: Callable[[User], None], on_show_register: Callable[[], None]):
        """
        Args:
            master: A janela principal (App).
            on_login_success: Callback a ser chamado com o objeto User em caso de sucesso.
            on_show_register: Callback para navegar para a tela de registro.
        """
        super().__init__(master, fg_color="transparent")
        
        self.on_login_success = on_login_success
        self.on_show_register = on_show_register

        # Instancia o serviço de autenticação. A tela não usa mais métodos estáticos.
        self.auth_service = AuthService()

        self._setup_layout()
        self._create_widgets()

    def _setup_layout(self):
        """Configura o grid para centralizar todo o conteúdo."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _create_widgets(self):
        """Cria e posiciona todos os elementos visuais da tela."""
        main_container = ctk.CTkFrame(self, fg_color="transparent", width=350)
        main_container.grid(row=0, column=0)

        ctk.CTkLabel(main_container, text="", image=assets.cabana_logo_large).pack(pady=(0, 10))
        ctk.CTkLabel(main_container, text=settings.APP_NAME, font=FontManager.get("normal_bold")).pack(pady=(0, 40))
        ctk.CTkLabel(main_container, text="Acesse sua Conta", font=FontManager.get("title_medium")).pack(pady=(0, 20))
        
        self.email_entry = ctk.CTkEntry(main_container, placeholder_text="E-mail", height=40, font=FontManager.get("normal"))
        self.email_entry.pack(pady=5, fill="x")
        
        self.password_entry = ctk.CTkEntry(main_container, placeholder_text="Senha", show="*", height=40, font=FontManager.get("normal"))
        self.password_entry.pack(pady=5, fill="x")
        
        self.error_label = ctk.CTkLabel(main_container, text="", text_color="red")
        self.error_label.pack(pady=10)
        
        login_button = ctk.CTkButton(main_container, text="Entrar", height=40, font=FontManager.get("normal_bold"), command=self.login_event)
        login_button.pack(pady=10, fill="x")
        
        register_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        register_frame.pack(pady=20, fill="x")
        
        ctk.CTkLabel(register_frame, text="Ainda não possui uma conta?", font=FontManager.get("normal")).pack()
        ctk.CTkButton(register_frame, text="Crie sua conta gratuitamente", fg_color="transparent", text_color=settings.LINK_COLOR, command=self.on_show_register).pack()

    def login_event(self):
        """Coleta os dados, valida e tenta autenticar o usuário usando o AuthService."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            self.error_label.configure(text="Por favor, preencha todos os campos.")
            return

        user = self.auth_service.login(email, password)
        
        if user:
            # Chama o callback passando o objeto User inteiro.
            self.on_login_success(user)
        else:
            self.error_label.configure(text="E-mail ou senha inválidos.")