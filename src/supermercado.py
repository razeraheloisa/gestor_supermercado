# ==============================
# ui/paginas/supermercados.py
# ==============================

from ui.paginas.base import PaginaBase
from ui.widgets import CampoForm


class PaginaSupermercados(PaginaBase):
    TITULO  = "Supermercados"
    COLUNAS = [
        ("id",     "ID",     70),
        ("numero", "Número", 100),
        ("morada", "Morada", 280),
        ("nif",    "NIF",    110),
    ]

    def _construir_campos(self, frame):
        self._campo_numero = CampoForm(frame, "Número")
        self._campo_numero.pack(fill="x", pady=6)

        self._campo_morada = CampoForm(frame, "Morada")
        self._campo_morada.pack(fill="x", pady=6)

        self._campo_nif    = CampoForm(frame, "NIF",
                                       placeholder="9 dígitos")
        self._campo_nif.pack(fill="x", pady=6)

    def _carregar_tabela(self, termo=""):
        from supermercado import supermercados, carregar_supermercado

        carregar_supermercado()

        fonte = {
            sid: d for sid, d in supermercados.items()
            if not termo or termo.lower() in d["morada"].lower()
               or termo.lower() in d["numero"].lower()
               or termo in d["nif"]
        }

        linhas = [
            (sid, d["numero"], d["morada"], d["nif"])
            for sid, d in fonte.items()
        ]
        self._tabela.preencher(linhas)

    def _guardar(self):
        from supermercado import criar_supermercado, atualizar_supermercado

        numero = self._campo_numero.get()
        morada = self._campo_morada.get()
        nif    = self._campo_nif.get()

        if self._id_seleccionado:
            codigo, resultado = atualizar_supermercado(
                self._id_seleccionado, numero=numero, morada=morada, nif=nif)
        else:
            codigo, resultado = criar_supermercado(numero, morada, nif)

        if codigo in (200, 201):
            self._feedback.sucesso(
                f"Supermercado {'atualizado' if self._id_seleccionado else 'criado'} com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback_form.erro(resultado)

    def _remover(self):
        from supermercado import remover_supermercado

        codigo, resultado = remover_supermercado(self._id_seleccionado)
        if codigo == 200:
            self._feedback.sucesso("Supermercado removido com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback.erro(resultado)

    def _preencher_campos(self, valores):
        self._campo_numero.set(valores[1])
        self._campo_morada.set(valores[2])
        self._campo_nif.set(valores[3])

    def _limpar_campos(self):
        self._campo_numero.limpar()
        self._campo_morada.limpar()
        self._campo_nif.limpar()
