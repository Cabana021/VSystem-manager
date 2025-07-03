import customtkinter as ctk
from typing import Callable
from sistema.config import settings
from sistema.ui.FontManager import FontManager
from sistema.utils.asset_loader import assets

class MainScreen(ctk.CTkFrame):
    """
    Tela principal de seleção de módulos, redesenhada para melhor UI.
    """
    def __init__(self, master: ctk.CTk, *, user_full_name: str, subscription_type: str, 
                 logout_callback: Callable, show_loja_callback: Callable, 
                 show_profile_callback: Callable, show_escola_callback: Callable):
        super().__init__(master, fg_color="transparent")
        
        self.logout_callback = logout_callback
        self.show_loja_callback = show_loja_callback
        self.show_profile_callback = show_profile_callback
        self.show_escola_callback = show_escola_callback

        self._setup_layout()
        self._create_widgets(user_full_name, subscription_type)

    def _setup_layout(self):
        """Configura o grid para ter 2 linhas: Cabeçalho e Conteúdo."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _create_widgets(self, user_full_name: str, subscription_type: str):
        """Cria e posiciona todos os elementos visuais da tela de forma organizada."""
        
        # --- 1. CABEÇALHO COM LOGO E BOTÕES DE AÇÃO ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header_frame.grid(row=0, column=0, padx=40, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1) # Faz o espaço do meio expandir

        # Logo da aplicação
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(logo_frame, text="", image=assets.cabana_logo_small).pack(side="left")
        ctk.CTkLabel(logo_frame, text=settings.APP_NAME, font=FontManager.get("subtitle")).pack(side="left", padx=10)

        # Botões de ação do usuário
        user_actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_actions_frame.grid(row=0, column=2, sticky="e")
        
        profile_button = ctk.CTkButton(user_actions_frame, text="Meu Perfil", image=assets.user_icon, command=self.show_profile_callback, width=120)
        profile_button.pack(side="left", padx=(0, 10))
        
        logout_button = ctk.CTkButton(user_actions_frame, text="Sair", image=assets.logout_icon, command=self.logout_callback, width=120)
        logout_button.pack(side="left")

        # --- 2. CONTEÚDO CENTRAL ---
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 40)) # Adiciona um respiro na parte de baixo
        content_frame.grid_rowconfigure((0, 3), weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Saudação e subtítulo
        greeting_label = ctk.CTkLabel(content_frame, text=f"Bem-vindo(a), {user_full_name}!", font=FontManager.get("title_large"))
        greeting_label.grid(row=0, column=0, sticky="s", pady=(0, 10))

        subtitle_label = ctk.CTkLabel(content_frame, text="Selecione um dos seus módulos para começar a gerenciar.", 
                                      font=FontManager.get("subtitle"), text_color=settings.TEXT_SUBTLE_COLOR)
        subtitle_label.grid(row=1, column=0, sticky="n", pady=(0, 50)) # Aumenta o espaçamento

        # Frame para os cards de módulo
        cards_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        cards_frame.grid(row=2, column=0, sticky="n")

        # Lógica de Exibição dos Cards
        if subscription_type in ['loja', 'ambos']:
            loja_card = self._create_module_card(cards_frame, assets.store_module_icon, "Gestão da Loja", "Controle de produtos,\nestoque e vendas.", self.show_loja_callback)
            loja_card.pack(side="left", padx=25, pady=20) # Aumenta o espaçamento entre os cards

        if subscription_type in ['escola', 'ambos']:
            escola_card = self._create_module_card(cards_frame, assets.school_module_icon, "Gestão da Escola", "Gerencie alunos, turmas\ne mensalidades.", self.show_escola_callback)
            escola_card.pack(side="left", padx=25, pady=20)

    def _create_module_card(self, parent, icon, title, description, command):
        """Função auxiliar para criar um card de módulo interativo e padronizado."""
        card = ctk.CTkFrame(parent, width=320, height=350, fg_color=settings.CARD_BG_COLOR, border_color=settings.CARD_BORDER_COLOR, border_width=1, corner_radius=15)
        card.pack_propagate(False)
        card.grid_rowconfigure(2, weight=1)
        card.grid_columnconfigure(0, weight=1)
        
        # EFEITO HOVER (passar o mouse por cima) 
        card.bind("<Enter>", lambda e: card.configure(border_color=settings.LINK_COLOR, border_width=2))
        card.bind("<Leave>", lambda e: card.configure(border_color=settings.CARD_BORDER_COLOR, border_width=1))
        card.bind("<Button-1>", lambda e: command()) # Torna o card inteiro clicável
        
        # Widgets internos também acionam o comando ao serem clicados 
        icon_label = ctk.CTkLabel(card, text="", image=icon, fg_color="transparent")
        icon_label.grid(row=0, column=0, pady=(50, 20)); icon_label.bind("<Button-1>", lambda e: command())
        
        title_label = ctk.CTkLabel(card, text=title, font=FontManager.get("normal_bold"), fg_color="transparent")
        title_label.grid(row=1, column=0); title_label.bind("<Button-1>", lambda e: command())
        
        desc_label = ctk.CTkLabel(card, text=description, justify="center", wraplength=250, font=FontManager.get("small"), fg_color="transparent")
        desc_label.grid(row=2, column=0, sticky="n", pady=15, padx=10); desc_label.bind("<Button-1>", lambda e: command())
        
        access_button = ctk.CTkButton(card, text="Acessar", height=40, command=command)
        access_button.grid(row=3, column=0, pady=(20, 30), padx=30, sticky="ew")
        
        return card