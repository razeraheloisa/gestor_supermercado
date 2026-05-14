# ==============================
# produto.py
# CRUD simples para entidade Produto
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_produto, validar_preco, validar_quantidade, validar_peso


import json
import os


produtos = {}
FICHEIRO_PRODUTOS = "produtos.json"

# ==============================
# Persistência
# ==============================

def guardar_produtos():
    with open(FICHEIRO_PRODUTOS, "w", encoding="utf-8") as ficheiro:
        json.dump(produtos, ficheiro, indent=4, ensure_ascii=False)


def carregar_produtos():
    global produtos

    if os.path.exists(FICHEIRO_PRODUTOS):
        with open(FICHEIRO_PRODUTOS, "r", encoding="utf-8") as ficheiro:
            produtos = json.load(ficheiro)
    else:
        produtos = {}

# CREATE
def criar_produto(nome, preco_texto, quantidade_texto, id_categoria, peso_texto):
    carregar_produtos()
    from categoria import categoria_existe

    if not nome.strip():
        return 400, "o nome do produto não pode estar vazio."

    if not validar_preco(preco_texto):
        return 400, "preço inválido. Introduza um número positivo (ex: 1.99)."

    if not validar_quantidade(quantidade_texto):
        return 400, "quantidade inválida. Introduza um número inteiro não negativo."

    if not categoria_existe(id_categoria):
        return 404, f"categoria '{id_categoria}' não encontrada."

    if not validar_peso(peso_texto):
        return 400, "peso inválido. Introduza um número positivo (ex: 0.5)."

    id_produto = gerar_id_produto()
    produtos[id_produto] = {
        "nome": nome.strip(),
        "preco": float(preco_texto),
        "quantidade_stock": int(quantidade_texto),
        "id_categoria": id_categoria,
        "peso": float(peso_texto)
    }
    guardar_produtos()
    return 201, produtos[id_produto]


# READ (listar todos)
def listar_produtos():
    carregar_produtos()
    from categoria import categorias

    if not produtos:
        return 404, "não existem produtos registados."

    print("\n{:<8} {:<22} {:<10} {:<10} {:<10} {:<10}".format(
        "ID", "Nome", "Preço (€)", "Stock", "Peso (kg)", "Categoria"
    ))
    print("-" * 75)
    for id_produto, dados in produtos.items():
        nome_cat = categorias.get(dados["id_categoria"], {}).get("nome_categoria", "?")
        print("{:<8} {:<22} {:<10.2f} {:<10} {:<10.3f} {}".format(
            id_produto,
            dados["nome"],
            dados["preco"],
            dados["quantidade_stock"],
            dados["peso"],
            nome_cat
        ))
   return 200, produtos


# READ (listar por categoria)
def listar_produtos_por_categoria(id_categoria):
    carregar_produtos()
    from categoria import categoria_existe, categorias

    if not categoria_existe(id_categoria):
        return 404, f"categoria '{id_categoria}' não encontrada."

    nome_cat = categorias[id_categoria]["nome_categoria"]
    encontrados = {pid: d for pid, d in produtos.items() if d["id_categoria"] == id_categoria}

    if not encontrados:
        return 404, f"não existem produtos na categoria '{nome_cat}'."

    print(f"\n--- Produtos da categoria: {nome_cat} ---")
    print("{:<8} {:<22} {:<10} {:<10} {}".format("ID", "Nome", "Preço (€)", "Stock", "Peso (kg)"))
    print("-" * 60)
    for id_produto, dados in encontrados.items():
        print("{:<8} {:<22} {:<10.2f} {:<10} {:.3f}".format(
            id_produto,
            dados["nome"],
            dados["preco"],
            dados["quantidade_stock"],
            dados["peso"]
        ))
    return 200, encontrados


# READ (consultar individual)
def consultar_produto(id_produto):
    carregar_produtos()
    from categoria import categorias

    if id_produto not in produtos:
        return 404, f"produto '{id_produto}' não encontrado."

    dados = produtos[id_produto]
    nome_cat = categorias.get(dados["id_categoria"], {}).get("nome_categoria", "?")
    print(f"\n--- Produto ---")
    print(f"ID:              {id_produto}")
    print(f"Nome:            {dados['nome']}")
    print(f"Preço:           {dados['preco']:.2f} €")
    print(f"Stock:           {dados['quantidade_stock']} unidades")
    print(f"Peso:            {dados['peso']:.3f} kg")
    print(f"Categoria:       {nome_cat} ({dados['id_categoria']})")
    return 200, produtos[id_produto]


# UPDATE
def atualizar_produto(id_produto, nome=None, preco_texto=None, quantidade_texto=None, id_categoria=None, peso_texto=None):
    carregar_produtos()
    from categoria import categoria_existe

    if id_produto not in produtos:
        return 404, f"produto '{id_produto}' não encontrado."

    if nome:
        produtos[id_produto]["nome"] = nome.strip()

    if preco_texto:
        if not validar_preco(preco_texto):
            return 400, "preço inválido."
        produtos[id_produto]["preco"] = float(preco_texto)

    if quantidade_texto:
        if not validar_quantidade(quantidade_texto):
            return 400, "quantidade inválida."
        produtos[id_produto]["quantidade_stock"] = int(quantidade_texto)

    if id_categoria:
        if not categoria_existe(id_categoria):
            return 404, f"categoria '{id_categoria}' não encontrada."
        produtos[id_produto]["id_categoria"] = id_categoria

    if peso_texto:
        if not validar_peso(peso_texto):
            return 400, "peso inválido."
        produtos[id_produto]["peso"] = float(peso_texto)
    guardar_produtos()
    return 200, produtos[id_produto]


# DELETE
def remover_produto(id_produto):
    carregar_produtos()
    if id_produto not in produtos:
        return 404, f"produto '{id_produto}' não encontrado."

    del produtos[id_produto]
    guardar_produtos()
    return 200, id_produto
