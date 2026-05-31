# ==============================
# ui/paginas/base.py
# Classe base para páginas CRUD
# Fornece: cabeçalho, tabela, barra de pesquisa,
#          botões de acção, painel lateral de formulário
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.theme import (
    COR_FUNDO, COR_BRANCO, COR_BORDA, COR_TEXTO, COR_PRIMARIA,
    FONTE_TITULO, FONTE_SUBTITULO, FONTE_NORMAL, FONTE_NEGRITO, FONTE_PEQUENA,
)
from ui.widgets import (
    BotaoPrimario, BotaoPerigo, BotaoSecundario,
    Tabela, BarraPesquisa, MensagemFeedback, DialogoConfirmacao,
)


class PaginaBase(ttk.Frame):
    """
    Layout padrão:
    ┌─────────────────────────────────────────────┐
    │  Cabeçalho (título + botão Novo)            │
    ├──────────────────────┬──────────────────────┤
    │  Pesquisa + Tabela   │  Painel formulário   │
    └──────────────────────┴──────────────────────┘
    """

    TITULO = "Entidade"
    COLUNAS = []          # lista de (id, título, largura)

    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._painel_aberto = False
        self._id_seleccionado = None

        self._construir_layout()
        self._construir_formulario_interno()

    # ── Layout principal ─────────────────────────────────
    def _construir_layout(self):
        # Cabeçalho
        cab = ttk.Frame(self, style="TFrame")
        cab.pack(fill="x", padx=28, pady=(24, 0))

        ttk.Label(cab, text=self.TITULO, style="Titulo.TLabel").pack(side="left")

        self._btn_novo = BotaoPrimario(cab, f"+ Novo",
                                       comando=self._abrir_form_novo)
        self._btn_novo.pack(side="right")

        # Feedback
        self._feedback = MensagemFeedback(self)
        self._feedback.pack(fill="x", padx=28, pady=(6, 0))

        # Corpo: tabela + painel lateral
        corpo = ttk.Frame(self, style="TFrame")
        corpo.pack(fill="both", expand=True, padx=28, pady=16)

        # Lado esquerdo: pesquisa + tabela
        self._lado_esq = ttk.Frame(corpo, style="TFrame")
        self._lado_esq.pack(side="left", fill="both", expand=True)

        self._barra_pesquisa = BarraPesquisa(
            self._lado_esq, placeholder="Pesquisar...",
            comando=self._ao_pesquisar,
        )
        self._barra_pesquisa.pack(fill="x", pady=(0, 10))

        self._tabela = Tabela(self._lado_esq, colunas=self.COLUNAS)
        self._tabela.pack(fill="both", expand=True)
        self._tabela.bind_duplo_clique(self._ao_duplo_clique)

        # Botões de acção abaixo da tabela
        bts_tabela = ttk.Frame(self._lado_esq, style="TFrame")
        bts_tabela.pack(fill="x", pady=(10, 0))

        self._btn_editar = BotaoSecundario(bts_tabela, "✏  Editar",
                                           comando=self._abrir_form_editar)
        self._btn_editar.pack(side="left", padx=(0, 8))

        self._btn_remover = BotaoPerigo(bts_tabela, "🗑  Remover",
                                        comando=self._confirmar_remover)
        self._btn_remover.pack(side="left")

        # Lado direito: painel formulário (inicialmente oculto)
        self._painel = tk.Frame(corpo, bg=COR_BRANCO, width=320,
                                relief="flat", bd=0)
        # Não é mostrado ainda

    # ── Painel de formulário ─────────────────────────────
    def _construir_formulario_interno(self):
        """Subclasses constroem campos aqui."""
        pass

    def _abrir_painel(self, titulo_form):
        if not self._painel_aberto:
            self._painel.pack(side="right", fill="y", padx=(16, 0))
            self._painel_aberto = True

        # Limpar painel
        for w in self._painel.winfo_children():
            w.destroy()

        # Cabeçalho do painel
        cab = tk.Frame(self._painel, bg=COR_PRIMARIA, pady=14)
        cab.pack(fill="x")
        tk.Label(cab, text=titulo_form, font=FONTE_SUBTITULO,
                 bg=COR_PRIMARIA, fg=COR_BRANCO).pack(padx=16)

        # Área de campos (scroll se necessário)
        self._frame_campos = tk.Frame(self._painel, bg=COR_BRANCO)
        self._frame_campos.pack(fill="both", expand=True, padx=16, pady=12)

        # Subclasses preenchem os campos
        self._construir_campos(self._frame_campos)

        # Botões do formulário
        bts = tk.Frame(self._painel, bg=COR_BRANCO, pady=12)
        bts.pack(fill="x", padx=16)

        BotaoPrimario(bts, "Guardar", comando=self._guardar,
                      largura=14).pack(side="left", padx=(0, 8))
        BotaoSecundario(bts, "Cancelar", comando=self._fechar_painel,
                        largura=10).pack(side="left")

        self._feedback_form = MensagemFeedback(self._painel)
        self._feedback_form.pack(fill="x", padx=16, pady=(0, 8))

    def _fechar_painel(self):
        if self._painel_aberto:
            self._painel.pack_forget()
            self._painel_aberto = False
            self._id_seleccionado = None

    # ── Métodos para as subclasses implementarem ─────────
    def _construir_campos(self, frame):
        """Criar os CampoForm dentro de frame."""
        pass

    def _guardar(self):
        """Chamar criar_* ou atualizar_* e dar feedback."""
        pass

    def _carregar_tabela(self, termo=""):
        """Preencher self._tabela com dados."""
        pass

    def _ao_pesquisar(self, termo):
        self._carregar_tabela(termo)

    def _abrir_form_novo(self):
        self._id_seleccionado = None
        self._abrir_painel(f"Novo — {self.TITULO}")
        self._limpar_campos()

    def _abrir_form_editar(self):
        sel = self._tabela.seleccionado()
        if not sel:
            self._feedback.aviso("Seleccione um registo para editar.")
            return
        self._id_seleccionado = sel[0]
        self._abrir_painel(f"Editar — {self.TITULO}")
        self._preencher_campos(sel)

    def _ao_duplo_clique(self):
        self._abrir_form_editar()

    def _confirmar_remover(self):
        sel = self._tabela.seleccionado()
        if not sel:
            self._feedback.aviso("Seleccione um registo para remover.")
            return
        self._id_seleccionado = sel[0]
        DialogoConfirmacao(
            self,
            titulo="Confirmar remoção",
            mensagem=f"Tem a certeza que quer remover\n'{self._id_seleccionado}'?",
            callback_sim=self._remover,
        )

    def _remover(self):
        pass

    def _limpar_campos(self):
        pass

    def _preencher_campos(self, valores):
        pass

    def ao_mostrar(self):
        """Chamado quando a página fica visível."""
        self._fechar_painel()
        self._carregar_tabela()
