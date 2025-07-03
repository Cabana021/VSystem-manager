from dataclasses import dataclass

@dataclass
class Produto:
    """Representa um produto da loja."""
    nome: str
    preco: float
    estoque: int
    descricao: str | None = None
    id: int | None = None
    user_id: int | None = None 

@dataclass
class Venda:
    """Representa uma venda registrada."""
    produto_id: int
    quantidade: int
    preco_unitario_na_venda: float
    preco_total: float
    data_venda: str | None = None
    id: int | None = None
    user_id: int | None = None 