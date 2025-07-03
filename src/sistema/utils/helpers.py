import sys
import os

def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso. Funciona em dev e no PyInstaller.
    Sempre espere um caminho relativo que comece com 'assets/'.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".") # Aponta para a pasta raiz (SISTEMA)

    return os.path.join(base_path, relative_path)