import os
from pathlib import Path

# 1. Obtém a pasta APPDATA. 
app_data_path_str = os.getenv('APPDATA')
if not app_data_path_str:
    # Fallback para o diretório 'home' se APPDATA não for encontrado
    app_data_path_str = os.path.expanduser('~')

# 2. Constrói o caminho para a pasta específica da nossa aplicação usando pathlib
app_dir = Path(app_data_path_str) / "VSystem"

# 3. Garante que o diretório da nossa aplicação exista
app_dir.mkdir(parents=True, exist_ok=True)

# 4. Define a variável DB_FILE com o caminho completo e seguro.
#    O resto do sistema usará esta variável para encontrar o banco de dados.
DB_NAME = 'sistema.db' 
DB_FILE = app_dir / DB_NAME

# --- CONFIGURAÇÕES GERAIS DO APP ---
APP_NAME = "VSystem" 
APP_VERSION = "1.0.0"

# --- CORES ---
LINK_COLOR = ("blue", "cyan")
TEXT_SUBTLE_COLOR = "gray70"
BRANDING_BG_COLOR = ("gray90", "gray12")
CARD_BG_COLOR = "gray14"
CARD_BORDER_COLOR = "gray25"

# --- FONTES ---
FONT_FAMILY = "Roboto"