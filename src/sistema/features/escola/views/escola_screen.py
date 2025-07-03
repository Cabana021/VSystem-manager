import customtkinter as ctk
from tkinter import messagebox
from typing import Callable
from sistema.features.escola.services import EscolaService
from sistema.utils.asset_loader import assets
from sistema.ui.FontManager import FontManager
from sistema.core.models import User

class EscolaDashboard(ctk.CTkFrame):
    def __init__(self, master, *, current_user: User, show_home_callback: Callable):
        super().__init__(master, fg_color="transparent")
        
        self.current_user = current_user
        self.show_home_callback = show_home_callback
        self.escola_service = EscolaService()
        self.selected_aluno_id = None
        
        self._setup_layout()
        self._create_header()
        self._create_form_frame()
        self._create_list_frame()
        
        self.populate_alunos_list()

    def _setup_layout(self):
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(1, weight=1)

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 0))
        ctk.CTkButton(header_frame, text=" Voltar", image=assets.back_arrow_icon, command=self.show_home_callback).pack(side="left")

    def _create_form_frame(self):
        self.form_frame = ctk.CTkFrame(self, width=350, corner_radius=10)
        self.form_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)
        self.form_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.form_frame, text="Gestão de Alunos", font=FontManager.get("normal_bold")).pack(pady=15)
        
        ctk.CTkLabel(self.form_frame, text="Nome Completo", anchor="w").pack(fill="x", padx=20)
        self.nome_entry = ctk.CTkEntry(self.form_frame, height=35); self.nome_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.form_frame, text="Nº de Contato", anchor="w").pack(fill="x", padx=20)
        self.contato_entry = ctk.CTkEntry(self.form_frame, height=35); self.contato_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.form_frame, text="Vencimento Mensalidade", anchor="w").pack(fill="x", padx=20)
        self.vencimento_entry = ctk.CTkEntry(self.form_frame, height=35); self.vencimento_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Cronograma de Aulas", anchor="w").pack(fill="x", padx=20)
        self.cronograma_entry = ctk.CTkEntry(self.form_frame, height=35); self.cronograma_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Aulas Concluídas", anchor="w").pack(fill="x", padx=20)
        self.aulas_concluidas_entry = ctk.CTkEntry(self.form_frame, height=35); self.aulas_concluidas_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Aproveitamento (%)", anchor="w").pack(fill="x", padx=20)
        self.aproveitamento_entry = ctk.CTkEntry(self.form_frame, height=35); self.aproveitamento_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        self.save_button = ctk.CTkButton(self.form_frame, text="Adicionar Aluno", height=40, command=self.save_aluno)
        self.save_button.pack(fill="x", padx=20, pady=10)
        
        self.clear_button = ctk.CTkButton(self.form_frame, text="Limpar Formulário", height=40, fg_color="gray", command=self.clear_form)
        self.clear_button.pack(fill="x", padx=20)

    def _create_list_frame(self):
        self.list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.list_frame.grid(row=1, column=1, sticky="nswe", padx=(0, 20), pady=20)
        ctk.CTkLabel(self.list_frame, text="Alunos Matriculados", font=FontManager.get("normal_bold")).pack(pady=20)
        self.alunos_scroll_frame = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent")
        self.alunos_scroll_frame.pack(expand=True, fill="both", padx=10)

    def populate_alunos_list(self):
        for widget in self.alunos_scroll_frame.winfo_children(): widget.destroy()
        lista_de_alunos = self.escola_service.list_all_alunos(self.current_user.id)

        for aluno in lista_de_alunos:
            aluno_frame = ctk.CTkFrame(self.alunos_scroll_frame, border_width=1, border_color="gray25")
            aluno_frame.pack(fill="x", pady=5)
            aluno_frame.grid_columnconfigure(0, weight=1)
            
            label_info = ctk.CTkLabel(aluno_frame, text=f"{aluno.nome_completo}\n{aluno.contato}", justify="left")
            label_info.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            buttons_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
            buttons_frame.grid(row=0, column=1, sticky="e", padx=10)

            ctk.CTkButton(buttons_frame, text="", image=assets.info_icon, width=30, command=lambda a=aluno: self.show_aluno_details(a)).pack(side="left", padx=5)
            ctk.CTkButton(buttons_frame, text="", image=assets.edit_icon_geral, width=30, command=lambda a=aluno: self.select_aluno_for_edit(a)).pack(side="left", padx=5)
            ctk.CTkButton(buttons_frame, text="", image=assets.delete_icon_geral, width=30, fg_color="#DB3E3E", hover_color="#B82E2E", command=lambda a_id=aluno.id, a_nome=aluno.nome_completo: self.delete_aluno(a_id, a_nome)).pack(side="left")
    
    def show_aluno_details(self, aluno):
        details = (f"Nome: {aluno.nome_completo}\n"
                   f"Contato: {aluno.contato or 'N/A'}\n\n"
                   f"Vencimento Mensalidade: {aluno.vencimento_mensalidade or 'N/A'}\n"
                   f"Cronograma: {aluno.cronograma_aulas or 'N/A'}\n"
                   f"Aulas Concluídas: {aluno.aulas_concluidas}\n"
                   f"Aproveitamento: {aluno.aproveitamento}%")
        messagebox.showinfo(f"Detalhes de {aluno.nome_completo}", details)

    def save_aluno(self):
        # Coleta de dados
        aluno_data = {
            "nome": self.nome_entry.get(),
            "contato": self.contato_entry.get() or None,
            "vencimento": self.vencimento_entry.get() or None,
            "cronograma": self.cronograma_entry.get() or None,
            "aulas_concluidas": int(self.aulas_concluidas_entry.get() or 0),
            "aproveitamento": float(self.aproveitamento_entry.get() or 0.0)
        }
        if not aluno_data["nome"]: messagebox.showerror("Erro", "Nome é obrigatório."); return
        
        if self.selected_aluno_id is None:
            aluno = self.escola_service.add_aluno(self.current_user.id, **aluno_data)
            if aluno: messagebox.showinfo("Sucesso", "Aluno adicionado.")
            else: messagebox.showerror("Erro", "Não foi possível adicionar. O nome pode já existir.")
        else:
            success = self.escola_service.update_aluno(self.selected_aluno_id, **aluno_data)
            if success: messagebox.showinfo("Sucesso", "Aluno atualizado.")
            else: messagebox.showerror("Erro", "Não foi possível atualizar.")

        if (self.selected_aluno_id and success) or (not self.selected_aluno_id and aluno):
            self.populate_alunos_list(); self.clear_form()

    def delete_aluno(self, aluno_id: int, aluno_nome: str):
        if messagebox.askyesno("Confirmar", f"Deseja deletar '{aluno_nome}'?"):
            success, message = self.escola_service.delete_aluno(self.current_user.id, aluno_id)
            if success: messagebox.showinfo("Sucesso", message)
            else: messagebox.showerror("Erro", message)
            self.populate_alunos_list(); self.clear_form()

    def select_aluno_for_edit(self, aluno):
        self.clear_form(); self.selected_aluno_id = aluno.id
        self.nome_entry.insert(0, aluno.nome_completo); self.contato_entry.insert(0, aluno.contato or "")
        self.vencimento_entry.insert(0, aluno.vencimento_mensalidade or "")
        self.cronograma_entry.insert(0, aluno.cronograma_aulas or "")
        self.aulas_concluidas_entry.insert(0, str(aluno.aulas_concluidas))
        self.aproveitamento_entry.insert(0, str(aluno.aproveitamento))
        self.save_button.configure(text="Atualizar Aluno")

    def clear_form(self):
        self.selected_aluno_id = None
        for entry in [self.nome_entry, self.contato_entry, self.vencimento_entry, self.cronograma_entry, self.aulas_concluidas_entry, self.aproveitamento_entry]:
            entry.delete(0, "end")
        self.save_button.configure(text="Adicionar Aluno")