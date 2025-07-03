import customtkinter as ctk
from typing import Callable
from tkinter import messagebox
from sistema.core.models import User
from sistema.core.service import AuthService
from sistema.ui.FontManager import FontManager
from sistema.utils.asset_loader import assets

class ProfileScreen(ctk.CTkFrame):
    """Tela para o usuário editar seu perfil e apagar sua conta."""

    def __init__(self, master: ctk.CTk, current_user: User, *, on_back: Callable, on_delete_account: Callable):
        super().__init__(master, fg_color="transparent")
        
        self.current_user = current_user
        self.on_back = on_back
        self.on_delete_account = on_delete_account
        self.auth_service = AuthService()

        self._setup_ui()

    def _setup_ui(self):
        """Cria e posiciona os widgets da tela."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        ctk.CTkButton(header, text=" Voltar", image=assets.back_arrow_icon, command=self.on_back).pack(side="left")

        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=100, pady=20)
        
        ctk.CTkLabel(form_frame, text="Meu Perfil", font=FontManager.get("title_medium")).pack(pady=20)

        ctk.CTkLabel(form_frame, text="Nome Completo", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(form_frame, height=35)
        self.name_entry.insert(0, self.current_user.full_name)
        self.name_entry.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(form_frame, text="Nova Senha (deixe em branco para não alterar)", anchor="w").pack(fill="x", padx=20)
        self.password_entry = ctk.CTkEntry(form_frame, show="*", height=35)
        self.password_entry.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkButton(form_frame, text=" Salvar Alterações", image=assets.edit_icon_geral, command=self.save_changes).pack(pady=20, fill="x", padx=20)
        
        ctk.CTkButton(form_frame, text=" Deletar Minha Conta", image=assets.delete_icon_geral, fg_color="#DB3E3E", hover_color="#B82E2E", command=self.delete_account).pack(pady=10, fill="x", padx=20)

    def save_changes(self):
        """Salva as alterações no perfil do usuário."""
        new_name = self.name_entry.get()
        new_password = self.password_entry.get() or None
        
        success = self.auth_service.update_user_details(self.current_user.id, new_name, new_password)

        if success:
            messagebox.showinfo("Sucesso", "Seu perfil foi atualizado!")
            self.current_user.full_name = new_name
            self.on_back()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar seu perfil.")
            
    def delete_account(self):
        """Inicia o processo de exclusão da conta."""
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar sua conta? Esta ação é irreversível."):
            success = self.auth_service.delete_user_account(self.current_user.id)
            if success:
                messagebox.showinfo("Conta Deletada", "Sua conta foi deletada com sucesso.")
                self.on_delete_account()
            else:
                messagebox.showerror("Erro", "Não foi possível deletar sua conta.")