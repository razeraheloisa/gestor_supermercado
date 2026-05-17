# ==============================
# categoria.py
# CRUD simples para entidade Categoria
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_categoria
import json
import os

categorias = {}
FICHEIRO_CATEGORIAS = "categorias.json"

# ==============================
# Persistência
# ==============================

def guardar_categorias():
    with open(FICHEIRO_CATEGORIAS, "w", encoding="utf-8") as ficheiro:
        json.dump(categorias, ficheiro, indent=4, ensure_ascii=False)


def carregar_categorias():
    global categorias
    if os.path.exists(FICHEIRO_CATEGORIAS):
        with open(FICHEIRO_CATEGORIAS, "r", encoding="utf-8") as ficheiro:
            categorias = json.load(ficheiro)
    else:
        categorias = {}


# CREATE
def criar_categoria(nome_categoria, descricao):
    carregar_categorias()

    if not nome_categoria.strip():
        return 400, "o nome da categoria não pode estar vazio."

    if not descricao.strip():
        return 400, "a descrição não pode estar vazia."

    for dados in categorias.values():
        if dados["nome_categoria"].lower() == nome_categoria.strip().lower():
            return 409, f"já existe uma categoria com o nome '{nome_categoria}'."

    id_categoria = gerar_id_categoria()
    categorias[id_categoria] = {
        "id_categoria": id_categoria,
        "nome_categoria": nome_categoria.strip(),
        "descricao": descricao.strip()
    }
    guardar_categorias()
    return 201, categorias[id_categoria]


# READ (listar todas)
def listar_categorias():
    carregar_categorias()

    if not categorias:
        return 404, "não existem categorias registadas."

    print("\n{:<8} {:<20} {}".format("ID", "Nome", "Descrição"))
    print("-" * 60)
    for id_categoria, dados in categorias.items():
        print("{:<8} {:<20} {}".format(
            id_categoria,
            dados["nome_categoria"],
            dados["descricao"]
        ))
    return 200, categorias


# READ (consultar individual)
def consultar_categoria(id_categoria):
    carregar_categorias()

    if id_categoria not in categorias:
        return 404, f"categoria '{id_categoria}' não encontrada."

    dados = categorias[id_categoria]
    print(f"\n--- Categoria ---")
    print(f"ID:        {id_categoria}")
    print(f"Nome:      {dados['nome_categoria']}")
    print(f"Descrição: {dados['descricao']}")
    return 200, dados


# UPDATE
def atualizar_categoria(id_categoria, nome_categoria=None, descricao=None):
    carregar_categorias()

    if id_categoria not in categorias:
        return 404, f"categoria '{id_categoria}' não encontrada."

    if nome_categoria is not None:
        if not nome_categoria.strip():
            return 400, "o nome da categoria não pode estar vazio."
        for cid, dados in categorias.items():
            if cid != id_categoria and dados["nome_categoria"].lower() == nome_categoria.strip().lower():
                return 409, f"já existe uma categoria com o nome '{nome_categoria}'."
        categorias[id_categoria]["nome_categoria"] = nome_categoria.strip()

    if descricao is not None:
        if not descricao.strip():
            return 400, "a descrição não pode estar vazia."
        categorias[id_categoria]["descricao"] = descricao.strip()

    guardar_categorias()
    return 200, categorias[id_categoria]


# DELETE
def remover_categoria(id_categoria):
    carregar_categorias()

    if id_categoria not in categorias:
        return 404, f"categoria '{id_categoria}' não encontrada."

    from produto import produtos
    for dados_produto in produtos.values():
        if dados_produto["id_categoria"] == id_categoria:
            return 409, f"não é possível remover a categoria '{id_categoria}' porque existem produtos associados."

    del categorias[id_categoria]
    guardar_categorias()
    return 200, id_categoria


def categoria_existe(id_categoria):
    """Verifica se uma categoria existe. Usada por produto.py."""
    carregar_categorias()
    return id_categoria in categorias
