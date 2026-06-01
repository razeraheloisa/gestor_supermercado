# ==============================
# ui/theme.py
# Cores, fontes e estilos globais
# ==============================

import tkinter as tk
from tkinter import ttk

# ── Paleta de Cores (Todas que o seu projeto importa) ──────────────────
COR_FUNDO        = "#F7F8FA"
COR_BRANCO       = "#FFFFFF"
COR_BORDA        = "#DDE1E7"
COR_CABECALHO    = "#E8ECF0"

# Cores de Destaque e Estados
COR_PRIMARIA     = "#2ECC71"  # Verde
COR_PRIMARIA_ESC = "#27AE60"
COR_PERIGO       = "#E74C3C"  # Vermelho
COR_PERIGO_ESC   = "#C0392B"
COR_AVISO        = "#F39C12"  # Laranja

# Cores de Texto
COR_TEXTO        = "#2C3E50"
COR_TEXTO_CLARO  = "#7F8C8D"

# Cores da Sidebar (Menu Lateral)
COR_SIDEBAR      = "#1E2A3A"
COR_SIDEBAR_ITEM = "#2C3E50"
COR_SIDEBAR_SEL  = "#2ECC71"

# Cores das Linhas da Tabela (Alternadas)
COR_LINHA_PAR    = "#F0F4F8"
COR_LINHA_IMPAR  = "#FFFFFF"

# Outros elementos de formulário
COR_ENTRADA      = "#FFFFFF"


# ── Fontes (Todas que o seu projeto importa) ───────────────────────────
FONTE_TITULO     = ("Segoe UI", 18, "bold")
FONTE_SUBTITULO  = ("Segoe UI", 13, "bold")
FONTE_NORMAL     = ("Segoe UI", 10)
FONTE_NEGRITO    = ("Segoe UI", 10, "bold")
FONTE_PEQUENA    = ("Segoe UI", 9)
FONTE_SIDEBAR    = ("Segoe UI", 11)
FONTE_SIDEBAR_T  = ("Segoe UI", 12, "bold")
FONTE_BOTAO      = ("Segoe UI", 10, "bold")


# ── Função para Aplicar o Tema nos Componentes do Tkinter ─────────────
def aplicar_tema(root: tk.Tk):
    root.configure(bg=COR_FUNDO)

    style = ttk.Style(root)
    style.theme_use("clam")

    # Tabela (Treeview)
    style.configure("Treeview",
        background=COR_BRANCO,
        foreground=COR_TEXTO,
        fieldbackground=COR_BRANCO,
        rowheight=30,
        font=FONTE_NORMAL,
        borderwidth=0,
    )
    style.configure("Treeview.Heading",
        background=COR_CABECALHO,
        foreground=COR_TEXTO,
        font=FONTE_NEGRITO,
        relief="flat",
        padding=(8, 6),
    )
    style.map("Treeview",
        background=[("selected", COR_PRIMARIA)],
        foreground=[("selected", COR_BRANCO)],
    )
    style.map("Treeview.Heading",
        background=[("active", COR_BORDA)],
    )

    # Campos de Entrada (Entry)
    style.configure("TEntry",
        fieldbackground=COR_ENTRADA,
        foreground=COR_TEXTO,
        font=FONTE_NORMAL,
        padding=(8, 6),
        relief="flat",
        borderwidth=1,
    )
    style.map("TEntry",
        bordercolor=[("focus", COR_PRIMARIA), ("!focus", COR_BORDA)],
    )

    # Etiquetas (Labels)
    style.configure("TLabel",
        background=COR_FUNDO,
        foreground=COR_TEXTO,
        font=FONTE_NORMAL,
    )
    style.configure("Titulo.TLabel",
        background=COR_FUNDO,
        foreground=COR_TEXTO,
        font=FONTE_TITULO,
    )
    style.configure("Subtitulo.TLabel",
        background=COR_FUNDO,
        foreground=COR_TEXTO,
        font=FONTE_SUBTITULO,
    )
    style.configure("Info.TLabel",
        background=COR_FUNDO,
        foreground=COR_TEXTO_CLARO,
        font=FONTE_PEQUENA,
    )

    # Painéis (Frames)
    style.configure("TFrame", background=COR_FUNDO)
    style.configure("Card.TFrame",
        background=COR_BRANCO,
        relief="flat",
    )

    # Barras de Rolagem (Scrollbar)
    style.configure("TScrollbar",
        background=COR_BORDA,
        troughcolor=COR_FUNDO,
        borderwidth=0,
        arrowsize=12,
    )
    style.map("TScrollbar",
        background=[("active", COR_TEXTO_CLARO)],
    )

    # Abas (Notebook)
    style.configure("TNotebook",
        background=COR_FUNDO,
        borderwidth=0,
    )
    style.configure("TNotebook.Tab",
        background=COR_CABECALHO,
        foreground=COR_TEXTO,
        font=FONTE_NORMAL,
        padding=(14, 6),
    )
    style.map("TNotebook.Tab",
        background=[("selected", COR_BRANCO)],
        foreground=[("selected", COR_PRIMARIA)],
    )

    # Caixa de Seleção (Combobox)
    style.configure("TCombobox",
        fieldbackground=COR_ENTRADA,
        background=COR_ENTRADA,
        foreground=COR_TEXTO,
        font=FONTE_NORMAL,
        padding=(8, 6),
    )
