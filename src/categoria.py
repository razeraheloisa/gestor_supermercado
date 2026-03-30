# ==============================
# categoria.py
# CRUD simples para entidade Categoria
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_categoria

categorias = {}


def _erro(codigo_http, mensagem):
    """Imprime uma mensagem de erro formatada com o código HTTP correspondente."""
    print(f"[{codigo_http}] Erro: {mensagem}")


# CREATE
def criar_categoria(nome_categoria, descricao):
    if not nome_categoria.strip():
        _erro(400, "o nome da categoria não pode estar vazio.")
        return
    if not descricao.strip():
        _erro(400, "a descrição não pode estar vazia.")
        return

    # verificar se já existe categoria com o mesmo nome
    for dados in categorias.values():
        if dados["nome_categoria"].lower() == nome_categoria.strip().lower():
            _erro(409, f"já existe uma categoria com o nome '{nome_categoria}'.")
            return

    id_categoria = gerar_id_categoria()
    categorias[id_categoria] = {
        "nome_categoria": nome_categoria.strip(),
        "descricao": descricao.strip()
    }
    print(f"[201] Categoria criada com sucesso. ID: {id_categoria}")


# READ (listar todas)
def listar_categorias():
    if not categorias:
        _erro(404, "não existem categorias registadas.")
        return

    print("\n{:<8} {:<20} {}".format("ID", "Nome", "Descrição"))
    print("-" * 60)
    for id_categoria, dados in categorias.items():
        print("{:<8} {:<20} {}".format(
            id_categoria,
            dados["nome_categoria"],
            dados["descricao"]
        ))


# READ (consultar individual)
def consultar_categoria(id_categoria):
    if id_categoria not in categorias:
        _erro(404, f"categoria '{id_categoria}' não encontrada.")
        return

    dados = categorias[id_categoria]
    print(f"\n--- Categoria ---")
    print(f"ID:        {id_categoria}")
    print(f"Nome:      {dados['nome_categoria']}")
    print(f"Descrição: {dados['descricao']}")


# UPDATE
def atualizar_categoria(id_categoria, nome_categoria=None, descricao=None):
    if id_categoria not in categorias:
        _erro(404, f"categoria '{id_categoria}' não encontrada.")
        return

    if nome_categoria:
        # verificar duplicado (excluindo a própria)
        for cid, dados in categorias.items():
            if cid != id_categoria and dados["nome_categoria"].lower() == nome_categoria.strip().lower():
                _erro(409, f"já existe uma categoria com o nome '{nome_categoria}'.")
                return
        categorias[id_categoria]["nome_categoria"] = nome_categoria.strip()

    if descricao:
        categorias[id_categoria]["descricao"] = descricao.strip()

    print("[200] Categoria atualizada com sucesso.")


# DELETE
def remover_categoria(id_categoria):
    if id_categoria not in categorias:
        _erro(404, f"categoria '{id_categoria}' não encontrada.")
        return

    from produto import produtos
    for dados_produto in produtos.values():
        if dados_produto["id_categoria"] == id_categoria:
            _erro(409, f"não é possível remover a categoria '{id_categoria}' porque existem produtos associados.")
            return

    del categorias[id_categoria]
    print("[200] Categoria removida com sucesso.")


def categoria_existe(id_categoria):
    """Verifica se uma categoria existe. Usada por produto.py."""
    return id_categoria in categorias
