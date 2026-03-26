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
    # TODO: implementa esta função
    # Deve funcionar exatamente como gerar_id_produto()
    # mas usando contador_categorias e o prefixo "C"
    pass


def validar_preco(valor_texto):
    """Valida se o valor introduzido é um número decimal positivo."""
    try:
        valor = float(valor_texto)
        return valor >= 0
    except ValueError:
        return False


def validar_quantidade(valor_texto):
    # TODO: implementa esta função
    # Deve tentar converter valor_texto para int
    # Retorna True se for inteiro e >= 0, False caso contrário
    pass


def validar_peso(valor_texto):
    """Valida se o peso introduzido é um número decimal positivo."""
    try:
        valor = float(valor_texto)
        return valor > 0
    except ValueError:
        return False
