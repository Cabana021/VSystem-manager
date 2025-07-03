from .database import get_db_connection
from .models import User
import sqlite3

class UserRepository:
    """
    Gerencia as operações de banco de dados para a entidade User.
    """
    def find_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo email."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row:
                # Convertendo a linha do banco em um objeto User
                return User(id=row["id"], full_name=row["full_name"], email=row["email"], 
                              password_hash=row["password_hash"], subscription_type=row["subscription_type"])
            return None
    
    def find_by_id(self, user_id: int) -> User | None:
        """Busca um usuário pelo seu ID único."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                # Converte a linha do banco de dados em um objeto User
                return User(id=row["id"], full_name=row["full_name"], email=row["email"], 
                              password_hash=row["password_hash"], subscription_type=row["subscription_type"])
            return None
    
    def create(self, user: User) -> User | None:
        """Salva um novo usuário no banco de dados e atualiza seu ID."""
        try:
            with get_db_connection(commit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (full_name, email, password_hash, subscription_type) VALUES (?, ?, ?, ?)",
                    (user.full_name, user.email, user.password_hash, user.subscription_type)
                )
                user.id = cursor.lastrowid
                return user
        # Captura os erros que podem ocorrer na escrita
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            print(f"ERRO ao criar usuário (email duplicado ou DB lock): {e}")
            return None

    def update(self, user: User) -> bool:
        """Atualiza os dados de um usuário no banco de dados."""
        if not user.id:
            return False
        try:
            with get_db_connection(commit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE usuarios SET full_name = ?, password_hash = ? WHERE id = ?",
                    (user.full_name, user.password_hash, user.id)
                )
                return cursor.rowcount > 0
        except sqlite3.OperationalError as e:
            print(f"ERRO ao atualizar usuário (provavelmente DB lock): {e}")
            return False

    def delete(self, user_id: int) -> bool:
        """Deleta um usuário do banco de dados pelo seu ID."""
        try:
            with get_db_connection(commit=True) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
                return cursor.rowcount > 0
        except sqlite3.OperationalError as e:
            print(f"ERRO ao deletar usuário (provavelmente DB lock): {e}")
            return False

    def exists(self, email: str) -> bool:
        """Verifica se um usuário com o email especificado já existe."""
        return self.find_by_email(email) is not None