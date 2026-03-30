# ==============================
# produto.py
# CRUD simples para entidade Produto
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_produto, validar_preco, validar_quantidade, validar_peso

produtos = {}


def _erro(codigo_http, mensagem):
    """Imprime uma mensagem de erro formatada com o código HTTP correspondente."""
    print(f"[{codigo_http}] Erro: {mensagem}")


# CREATE
def criar_produto(nome, preco_texto, quantidade_texto, id_categoria, peso_texto):
    from categoria import categoria_existe, categorias

    if not nome.strip():
        _erro(400, "o nome do produto não pode estar vazio.")
        return

    if not validar_preco(preco_texto):
        _erro(400, "preço inválido. Introduza um número positivo (ex: 1.99).")
        return

    if not validar_quantidade(quantidade_texto):
        _erro(400, "quantidade inválida. Introduza um número inteiro não negativo.")
        return

    if not categoria_existe(id_categoria):
        _erro(404, f"categoria '{id_categoria}' não encontrada.")
        return

    if not validar_peso(peso_texto):
        _erro(400, "peso inválido. Introduza um número positivo (ex: 0.5).")
        return

    id_produto = gerar_id_produto()
    produtos[id_produto] = {
        "nome": nome.strip(),
        "preco": float(preco_texto),
        "quantidade_stock": int(quantidade_texto),
        "id_categoria": id_categoria,
        "peso": float(peso_texto)
    }
    print(f"[201] Produto criado com sucesso. ID: {id_produto}")


# READ (listar todos)
def listar_produtos():
    from categoria import categorias

    if not produtos:
        _erro(404, "não existem produtos registados.")
        return

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


# READ (listar por categoria)
def listar_produtos_por_categoria(id_categoria):
    from categoria import categoria_existe, categorias

    if not categoria_existe(id_categoria):
        _erro(404, f"categoria '{id_categoria}' não encontrada.")
        return

    nome_cat = categorias[id_categoria]["nome_categoria"]
    encontrados = {pid: d for pid, d in produtos.items() if d["id_categoria"] == id_categoria}

    if not encontrados:
        _erro(404, f"não existem produtos na categoria '{nome_cat}'.")
        return

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


# READ (consultar individual)
def consultar_produto(id_produto):
    from categoria import categorias

    if id_produto not in produtos:
        _erro(404, f"produto '{id_produto}' não encontrado.")
        return

    dados = produtos[id_produto]
    nome_cat = categorias.get(dados["id_categoria"], {}).get("nome_categoria", "?")
    print(f"\n--- Produto ---")
    print(f"ID:              {id_produto}")
    print(f"Nome:            {dados['nome']}")
    print(f"Preço:           {dados['preco']:.2f} €")
    print(f"Stock:           {dados['quantidade_stock']} unidades")
    print(f"Peso:            {dados['peso']:.3f} kg")
    print(f"Categoria:       {nome_cat} ({dados['id_categoria']})")


# UPDATE
def atualizar_produto(id_produto, nome=None, preco_texto=None, quantidade_texto=None, id_categoria=None, peso_texto=None):
    from categoria import categoria_existe

    if id_produto not in produtos:
        _erro(404, f"produto '{id_produto}' não encontrado.")
        return

    if nome:
        produtos[id_produto]["nome"] = nome.strip()

    if preco_texto:
        if not validar_preco(preco_texto):
            _erro(400, "preço inválido.")
            return
        produtos[id_produto]["preco"] = float(preco_texto)

    if quantidade_texto:
        if not validar_quantidade(quantidade_texto):
            _erro(400, "quantidade inválida.")
            return
        produtos[id_produto]["quantidade_stock"] = int(quantidade_texto)

    if id_categoria:
        if not categoria_existe(id_categoria):
            _erro(404, f"categoria '{id_categoria}' não encontrada.")
            return
        produtos[id_produto]["id_categoria"] = id_categoria

    if peso_texto:
        if not validar_peso(peso_texto):
            _erro(400, "peso inválido.")
            return
        produtos[id_produto]["peso"] = float(peso_texto)

    print("[200] Produto atualizado com sucesso.")


# DELETE
def remover_produto(id_produto):
    if id_produto not in produtos:
        _erro(404, f"produto '{id_produto}' não encontrado.")
        return
    del produtos[id_produto]
    print("[200] Produto removido com sucesso.")
