# ==============================
# main.py
# menu terminal para testar CRUD
# Gestor de Supermercado
# ==============================

from categoria import (
    criar_categoria,
    consultar_categoria,
    atualizar_categoria,
    remover_categoria
)
from produto import (
    criar_produto,
    listar_produtos,
    consultar_produto,
    atualizar_produto,
    remover_produto,
    listar_produtos_por_categoria
)


# ---- menus ----

def menu_principal():
    print("\n╔══════════════════════════════╗")
    print("║    GESTOR DE SUPERMERCADO    ║")
    print("╠══════════════════════════════╣")
    print("║  1 - Gerir Categorias        ║")
    print("║  2 - Gerir Produtos          ║")
    print("║  0 - Sair                    ║")
    print("╚══════════════════════════════╝")


def menu_categorias():
    print("\n===== MENU CATEGORIAS =====")
    print("1 - Criar categoria")
    print("3 - Consultar categoria")
    print("4 - Atualizar categoria")
    print("5 - Remover categoria")
    print("0 - Voltar")


def menu_produtos():
    print("\n===== MENU PRODUTOS =====")
    print("1 - Criar produto")
    print("2 - Listar todos os produtos")
    print("3 - Listar produtos por categoria")
    print("4 - Consultar produto")
    print("5 - Atualizar produto")
    print("6 - Remover produto")
    print("0 - Voltar")


# ---- submenu categorias ----

def submenu_categorias():
    while True:
        menu_categorias()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome_categoria = input("Nome da categoria: ")
            descricao = input("Descrição: ")
            criar_categoria(nome_categoria, descricao)



        elif opcao == "3":
            id_categoria = input("ID da categoria: ").upper()
            consultar_categoria(id_categoria)

        elif opcao == "4":
            id_categoria = input("ID da categoria: ").upper()
            nome_categoria = input("Novo nome (enter para manter): ")
            descricao = input("Nova descrição (enter para manter): ")
            atualizar_categoria(
                id_categoria,
                nome_categoria if nome_categoria else None,
                descricao if descricao else None
            )

        elif opcao == "5":
            id_categoria = input("ID da categoria: ").upper()
            remover_categoria(id_categoria)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


# ---- submenu produtos ----

def submenu_produtos():
    while True:
        menu_produtos()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = input("Preço (ex: 1.99): ")
            quantidade = input("Quantidade em stock: ")
            id_categoria = input("ID da categoria: ").upper()
            peso = input("Peso em kg (ex: 0.500): ")
            criar_produto(nome, preco, quantidade, id_categoria, peso)

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            id_categoria = input("ID da categoria: ").upper()
            listar_produtos_por_categoria(id_categoria)

        elif opcao == "4":
            id_produto = input("ID do produto: ").upper()
            consultar_produto(id_produto)

        elif opcao == "5":
            id_produto = input("ID do produto: ").upper()
            print("(Deixe em branco para manter o valor atual)")
            nome = input("Novo nome: ")
            preco = input("Novo preço: ")
            quantidade = input("Nova quantidade em stock: ")
            id_categoria = input("Novo ID de categoria: ").upper()
            peso = input("Novo peso (kg): ")
            atualizar_produto(
                id_produto,
                nome if nome else None,
                preco if preco else None,
                quantidade if quantidade else None,
                id_categoria if id_categoria else None,
                peso if peso else None
            )

        elif opcao == "6":
            id_produto = input("ID do produto: ").upper()
            remover_produto(id_produto)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


# ---- programa principal ----

def main():
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            submenu_categorias()

        elif opcao == "2":
            submenu_produtos()

        elif opcao == "0":
            print("A sair do Gestor de Supermercado. Até logo!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
