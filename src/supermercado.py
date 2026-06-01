# ==============================
# ui/paginas/supermercados.py
# Interface Gráfica para Entidade Supermercado
# ==============================

import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import tkinter as tk
from tkinter import ttk
from ui.widgets import CampoForm, BotaoPrimario, BotaoPerigo, Tabela, MensagemFeedback, DialogoConfirmacao
import supermercado

class PaginaSupermercados(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")

        # ── Cabeçalho de Feedback ──────────────────────────────────────────
        topo = ttk.Frame(self, style="TFrame")
        topo.pack(fill="x", padx=30, pady=20)
        ttk.Label(topo, text="Gestão de Supermercados", style="Titulo.TLabel").pack(side="left")
        self.feedback = MensagemFeedback(topo)
        self.feedback.pack(side="right", padx=10)

        # ── Divisão do Ecrã (Formulário à esquerda | Tabela à direita) ──────
        corpo = ttk.Frame(self, style="TFrame")
        corpo.pack(fill="both", expand=True, padx=30, pady=10)

        # Formulário Lateral
        self.frame_form = ttk.LabelFrame(corpo, text=" Dados do Estabelecimento ", style="TFrame", padding=15)
        self.frame_form.pack(side="left", fill="y", padx=(0, 20))

        self.txt_id = CampoForm(self.frame_form, label="ID Interno", obrigatorio=False,
                                placeholder="Gerado automaticamente")
        self.txt_id._entry.config(state="disabled")
        self.txt_id.pack(fill="x", pady=4)

        self.txt_numero = CampoForm(self.frame_form, label="Número da Loja / Código",
                                    placeholder="Ex: Loja 01, Premium-Lx")
        self.txt_numero.pack(fill="x", pady=4)

        self.txt_morada = CampoForm(self.frame_form, label="Morada / Localização",
                                    placeholder="Ex: Av. da República, Lisboa")
        self.txt_morada.pack(fill="x", pady=4)

        self.txt_nif = CampoForm(self.frame_form, label="NIF Corporativo", placeholder="9 dígitos fiscais")
        self.txt_nif.pack(fill="x", pady=4)

        # Contentor de botões do formulário
        btn_box = ttk.Frame(self.frame_form, style="TFrame")
        btn_box.pack(fill="x", pady=15)

        BotaoPrimario(btn_box, "Gravar", comando=self._submeter).pack(side="left", expand=True, fill="x", padx=2)
        BotaoPerigo(btn_box, "Limpar", comando=self._limpar_formulario).pack(side="left", expand=True, fill="x", padx=2)

        # ── Área da Tabela de Dados ───────────────────────────────────────
        frame_tabela = ttk.Frame(corpo, style="TFrame")
        frame_tabela.pack(side="right", fill="both", expand=True)

        colunas = [
            ("id", "ID", 80),
            ("numero", "Número / Cód.", 120),
            ("morada", "Morada Completa", 320),
            ("nif", "NIF", 120)
        ]
        self.tabela = Tabela(frame_tabela, colunas=colunas)
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind_duplo_clique(self._carregar_registo)

        # Ação crítica abaixo do componente Treeview
        BotaoPerigo(frame_tabela, "Remover Loja Selecionada", comando=self._confirmar_remocao).pack(anchor="e", pady=10)

        # Renderização inicial
        self._atualizar_grid()

    def _atualizar_grid(self):
        """Varre o dicionário em memória do backend e popula as linhas do Grid"""
        dados_tabela = []
        for sid, dados in supermercado.supermercados.items():
            dados_tabela.append((sid, dados["numero"], dados["morada"], dados["nif"]))
        self.tabela.preencher(dados_tabela)

    def _submeter(self):
        """Avalia se a requisição de gravação invoca o CREATE ou o UPDATE"""
        id_atual = self.txt_id.get()
        numero = self.txt_numero.get()
        morada = self.txt_morada.get()
        nif = self.txt_nif.get()

        # Reseta sinalizações de erro anteriores nos campos
        self.txt_numero.limpar_erro()
        self.txt_morada.limpar_erro()
        self.txt_nif.limpar_erro()

        if id_atual == "":
            status, msg = supermercado.criar_supermercado(numero, morada, nif)
        else:
            status, msg = supermercado.atualizar_supermercado(id_atual, numero, morada, nif)

        if status in (200, 201):
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _carregar_registo(self):
        """Disparado no Duplo Clique: Mapeia a linha selecionada de volta ao formulário"""
        sel = self.tabela.seleccionado()
        if sel:
            self.txt_id._entry.config(state="normal")
            self.txt_id.set(sel[0])
            self.txt_id._entry.config(state="disabled")
            self.txt_numero.set(sel[1])
            self.txt_morada.set(sel[2])
            self.txt_nif.set(sel[3])

    def _confirmar_remocao(self):
        sel = self.tabela.seleccionado()
        if not sel:
            self.feedback.aviso("Selecione um supermercado na tabela antes de clicar em remover.")
            return

        DialogoConfirmacao(
            self, "Remover Estabelecimento", f"Tem a certeza que deseja excluir a filial '{sel[1]}'?",
            callback_sim=lambda: self._executar_remocao(sel[0])
        )

    def _executar_remocao(self, id_sup):
        status, msg = supermercado.remover_supermercado(id_sup)
        if status == 200:
            self.feedback.sucesso(msg)
            self._limpar_formulario()
            self._atualizar_grid()
        else:
            self.feedback.erro(msg)

    def _limpar_formulario(self):
        self.txt_id._entry.config(state="normal")
        self.txt_id.limpar()
        self.txt_id._entry.config(state="disabled")
        self.txt_numero.limpar()
        self.txt_morada.limpar()
        self.txt_nif.limpar()
