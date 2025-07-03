from .repository import LojaRepository
from .models import Produto, Venda

class LojaService:
    def __init__(self): self.repo = LojaRepository()

    def add_product(self, user_id: int, nome: str, desc: str, preco: float, estoque: int) -> Produto | None:
        produto = Produto(nome=nome, descricao=desc, preco=preco, estoque=estoque)
        try: return self.repo.create_product(user_id, produto)
        except Exception: return None

    def list_all_products(self, user_id: int) -> list[Produto]:
        return self.repo.get_all_products(user_id)

    def update_product(self, prod_id: int, nome: str, desc: str, preco: float, estoque: int) -> bool:
        produto = Produto(id=prod_id, nome=nome, descricao=desc, preco=preco, estoque=estoque)
        return self.repo.update_product(produto)

    def delete_product(self, user_id: int, produto_id: int) -> tuple[bool, str]:
        if self.repo.product_has_sales(produto_id):
            return False, "Produto não pode ser deletado pois possui vendas."
        success = self.repo.delete_product(user_id, produto_id)
        return (success, "Produto deletado.") if success else (False, "Erro ao deletar.")

    def register_sale(self, user_id: int, produto_id: int, quantidade: int) -> tuple[bool, str]:
        produto = self.repo.find_product_by_id(produto_id)
        if not produto: return False, "Produto não encontrado."
        if produto.estoque < quantidade: return False, f"Estoque insuficiente ({produto.estoque})."
        
        produto.estoque -= quantidade
        self.repo.update_product(produto)
        
        preco_total = produto.preco * quantidade
        venda = Venda(produto_id=produto_id, quantidade=quantidade, preco_unitario_na_venda=produto.preco, preco_total=preco_total)
        self.repo.create_sale(user_id, venda)
        
        return True, "Venda registrada com sucesso."