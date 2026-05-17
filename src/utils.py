# ==============================
# utils.py
# funções auxiliares
# ==============================

import re
import json
import os

FICHEIRO_CONTADORES = "contadores.json"

# ==============================
# Persistência dos contadores
# (evita IDs duplicados após reinício)
# ==============================

def _carregar_contadores():
    if os.path.exists(FICHEIRO_CONTADORES):
        with open(FICHEIRO_CONTADORES, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "produtos": 1,
        "categorias": 1,
        "clientes": 1,
        "compras": 1,
        "supermercados": 1
    }

def _guardar_contadores(contadores):
    with open(FICHEIRO_CONTADORES, "w", encoding="utf-8") as f:
        json.dump(contadores, f, indent=4)


def gerar_id_produto():
    c = _carregar_contadores()
    novo_id = f"P{c['produtos']:03d}"
    c["produtos"] += 1
    _guardar_contadores(c)
    return novo_id

def gerar_id_categoria():
    c = _carregar_contadores()
    novo_id = f"C{c['categorias']:03d}"
    c["categorias"] += 1
    _guardar_contadores(c)
    return novo_id

def gerar_id_cliente():
    c = _carregar_contadores()
    novo_id = f"CL{c['clientes']:03d}"
    c["clientes"] += 1
    _guardar_contadores(c)
    return novo_id

def gerar_id_compra():
    c = _carregar_contadores()
    novo_id = f"CO{c['compras']:03d}"
    c["compras"] += 1
    _guardar_contadores(c)
    return novo_id

def gerar_id_supermercado():
    c = _carregar_contadores()
    novo_id = f"S{c['supermercados']:03d}"
    c["supermercados"] += 1
    _guardar_contadores(c)
    return novo_id


def validar_preco(valor_texto):
    """Valida se o valor introduzido é um número decimal positivo."""
    try:
        valor = float(valor_texto)
        return valor >= 0
    except ValueError:
        return False

def validar_quantidade(valor_texto):
    """Valida se o valor introduzido é um número inteiro não negativo."""
    try:
        valor = int(valor_texto)
        return valor >= 0
    except ValueError:
        return False

def validar_peso(valor_texto):
    """Valida se o peso introduzido é um número decimal positivo."""
    try:
        valor = float(valor_texto)
        return valor > 0
    except ValueError:
        return False

def validar_contacto(contacto):
    """Valida se o contacto tem exactamente 9 dígitos numéricos."""
    return bool(re.fullmatch(r"\d{9}", contacto.strip()))

def validar_email(email):
    """Valida se o email tem um formato básico válido."""
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()))

def validar_nif(nif):
    """Valida se o NIF tem exactamente 9 dígitos numéricos."""
    return bool(re.fullmatch(r"\d{9}", nif.strip()))

def validar_data(data):
    """Valida se a data está no formato DD/MM/AAAA."""
    return bool(re.fullmatch(r"\d{2}/\d{2}/\d{4}", data.strip()))
