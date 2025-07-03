from sistema.core.database import get_db_connection
from .models import Aluno, Aula # Aula é para função futura

class EscolaRepository:
    """Gerencia as operações de banco de dados para a feature Escola."""

    def create_aluno(self, user_id: int, aluno: Aluno) -> Aluno:
        """Cria um novo aluno no banco de dados para um usuário específico."""
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alunos 
                (user_id, nome_completo, contato, vencimento_mensalidade, cronograma_aulas, aulas_concluidas, aproveitamento) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, aluno.nome_completo, aluno.contato, aluno.vencimento_mensalidade, 
                  aluno.cronograma_aulas, aluno.aulas_concluidas, aluno.aproveitamento))
            aluno.id = cursor.lastrowid
            return aluno

    def get_all_alunos(self, user_id: int) -> list[Aluno]:
        """Busca todos os alunos de um usuário específico."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Query SELECT filtra por user_id 
            cursor.execute("SELECT * FROM alunos WHERE user_id = ? ORDER BY nome_completo", (user_id,))
            rows = cursor.fetchall()
            return [Aluno(**row) for row in rows]

    def update_aluno(self, aluno: Aluno) -> bool:
        """Atualiza os dados de um aluno existente."""
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE alunos SET 
                nome_completo=?, contato=?, vencimento_mensalidade=?, cronograma_aulas=?, aulas_concluidas=?, aproveitamento=? 
                WHERE id=?
            """, (aluno.nome_completo, aluno.contato, aluno.vencimento_mensalidade, 
                  aluno.cronograma_aulas, aluno.aulas_concluidas, aluno.aproveitamento, aluno.id))
            return cursor.rowcount > 0

    def delete_aluno(self, user_id: int, aluno_id: int) -> bool:
        """Deleta um aluno de um usuário específico."""
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor()
            # Query DELETE verifica o user_id por segurança 
            cursor.execute("DELETE FROM alunos WHERE id = ? AND user_id = ?", (aluno_id, user_id))
            return cursor.rowcount > 0

    def aluno_is_matriculado(self, aluno_id: int) -> bool:
        """Verifica se um aluno está matriculado em alguma aula."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM matriculas WHERE aluno_id = ? LIMIT 1", (aluno_id,))
            return cursor.fetchone() is not None