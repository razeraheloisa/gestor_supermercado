# ==============================
# ui/paginas/compras.py
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.paginas.base import PaginaBase
from ui.widgets import CampoForm
from ui.theme import FONTE_NEGRITO, FONTE_NORMAL, FONTE_PEQUENA, COR_BRANCO, COR_PERIGO


class PaginaCompras(PaginaBase):
    TITULO  = "Compras"
    COLUNAS = [
        ("id",          "ID",           70),
        ("cliente",     "Cliente",      160),
        ("supermercado","Supermercado", 180),
        ("data",        "Data",         100),
        ("valor",       "Valor (€)",    90),
    ]

    def _construir_campos(self, frame):
        # Dropdown: cliente
        self._var_cliente = tk.StringVar()
        self._mapa_clientes = {}
        self._combo_cliente, self._lbl_err_cli = self._dropdown(
            frame, "Cliente", self._var_cliente)

        # Dropdown: supermercado
        self._var_super = tk.StringVar()
        self._mapa_super = {}
        self._combo_super, self._lbl_err_sup = self._dropdown(
            frame, "Supermercado", self._var_super)

        # Data e valor
        self._campo_data  = CampoForm(frame, "Data",
                                       placeholder="DD/MM/AAAA")
        self._campo_data.pack(fill="x", pady=6)

        self._campo_valor = CampoForm(frame, "Valor total (€)",
                                      placeholder="ex: 24.90")
        self._campo_valor.pack(fill="x", pady=6)

        self._recarregar_dropdowns()

    def _dropdown(self, frame, titulo, var):
        lbl_f = tk.Frame(frame, bg=COR_BRANCO)
        lbl_f.pack(fill="x", pady=(6, 0))
        tk.Label(lbl_f, text=f"{titulo} *", font=FONTE_NEGRITO,
                 bg=COR_BRANCO).pack(side="left")

        combo = ttk.Combobox(frame, textvariable=var,
                             font=FONTE_NORMAL, state="readonly")
        combo.pack(fill="x", pady=(4, 0), ipady=4)

        lbl_err = tk.Label(frame, text="", foreground=COR_PERIGO,
                           font=FONTE_PEQUENA, bg=COR_BRANCO)
        lbl_err.pack(fill="x")
        return combo, lbl_err

    def _recarregar_dropdowns(self):
        from cliente      import clientes,      carregar_clientes
        from supermercado import supermercados,  carregar_supermercado

        carregar_clientes()
        carregar_supermercado()

        self._mapa_clientes = {
            f"{cid} – {d['nome']}": cid for cid, d in clientes.items()
        }
        self._mapa_super = {
            f"{sid} – {d['morada']}": sid for sid, d in supermercados.items()
        }

        self._combo_cliente["values"] = list(self._mapa_clientes.keys())
        self._combo_super["values"]   = list(self._mapa_super.keys())

    def _carregar_tabela(self, termo=""):
        from compra       import compras,        carregar_compras
        from cliente      import clientes,       carregar_clientes
        from supermercado import supermercados,   carregar_supermercado

        carregar_compras()
        carregar_clientes()
        carregar_supermercado()

        fonte = {
            cid: d for cid, d in compras.items()
            if not termo
               or termo.lower() in clientes.get(d["id_cliente"], {}).get("nome", "").lower()
               or termo.lower() in supermercados.get(d["id_supermercado"], {}).get("morada", "").lower()
        }

        linhas = [
            (cid,
             clientes.get(d["id_cliente"], {}).get("nome", "?"),
             supermercados.get(d["id_supermercado"], {}).get("morada", "?"),
             d["data"],
             f"{d['valor_total']:.2f}")
            for cid, d in fonte.items()
        ]
        self._tabela.preencher(linhas)

    def _guardar(self):
        from compra import criar_compra, atualizar_compra

        cli_label = self._var_cliente.get()
        sup_label = self._var_super.get()
        data      = self._campo_data.get()
        valor     = self._campo_valor.get()

        valido = True
        if not cli_label:
            self._lbl_err_cli.config(text="  ✖  Seleccione um cliente.")
            valido = False
        else:
            self._lbl_err_cli.config(text="")

        if not sup_label:
            self._lbl_err_sup.config(text="  ✖  Seleccione um supermercado.")
            valido = False
        else:
            self._lbl_err_sup.config(text="")

        if not valido:
            return

        id_cli = self._mapa_clientes.get(cli_label, "")
        id_sup = self._mapa_super.get(sup_label, "")

        if self._id_seleccionado:
            codigo, resultado = atualizar_compra(
                self._id_seleccionado, data=data, valor_total_texto=valor)
        else:
            codigo, resultado = criar_compra(id_cli, id_sup, data, valor)

        if codigo in (200, 201):
            self._feedback.sucesso(
                f"Compra {'atualizada' if self._id_seleccionado else 'registada'} com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback_form.erro(resultado)

    def _remover(self):
        from compra import remover_compra

        codigo, resultado = remover_compra(self._id_seleccionado)
        if codigo == 200:
            self._feedback.sucesso("Compra removida com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback.erro(resultado)

    def _preencher_campos(self, valores):
        # valores = (id, nome_cliente, morada_super, data, valor)
        from compra       import compras,        carregar_compras
        from cliente      import clientes,       carregar_clientes
        from supermercado import supermercados,   carregar_supermercado

        carregar_compras()
        self._recarregar_dropdowns()

        cid = valores[0]
        dados = compras.get(cid, {})

        # Seleccionar cliente no dropdown
        id_cli = dados.get("id_cliente", "")
        for label, cid_val in self._mapa_clientes.items():
            if cid_val == id_cli:
                self._var_cliente.set(label)
                break

        # Seleccionar supermercado no dropdown
        id_sup = dados.get("id_supermercado", "")
        for label, sid_val in self._mapa_super.items():
            if sid_val == id_sup:
                self._var_super.set(label)
                break

        self._campo_data.set(dados.get("data", ""))
        self._campo_valor.set(str(dados.get("valor_total", "")))

    def _limpar_campos(self):
        self._var_cliente.set("")
        self._var_super.set("")
        self._campo_data.limpar()
        self._campo_valor.limpar()
        self._lbl_err_cli.config(text="")
        self._lbl_err_sup.config(text="")
        self._recarregar_dropdowns()

    def ao_mostrar(self):
        super().ao_mostrar()
