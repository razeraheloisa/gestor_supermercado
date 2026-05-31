# ==============================
# ui/paginas/clientes.py
# ==============================

import tkinter as tk
from ui.paginas.base import PaginaBase
from ui.widgets import CampoForm


class PaginaClientes(PaginaBase):
    TITULO  = "Clientes"
    COLUNAS = [
        ("id",       "ID",       70),
        ("nome",     "Nome",     200),
        ("contacto", "Contacto", 110),
        ("email",    "Email",    200),
        ("nif",      "NIF",      100),
    ]

    # ── Campos do formulário ─────────────────────────────
    def _construir_campos(self, frame):
        self._campo_nome     = CampoForm(frame, "Nome")
        self._campo_nome.pack(fill="x", pady=6)

        self._campo_contacto = CampoForm(frame, "Contacto",
                                         placeholder="ex: 912345678")
        self._campo_contacto.pack(fill="x", pady=6)

        self._campo_email    = CampoForm(frame, "Email", obrigatorio=False,
                                         placeholder="ex: nome@dominio.pt")
        self._campo_email.pack(fill="x", pady=6)

        self._campo_nif      = CampoForm(frame, "NIF", obrigatorio=False,
                                         placeholder="9 dígitos")
        self._campo_nif.pack(fill="x", pady=6)

    # ── Tabela ───────────────────────────────────────────
    def _carregar_tabela(self, termo=""):
        from cliente import listar_clientes, pesquisar_cliente, clientes, carregar_clientes

        carregar_clientes()

        if termo:
            codigo, dados = pesquisar_cliente(termo)
            fonte = dados if codigo == 200 else {}
        else:
            fonte = clientes

        linhas = [
            (cid,
             d["nome"],
             d["contacto"],
             d["email"] or "—",
             d["nif"]   or "—")
            for cid, d in fonte.items()
        ]
        self._tabela.preencher(linhas)

    # ── Guardar ──────────────────────────────────────────
    def _guardar(self):
        from cliente import criar_cliente, atualizar_cliente

        nome     = self._campo_nome.get()
        contacto = self._campo_contacto.get()
        email    = self._campo_email.get()
        nif      = self._campo_nif.get()

        if self._id_seleccionado:
            codigo, resultado = atualizar_cliente(
                self._id_seleccionado,
                nome=nome, contacto=contacto, email=email, nif=nif,
            )
        else:
            codigo, resultado = criar_cliente(nome, contacto, email, nif)

        if codigo in (200, 201):
            self._feedback.sucesso(
                f"Cliente {'atualizado' if self._id_seleccionado else 'criado'} com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback_form.erro(resultado)

    # ── Remover ──────────────────────────────────────────
    def _remover(self):
        from cliente import remover_cliente

        codigo, resultado = remover_cliente(self._id_seleccionado)
        if codigo == 200:
            self._feedback.sucesso("Cliente removido com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback.erro(resultado)

    # ── Preencher / limpar campos ────────────────────────
    def _preencher_campos(self, valores):
        # valores = (id, nome, contacto, email, nif)
        self._campo_nome.set(valores[1])
        self._campo_contacto.set(valores[2])
        self._campo_email.set(valores[3] if valores[3] != "—" else "")
        self._campo_nif.set(valores[4]   if valores[4] != "—" else "")

    def _limpar_campos(self):
        self._campo_nome.limpar()
        self._campo_contacto.limpar()
        self._campo_email.limpar()
        self._campo_nif.limpar()
