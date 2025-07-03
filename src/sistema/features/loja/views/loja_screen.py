import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkinter import messagebox
from typing import Callable
from sistema.features.loja.services import LojaService
from sistema.utils.asset_loader import assets
from sistema.ui.FontManager import FontManager
from sistema.core.models import User

class LojaDashboard(ctk.CTkFrame):
    """
    Tela de gerenciamento da loja, agora ciente do usuário logado.
    """
    def __init__(self, master, *, current_user: User, show_home_callback: Callable):
        super().__init__(master, fg_color="transparent")
        
        self.current_user = current_user
        self.show_home_callback = show_home_callback
        self.loja_service = LojaService()
        self.selected_product_id = None
        
        self._setup_layout()
        self._create_header()
        self._create_form_frame()
        self._create_list_frame()
        
        self.populate_products_list()

    def _setup_layout(self):
        """Define o grid principal da tela."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def _create_header(self):
        """Cria o cabeçalho com o botão de voltar."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 0))
        
        back_button = ctk.CTkButton(header_frame, text=" Voltar", image=assets.back_arrow_icon, command=self.show_home_callback)
        back_button.pack(side="left")

    def _create_form_frame(self):
        """Cria o painel de formulário à esquerda."""
        self.form_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.form_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)
        self.form_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.form_frame, text="Gestão de Produtos", font=FontManager.get("normal_bold")).pack(pady=20)
        
        ctk.CTkLabel(self.form_frame, text="Nome do Produto", anchor="w").pack(fill="x", padx=20)
        self.nome_entry = ctk.CTkEntry(self.form_frame, height=35)
        self.nome_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(self.form_frame, text="Descrição", anchor="w").pack(fill="x", padx=20)
        self.desc_entry = ctk.CTkEntry(self.form_frame, height=35)
        self.desc_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(self.form_frame, text="Preço (ex: 19.99)", anchor="w").pack(fill="x", padx=20)
        self.preco_entry = ctk.CTkEntry(self.form_frame, height=35)
        self.preco_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(self.form_frame, text="Estoque", anchor="w").pack(fill="x", padx=20)
        self.estoque_entry = ctk.CTkEntry(self.form_frame, height=35)
        self.estoque_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        self.save_button = ctk.CTkButton(self.form_frame, text="Adicionar Produto", height=40, command=self.save_product)
        self.save_button.pack(fill="x", padx=20, pady=10)
        
        self.clear_button = ctk.CTkButton(self.form_frame, text="Limpar Formulário", height=40, fg_color="gray", command=self.clear_form)
        self.clear_button.pack(fill="x", padx=20)

    def _create_list_frame(self):
        """Cria o painel de lista de produtos à direita."""
        self.list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.list_frame.grid(row=1, column=1, sticky="nswe", padx=(0, 20), pady=20)
        
        ctk.CTkLabel(self.list_frame, text="Produtos Cadastrados", font=FontManager.get("normal_bold")).pack(pady=20)
        
        self.products_scroll_frame = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent")
        self.products_scroll_frame.pack(expand=True, fill="both", padx=10)

    def populate_products_list(self):
        for widget in self.products_scroll_frame.winfo_children():
            widget.destroy()

        # Passamos o ID do usuário logado para buscar apenas seus produtos.
        lista_de_produtos = self.loja_service.list_all_products(self.current_user.id)

        for product in lista_de_produtos:
            product_frame = ctk.CTkFrame(self.products_scroll_frame, border_width=1, border_color="gray25")
            product_frame.pack(fill="x", pady=5)
            product_frame.grid_columnconfigure(0, weight=1)
            
            description = product.descricao if product.descricao else "Sem descrição."
            CTkToolTip(product_frame, message=description, delay=0.5)
            
            label_info = ctk.CTkLabel(product_frame, text=f"{product.nome}\nEstoque: {product.estoque} | Preço: R$ {product.preco:.2f}", justify="left")
            label_info.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            buttons_frame = ctk.CTkFrame(product_frame, fg_color="transparent")
            buttons_frame.grid(row=0, column=1, sticky="e", padx=10)

            ctk.CTkButton(buttons_frame, text="", image=assets.sell_icon, width=30, command=lambda p=product: self.sell_product(p)).pack(side="left", padx=5)
            ctk.CTkButton(buttons_frame, text="", image=assets.edit_icon_loja, width=30, command=lambda p=product: self.select_product_for_edit(p)).pack(side="left", padx=5)
            ctk.CTkButton(buttons_frame, text="", image=assets.delete_icon_loja, width=30, fg_color="#DB3E3E", hover_color="#B82E2E", command=lambda p_id=product.id, p_name=product.nome: self.delete_product(p_id, p_name)).pack(side="left")

    def save_product(self):
        nome, desc = self.nome_entry.get(), self.desc_entry.get()
        preco_str, estoque_str = self.preco_entry.get(), self.estoque_entry.get()
        if not all([nome, preco_str, estoque_str]):
            messagebox.showerror("Erro de Validação", "Nome, preço e estoque são obrigatórios.")
            return
        try:
            preco, estoque = float(preco_str.replace(",", ".")), int(estoque_str)
        except ValueError:
            messagebox.showerror("Erro de Validação", "Preço e estoque devem ser números válidos.")
            return

        produto, success = None, False
        if self.selected_product_id is None:
            # Passamos o ID do usuário ao adicionar um novo produto.
            produto = self.loja_service.add_product(self.current_user.id, nome, desc, preco, estoque)
            if produto:
                messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado.")
            else:
                messagebox.showerror("Erro", "Não foi possível adicionar o produto. O nome já pode existir.")
        else:
            # A atualização não precisa de user_id se já temos o product_id.
            success = self.loja_service.update_product(self.selected_product_id, nome, desc, preco, estoque)
            if success:
                messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado.")
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o produto.")

        if produto or success:
            self.populate_products_list()
            self.clear_form()

    def delete_product(self, product_id: int, product_name: str):
        if messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja deletar o produto '{product_name}'?"):
            # Passamos o ID do usuário para garantir que ele só delete seus próprios produtos.
            success, message = self.loja_service.delete_product(self.current_user.id, product_id)
            if success:
                messagebox.showinfo("Sucesso", message)
                self.populate_products_list()
                self.clear_form()
            else:
                messagebox.showerror("Ação Bloqueada", message)

    def sell_product(self, product):
        dialog = ctk.CTkInputDialog(text=f"Vender '{product.nome}'\nEstoque: {product.estoque}\n\nQuantidade:", title="Registrar Venda")
        quantity_str = dialog.get_input()
        if quantity_str:
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError("Quantidade deve ser positiva.")
                
                # Passamos o ID do usuário para registrar a venda em seu nome.
                success, message = self.loja_service.register_sale(self.current_user.id, product.id, quantity)
                if success:
                    messagebox.showinfo("Sucesso", message)
                    self.populate_products_list()
                else:
                    messagebox.showerror("Erro", message)
            except ValueError:
                messagebox.showerror("Entrada Inválida", "Por favor, insira um número inteiro positivo.")
    
    def select_product_for_edit(self, product):
        self.clear_form()
        self.selected_product_id = product.id
        self.nome_entry.insert(0, product.nome)
        self.desc_entry.insert(0, product.descricao or "")
        self.preco_entry.insert(0, str(product.preco))
        self.estoque_entry.insert(0, str(product.estoque))
        self.save_button.configure(text="Atualizar Produto")

    def clear_form(self):
        self.selected_product_id = None
        for entry in [self.nome_entry, self.desc_entry, self.preco_entry, self.estoque_entry]:
            entry.delete(0, "end")
        self.save_button.configure(text="Adicionar Produto")