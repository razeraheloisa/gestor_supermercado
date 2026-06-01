# ==============================
# ui/janela_principal.py
# Gerenciador de navegação e layout principal
# ==============================

# Dentro de ui/janela_principal.py
import tkinter as tk
from tkinter import ttk

# Importações das páginas (devem começar sempre por ui.paginas)
from ui.paginas.inicio import PaginaInicio
from ui.paginas.categorias import PaginaCategorias
from ui.paginas.produtos import PaginaProdutos
from ui.paginas.clientes import PaginaClientes
from ui.paginas.compras import PaginaCompras
from ui.paginas.supermercados import PaginaSupermercados


class JanelaPrincipal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        # Dicionário para rastrear os botões do menu lateral
        self._botoes_menu = {}
        self._pagina_atual = None

        # ── Layout Base (Menu Lateral + Área de Conteúdo) ──────────────────
        self._sidebar = tk.Frame(self, bg=COR_SIDEBAR, width=240)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        self._conteudo = ttk.Frame(self, style="TFrame")
        self._conteudo.pack(side="right", fill="both", expand=True)

        self._construir_sidebar()

        # Iniciar na página de boas-vindas / dashboard
        self._ir_para("inicio", PaginaInicio)

    def _construir_sidebar(self):
        # Título do Sistema
        lbl_titulo = tk.Label(
            self._sidebar, text="SUPERMERCADO", bg=COR_SIDEBAR, fg=COR_BRANCO,
            font=FONTE_SIDEBAR_T, pady=25
        )
        lbl_titulo.pack(fill="x")

        # Itens de Menu (Chave: (Texto, Classe_da_Pagina))
        itens = [
            ("inicio", "Dashboard", PaginaInicio),
            ("categorias", "Categorias", PaginaCategorias),
            ("produtos", "Produtos", PaginaProdutos),
            ("clientes", "Clientes", PaginaClientes),
            ("compras", "Compras", PaginaCompras),
        ]

        for chave, texto, classe_pagina in itens:
            btn = tk.Button(
                self._sidebar, text=f"  {texto}", anchor="w", bg=COR_SIDEBAR,
                fg=COR_TEXTO_CLARO, font=FONTE_SIDEBAR, relief="flat",
                activebackground=COR_SIDEBAR_ITEM, activeforeground=COR_BRANCO,
                cursor="hand2", bd=0, highlightthickness=0, pady=12
            )
            btn.config(command=lambda c=chave, cls=classe_pagina: self._ir_para(c, cls))
            btn.pack(fill="x", padx=10, pady=2)
            self._botoes_menu[chave] = btn

    def _ir_para(self, chave, classe_pagina):
        # Atualizar destaque visual do menu lateral
        for k, btn in self._botoes_menu.items():
            if k == chave:
                btn.config(bg=COR_SIDEBAR_ITEM, fg=COR_SIDEBAR_SEL)
            else:
                btn.config(bg=COR_SIDEBAR, fg=COR_TEXTO_CLARO)

        # Destruir a página anterior, se existir
        if self._pagina_atual:
            self._pagina_atual.destroy()

        # Instanciar e empacotar a nova página na área de conteúdo
        self._pagina_atual = classe_pagina(self._conteudo)
        self._pagina_atual.pack(fill="both", expand=True)
