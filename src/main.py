# ==============================
# app_4.py
# ==============================
import tkinter as tk
from ui.theme import aplicar_tema
from ui.janela_principal import JanelaPrincipal

def main():
    root = tk.Tk()
    root.title("Sistema Integrado de Gestão de Supermercados")
    root.geometry("1150x700")
    root.minsize(950, 600)

    aplicar_tema(root)

    app = JanelaPrincipal(root)
    app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
