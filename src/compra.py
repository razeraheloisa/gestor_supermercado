# ==============================
# compra.py
# CRUD simples para entidade Compra
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================


from utils import gerar_id_compra, validar_preco, validar_data
import json
import os


compras = {}
FICHEIRO_COMPRAS = "compras.json"

# ==============================
# Persistência
# ==============================

def guardar_compras():
    with open(FICHEIRO_COMPRAS, "w", encoding="utf-8") as ficheiro:
        json.dump(compras, ficheiro, indent=4, ensure_ascii=False)


def carregar_compras():
    global compras

    if os.path.exists(FICHEIRO_COMPRAS):
        with open(FICHEIRO_COMPRAS, "r", encoding="utf-8") as ficheiro:
            compras = json.load(ficheiro)
    else:
        compras = {}

# CREATE
def criar_compra(id_cliente, id_supermercado, data, valor_total_texto):
    from cliente import cliente_existe
    from supermercado import supermercado_existe

    if not cliente_existe(id_cliente):
        return 404, f"cliente '{id_cliente}' não encontrado."

    if not supermercado_existe(id_supermercado):
        return 404, f"supermercado '{id_supermercado}' não encontrado."

    if not validar_data(data):
        return 400, "data inválida. Utilize o formato DD/MM/AAAA (ex: 25/04/2025)."

    if not validar_preco(valor_total_texto):
        return 400, "valor total inválido. Introduza um número positivo (ex: 15.99)."

    id_compra = gerar_id_compra()
    compras[id_compra] = {
        "id_cliente": id_cliente,
        "id_supermercado": id_supermercado,
        "data": data.strip(),
        "valor_total": float(valor_total_texto)
    }
    return 201, f"Compra registada com sucesso. ID: {id_compra}"


# READ (listar todas)
def listar_compras():
    from cliente import clientes
    from supermercado import supermercados

    if not compras:
        return 404, "não existem compras registadas."

    print("\n{:<8} {:<8} {:<25} {:<8} {:<35} {:<12}".format(
        "ID", "Cliente", "Nome Cliente", "Superm.", "Morada Supermercado", "Valor (€)"
    ))
    print("-" * 100)
    for id_compra, dados in compras.items():
        nome_cliente = clientes.get(dados["id_cliente"], {}).get("nome", "?")
        morada_super = supermercados.get(dados["id_supermercado"], {}).get("morada", "?")
        print("{:<8} {:<8} {:<25} {:<8} {:<35} {:<10.2f}  {}".format(
            id_compra,
            dados["id_cliente"],
            nome_cliente,
            dados["id_supermercado"],
            morada_super,
            dados["valor_total"],
            dados["data"]
        ))
    return 200, ""


# READ (listar compras de um cliente)
def listar_compras_por_cliente(id_cliente):
    from cliente import cliente_existe, clientes
    from supermercado import supermercados

    if not cliente_existe(id_cliente):
        return 404, f"cliente '{id_cliente}' não encontrado."

    nome_cliente = clientes[id_cliente]["nome"]
    encontradas = {cid: d for cid, d in compras.items() if d["id_cliente"] == id_cliente}

    if not encontradas:
        return 404, f"o cliente '{nome_cliente}' não tem compras registadas."

    print(f"\n--- Compras do cliente: {nome_cliente} ({id_cliente}) ---")
    print("\n{:<8} {:<8} {:<35} {:<12} {:<12}".format(
        "ID", "Superm.", "Morada", "Data", "Valor (€)"
    ))
    print("-" * 78)
    for id_compra, dados in encontradas.items():
        morada_super = supermercados.get(dados["id_supermercado"], {}).get("morada", "?")
        print("{:<8} {:<8} {:<35} {:<12} {:<10.2f}".format(
            id_compra,
            dados["id_supermercado"],
            morada_super,
            dados["data"],
            dados["valor_total"]
        ))
    return 200, ""


# READ (listar compras de um supermercado)
def listar_compras_por_supermercado(id_supermercado):
    from supermercado import supermercado_existe, supermercados
    from cliente import clientes

    if not supermercado_existe(id_supermercado):
        return 404, f"supermercado '{id_supermercado}' não encontrado."

    morada = supermercados[id_supermercado]["morada"]
    encontradas = {cid: d for cid, d in compras.items() if d["id_supermercado"] == id_supermercado}

    if not encontradas:
        return 404, f"o supermercado '{morada}' não tem compras registadas."

    print(f"\n--- Compras no supermercado: {morada} ({id_supermercado}) ---")
    print("\n{:<8} {:<8} {:<25} {:<12} {:<12}".format(
        "ID", "Cliente", "Nome Cliente", "Data", "Valor (€)"
    ))
    print("-" * 70)
    for id_compra, dados in encontradas.items():
        nome_cliente = clientes.get(dados["id_cliente"], {}).get("nome", "?")
        print("{:<8} {:<8} {:<25} {:<12} {:<10.2f}".format(
            id_compra,
            dados["id_cliente"],
            nome_cliente,
            dados["data"],
            dados["valor_total"]
        ))
    return 200, ""


# READ (consultar individual)
def consultar_compra(id_compra):
    from cliente import clientes
    from supermercado import supermercados

    if id_compra not in compras:
        return 404, f"compra '{id_compra}' não encontrada."

    dados = compras[id_compra]
    nome_cliente = clientes.get(dados["id_cliente"], {}).get("nome", "?")
    morada_super = supermercados.get(dados["id_supermercado"], {}).get("morada", "?")
    nif_super = supermercados.get(dados["id_supermercado"], {}).get("nif", "?")

    print(f"\n--- Compra ---")
    print(f"ID Compra:       {id_compra}")
    print(f"Cliente:         {nome_cliente} ({dados['id_cliente']})")
    print(f"Supermercado:    {morada_super} | NIF: {nif_super} ({dados['id_supermercado']})")
    print(f"Data:            {dados['data']}")
    print(f"Valor Total:     {dados['valor_total']:.2f} €")
    return 200, ""


# UPDATE
def atualizar_compra(id_compra, data=None, valor_total_texto=None):
    if id_compra not in compras:
        return 404, f"compra '{id_compra}' não encontrada."

    if data is not None:
        if not validar_data(data):
            return 400, "data inválida. Utilize o formato DD/MM/AAAA."
        compras[id_compra]["data"] = data.strip()

    if valor_total_texto is not None:
        if not validar_preco(valor_total_texto):
            return 400, "valor total inválido. Introduza um número positivo."
        compras[id_compra]["valor_total"] = float(valor_total_texto)

    return 200, "compra atualizada com sucesso."


# DELETE
def remover_compra(id_compra):
    if id_compra not in compras:
        return 404, f"compra '{id_compra}' não encontrada."

    del compras[id_compra]
    return 200, "compra removida com sucesso."


def compra_existe(id_compra):
    """Verifica se uma compra existe."""
    return id_compra in compras
