# ==============================
# ui/janela_principal.py
# Layout raiz: sidebar + área de conteúdo
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.theme import (
    COR_SIDEBAR, COR_SIDEBAR_ITEM, COR_SIDEBAR_SEL, COR_BRANCO,
    COR_TEXTO_CLARO, COR_FUNDO, COR_BORDA,
    FONTE_SIDEBAR, FONTE_SIDEBAR_T, FONTE_PEQUENA,
)


SECOES = [
    ("Início",         "inicio"),
    ("👤",  "Clientes",       "clientes"),
    ("Supermercados",  "supermercados"),
    ("Categorias",     "categorias"),
    ("Produtos",       "produtos"),
    ("🛒",  "Compras",        "compras"),
]


class JanelaPrincipal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        self._secao_atual = None
        self._botoes_nav = {}
        self._frames_conteudo = {}

        self._construir_sidebar()
        self._construir_conteudo()
        self._navegar("inicio")

    # ── Sidebar ─────────────────────────────────────────
    def _construir_sidebar(self):
        sidebar = tk.Frame(self, bg=COR_SIDEBAR, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo / título
        topo = tk.Frame(sidebar, bg=COR_SIDEBAR, pady=24)
        topo.pack(fill="x")
        tk.Label(topo, text="🛒", font=("Segoe UI", 28),
                 bg=COR_SIDEBAR, fg=COR_SIDEBAR_SEL).pack()
        tk.Label(topo, text="Gestão", font=("Segoe UI", 13, "bold"),
                 bg=COR_SIDEBAR, fg=COR_BRANCO).pack()
        tk.Label(topo, text="de Supermercado", font=("Segoe UI", 9),
                 bg=COR_SIDEBAR, fg=COR_TEXTO_CLARO).pack()

        separador = tk.Frame(sidebar, bg=COR_SIDEBAR_ITEM, height=1)
        separador.pack(fill="x", padx=16, pady=8)

        # Botões de navegação
        nav = tk.Frame(sidebar, bg=COR_SIDEBAR)
        nav.pack(fill="both", expand=True, pady=8)

        for icone, titulo, chave in SECOES:
            btn = _BotaoNav(nav, icone, titulo,
                            comando=lambda c=chave: self._navegar(c))
            btn.pack(fill="x", padx=10, pady=2)
            self._botoes_nav[chave] = btn

        # Rodapé
        rodape = tk.Frame(sidebar, bg=COR_SIDEBAR, pady=12)
        rodape.pack(fill="x", side="bottom")
        tk.Label(rodape, text="v1.0  •  2026",
                 font=("Segoe UI", 8), bg=COR_SIDEBAR,
                 fg=COR_TEXTO_CLARO).pack()

    # ── Área de conteúdo ────────────────────────────────
    def _construir_conteudo(self):
        self._area = tk.Frame(self, bg=COR_FUNDO)
        self._area.pack(side="left", fill="both", expand=True)

        # Importações tardias para evitar circulares
        from ui.paginas.inicio        import PaginaInicio
        from ui.paginas.clientes      import PaginaClientes
        from ui.paginas.supermercados import PaginaSupermercados
        from ui.paginas.categorias    import PaginaCategorias
        from ui.paginas.produtos      import PaginaProdutos
        from ui.paginas.compras       import PaginaCompras

        paginas = {
            "inicio":        PaginaInicio,
            "clientes":      PaginaClientes,
            "supermercados": PaginaSupermercados,
            "categorias":    PaginaCategorias,
            "produtos":      PaginaProdutos,
            "compras":       PaginaCompras,
        }

        for chave, Cls in paginas.items():
            frame = Cls(self._area)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._frames_conteudo[chave] = frame

    # ── Navegação ────────────────────────────────────────
    def _navegar(self, chave):
        if self._secao_atual == chave:
            return

        # Atualizar sidebar
        if self._secao_atual and self._secao_atual in self._botoes_nav:
            self._botoes_nav[self._secao_atual].desseleccionar()
        self._botoes_nav[chave].seleccionar()
        self._secao_atual = chave

        # Mostrar página
        frame = self._frames_conteudo.get(chave)
        if frame:
            frame.lift()
            if hasattr(frame, "ao_mostrar"):
                frame.ao_mostrar()


# ── Botão de navegação na sidebar ───────────────────────
class _BotaoNav(tk.Frame):
    def __init__(self, parent, icone, titulo, comando):
        super().__init__(parent, bg=COR_SIDEBAR, cursor="hand2")

        self._comando = comando
        self._seleccionado = False

        self._inner = tk.Frame(self, bg=COR_SIDEBAR, padx=14, pady=10)
        self._inner.pack(fill="x")

        self._lbl_icone = tk.Label(self._inner, text=icone,
                                   font=("Segoe UI", 13),
                                   bg=COR_SIDEBAR, fg=COR_BRANCO)
        self._lbl_icone.pack(side="left")

        self._lbl_titulo = tk.Label(self._inner, text=f"  {titulo}",
                                    font=FONTE_SIDEBAR,
                                    bg=COR_SIDEBAR, fg=COR_TEXTO_CLARO,
                                    anchor="w")
        self._lbl_titulo.pack(side="left", fill="x", expand=True)

        self._indicador = tk.Frame(self, bg=COR_SIDEBAR, width=4)
        self._indicador.pack(side="right", fill="y")

        for widget in [self, self._inner, self._lbl_icone, self._lbl_titulo]:
            widget.bind("<Button-1>", lambda e: comando())
            widget.bind("<Enter>", self._hover_on)
            widget.bind("<Leave>", self._hover_off)

    def seleccionar(self):
        self._seleccionado = True
        cor_fundo = COR_SIDEBAR_ITEM
        for w in [self, self._inner, self._lbl_icone, self._lbl_titulo]:
            w.config(bg=cor_fundo)
        self._lbl_titulo.config(fg=COR_BRANCO)
        self._indicador.config(bg=COR_SIDEBAR_SEL)

    def desseleccionar(self):
        self._seleccionado = False
        for w in [self, self._inner, self._lbl_icone, self._lbl_titulo]:
            w.config(bg=COR_SIDEBAR)
        self._lbl_titulo.config(fg=COR_TEXTO_CLARO)
        self._indicador.config(bg=COR_SIDEBAR)

    def _hover_on(self, _):
        if not self._seleccionado:
            for w in [self, self._inner, self._lbl_icone, self._lbl_titulo]:
                w.config(bg=COR_SIDEBAR_ITEM)

    def _hover_off(self, _):
        if not self._seleccionado:
            for w in [self, self._inner, self._lbl_icone, self._lbl_titulo]:
                w.config(bg=COR_SIDEBAR)
