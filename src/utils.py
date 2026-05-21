# ==============================
# utils.py
# funções auxiliares
# ==============================

import re
import json
import os
import logging

# contadores simples para gerar IDs automáticos
contador_produtos = 1
contador_categorias = 1
contador_clientes = 1
contador_compras = 1
contador_supermercados = 1


def gerar_id_produto():
    global contador_produtos
    novo_id = f"P{contador_produtos:03d}"
    contador_produtos += 1
    return novo_id


def gerar_id_categoria():
    global contador_categorias
    novo_id = f"C{contador_categorias:03d}"
    contador_categorias += 1
    return novo_id


def gerar_id_cliente():
    global contador_clientes
    novo_id = f"CL{contador_clientes:03d}"
    contador_clientes += 1
    return novo_id


def gerar_id_compra():
    global contador_compras
    novo_id = f"CO{contador_compras:03d}"
    contador_compras += 1
    return novo_id


def gerar_id_supermercado():
    global contador_supermercados
    novo_id = f"S{contador_supermercados:03d}"
    contador_supermercados += 1
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


# Criar pasta de logs automaticamente
os.makedirs("logs", exist_ok=True)

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler("logs/gestor.log"),
        logging.StreamHandler()
    ]
)

# Criar logger
logger = logging.getLogger("gestor")
