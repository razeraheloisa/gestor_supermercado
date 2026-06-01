import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import tkinter as tk
from tkinter import ttk
from ui.widgets import CampoForm, BotaoPrimario, BotaoPerigo, Tabela, MensagemFeedback, DialogoConfirmacao, BarraPesquisa
import cliente

class PaginaClientes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        topo = ttk.Frame(self, style="TFrame")
        topo.pack(fill="x", padx=30, pady=20)
        ttk.Label(topo, text="Gestão de Clientes", style="Titulo.TLabel").pack(side="left")
        self.feedback = MensagemFeedback(topo)
        self.feedback.pack(side="right", padx=10)

        corpo = ttk.Frame(self, style="TFrame")
        corpo.pack(fill="both", expand=True, padx=30, pady=10)

        self.frame_form = ttk.LabelFrame(corpo, text=" Ficha de Cliente ", style="TFrame", padding=15)
        self.frame_form.pack(side="left", fill="y", padx=(0, 20))

        self.txt_id = CampoForm(self.frame_form, label="ID Cliente", obrigatorio=False)
        self.txt_id._entry.config(state="disabled")
        self.txt_id.pack(fill="x", pady=2)

        self.txt_nome = CampoForm(self.frame_form, label="Nome Completo")
        self.txt_nome.pack(fill="x", pady=2)

        self.txt_contacto = CampoForm(self.frame_form, label="Contacto Telefónico", placeholder="9 dígitos")
        self.txt_contacto.pack(fill="x", pady=2)

        self.txt_email = CampoForm(self.frame_form, label="E-mail", obrigatorio=False, placeholder="nome@provedor.pt")
        self.txt_email.pack(fill="x", pady=2)

        self.txt_nif = CampoForm(self.frame_form, label="NIF", obrigatorio=False, placeholder="9 dígitos fiscais")
        self.txt_nif.pack(fill="x", pady=2)

        btn_box = ttk.Frame(self.frame_form, style="TFrame")
        btn_box.pack(fill="x", pady=10)
        BotaoPrimario(btn_box, "Salvar", comando=self._submeter).pack(side="left", expand=True, fill="x", padx=2)
        BotaoPerigo(btn_box, "Limpar", comando=self._limpar_formulario).pack(side="left", expand=True, fill="x", padx=2)

        frame_tabela = ttk.Frame(corpo, style="TFrame")
        frame_tabela.pack(side="right", fill="both", expand=True)

        # Barra de Pesquisa Dinâmica integrada à tabela (funciona via trace na variável)
        self.pesquisa = BarraPesquisa(frame_tabela, placeholder="Filtrar por nome ou NIF...",
                                      comando=self._filtrar_grid)
        self.pesquisa.pack(fill="x", pady=(0, 10))

        colunas = [("id", "ID", 70), ("nome", "Nome", 200), ("contacto", "Contacto", 100), ("email", "Email", 180),
                   ("nif", "NIF", 100)]
        self.tabela = Tabela(frame_tabela, colunas=colunas)
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind_duplo_clique(self._carregar_registo)

        BotaoPerigo(frame_tabela, "Remover Cliente", comando=self._confirmar_remocao).pack(anchor="e", pady=10)

        self._atualizar_grid()

    def _atualizar_grid(self, dados_customizados=None):
        dados_tabela = []
        fonte = dados_customizados if dados_customizados is not None else cliente.clientes.items()
        for cid, d in fonte:
            dados_tabela.append((cid, d["nome"], d["contacto"], d["email"] or "-", d["nif"] or "-"))
        self.tabela.preencher(dados_tabela)

    def _filtrar_grid(self, termo):
        if not termo.strip() or termo == "Filtrar por nome ou NIF...":
            self._atualizar_grid()
            return
        termo = termo.lower()
        filtrados = [(cid, d) for cid, d in cliente.clientes.items() if termo in d["nome"].lower() or termo == d["nif"]]
        self._atualizar_grid(filtrados)

    def _submeter(self):
        id_atual = self.txt_id.get()
        nome = self.txt_nome.get()
        contacto = self.txt_contacto.get()
        email = self.txt_email.get()
        nif = self.txt_nif.get()

        if id_atual == "":
            status, msg = cliente.criar_cliente(nome, contacto, email, nif)
        else:
            status, msg = cliente.atualizar_cliente(id_atual, nome, contacto, email, nif)

        if status in (200, 201):
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _carregar_registo(self):
        sel = self.tabela.seleccionado()
        if sel:
            cid = sel[0]
            d = cliente.clientes[cid]
            self.txt_id._entry.config(state="normal")
            self.txt_id.set(cid)
            self.txt_id._entry.config(state="disabled")
            self.txt_nome.set(d["nome"])
            self.txt_contacto.set(d["contacto"])
            self.txt_email.set(d["email"])
            self.txt_nif.set(d["nif"])

    def _confirmar_remocao(self):
        sel = self.tabela.seleccionado()
        if not sel: return
        DialogoConfirmacao(self, "Remover Cliente", f"Remover o cliente {sel[1]}?",
                           callback_sim=lambda: self._executar_remocao(sel[0]))

    def _executar_remocao(self, cid):
        status, msg = cliente.remover_cliente(cid)
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
        self.txt_contacto.limpar()
        self.txt_email.limpar()
        self.txt_nif.limpar()
