from dataclasses import dataclass

@dataclass
class Aluno:
    nome_completo: str
    contato: str | None = None
    vencimento_mensalidade: str | None = None
    cronograma_aulas: str | None = None
    aulas_concluidas: int = 0
    aproveitamento: float = 0.0
    id: int | None = None
    user_id: int | None = None
    data_matricula: str | None = None

@dataclass
class Aula:
    nome_curso: str
    descricao: str | None = None
    professor: str | None = None
    id: int | None = None