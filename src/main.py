# ==============================
# main.py
# Menu principal do sistema
# ==============================

from categoria import criar_categoria, listar_categorias, consultar_categoria, atualizar_categoria, remover_categoria
from produto import criar_produto, listar_produtos, listar_produtos_por_categoria, consultar_produto, atualizar_produto, remover_produto
from cliente import criar_cliente, listar_clientes, consultar_cliente, pesquisar_cliente, atualizar_cliente, remover_cliente
from supermercado import criar_supermercado, listar_supermercados, consultar_supermercado, atualizar_supermercado, remover_supermercado
from compra import criar_compra, listar_compras, listar_compras_por_cliente, listar_compras_por_supermercado, consultar_compra, atualizar_compra, remover_compra


def _mostrar_resultado(resultado):
    """Interpreta e imprime o retorno (codigo, mensagem) das funções CRUD."""
    if resultado is None:
        return
    if isinstance(resultado, tuple):
        codigo, mensagem = resultado
        prefixo = "OK" if codigo in (200, 201) else "Erro"
        print(f"[{codigo}] {prefixo}: {mensagem}")


# ==============================
# MENUS DE CATEGORIA
# ==============================

def menu_categorias():
    while True:
        print("\n========== CATEGORIAS ==========")
        print("1. Criar categoria")
        print("2. Listar categorias")
        print("3. Consultar categoria")
        print("4. Atualizar categoria")
        print("5. Remover categoria")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome da categoria: ")
            descricao = input("Descrição: ")
            _mostrar_resultado(criar_categoria(nome, descricao))

        elif opcao == "2":
            _mostrar_resultado(listar_categorias())

        elif opcao == "3":
            id_cat = input("ID da categoria: ").strip()
            consultar_categoria(id_cat)

        elif opcao == "4":
            id_cat = input("ID da categoria: ").strip()
            print("(Deixe em branco para não alterar)")
            nome = input("Novo nome: ").strip() or None
            descricao = input("Nova descrição: ").strip() or None
            _mostrar_resultado(atualizar_categoria(id_cat, nome, descricao))

        elif opcao == "5":
            id_cat = input("ID da categoria: ").strip()
            _mostrar_resultado(remover_categoria(id_cat))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE PRODUTO
# ==============================

def menu_produtos():
    while True:
        print("\n========== PRODUTOS ==========")
        print("1. Criar produto")
        print("2. Listar todos os produtos")
        print("3. Listar produtos por categoria")
        print("4. Consultar produto")
        print("5. Atualizar produto")
        print("6. Remover produto")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = input("Preço (€): ")
            quantidade = input("Quantidade em stock: ")
            id_cat = input("ID da categoria: ").strip()
            peso = input("Peso (kg): ")
            _mostrar_resultado(criar_produto(nome, preco, quantidade, id_cat, peso))

        elif opcao == "2":
            _mostrar_resultado(listar_produtos())

        elif opcao == "3":
            id_cat = input("ID da categoria: ").strip()
            _mostrar_resultado(listar_produtos_por_categoria(id_cat))

        elif opcao == "4":
            id_prod = input("ID do produto: ").strip()
            consultar_produto(id_prod)

        elif opcao == "5":
            id_prod = input("ID do produto: ").strip()
            print("(Deixe em branco para não alterar)")
            nome = input("Novo nome: ").strip() or None
            preco = input("Novo preço (€): ").strip() or None
            quantidade = input("Nova quantidade: ").strip() or None
            id_cat = input("Novo ID de categoria: ").strip() or None
            peso = input("Novo peso (kg): ").strip() or None
            _mostrar_resultado(atualizar_produto(id_prod, nome, preco, quantidade, id_cat, peso))

        elif opcao == "6":
            id_prod = input("ID do produto: ").strip()
            _mostrar_resultado(remover_produto(id_prod))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE CLIENTE
# ==============================

def menu_clientes():
    while True:
        print("\n========== CLIENTES ==========")
        print("1. Criar cliente")
        print("2. Listar clientes")
        print("3. Consultar cliente")
        print("4. Pesquisar cliente (nome ou NIF)")
        print("5. Atualizar cliente")
        print("6. Remover cliente")
        print("0. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ")
            contacto = input("Contacto (9 dígitos): ")
            email = input("Email (opcional): ")
            nif = input("NIF (opcional): ")
            _mostrar_resultado(criar_cliente(nome, contacto, email, nif))

        elif opcao == "2":
            _mostrar_resultado(listar_clientes())

        elif opcao == "3":
            id_cl = input("ID do cliente: ").strip()
            consultar_cliente(id_cl)

        elif opcao == "4":
            termo = input("Nome ou NIF a pesquisar: ")
            _mostrar_resultado(pesquisar_cliente(termo))

        elif opcao == "5":
            id_cl = input("ID do cliente: ").strip()
            print("(Deixe em branco para não alterar)")
            nome = input("Novo nome: ").strip() or None
            contacto = input("Novo contacto: ").strip() or None
            email = input("Novo email: ").strip() or None
            nif = input("Novo NIF: ").strip() or None
            _mostrar_resultado(atualizar_cliente(id_cl, nome, contacto, email, nif))

        elif opcao == "6":
            id_cl = input("ID do cliente: ").strip()
            _mostrar_resultado(remover_cliente(id_cl))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE SUPERMERCADO
# ==============================

def menu_supermercados():
    while True:
        print("\n========== SUPERMERCADOS ==========")
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
            nif = input("NIF: ")
            _mostrar_resultado(criar_supermercado(numero, morada, nif))

        elif opcao == "2":
            _mostrar_resultado(listar_supermercados())

        elif opcao == "3":
            id_sup = input("ID do supermercado: ").strip()
            consultar_supermercado(id_sup)

        elif opcao == "4":
            id_sup = input("ID do supermercado: ").strip()
            print("(Deixe em branco para não alterar)")
            numero = input("Novo número: ").strip() or None
            morada = input("Nova morada: ").strip() or None
            nif = input("Novo NIF: ").strip() or None
            _mostrar_resultado(atualizar_supermercado(id_sup, numero, morada, nif))

        elif opcao == "5":
            id_sup = input("ID do supermercado: ").strip()
            _mostrar_resultado(remover_supermercado(id_sup))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENUS DE COMPRA
# ==============================

def menu_compras():
    while True:
        print("\n========== COMPRAS ==========")
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
            id_cl = input("ID do cliente: ").strip()
            id_sup = input("ID do supermercado: ").strip()
            data = input("Data (DD/MM/AAAA): ").strip()
            valor = input("Valor total (€): ").strip()
            _mostrar_resultado(criar_compra(id_cl, id_sup, data, valor))

        elif opcao == "2":
            _mostrar_resultado(listar_compras())

        elif opcao == "3":
            id_cl = input("ID do cliente: ").strip()
            _mostrar_resultado(listar_compras_por_cliente(id_cl))

        elif opcao == "4":
            id_sup = input("ID do supermercado: ").strip()
            _mostrar_resultado(listar_compras_por_supermercado(id_sup))

        elif opcao == "5":
            id_comp = input("ID da compra: ").strip()
            consultar_compra(id_comp)

        elif opcao == "6":
            id_comp = input("ID da compra: ").strip()
            print("(Deixe em branco para não alterar)")
            data = input("Nova data (DD/MM/AAAA): ").strip() or None
            valor = input("Novo valor total (€): ").strip() or None
            _mostrar_resultado(atualizar_compra(id_comp, data, valor))

        elif opcao == "7":
            id_comp = input("ID da compra: ").strip()
            _mostrar_resultado(remover_compra(id_comp))

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ==============================
# MENU PRINCIPAL
# ==============================

def menu_principal():
    while True:
        print("\n========================================")
        print("     SISTEMA DE GESTÃO - SUPERMERCADO   ")
        print("========================================")
        print("1. Categorias")
        print("2. Produtos")
        print("3. Clientes")
        print("4. Supermercados")
        print("5. Compras")
        print("0. Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            menu_categorias()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            menu_clientes()
        elif opcao == "4":
            menu_supermercados()
        elif opcao == "5":
            menu_compras()
        elif opcao == "0":
            print("A sair... Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
