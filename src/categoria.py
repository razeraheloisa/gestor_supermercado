# ==============================
# ui/paginas/categorias.py
# ==============================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import tkinter as tk
from tkinter import ttk
from ui.widgets import CampoForm, BotaoPrimario, BotaoPerigo, Tabela, MensagemFeedback, DialogoConfirmacao
import categoria


class PaginaCategorias(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        # Título e Feedback
        topo = ttk.Frame(self, style="TFrame")
        topo.pack(fill="x", padx=30, pady=20)
        ttk.Label(topo, text="Gestão de Categorias", style="Titulo.TLabel").pack(side="left")
        self.feedback = MensagemFeedback(topo)
        self.feedback.pack(side="right", padx=10)

        # Divisão de ecrã: Esquerda (Formulário) | Direita (Tabela)
        corpo = ttk.Frame(self, style="TFrame")
        corpo.pack(fill="both", expand=True, padx=30, pady=10)

        # Formulário
        self.frame_form = ttk.LabelFrame(corpo, text=" Dados da Categoria ", style="TFrame", padding=15)
        self.frame_form.pack(side="left", fill="y", padx=(0, 20))

        self.txt_id = CampoForm(self.frame_form, label="ID Categoria", obrigatorio=False,
                                placeholder="Gerado automaticamente")
        self.txt_id._entry.config(state="disabled")  # Bloqueado
        self.txt_id.pack(fill="x", pady=5)

        self.txt_nome = CampoForm(self.frame_form, label="Nome da Categoria", placeholder="Ex: Bebidas")
        self.txt_nome.pack(fill="x", pady=5)

        self.txt_desc = CampoForm(self.frame_form, label="Descrição", placeholder="Ex: Sumos, Águas e Refrigerantes")
        self.txt_desc.pack(fill="x", pady=5)

        # Botões de Ação
        btn_box = ttk.Frame(self.frame_form, style="TFrame")
        btn_box.pack(fill="x", pady=15)

        self.btn_salvar = BotaoPrimario(btn_box, "Salvar", comando=self._submeter)
        self.btn_salvar.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_limpar = BotaoPerigo(btn_box, "Limpar / Cancelar", comando=self._limpar_formulario)
        self.btn_limpar.pack(side="left", expand=True, fill="x", padx=2)

        # Área da Direita: Tabela
        frame_tabela = ttk.Frame(corpo, style="TFrame")
        frame_tabela.pack(side="right", fill="both", expand=True)

        colunas = [("id", "ID", 100), ("nome", "Nome Categoria", 200), ("desc", "Descrição", 350)]
        self.tabela = Tabela(frame_tabela, colunas=colunas)
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind_duplo_clique(self._carregar_registo)

        # Botão de remoção abaixo da tabela
        self.btn_remover = BotaoPerigo(frame_tabela, "Remover Selecionada", comando=self._confirmar_remocao)
        self.btn_remover.pack(anchor="e", pady=10)

        self._atualizar_grid()

    def _atualizar_grid(self):
        dados_tabela = []
        for id_cat, dados in categoria.categorias.items():
            dados_tabela.append((id_cat, dados["nome_categoria"], dados["descricao"]))
        self.tabela.preencher(dados_tabela)

    def _submeter(self):
        id_atual = self.txt_id.get()
        nome = self.txt_nome.get()
        desc = self.txt_desc.get()

        # Limpa estados de erro visuais anteriores
        self.txt_nome.limpar_erro()
        self.txt_desc.limpar_erro()

        if id_atual == "":  # Operação CREATE
            status, msg = categoria.criar_categoria(nome, desc)
        else:  # Operação UPDATE
            status, msg = categoria.atualizar_categoria(id_atual, nome, desc)

        if status in (200, 201):
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _carregar_registo(self):
        sel = self.tabela.seleccionado()
        if sel:
            self.txt_id._entry.config(state="normal")
            self.txt_id.set(sel[0])
            self.txt_id._entry.config(state="disabled")
            self.txt_id.config(foreground="gray")
            self.txt_nome.set(sel[1])
            self.txt_desc.set(sel[2])

    def _confirmar_remocao(self):
        sel = self.tabela.seleccionado()
        if not sel:
            self.feedback.aviso("Selecione uma categoria na tabela primeiro.")
            return

        DialogoConfirmacao(
            self, "Remover Categoria", f"Tem a certeza que deseja remover a categoria {sel[1]}?",
            callback_sim=lambda: self._executar_remocao(sel[0])
        )

    def _executar_remocao(self, id_cat):
        status, msg = categoria.remover_categoria(id_cat)
        if status == 200:
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _limpar_formulario(self):
        self.txt_id._entry.config(state="normal")
        self.txt_id.limpar()
        self.txt_id._entry.config(state="disabled")
        self.txt_nome.limpar()
        self.txt_desc.limpar()
