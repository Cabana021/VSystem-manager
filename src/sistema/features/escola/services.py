from .repository import EscolaRepository
from .models import Aluno

class EscolaService:
    """Contém a lógica de negócio para a feature da Escola."""
    def __init__(self):
        self.repo = EscolaRepository()

    def add_aluno(self, user_id: int, nome: str, contato: str, vencimento: str, cronograma: str, aulas_concluidas: int, aproveitamento: float) -> Aluno | None:
        """Adiciona um novo aluno, agora com todos os novos campos."""
        aluno = Aluno(
            nome_completo=nome, 
            contato=contato, 
            vencimento_mensalidade=vencimento, 
            cronograma_aulas=cronograma, 
            aulas_concluidas=aulas_concluidas,
            aproveitamento=aproveitamento
        )
        try:
            return self.repo.create_aluno(user_id, aluno)
        except Exception as e:
            print(f"Erro no serviço ao adicionar aluno: {e}")
            return None

    def list_all_alunos(self, user_id: int) -> list[Aluno]:
        """Lista todos os alunos pertencentes a um usuário."""
        return self.repo.get_all_alunos(user_id)

    def update_aluno(self, aluno_id: int, nome: str, contato: str, vencimento: str, cronograma: str, aulas_concluidas: int, aproveitamento: float) -> bool:
        """Atualiza os dados de um aluno existente."""
        aluno = Aluno(
            id=aluno_id,
            nome_completo=nome,
            contato=contato,
            vencimento_mensalidade=vencimento,
            cronograma_aulas=cronograma,
            aulas_concluidas=aulas_concluidas,
            aproveitamento=aproveitamento
        )
        return self.repo.update_aluno(aluno)

    def delete_aluno(self, user_id: int, aluno_id: int) -> tuple[bool, str]:
        """Deleta um aluno, verificando primeiro as matrículas."""
        if self.repo.aluno_is_matriculado(aluno_id):
            return False, "Aluno não pode ser deletado pois está matriculado em uma ou mais aulas."
        
        success = self.repo.delete_aluno(user_id, aluno_id)
        msg = "Aluno deletado com sucesso." if success else "Erro ao deletar aluno."
        return success, msg