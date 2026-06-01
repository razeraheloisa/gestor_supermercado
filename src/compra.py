import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import tkinter as tk
from tkinter import ttk
from ui.widgets import CampoForm, BotaoPrimario, BotaoPerigo, Tabela, MensagemFeedback, DialogoConfirmacao
import compra
import cliente
import supermercado

class PaginaCompras(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        topo = ttk.Frame(self, style="TFrame")
        topo.pack(fill="x", padx=30, pady=20)
        ttk.Label(topo, text="Registo de Compras", style="Titulo.TLabel").pack(side="left")
        self.feedback = MensagemFeedback(topo)
        self.feedback.pack(side="right", padx=10)

        corpo = ttk.Frame(self, style="TFrame")
        corpo.pack(fill="both", expand=True, padx=30, pady=10)

        self.frame_form = ttk.LabelFrame(corpo, text=" Nova Compra ", style="TFrame", padding=15)
        self.frame_form.pack(side="left", fill="y", padx=(0, 20))

        self.txt_id = CampoForm(self.frame_form, label="ID Compra", obrigatorio=False)
        self.txt_id._entry.config(state="disabled")
        self.txt_id.pack(fill="x", pady=2)

        # Dropdown Clientes
        ttk.Label(self.frame_form, text="Cliente *", font=("Segoe UI", 10, "bold"), style="TLabel").pack(anchor="w",
                                                                                                         pady=(4, 2))
        self.cb_cliente = ttk.Combobox(self.frame_form, state="readonly", font=("Segoe UI", 10))
        self.cb_cliente.pack(fill="x", ipady=4, pady=(0, 6))

        # Dropdown Supermercados
        ttk.Label(self.frame_form, text="Supermercado *", font=("Segoe UI", 10, "bold"), style="TLabel").pack(
            anchor="w", pady=(4, 2))
        self.cb_super = ttk.Combobox(self.frame_form, state="readonly", font=("Segoe UI", 10))
        self.cb_super.pack(fill="x", ipady=4, pady=(0, 6))

        self._carregar_comboboxes()

        self.txt_data = CampoForm(self.frame_form, label="Data (DD/MM/AAAA)", placeholder="Ex: 25/04/2025")
        self.txt_data.pack(fill="x", pady=2)

        self.txt_valor = CampoForm(self.frame_form, label="Valor Total (€)", placeholder="Ex: 45.90")
        self.txt_valor.pack(fill="x", pady=2)

        btn_box = ttk.Frame(self.frame_form, style="TFrame")
        btn_box.pack(fill="x", pady=15)
        BotaoPrimario(btn_box, "Registar", comando=self._submeter).pack(side="left", expand=True, fill="x", padx=2)
        BotaoPerigo(btn_box, "Limpar", comando=self._limpar_formulario).pack(side="left", expand=True, fill="x", padx=2)

        # Tabela de Compras
        frame_tabela = ttk.Frame(corpo, style="TFrame")
        frame_tabela.pack(side="right", fill="both", expand=True)

        colunas = [("id", "ID Compra", 80), ("cliente", "Cliente", 180), ("super", "Supermercado", 180),
                   ("data", "Data", 100), ("valor", "Valor total", 100)]
        self.tabela = Tabela(frame_tabela, colunas=colunas)
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind_duplo_clique(self._carregar_registo)

        BotaoPerigo(frame_tabela, "Anular Compra", comando=self._confirmar_remocao).pack(anchor="e", pady=10)

        self._atualizar_grid()

    def _carregar_comboboxes(self):
        self.cb_cliente["values"] = [f"{cid} - {d['nome']}" for cid, d in cliente.clientes.items()]
        self.cb_super["values"] = [f"{sid} - {d['morada']}" for sid, d in supermercado.supermercados.items()]

    def _atualizar_grid(self):
        dados_tabela = []
        for cmp_id, d in compra.compras.items():
            nome_cli = cliente.clientes.get(d["id_cliente"], {}).get("nome", d["id_cliente"])
            morada_sup = supermercado.supermercados.get(d["id_supermercado"], {}).get("morada", d["id_supermercado"])
            dados_tabela.append((cmp_id, nome_cli, morada_sup, d["data"], f"{d['valor_total']:.2f} €"))
        self.tabela.preencher(dados_tabela)

    def _submeter(self):
        id_atual = self.txt_id.get()
        data = self.txt_data.get()
        valor = self.txt_valor.get()

        sel_cli = self.cb_cliente.get()
        id_cli = sel_cli.split(" - ")[0] if sel_cli else ""

        sel_sup = self.cb_super.get()
        id_sup = sel_sup.split(" - ")[0] if sel_sup else ""

        if id_atual == "":
            status, msg = compra.criar_compra(id_cli, id_sup, data, valor)
        else:
            status, msg = compra.atualizar_compra(id_atual, data, valor)

        if status in (200, 201):
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _carregar_registo(self):
        sel = self.tabela.seleccionado()
        if sel:
            cmp_id = sel[0]
            d = compra.compras[cmp_id]
            self.txt_id._entry.config(state="normal")
            self.txt_id.set(cmp_id)
            self.txt_id._entry.config(state="disabled")
            self.txt_data.set(d["data"])
            self.txt_valor.set(str(d["valor_total"]))

            nome_cli = cliente.clientes.get(d["id_cliente"], {}).get("nome", "")
            self.cb_cliente.set(f"{d['id_cliente']} - {nome_cli}" if nome_cli else d["id_cliente"])

            morada_sup = supermercado.supermercados.get(d["id_supermercado"], {}).get("morada", "")
            self.cb_super.set(f"{d['id_supermercado']} - {morada_sup}" if morada_sup else d["id_supermercado"])

    def _confirmar_remocao(self):
        sel = self.tabela.seleccionado()
        if not sel: return
        DialogoConfirmacao(self, "Anular Compra", f"Deseja anular a compra {sel[0]}?",
                           callback_sim=lambda: self._executar_remocao(sel[0]))

    def _executar_remocao(self, cmp_id):
        status, msg = compra.remover_compra(cmp_id)
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
        self.txt_data.limpar()
        self.txt_valor.limpar()
        self.cb_cliente.set("")
        self.cb_super.set("")
        self._carregar_comboboxes()
