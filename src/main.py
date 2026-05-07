# ==============================
# main.py
# Menu principal da aplicação
# Apenas chama funções dos módulos
# e apresenta resultados ao utilizador
# ==============================

import categoria
import produto
import cliente
import supermercado
import compra


def responder(resultado):
    """Recebe o tuplo (codigo, mensagem) devolvido pelas funções e imprime o resultado."""
    if resultado is None:
        return
    codigo, mensagem = resultado
    if not mensagem:
        return
    if codigo >= 400:
        print(f"[ERRO {codigo}] {mensagem}")
    else:
        print(f"[{codigo}] {mensagem}")


# ==============================
# MENUS DE CATEGORIA
# ==============================

def menu_categoria():
    while True:
        print("\n===== CATEGORIAS =====")
        print("1. Criar categoria")
        print("2. Listar categorias")
        print("3. Consultar categoria")
        print("4. Atualizar categoria")
        print("5. Remover categoria")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome da categoria: ")
            desc = input("Descrição: ")
            responder(categoria.criar_categoria(nome, desc))

        elif opcao == "2":
            responder(categoria.listar_categorias())

        elif opcao == "3":
            id_cat = input("ID da categoria: ").strip()
            responder(categoria.consultar_categoria(id_cat))

        elif opcao == "4":
            id_cat = input("ID da categoria: ").strip()
            nome = input("Novo nome (Enter para manter): ").strip() or None
            desc = input("Nova descrição (Enter para manter): ").strip() or None
            responder(categoria.atualizar_categoria(id_cat, nome, desc))

        elif opcao == "5":
            id_cat = input("ID da categoria: ").strip()
            responder(categoria.remover_categoria(id_cat))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE PRODUTO
# ==============================

def menu_produto():
    while True:
        print("\n===== PRODUTOS =====")
        print("1. Criar produto")
        print("2. Listar produtos")
        print("3. Listar produtos por categoria")
        print("4. Consultar produto")
        print("5. Atualizar produto")
        print("6. Remover produto")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = input("Preço (ex: 1.99): ")
            qtd = input("Quantidade em stock: ")
            id_cat = input("ID da categoria: ").strip()
            peso = input("Peso em kg (ex: 0.5): ")
            responder(produto.criar_produto(nome, preco, qtd, id_cat, peso))

        elif opcao == "2":
            responder(produto.listar_produtos())

        elif opcao == "3":
            id_cat = input("ID da categoria: ").strip()
            responder(produto.listar_produtos_por_categoria(id_cat))

        elif opcao == "4":
            id_prod = input("ID do produto: ").strip()
            responder(produto.consultar_produto(id_prod))

        elif opcao == "5":
            id_prod = input("ID do produto: ").strip()
            nome = input("Novo nome (Enter para manter): ").strip() or None
            preco = input("Novo preço (Enter para manter): ").strip() or None
            qtd = input("Nova quantidade (Enter para manter): ").strip() or None
            id_cat = input("Nova categoria (Enter para manter): ").strip() or None
            peso = input("Novo peso (Enter para manter): ").strip() or None
            responder(produto.atualizar_produto(id_prod, nome, preco, qtd, id_cat, peso))

        elif opcao == "6":
            id_prod = input("ID do produto: ").strip()
            responder(produto.remover_produto(id_prod))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE CLIENTE
# ==============================

def menu_cliente():
    while True:
        print("\n===== CLIENTES =====")
        print("1. Criar cliente")
        print("2. Listar clientes")
        print("3. Consultar cliente")
        print("4. Pesquisar cliente")
        print("5. Atualizar cliente")
        print("6. Remover cliente")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ")
            contacto = input("Contacto (9 dígitos): ")
            email = input("Email (opcional, Enter para saltar): ")
            nif = input("NIF (opcional, Enter para saltar): ")
            responder(cliente.criar_cliente(nome, contacto, email, nif))

        elif opcao == "2":
            responder(cliente.listar_clientes())

        elif opcao == "3":
            id_cli = input("ID do cliente: ").strip()
            responder(cliente.consultar_cliente(id_cli))

        elif opcao == "4":
            termo = input("Nome ou NIF a pesquisar: ")
            responder(cliente.pesquisar_cliente(termo))

        elif opcao == "5":
            id_cli = input("ID do cliente: ").strip()
            nome = input("Novo nome (Enter para manter): ").strip() or None
            contacto = input("Novo contacto (Enter para manter): ").strip() or None
            email = input("Novo email (Enter para manter): ").strip() or None
            nif = input("Novo NIF (Enter para manter): ").strip() or None
            responder(cliente.atualizar_cliente(id_cli, nome, contacto, email, nif))

        elif opcao == "6":
            id_cli = input("ID do cliente: ").strip()
            responder(cliente.remover_cliente(id_cli))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE SUPERMERCADO
# ==============================

def menu_supermercado():
    while True:
        print("\n===== SUPERMERCADOS =====")
        print("1. Criar supermercado")
        print("2. Listar supermercados")
        print("3. Consultar supermercado")
        print("4. Atualizar supermercado")
        print("5. Remover supermercado")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            numero = input("Número do supermercado: ")
            morada = input("Morada: ")
            nif = input("NIF (9 dígitos): ")
            responder(supermercado.criar_supermercado(numero, morada, nif))

        elif opcao == "2":
            responder(supermercado.listar_supermercados())

        elif opcao == "3":
            id_sup = input("ID do supermercado: ").strip()
            responder(supermercado.consultar_supermercado(id_sup))

        elif opcao == "4":
            id_sup = input("ID do supermercado: ").strip()
            numero = input("Novo número (Enter para manter): ").strip() or None
            morada = input("Nova morada (Enter para manter): ").strip() or None
            nif = input("Novo NIF (Enter para manter): ").strip() or None
            responder(supermercado.atualizar_supermercado(id_sup, numero, morada, nif))

        elif opcao == "5":
            id_sup = input("ID do supermercado: ").strip()
            responder(supermercado.remover_supermercado(id_sup))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE COMPRA
# ==============================

def menu_compra():
    while True:
        print("\n===== COMPRAS =====")
        print("1. Registar compra")
        print("2. Listar todas as compras")
        print("3. Listar compras por cliente")
        print("4. Listar compras por supermercado")
        print("5. Consultar compra")
        print("6. Atualizar compra")
        print("7. Remover compra")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            id_cli = input("ID do cliente: ").strip()
            id_sup = input("ID do supermercado: ").strip()
            while True:
                data = input("Data (DD/MM/AAAA): ").strip()
                partes = data.replace("/", "")
                if len(data) == 10 and data[2] == "/" and data[5] == "/" and partes.isdigit():
                    break
                print("Formato inválido. Introduza apenas números no formato DD/MM/AAAA (ex: 25/04/2025).")
            valor = input("Valor total (ex: 25.50): ")
            responder(compra.criar_compra(id_cli, id_sup, data, valor))

        elif opcao == "2":
            responder(compra.listar_compras())

        elif opcao == "3":
            id_cli = input("ID do cliente: ").strip()
            responder(compra.listar_compras_por_cliente(id_cli))

        elif opcao == "4":
            id_sup = input("ID do supermercado: ").strip()
            responder(compra.listar_compras_por_supermercado(id_sup))

        elif opcao == "5":
            id_com = input("ID da compra: ").strip()
            responder(compra.consultar_compra(id_com))

        elif opcao == "6":
            id_com = input("ID da compra: ").strip()
            data = input("Nova data (Enter para manter): ").strip() or None
            valor = input("Novo valor total (Enter para manter): ").strip() or None
            responder(compra.atualizar_compra(id_com, data, valor))

        elif opcao == "7":
            id_com = input("ID da compra: ").strip()
            responder(compra.remover_compra(id_com))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENU PRINCIPAL
# ==============================

def menu_principal():
    while True:
        print("\n=============================")
        print("   SISTEMA DE SUPERMERCADO   ")
        print("=============================")
        print("1. Categorias")
        print("2. Produtos")
        print("3. Clientes")
        print("4. Supermercados")
        print("5. Compras")
        print("0. Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            menu_categoria()
        elif opcao == "2":
            menu_produto()
        elif opcao == "3":
            menu_cliente()
        elif opcao == "4":
            menu_supermercado()
        elif opcao == "5":
            menu_compra()
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
