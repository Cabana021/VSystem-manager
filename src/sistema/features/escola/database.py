from sistema.core.database import get_db_connection

def initialize_escola_database():
    """Cria as tabelas da Escola: alunos, aulas e matriculas."""
    with get_db_connection(commit=True) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nome_completo TEXT NOT NULL,
                contato TEXT,
                vencimento_mensalidade TEXT,
                cronograma_aulas TEXT,
                aulas_concluidas INTEGER DEFAULT 0,
                aproveitamento REAL DEFAULT 0.0,
                data_matricula TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
                UNIQUE(user_id, nome_completo),
                FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
            );
        """)

        # TABELA 'aulas' 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aulas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nome_curso TEXT NOT NULL,
                descricao TEXT,
                professor TEXT,
                UNIQUE(user_id, nome_curso),
                FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
            );
        """)

        # TABELA 'matriculas'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                aluno_id INTEGER NOT NULL,
                aula_id INTEGER NOT NULL,
                data_inscricao TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
                FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE CASCADE,
                FOREIGN KEY (aula_id) REFERENCES aulas (id) ON DELETE CASCADE,
                PRIMARY KEY (aluno_id, aula_id)
            );
        """)

    print("Tabelas da Escola (multi-usuário e novos campos) verificadas/criadas.")