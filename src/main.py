# ==============================
# app.py
# Ponto de entrada da aplicação Tkinter
# Substitui o main.py (terminal)
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.theme import aplicar_tema
from ui.janela_principal import JanelaPrincipal


def main():
    root = tk.Tk()
    root.title("Gestão de Supermercado")
    root.geometry("1100x680")
    root.minsize(900, 580)

    aplicar_tema(root)

    app = JanelaPrincipal(root)
    app.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
