# ==============================
# utils.py
# funções auxiliares
# ==============================

# contadores simples para gerar IDs automáticos
contador_produtos = 1
contador_categorias = 1


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
