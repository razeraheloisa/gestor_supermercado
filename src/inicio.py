# ==============================
# ui/paginas/inicio.py
# Dashboard de resumo
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.theme import (
    COR_FUNDO, COR_BRANCO, COR_PRIMARIA, COR_PERIGO, COR_AVISO,
    COR_TEXTO, COR_TEXTO_CLARO, COR_SIDEBAR,
    FONTE_TITULO, FONTE_SUBTITULO, FONTE_NORMAL, FONTE_NEGRITO,
)


class _Cartao(tk.Frame):
    def __init__(self, parent, titulo, valor, cor_acento, icone):
        super().__init__(parent, bg=COR_BRANCO, padx=20, pady=18,
                         relief="flat", bd=0)

        barra = tk.Frame(self, bg=cor_acento, width=4)
        barra.pack(side="left", fill="y", padx=(0, 14))

        interior = tk.Frame(self, bg=COR_BRANCO)
        interior.pack(side="left", fill="both", expand=True)

        tk.Label(interior, text=icone, font=("Segoe UI", 22),
                 bg=COR_BRANCO).pack(anchor="w")
        tk.Label(interior, text=titulo, font=("Segoe UI", 9),
                 bg=COR_BRANCO, fg=COR_TEXTO_CLARO).pack(anchor="w", pady=(2, 0))
        self._lbl_valor = tk.Label(interior, text=str(valor),
                                   font=("Segoe UI", 26, "bold"),
                                   bg=COR_BRANCO, fg=COR_TEXTO)
        self._lbl_valor.pack(anchor="w")

    def atualizar(self, valor):
        self._lbl_valor.config(text=str(valor))


class PaginaInicio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._cartoes = {}
        self._construir()

    def _construir(self):
        # Cabeçalho
        cab = ttk.Frame(self, style="TFrame")
        cab.pack(fill="x", padx=28, pady=(28, 4))
        ttk.Label(cab, text="Dashboard", style="Titulo.TLabel").pack(side="left")

        ttk.Label(self,
                  text="Resumo do sistema em tempo real",
                  style="Info.TLabel").pack(anchor="w", padx=28)

        # Grelha de cartões
        grelha = tk.Frame(self, bg=COR_FUNDO)
        grelha.pack(fill="x", padx=28, pady=24)

        info = [
            ("clientes",      "Clientes",      "👤", COR_PRIMARIA),
            ("supermercados", "Supermercados", "🏪", "#3498DB"),
            ("categorias",    "Categorias",    "🗂️", COR_AVISO),
            ("produtos",      "Produtos",      "📦", "#9B59B6"),
            ("compras",       "Compras",       "🛒", COR_PERIGO),
        ]

        for col, (chave, titulo, icone, cor) in enumerate(info):
            cartao = _Cartao(grelha, titulo, "—", cor, icone)
            cartao.grid(row=0, column=col, padx=8, sticky="nsew")
            grelha.columnconfigure(col, weight=1)
            self._cartoes[chave] = cartao

        # Secção informativa
        secao = tk.Frame(self, bg=COR_BRANCO, padx=24, pady=20)
        secao.pack(fill="x", padx=28, pady=(0, 24))

        tk.Label(secao, text="Como utilizar",
                 font=FONTE_SUBTITULO, bg=COR_BRANCO, fg=COR_TEXTO).pack(anchor="w")

        dicas = [
            "Utilize o menu lateral para navegar entre as entidades.",
            "Clique em '+ Novo' para criar um registo.",
            "Faça duplo clique numa linha da tabela para editar.",
            "Seleccione um registo e clique 'Remover' para o eliminar.",
            "Use a barra de pesquisa para filtrar resultados.",
        ]
        for dica in dicas:
            tk.Label(secao, text=f"  •  {dica}",
                     font=FONTE_NORMAL, bg=COR_BRANCO,
                     fg=COR_TEXTO_CLARO, anchor="w").pack(fill="x", pady=2)

    def ao_mostrar(self):
        self._atualizar_contagens()

    def _atualizar_contagens(self):
        try:
            from cliente      import clientes,      carregar_clientes
            from supermercado import supermercados,  carregar_supermercado
            from categoria    import categorias,     carregar_categorias
            from produto      import produtos,       carregar_produtos
            from compra       import compras,        carregar_compras

            carregar_clientes()
            carregar_supermercado()
            carregar_categorias()
            carregar_produtos()
            carregar_compras()

            self._cartoes["clientes"].atualizar(len(clientes))
            self._cartoes["supermercados"].atualizar(len(supermercados))
            self._cartoes["categorias"].atualizar(len(categorias))
            self._cartoes["produtos"].atualizar(len(produtos))
            self._cartoes["compras"].atualizar(len(compras))
        except Exception:
            pass
