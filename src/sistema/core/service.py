from sistema.core.UserRepository import UserRepository 
from sistema.core.models import User
from sistema.utils.crypto import hash_password, verify_password  

class AuthService:
    """
    Contém a lógica de negócio para autenticação e registro de usuários.
    """
    def __init__(self):
        # Instancia o repositório em vez de usar métodos estáticos.
        self.user_repo = UserRepository()

    def login(self, email: str, password: str) -> User | None:
        """
        Valida as credenciais do usuário.
        Retorna o objeto User em caso de sucesso, senão None.
        """
        user = self.user_repo.find_by_email(email)
        
        # Usando o objeto User e a função de verificação de hash
        if user and verify_password(password, user.password_hash):
            return user
        return None

    def register(self, full_name: str, email: str, password: str, subscription_type: str) -> User | None:
        """
        Registra um novo usuário.
        Retorna o objeto User criado em caso de sucesso, senão None.
        """
        if self.user_repo.exists(email):
            print(f"Tentativa de registrar email já existente: {email}")
            return None
        
        hashed_pwd = hash_password(password)
        
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hashed_pwd,
            subscription_type=subscription_type
        )

        return self.user_repo.create(new_user)
    
    def update_user_details(self, user_id: int, new_full_name: str, new_password: str | None = None) -> bool:
        """
        Atualiza os detalhes de um usuário. Se a nova senha for fornecida, ela é atualizada.
        """
        user = self.user_repo.find_by_id(user_id) 
        if not user:
            return False

        user.full_name = new_full_name
        if new_password:
            user.password_hash = hash_password(new_password)
        
        return self.user_repo.update(user)

    def delete_user_account(self, user_id: int) -> bool:
        """Deleta a conta de um usuário."""
        return self.user_repo.delete(user_id)