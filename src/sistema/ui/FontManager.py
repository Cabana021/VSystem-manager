import customtkinter as ctk
from typing import Dict, Optional
from sistema.config import settings 

class FontManager:
    """Gerencia a criação e o acesso a fontes da aplicação."""
    _fonts: Dict[str, ctk.CTkFont] = {}

    @classmethod
    def initialize(cls):
        """
        Cria todas as fontes necessárias para a aplicação.
        Esta função deve ser chamada uma vez no início da aplicação.
        """
        if cls._fonts: # Evita inicializar mais de uma vez
            return

        font_family = settings.FONT_FAMILY
        
        cls._fonts["title_large"] = ctk.CTkFont(family=font_family, size=48, weight="bold")
        cls._fonts["title_medium"] = ctk.CTkFont(family=font_family, size=32, weight="bold")
        cls._fonts["subtitle"] = ctk.CTkFont(family=font_family, size=18)
        cls._fonts["normal_bold"] = ctk.CTkFont(family=font_family, size=20, weight="bold")
        cls._fonts["normal"] = ctk.CTkFont(family=font_family, size=14)
        cls._fonts["small"] = ctk.CTkFont(family=font_family, size=12)
        cls._fonts["xsmall"] = ctk.CTkFont(family=font_family, size=10)
        
        print("FontManager inicializado com sucesso.")

    @classmethod
    def get(cls, name: str) -> Optional[ctk.CTkFont]:
        """Busca uma fonte pré-criada, garantindo que foi inicializada."""
        if not cls._fonts:
            print("AVISO: FontManager.get() chamado antes de initialize().")
            cls.initialize()
            
        font = cls._fonts.get(name)
        if not font:
            print(f"AVISO: Fonte '{name}' não encontrada.")
            # Retorna uma fonte padrão para evitar que a UI quebre
            return cls._fonts.get("normal") 
            
        return font