import customtkinter as ctk
from typing import Callable
from sistema.config import settings
from sistema.ui.FontManager import FontManager
from sistema.core.service import AuthService
from sistema.utils.asset_loader import assets

class RegisterScreen(ctk.CTkFrame):
    """Tela de registro de novos usuários."""
    
    def __init__(self, master: ctk.CTk, *, on_show_login: Callable[[], None]):
        super().__init__(master, fg_color="transparent")
        
        self.on_show_login = on_show_login
        
        # Instancia o serviço para uso no evento de registro.
        self.auth_service = AuthService()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_left_panel()
        self._setup_right_panel()

    def _setup_left_panel(self):
        left_frame = ctk.CTkFrame(self, fg_color=settings.BRANDING_BG_COLOR, corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(2, weight=1) # Empurra o conteúdo para cima

        header_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        ctk.CTkLabel(header_frame, text="", image=assets.cabana_logo_small).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header_frame, text=settings.APP_NAME, font=FontManager.get("normal_bold")).pack(side="left")

        plans_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        plans_container.grid(row=1, column=0, padx=40, pady=(40, 20), sticky="n")
        ctk.CTkLabel(plans_container, text="Escolha o plano ideal para você:", font=FontManager.get("subtitle"), anchor="w").pack(fill="x", pady=(0, 20), anchor="w")
        cards_grid_frame = ctk.CTkFrame(plans_container, fg_color="transparent")
        cards_grid_frame.pack(fill="x")
        cards_grid_frame.grid_columnconfigure((0, 1), weight=1)

        self.subscription_var = ctk.StringVar(value="ambos")
        self.subscription_var.trace_add("write", self._update_cards_visual_state)
        
        self.loja_card = self._create_plan_card(cards_grid_frame, assets.store_module_icon, "Apenas Loja", "Gerencie produtos, estoque e vendas.", "loja")
        self.loja_card.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")
        self.escola_card = self._create_plan_card(cards_grid_frame, assets.school_module_icon, "Apenas Escola", "Controle alunos, turmas e mensalidades.", "escola")
        self.escola_card.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")
        self.ambos_card = self._create_plan_card(cards_grid_frame, assets.complete_module_icon, "Completo (Loja e Escola)", "A solução definitiva com todos os recursos integrados.", "ambos")
        self.ambos_card.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")
        self._update_cards_visual_state()

    def _create_plan_card(self, parent, icon, title, description, value):
        card = ctk.CTkFrame(parent, border_width=2, corner_radius=15)
        card.grid_columnconfigure(0, weight=1)
        
        select_command = lambda v=value: self.subscription_var.set(v)
        card.bind("<Button-1>", lambda e: select_command())
        
        icon_label = ctk.CTkLabel(card, text="", image=icon, fg_color="transparent")
        icon_label.grid(row=0, column=0, pady=(20, 10)); icon_label.bind("<Button-1>", lambda e: select_command())
        title_label = ctk.CTkLabel(card, text=title, font=FontManager.get("normal_bold"), fg_color="transparent")
        title_label.grid(row=1, column=0); title_label.bind("<Button-1>", lambda e: select_command())
        desc_label = ctk.CTkLabel(card, text=description, wraplength=180, justify="center", font=FontManager.get("small"), fg_color="transparent")
        desc_label.grid(row=2, column=0, padx=10, pady=(5, 15)); desc_label.bind("<Button-1>", lambda e: select_command())

        return card

    def _update_cards_visual_state(self, *args):
        selected_value = self.subscription_var.get()
        self.loja_card.configure(border_color=settings.LINK_COLOR if selected_value == 'loja' else "gray25")
        self.escola_card.configure(border_color=settings.LINK_COLOR if selected_value == 'escola' else "gray25")
        self.ambos_card.configure(border_color=settings.LINK_COLOR if selected_value == 'ambos' else "gray25")

    def _setup_right_panel(self):
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        
        ctk.CTkFrame(right_frame, fg_color="transparent", height=72).grid(row=0, column=0, sticky="ew")

        form_container = ctk.CTkFrame(right_frame, fg_color="transparent", width=350)
        form_container.grid(row=1, column=0, pady=(40, 20), sticky="n")
        
        ctk.CTkLabel(form_container, text="Crie sua Conta", font=FontManager.get("title_medium")).pack(pady=(0, 30))
        self.full_name_entry = ctk.CTkEntry(form_container, placeholder_text="Nome Completo", height=40)
        self.full_name_entry.pack(fill="x", pady=5)
        self.email_entry = ctk.CTkEntry(form_container, placeholder_text="Seu melhor e-mail", height=40)
        self.email_entry.pack(fill="x", pady=5)
        self.password_entry = ctk.CTkEntry(form_container, placeholder_text="Crie uma Senha", show="*", height=40)
        self.password_entry.pack(fill="x", pady=5)
        self.confirm_password_entry = ctk.CTkEntry(form_container, placeholder_text="Confirme sua Senha", show="*", height=40)
        self.confirm_password_entry.pack(fill="x", pady=5)
        self.error_label = ctk.CTkLabel(form_container, text="", text_color="red")
        self.error_label.pack(pady=10)
        ctk.CTkButton(form_container, text="Registrar Conta", height=40, font=FontManager.get("normal_bold"), command=self.register_event).pack(fill="x", pady=10)
        
        login_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        login_frame.pack(fill="x", pady=20)
        ctk.CTkLabel(login_frame, text="Já possui uma conta?", font=FontManager.get("normal")).pack()
        ctk.CTkButton(login_frame, text="Acesse aqui", fg_color="transparent", text_color=settings.LINK_COLOR, command=self.on_show_login).pack()

    def register_event(self):
        """Coleta, valida e tenta registrar o novo usuário."""
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        subscription_type = self.subscription_var.get()

        if not all([full_name, email, password, confirm_password]):
            self.error_label.configure(text="Todos os campos são obrigatórios.")
            return
        if password != confirm_password:
            self.error_label.configure(text="As senhas não coincidem.")
            return

        self.error_label.configure(text="")
        
        # Usa o serviço para tentar registrar o usuário.
        user = self.auth_service.register(full_name, email, password, subscription_type)
        
        if user:
            # Em caso de sucesso, mostra uma mensagem e navega para o login.
            print(f"Usuário {user.email} registrado com sucesso!")
            self.on_show_login()
        else:
            self.error_label.configure(text="Este e-mail já está em uso.")