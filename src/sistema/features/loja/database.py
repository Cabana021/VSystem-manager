from sistema.core.database import get_db_connection

def initialize_loja_database():
    with get_db_connection(commit=True) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materia_prima (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                unidade_medida TEXT,
                estoque_atual REAL NOT NULL,
                UNIQUE(user_id, nome),
                FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL DEFAULT 0,
                UNIQUE(user_id, nome),
                FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                produto_id INTEGER,
                quantidade INTEGER NOT NULL,
                preco_unitario_na_venda REAL NOT NULL,
                preco_total REAL NOT NULL,
                data_venda TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
                FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE SET NULL
            );
        """)
    print("Tabelas da Loja (multi-usuário) verificadas/criadas.")