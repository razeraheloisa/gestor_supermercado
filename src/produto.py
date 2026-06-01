import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import tkinter as tk
from tkinter import ttk
from ui.widgets import CampoForm, BotaoPrimario, BotaoPerigo, Tabela, MensagemFeedback, DialogoConfirmacao
import produto
import categoria

class PaginaProdutos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        topo = ttk.Frame(self, style="TFrame")
        topo.pack(fill="x", padx=30, pady=20)
        ttk.Label(topo, text="Gestão de Produtos", style="Titulo.TLabel").pack(side="left")
        self.feedback = MensagemFeedback(topo)
        self.feedback.pack(side="right", padx=10)

        corpo = ttk.Frame(self, style="TFrame")
        corpo.pack(fill="both", expand=True, padx=30, pady=10)

        # Form
        self.frame_form = ttk.LabelFrame(corpo, text=" Dados do Produto ", style="TFrame", padding=15)
        self.frame_form.pack(side="left", fill="y", padx=(0, 20))

        self.txt_id = CampoForm(self.frame_form, label="ID Produto", obrigatorio=False)
        self.txt_id._entry.config(state="disabled")
        self.txt_id.pack(fill="x", pady=2)

        self.txt_nome = CampoForm(self.frame_form, label="Nome do Produto")
        self.txt_nome.pack(fill="x", pady=2)

        self.txt_preco = CampoForm(self.frame_form, label="Preço (€)", placeholder="Ex: 1.99")
        self.txt_preco.pack(fill="x", pady=2)

        self.txt_stock = CampoForm(self.frame_form, label="Stock Disponível", placeholder="Ex: 50")
        self.txt_stock.pack(fill="x", pady=2)

        # Label + Dropdown nativo (Combobox) para vincular ID Categorias existentes
        ttk.Label(self.frame_form, text="Categoria *", font=("Segoe UI", 10, "bold"), style="TLabel").pack(anchor="w",
                                                                                                           pady=(5, 2))
        self.cb_categoria = ttk.Combobox(self.frame_form, state="readonly", font=("Segoe UI", 10))
        self.cb_categoria.pack(fill="x", ipady=4, pady=(0, 5))
        self._carregar_dropdown_categorias()

        self.txt_peso = CampoForm(self.frame_form, label="Peso (kg)", placeholder="Ex: 0.500")
        self.txt_peso.pack(fill="x", pady=2)

        btn_box = ttk.Frame(self.frame_form, style="TFrame")
        btn_box.pack(fill="x", pady=10)
        BotaoPrimario(btn_box, "Salvar", comando=self._submeter).pack(side="left", expand=True, fill="x", padx=2)
        BotaoPerigo(btn_box, "Limpar", comando=self._limpar_formulario).pack(side="left", expand=True, fill="x", padx=2)

        # Tabela
        frame_tabela = ttk.Frame(corpo, style="TFrame")
        frame_tabela.pack(side="right", fill="both", expand=True)

        colunas = [("id", "ID", 70), ("nome", "Nome", 180), ("preco", "Preço", 80), ("stock", "Stock", 80),
                   ("peso", "Peso", 80), ("cat", "Categoria", 150)]
        self.tabela = Tabela(frame_tabela, colunas=colunas)
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind_duplo_clique(self._carregar_registo)

        BotaoPerigo(frame_tabela, "Remover Selecionado", comando=self._confirmar_remocao).pack(anchor="e", pady=10)

        self._atualizar_grid()

    def _carregar_dropdown_categorias(self):
        valores = [f"{id_cat} - {d['nome_categoria']}" for id_cat, d in categoria.categorias.items()]
        self.cb_categoria["values"] = valores

    def _atualizar_grid(self):
        dados_tabela = []
        for pid, d in produto.produtos.items():
            nome_cat = categoria.categorias.get(d["id_categoria"], {}).get("nome_categoria", d["id_categoria"])
            dados_tabela.append(
                (pid, d["nome"], f"{d['preco']:.2f} €", d["quantidade_stock"], f"{d['peso']:.3f} kg", nome_cat))
        self.tabela.preencher(dados_tabela)

    def _submeter(self):
        id_atual = self.txt_id.get()
        nome = self.txt_nome.get()
        preco = self.txt_preco.get()
        stock = self.txt_stock.get()
        peso = self.txt_peso.get()

        sel_cat = self.cb_categoria.get()
        id_cat = sel_cat.split(" - ")[0] if sel_cat else ""

        if id_atual == "":
            status, msg = produto.criar_produto(nome, preco, stock, id_cat, peso)
        else:
            status, msg = produto.atualizar_produto(id_atual, nome, preco, stock, id_cat, peso)

        if status in (200, 201):
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _carregar_registo(self):
        sel = self.tabela.seleccionado()
        if sel:
            pid = sel[0]
            d = produto.produtos[pid]
            self.txt_id._entry.config(state="normal")
            self.txt_id.set(pid)
            self.txt_id._entry.config(state="disabled")
            self.txt_nome.set(d["nome"])
            self.txt_preco.set(str(d["preco"]))
            self.txt_stock.set(str(d["quantidade_stock"]))
            self.txt_peso.set(str(d["peso"]))

            nome_cat = categoria.categorias.get(d["id_categoria"], {}).get("nome_categoria", "")
            self.cb_categoria.set(f"{d['id_categoria']} - {nome_cat}" if nome_cat else d["id_categoria"])

    def _confirmar_remocao(self):
        sel = self.tabela.seleccionado()
        if not sel: return
        DialogoConfirmacao(self, "Remover Produto", f"Remover {sel[1]}?",
                           callback_sim=lambda: self._executar_remocao(sel[0]))

    def _executar_remocao(self, pid):
        status, msg = produto.remover_produto(pid)
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
        self.txt_preco.limpar()
        self.txt_stock.limpar()
        self.txt_peso.limpar()
        self.cb_categoria.set("")
        self._carregar_dropdown_categorias()
