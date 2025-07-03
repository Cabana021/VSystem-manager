from dataclasses import dataclass

@dataclass
class User:
    """Representa um usuário do sistema, mapeando a tabela 'usuarios'."""
    email: str
    full_name: str
    password_hash: str
    subscription_type: str
    id: int | None = None