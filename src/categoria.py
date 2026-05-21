# ==============================
# categoria.py
# CRUD simples para entidade Categoria
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

import logging

from utils import gerar_id_categoria

logger = logging.getLogger(__name__)

categorias = {}


# CREATE
def criar_categoria(nome_categoria, descricao):
    if not nome_categoria.strip():
        logging.error("Tentativa de criar categoria com nome vazio.")
        return 400, "o nome da categoria não pode estar vazio."

    if not descricao.strip():
        logging.error("Tentativa de criar categoria com descrição vazia.")
        return 400, "a descrição não pode estar vazia."

    for dados in categorias.values():
        if dados["nome_categoria"].lower() == nome_categoria.strip().lower():
            logging.warning(f"Categoria duplicada: '{nome_categoria}'.")
            return 409, f"já existe uma categoria com o nome '{nome_categoria}'."

    id_categoria = gerar_id_categoria()
    categorias[id_categoria] = {
        "id_categoria": id_categoria,
        "nome_categoria": nome_categoria.strip(),
        "descricao": descricao.strip()
    }
    logging.info(f"Categoria criada com sucesso. ID: {id_categoria} | Nome: '{nome_categoria.strip()}'.")
    return 201, f"Categoria criada com sucesso. ID: {id_categoria}"


# READ (listar todas)
def listar_categorias():
    if not categorias:
        logging.error("Listagem de categorias: nenhuma categoria registada.")
        return 404, "não existem categorias registadas."

    logging.debug(f"Listagem de categorias: {len(categorias)} categoria(s) encontrada(s).")
    print("\n{:<8} {:<20} {}".format("ID", "Nome", "Descrição"))
    print("-" * 60)
    for id_categoria, dados in categorias.items():
        print("{:<8} {:<20} {}".format(
            id_categoria,
            dados["nome_categoria"],
            dados["descricao"]
        ))
    return 200, ""


# READ (consultar individual)
def consultar_categoria(id_categoria):
    if id_categoria not in categorias:
        logging.error(f"Categoria não encontrada: {id_categoria}.")
        return 404, f"categoria '{id_categoria}' não encontrada."

    logging.debug(f"Consulta de categoria: {id_categoria}.")
    dados = categorias[id_categoria]
    print(f"\n--- Categoria ---")
    print(f"ID:        {id_categoria}")
    print(f"Nome:      {dados['nome_categoria']}")
    print(f"Descrição: {dados['descricao']}")
    return 200, ""


# UPDATE
def atualizar_categoria(id_categoria, nome_categoria=None, descricao=None):
    if id_categoria not in categorias:
        logging.error(f"Categoria não encontrada para atualização: {id_categoria}.")
        return 404, f"categoria '{id_categoria}' não encontrada."

    if nome_categoria:
        for cid, dados in categorias.items():
            if cid != id_categoria and dados["nome_categoria"].lower() == nome_categoria.strip().lower():
                logging.warning(f"Conflito no nome da categoria ao atualizar {id_categoria}: '{nome_categoria}' já existe.")
                return 409, f"já existe uma categoria com o nome '{nome_categoria}'."
        categorias[id_categoria]["nome_categoria"] = nome_categoria.strip()

    if descricao:
        categorias[id_categoria]["descricao"] = descricao.strip()

    logging.info(f"Categoria atualizada com sucesso. ID: {id_categoria}.")
    return 200, "categoria atualizada com sucesso."


# DELETE
def remover_categoria(id_categoria):
    if id_categoria not in categorias:
        logging.error(f"Categoria não encontrada para remoção: {id_categoria}.")
        return 404, f"categoria '{id_categoria}' não encontrada."

    from produto import produtos
    for dados_produto in produtos.values():
        if dados_produto["id_categoria"] == id_categoria:
            logging.warning(f"Tentativa de remover categoria {id_categoria} com produtos associados.")
            return 409, f"não é possível remover a categoria '{id_categoria}' porque existem produtos associados."

    del categorias[id_categoria]
    logging.info(f"Categoria removida com sucesso. ID: {id_categoria}.")
    return 200, "categoria removida com sucesso."


def categoria_existe(id_categoria):
    """Verifica se uma categoria existe. Usada por produto.py."""
    existe = id_categoria in categorias
    logging.debug(f"Verificação de existência de categoria {id_categoria}: {'encontrada' if existe else 'não encontrada'}.")
    return existe
