import sqlite3
from sistema.core.database import get_db_connection
from .models import Produto, Venda

class LojaRepository:
    def create_product(self, user_id: int, produto: Produto) -> Produto:
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produtos (user_id, nome, descricao, preco, estoque) VALUES (?, ?, ?, ?, ?)",
                           (user_id, produto.nome, produto.descricao, produto.preco, produto.estoque))
            produto.id = cursor.lastrowid; return produto

    def get_all_products(self, user_id: int) -> list[Produto]:
        with get_db_connection() as conn:
            cursor = conn.cursor(); cursor.execute("SELECT * FROM produtos WHERE user_id = ? ORDER BY nome", (user_id,))
            return [Produto(**row) for row in cursor.fetchall()]

    def update_product(self, produto: Produto) -> bool:
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor(); cursor.execute("UPDATE produtos SET nome=?, descricao=?, preco=?, estoque=? WHERE id=?",
                           (produto.nome, produto.descricao, produto.preco, produto.estoque, produto.id))
            return cursor.rowcount > 0

    def delete_product(self, user_id: int, produto_id: int) -> bool:
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor(); cursor.execute("DELETE FROM produtos WHERE id = ? AND user_id = ?", (produto_id, user_id))
            return cursor.rowcount > 0

    def find_product_by_id(self, produto_id: int) -> Produto | None:
        with get_db_connection() as conn:
            cursor = conn.cursor(); cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
            row = cursor.fetchone(); return Produto(**row) if row else None

    def create_sale(self, user_id: int, venda: Venda) -> Venda:
        with get_db_connection(commit=True) as conn:
            cursor = conn.cursor(); cursor.execute("INSERT INTO vendas (user_id, produto_id, quantidade, preco_unitario_na_venda, preco_total) VALUES (?, ?, ?, ?, ?)",
                           (user_id, venda.produto_id, venda.quantidade, venda.preco_unitario_na_venda, venda.preco_total))
            venda.id = cursor.lastrowid; return venda

    def product_has_sales(self, produto_id: int) -> bool:
        with get_db_connection() as conn:
            cursor = conn.cursor(); cursor.execute("SELECT 1 FROM vendas WHERE produto_id = ? LIMIT 1", (produto_id,))
            return cursor.fetchone() is not None