# ==============================
# ui/paginas/produtos.py
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.paginas.base import PaginaBase
from ui.widgets import CampoForm
from ui.theme import FONTE_NEGRITO, FONTE_NORMAL, FONTE_PEQUENA, COR_BRANCO, COR_PERIGO, COR_TEXTO_CLARO


class PaginaProdutos(PaginaBase):
    TITULO  = "Produtos"
    COLUNAS = [
        ("id",         "ID",         70),
        ("nome",       "Nome",       180),
        ("preco",      "Preço (€)",  90),
        ("stock",      "Stock",      70),
        ("peso",       "Peso (kg)",  90),
        ("categoria",  "Categoria",  130),
    ]

    def _construir_campos(self, frame):
        self._campo_nome      = CampoForm(frame, "Nome do produto")
        self._campo_nome.pack(fill="x", pady=6)

        self._campo_preco     = CampoForm(frame, "Preço (€)",
                                          placeholder="ex: 1.99")
        self._campo_preco.pack(fill="x", pady=6)

        self._campo_quantidade = CampoForm(frame, "Stock (unidades)",
                                           placeholder="ex: 10")
        self._campo_quantidade.pack(fill="x", pady=6)

        self._campo_peso      = CampoForm(frame, "Peso (kg)",
                                          placeholder="ex: 0.500")
        self._campo_peso.pack(fill="x", pady=6)

        # Dropdown de categoria
        lbl_cat = tk.Frame(frame, bg=COR_BRANCO)
        lbl_cat.pack(fill="x", pady=(6, 0))
        tk.Label(lbl_cat, text="Categoria *", font=FONTE_NEGRITO,
                 bg=COR_BRANCO).pack(side="left")

        self._var_categoria = tk.StringVar()
        self._combo_categoria = ttk.Combobox(
            frame, textvariable=self._var_categoria,
            font=FONTE_NORMAL, state="readonly",
        )
        self._combo_categoria.pack(fill="x", pady=(4, 0), ipady=4)

        self._lbl_erro_cat = tk.Label(frame, text="", foreground=COR_PERIGO,
                                      font=FONTE_PEQUENA, bg=COR_BRANCO)
        self._lbl_erro_cat.pack(fill="x")

        self._mapa_categorias = {}  # "C001 – Frutas" → "C001"
        self._recarregar_categorias()

    def _recarregar_categorias(self):
        from categoria import categorias, carregar_categorias
        carregar_categorias()
        self._mapa_categorias = {
            f"{cid} – {d['nome_categoria']}": cid
            for cid, d in categorias.items()
        }
        self._combo_categoria["values"] = list(self._mapa_categorias.keys())

    def _carregar_tabela(self, termo=""):
        from produto   import produtos, carregar_produtos
        from categoria import categorias, carregar_categorias

        carregar_produtos()
        carregar_categorias()

        fonte = {
            pid: d for pid, d in produtos.items()
            if not termo or termo.lower() in d["nome"].lower()
        }

        linhas = [
            (pid,
             d["nome"],
             f"{d['preco']:.2f}",
             d["quantidade_stock"],
             f"{d['peso']:.3f}",
             categorias.get(d["id_categoria"], {}).get("nome_categoria", "?"))
            for pid, d in fonte.items()
        ]
        self._tabela.preencher(linhas)

    def _guardar(self):
        from produto import criar_produto, atualizar_produto

        nome      = self._campo_nome.get()
        preco     = self._campo_preco.get()
        qtd       = self._campo_quantidade.get()
        peso      = self._campo_peso.get()
        cat_label = self._var_categoria.get()

        if not cat_label:
            self._lbl_erro_cat.config(text="  ✖  Seleccione uma categoria.")
            return
        self._lbl_erro_cat.config(text="")

        id_cat = self._mapa_categorias.get(cat_label, "")

        if self._id_seleccionado:
            codigo, resultado = atualizar_produto(
                self._id_seleccionado,
                nome=nome, preco_texto=preco,
                quantidade_texto=qtd, id_categoria=id_cat, peso_texto=peso,
            )
        else:
            codigo, resultado = criar_produto(nome, preco, qtd, id_cat, peso)

        if codigo in (200, 201):
            self._feedback.sucesso(
                f"Produto {'atualizado' if self._id_seleccionado else 'criado'} com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback_form.erro(resultado)

    def _remover(self):
        from produto import remover_produto

        codigo, resultado = remover_produto(self._id_seleccionado)
        if codigo == 200:
            self._feedback.sucesso("Produto removido com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback.erro(resultado)

    def _preencher_campos(self, valores):
        # valores = (id, nome, preco, stock, peso, categoria_nome)
        from produto import produtos, carregar_produtos
        from categoria import categorias, carregar_categorias

        carregar_produtos()
        carregar_categorias()
        self._recarregar_categorias()

        self._campo_nome.set(valores[1])
        self._campo_preco.set(valores[2])
        self._campo_quantidade.set(str(valores[3]))
        self._campo_peso.set(valores[4])

        pid = valores[0]
        id_cat = produtos.get(pid, {}).get("id_categoria", "")
        for label, cid in self._mapa_categorias.items():
            if cid == id_cat:
                self._var_categoria.set(label)
                break

    def _limpar_campos(self):
        self._campo_nome.limpar()
        self._campo_preco.limpar()
        self._campo_quantidade.limpar()
        self._campo_peso.limpar()
        self._var_categoria.set("")
        self._lbl_erro_cat.config(text="")
        self._recarregar_categorias()

    def ao_mostrar(self):
        super().ao_mostrar()
