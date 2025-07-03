import sqlite3
import contextlib
from sistema.config import settings  

@contextlib.contextmanager
def get_db_connection(commit: bool = False):
    """
    Gerenciador de contexto para conexões de banco de dados.
    Usa o caminho do banco definido em settings.py.
    """
    conn = None  # Inicializa conn para garantir que exista no bloco finally
    try:
        conn = sqlite3.connect(settings.DB_FILE, timeout=10)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        yield conn
        if commit:
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        if conn:
            conn.rollback()
        raise  # Re-lança a exceção para que a camada superior saiba do erro
    finally:
        if conn:
            conn.close()

def initialize_core_database():
    """
    Cria a tabela de usuários, que é essencial para o núcleo do sistema.
    """
    with get_db_connection(commit=True) as conn:
        cursor = conn.cursor()
        # Usuários
        # Apenas a tabela 'usuarios' é criada aqui.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                subscription_type TEXT NOT NULL CHECK(subscription_type IN ('loja', 'escola', 'ambos'))
            );
        """)
    print("Tabela de usuários (core) verificada/criada com sucesso.")