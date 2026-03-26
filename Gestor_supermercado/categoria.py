# ==============================
# categoria.py
# CRUD simples para entidade Categoria
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_categoria

categorias = {}


# CREATE
def criar_categoria(nome_categoria, descricao):
    if not nome_categoria.strip():
        print("Erro: o nome da categoria não pode estar vazio.")
        return
    if not descricao.strip():
        print("Erro: a descrição não pode estar vazia.")
        return

    # verificar se já existe categoria com o mesmo nome
    for dados in categorias.values():
        if dados["nome_categoria"].lower() == nome_categoria.strip().lower():
            print(f"Erro: já existe uma categoria com o nome '{nome_categoria}'.")
            return

    id_categoria = gerar_id_categoria()
    categorias[id_categoria] = {
        "nome_categoria": nome_categoria.strip(),
        "descricao": descricao.strip()
    }
    print(f"Categoria criada com sucesso. ID: {id_categoria}")


# READ (listar todas)
def listar_categorias():
    # TODO: implementa esta função
    # 1. Verifica se o dicionário categorias está vazio
    #    Se estiver, imprime "Não existem categorias registadas." e termina (return)
    # 2. Imprime o cabeçalho da tabela:
    #       ID       Nome                 Descrição
    #       ------------------------------------------------------------
    # 3. Percorre o dicionário e imprime cada categoria numa linha
    #    Usa o formato: "{:<8} {:<20} {}".format(id, nome, descricao)
    pass


# READ (consultar individual)
def consultar_categoria(id_categoria):
    # TODO: implementa esta função
    # 1. Verifica se id_categoria existe no dicionário categorias
    #    Se não existir, imprime "Categoria não encontrada." e termina (return)
    # 2. Guarda os dados dessa categoria numa variável
    # 3. Imprime:
    #       --- Categoria ---
    #       ID:        <id>
    #       Nome:      <nome_categoria>
    #       Descrição: <descricao>
    pass


# UPDATE
def atualizar_categoria(id_categoria, nome_categoria=None, descricao=None):
    if id_categoria not in categorias:
        print("Categoria não encontrada.")
        return

    if nome_categoria:
        # verificar duplicado (excluindo a própria)
        for cid, dados in categorias.items():
            if cid != id_categoria and dados["nome_categoria"].lower() == nome_categoria.strip().lower():
                print(f"Erro: já existe uma categoria com o nome '{nome_categoria}'.")
                return
        categorias[id_categoria]["nome_categoria"] = nome_categoria.strip()

    if descricao:
        categorias[id_categoria]["descricao"] = descricao.strip()

    print("Categoria atualizada com sucesso.")


# DELETE
def remover_categoria(id_categoria):
    # TODO: implementa esta função
    # 1. Verifica se id_categoria existe no dicionário categorias
    #    Se não existir, imprime "Categoria não encontrada." e termina
    # 2. Verifica se existem produtos associados a esta categoria:
    #       from produto import produtos
    #    Percorre os produtos e verifica se algum tem id_categoria igual ao recebido
    #    Se sim, imprime mensagem de erro e termina
    # 3. Se tudo estiver bem, remove a categoria do dicionário
    #    e imprime "Categoria removida com sucesso."
    pass


def categoria_existe(id_categoria):
    """Verifica se uma categoria existe. Usada por produto.py."""
    return id_categoria in categorias
