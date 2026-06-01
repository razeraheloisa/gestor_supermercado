import tkinter as tk
from tkinter import ttk
from ui.theme import FONTE_TITULO, COR_BRANCO, COR_TEXTO, COR_TEXTO_CLARO, FONTE_SUBTITULO

# ── FORÇAR O CAMINHO DA RAIZ DIRETAMENTE NO FICHEIRO QUE DÁ ERRO ──
import os
import sys
# Descobre onde está a raiz ("Supermercado - Cópia") recuando duas pastas
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if raiz_projeto not in sys.path:
    sys.path.insert(0, raiz_projeto)
# ─────────────────────────────────────────────────────────────────

# Agora o Python é obrigado a encontrar os ficheiros na raiz do projeto:
import categoria
import produto
import cliente
import compra
import supermercado

class PaginaInicio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        ttk.Label(self, text="Painel de Controlo", style="Titulo.TLabel").pack(anchor="w", padx=30, pady=30)

        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="x", padx=30)

        # Indicadores baseados no tamanho dos dicionários de dados
        self._criar_card(container, "Categorias", len(categoria.categorias), 0)
        self._criar_card(container, "Produtos", len(produto.produtos), 1)
        self._criar_card(container, "Clientes", len(cliente.clientes), 2)
        self._criar_card(container, "Compras Registadas", len(compra.compras), 3)

    def _criar_card(self, parent, titulo, valor, col):
        card = tk.Frame(parent, bg=COR_BRANCO, padx=20, pady=20, highlightbackground="#E0E0E0", highlightthickness=1)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        tk.Label(card, text=str(valor), bg=COR_BRANCO, fg=COR_TEXTO, font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(card, text=titulo, bg=COR_BRANCO, fg=COR_TEXTO_CLARO, font=FONTE_SUBTITULO).pack(anchor="w",
                                                                                                  pady=(5, 0))
