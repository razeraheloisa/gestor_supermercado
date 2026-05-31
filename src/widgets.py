# ==============================
# ui/widgets.py
# Widgets reutilizáveis da aplicação
# ==============================

import tkinter as tk
from tkinter import ttk
from ui.theme import (
    COR_PRIMARIA, COR_PRIMARIA_ESC, COR_PERIGO, COR_PERIGO_ESC,
    COR_AVISO, COR_BRANCO, COR_TEXTO, COR_TEXTO_CLARO, COR_BORDA,
    COR_FUNDO, COR_CABECALHO, COR_LINHA_PAR, COR_LINHA_IMPAR,
    FONTE_BOTAO, FONTE_NORMAL, FONTE_NEGRITO, FONTE_PEQUENA,
    FONTE_SUBTITULO,
)


# ── Botão primário (verde) ───────────────────────────────
class BotaoPrimario(tk.Button):
    def __init__(self, parent, texto, comando=None, largura=None, **kwargs):
        super().__init__(
            parent,
            text=texto,
            command=comando,
            bg=COR_PRIMARIA,
            fg=COR_BRANCO,
            activebackground=COR_PRIMARIA_ESC,
            activeforeground=COR_BRANCO,
            font=FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=8,
            borderwidth=0,
            **kwargs,
        )
        if largura:
            self.config(width=largura)
        self.bind("<Enter>", lambda e: self.config(bg=COR_PRIMARIA_ESC))
        self.bind("<Leave>", lambda e: self.config(bg=COR_PRIMARIA))


# ── Botão de perigo (vermelho) ───────────────────────────
class BotaoPerigo(tk.Button):
    def __init__(self, parent, texto, comando=None, largura=None, **kwargs):
        super().__init__(
            parent,
            text=texto,
            command=comando,
            bg=COR_PERIGO,
            fg=COR_BRANCO,
            activebackground=COR_PERIGO_ESC,
            activeforeground=COR_BRANCO,
            font=FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=8,
            borderwidth=0,
            **kwargs,
        )
        if largura:
            self.config(width=largura)
        self.bind("<Enter>", lambda e: self.config(bg=COR_PERIGO_ESC))
        self.bind("<Leave>", lambda e: self.config(bg=COR_PERIGO))


# ── Botão secundário (contorno) ──────────────────────────
class BotaoSecundario(tk.Button):
    def __init__(self, parent, texto, comando=None, largura=None, **kwargs):
        super().__init__(
            parent,
            text=texto,
            command=comando,
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            activebackground=COR_BORDA,
            activeforeground=COR_TEXTO,
            font=FONTE_BOTAO,
            relief="solid",
            cursor="hand2",
            padx=16,
            pady=7,
            borderwidth=1,
            **kwargs,
        )
        if largura:
            self.config(width=largura)


# ── Campo de entrada com label ───────────────────────────
class CampoForm(ttk.Frame):
    """Label + Entry numa linha, devolvendo o valor via .get()"""

    def __init__(self, parent, label, obrigatorio=True, placeholder="", **kwargs):
        super().__init__(parent, style="TFrame", **kwargs)

        self._obrigatorio = obrigatorio

        topo = ttk.Frame(self, style="TFrame")
        topo.pack(fill="x")

        lbl_text = label + (" *" if obrigatorio else "")
        ttk.Label(topo, text=lbl_text, style="TLabel",
                  font=FONTE_NEGRITO).pack(side="left")
        if not obrigatorio:
            ttk.Label(topo, text=" (opcional)", style="Info.TLabel").pack(side="left")

        self._var = tk.StringVar()
        self._entry = ttk.Entry(self, textvariable=self._var,
                                font=FONTE_NORMAL)
        self._entry.pack(fill="x", pady=(4, 0), ipady=4)

        self._lbl_erro = ttk.Label(self, text="", foreground=COR_PERIGO,
                                   font=FONTE_PEQUENA, style="TLabel")
        self._lbl_erro.pack(fill="x")

        if placeholder:
            self._entry.insert(0, placeholder)
            self._entry.config(foreground=COR_TEXTO_CLARO)
            self._entry.bind("<FocusIn>", self._limpar_placeholder)
            self._entry.bind("<FocusOut>", self._repor_placeholder)
            self._placeholder = placeholder
        else:
            self._placeholder = None

    def _limpar_placeholder(self, _):
        if self._var.get() == self._placeholder:
            self._entry.delete(0, "end")
            self._entry.config(foreground=COR_TEXTO)

    def _repor_placeholder(self, _):
        if self._var.get() == "" and self._placeholder:
            self._entry.insert(0, self._placeholder)
            self._entry.config(foreground=COR_TEXTO_CLARO)

    def get(self):
        val = self._var.get()
        if val == self._placeholder:
            return ""
        return val

    def set(self, valor):
        self._var.set(valor)
        self._entry.config(foreground=COR_TEXTO)

    def erro(self, mensagem):
        self._lbl_erro.config(text=f"  ✖  {mensagem}")
        self._entry.config(style="TEntry")  # pode adicionar estilo de erro

    def limpar_erro(self):
        self._lbl_erro.config(text="")

    def limpar(self):
        self._var.set("")
        self._lbl_erro.config(text="")
        if self._placeholder:
            self._entry.insert(0, self._placeholder)
            self._entry.config(foreground=COR_TEXTO_CLARO)

    def focar(self):
        self._entry.focus_set()


# ── Tabela (Treeview) com scrollbar ─────────────────────
class Tabela(ttk.Frame):
    def __init__(self, parent, colunas: list[tuple], **kwargs):
        """
        colunas: lista de (id, titulo, largura)
        """
        super().__init__(parent, style="TFrame", **kwargs)

        self._tree = ttk.Treeview(
            self,
            columns=[c[0] for c in colunas],
            show="headings",
            selectmode="browse",
        )

        for col_id, titulo, largura in colunas:
            self._tree.heading(col_id, text=titulo,
                               command=lambda c=col_id: self._ordenar(c, False))
            self._tree.column(col_id, width=largura, minwidth=40, anchor="w")

        scroll_y = ttk.Scrollbar(self, orient="vertical",
                                 command=self._tree.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal",
                                 command=self._tree.xview)
        self._tree.configure(yscrollcommand=scroll_y.set,
                             xscrollcommand=scroll_x.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._tree.tag_configure("par",   background=COR_LINHA_PAR)
        self._tree.tag_configure("impar", background=COR_LINHA_IMPAR)

        self._sort_col = None
        self._sort_rev = False

    def preencher(self, linhas: list[tuple]):
        """Limpa e repreenche a tabela. linhas: lista de tuplos com os valores."""
        self._tree.delete(*self._tree.get_children())
        for i, linha in enumerate(linhas):
            tag = "par" if i % 2 == 0 else "impar"
            self._tree.insert("", "end", iid=str(i), values=linha, tags=(tag,))

    def seleccionado(self):
        """Devolve os valores da linha seleccionada ou None."""
        sel = self._tree.selection()
        if not sel:
            return None
        return self._tree.item(sel[0], "values")

    def bind_duplo_clique(self, callback):
        self._tree.bind("<Double-1>", lambda e: callback())

    def _ordenar(self, col, reverso):
        dados = [(self._tree.set(k, col), k) for k in self._tree.get_children("")]
        try:
            dados.sort(key=lambda t: float(t[0]), reverse=reverso)
        except ValueError:
            dados.sort(key=lambda t: t[0].lower(), reverse=reverso)
        for idx, (_, k) in enumerate(dados):
            self._tree.move(k, "", idx)
            tag = "par" if idx % 2 == 0 else "impar"
            self._tree.item(k, tags=(tag,))
        self._tree.heading(col, command=lambda: self._ordenar(col, not reverso))


# ── Barra de pesquisa ────────────────────────────────────
class BarraPesquisa(ttk.Frame):
    def __init__(self, parent, placeholder="Pesquisar...", comando=None, **kwargs):
        super().__init__(parent, style="TFrame", **kwargs)

        self._var = tk.StringVar()
        self._var.trace_add("write", lambda *_: comando(self._var.get()) if comando else None)

        self._entry = ttk.Entry(self, textvariable=self._var, font=FONTE_NORMAL)
        self._entry.insert(0, placeholder)
        self._entry.config(foreground=COR_TEXTO_CLARO)
        self._entry.pack(fill="x", ipady=5)

        self._placeholder = placeholder
        self._entry.bind("<FocusIn>", self._limpar)
        self._entry.bind("<FocusOut>", self._repor)

    def _limpar(self, _):
        if self._var.get() == self._placeholder:
            self._entry.delete(0, "end")
            self._entry.config(foreground=COR_TEXTO)

    def _repor(self, _):
        if self._var.get() == "":
            self._entry.insert(0, self._placeholder)
            self._entry.config(foreground=COR_TEXTO_CLARO)

    def get(self):
        val = self._var.get()
        return "" if val == self._placeholder else val


# ── Mensagem de feedback (sucesso / erro) ────────────────
class MensagemFeedback(ttk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="", font=FONTE_PEQUENA,
                         style="TLabel", **kwargs)
        self._after_id = None

    def sucesso(self, texto, tempo_ms=3500):
        self._mostrar(f"  ✔  {texto}", COR_PRIMARIA, tempo_ms)

    def erro(self, texto, tempo_ms=4000):
        self._mostrar(f"  ✖  {texto}", COR_PERIGO, tempo_ms)

    def aviso(self, texto, tempo_ms=4000):
        self._mostrar(f"  ⚠  {texto}", COR_AVISO, tempo_ms)

    def _mostrar(self, texto, cor, tempo_ms):
        if self._after_id:
            self.after_cancel(self._after_id)
        self.config(text=texto, foreground=cor)
        self._after_id = self.after(tempo_ms, lambda: self.config(text=""))


# ── Diálogo de confirmação ───────────────────────────────
class DialogoConfirmacao(tk.Toplevel):
    def __init__(self, parent, titulo, mensagem, callback_sim):
        super().__init__(parent)
        self.title(titulo)
        self.resizable(False, False)
        self.grab_set()
        self.configure(bg=COR_FUNDO)

        # Centrar sobre o pai
        self.geometry("380x160")
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2 - 190
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 80
        self.geometry(f"+{px}+{py}")

        ttk.Label(self, text=mensagem, style="TLabel",
                  wraplength=340, justify="center").pack(pady=28)

        bts = ttk.Frame(self, style="TFrame")
        bts.pack(pady=4)

        BotaoPerigo(bts, "Confirmar", comando=lambda: [callback_sim(), self.destroy()],
                    largura=12).pack(side="left", padx=8)
        BotaoSecundario(bts, "Cancelar", comando=self.destroy,
                        largura=12).pack(side="left", padx=8)
