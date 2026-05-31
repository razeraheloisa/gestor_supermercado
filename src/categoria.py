# ==============================
# ui/paginas/categorias.py
# ==============================

from ui.paginas.base import PaginaBase
from ui.widgets import CampoForm


class PaginaCategorias(PaginaBase):
    TITULO  = "Categorias"
    COLUNAS = [
        ("id",        "ID",        80),
        ("nome",      "Nome",      160),
        ("descricao", "Descrição", 320),
    ]

    def _construir_campos(self, frame):
        self._campo_nome     = CampoForm(frame, "Nome da categoria")
        self._campo_nome.pack(fill="x", pady=6)

        self._campo_descricao = CampoForm(frame, "Descrição")
        self._campo_descricao.pack(fill="x", pady=6)

    def _carregar_tabela(self, termo=""):
        from categoria import categorias, carregar_categorias

        carregar_categorias()

        fonte = {
            cid: d for cid, d in categorias.items()
            if not termo or termo.lower() in d["nome_categoria"].lower()
               or termo.lower() in d["descricao"].lower()
        }

        linhas = [
            (cid, d["nome_categoria"], d["descricao"])
            for cid, d in fonte.items()
        ]
        self._tabela.preencher(linhas)

    def _guardar(self):
        from categoria import criar_categoria, atualizar_categoria

        nome     = self._campo_nome.get()
        descricao = self._campo_descricao.get()

        if self._id_seleccionado:
            codigo, resultado = atualizar_categoria(
                self._id_seleccionado, nome_categoria=nome, descricao=descricao)
        else:
            codigo, resultado = criar_categoria(nome, descricao)

        if codigo in (200, 201):
            self._feedback.sucesso(
                f"Categoria {'atualizada' if self._id_seleccionado else 'criada'} com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback_form.erro(resultado)

    def _remover(self):
        from categoria import remover_categoria

        codigo, resultado = remover_categoria(self._id_seleccionado)
        if codigo == 200:
            self._feedback.sucesso("Categoria removida com sucesso.")
            self._fechar_painel()
            self._carregar_tabela()
        else:
            self._feedback.erro(resultado)

    def _preencher_campos(self, valores):
        self._campo_nome.set(valores[1])
        self._campo_descricao.set(valores[2])

    def _limpar_campos(self):
        self._campo_nome.limpar()
        self._campo_descricao.limpar()
