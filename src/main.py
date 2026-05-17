# ==============================
# main.py
# Menu principal da aplicação
# Apenas chama funções dos módulos
# e apresenta resultados ao utilizador
# ==============================

import os
import sys

from cliente import (
    criar_cliente, listar_clientes, consultar_cliente,
    pesquisar_cliente, atualizar_cliente, remover_cliente
)
from supermercado import (
    criar_supermercado, listar_supermercados, consultar_supermercado,
    atualizar_supermercado, remover_supermercado
)
from categoria import (
    criar_categoria, listar_categorias, consultar_categoria,
    atualizar_categoria, remover_categoria
)
from produto import (
    criar_produto, listar_produtos, consultar_produto,
    listar_produtos_por_categoria, atualizar_produto, remover_produto
)
from compra import (
    criar_compra, listar_compras, consultar_compra,
    listar_compras_por_cliente, listar_compras_por_supermercado,
    atualizar_compra, remover_compra
)


# ==============================
# Utilitários de input com loop
# ==============================

CANCELAR = "x"

def input_campo(mensagem, validar_fn=None, obrigatorio=True, valor_atual=None):
    """
    Pede um campo em loop até ser válido.
    - Digite 'x' para cancelar (retorna None).
    - Se valor_atual fornecido, mostra entre colchetes e aceita Enter para manter.
    - validar_fn(texto) deve retornar (True, texto_tratado) ou (False, mensagem_erro).
    """
    sufixo = f" [{valor_atual}]" if valor_atual is not None else ""
    sufixo += f" (ou '{CANCELAR}' para cancelar)"

    while True:
        resposta = input(f"{mensagem}{sufixo}: ").strip()

        if resposta.lower() == CANCELAR:
            return None  # sinal de cancelamento

        # Enter sem valor → mantém valor actual (só em edições)
        if resposta == "" and valor_atual is not None:
            return valor_atual

        # Campo obrigatório vazio
        if resposta == "" and obrigatorio:
            print(f"  ✖  Este campo é obrigatório.")
            continue

        # Sem validação extra → aceita
        if validar_fn is None:
            return resposta

        ok, resultado = validar_fn(resposta)
        if ok:
            return resultado
        else:
            print(f"  ✖  {resultado}")
            # loop → repete só este campo


def confirmar(mensagem):
    """Pede s/n. Retorna True para 's', False para qualquer outra coisa."""
    resposta = input(f"{mensagem} (s/n): ").strip().lower()
    return resposta == "s"


def pausar():
    input("\nPrime Enter para continuar...")


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def tratar_resultado(codigo, mensagem_ou_dados):
    """
    Imprime resultado de uma operação CRUD e devolve True se sucesso.
    """
    if codigo in (200, 201):
        if isinstance(mensagem_ou_dados, str):
            print(f"\n  ✔  {mensagem_ou_dados}")
        else:
            print(f"\n  ✔  Operação concluída com sucesso.")
        return True
    else:
        print(f"\n  ✖  {mensagem_ou_dados}")
        return False


# ==============================
# Menus de input — cada campo
# tem o seu loop individual
# ==============================

# ---------- CLIENTES ----------

def menu_criar_cliente():
    print("\n=== Novo Cliente ===")

    # Nome — loop até válido ou cancelar
    nome = input_campo("Nome")
    if nome is None:
        return

    # Contacto — loop até 9 dígitos ou cancelar
    from utils import validar_contacto
    def val_contacto(v):
        if validar_contacto(v):
            return True, v
        return False, "contacto inválido. Introduza um número com 9 dígitos."
    contacto = input_campo("Contacto (9 dígitos)", val_contacto)
    if contacto is None:
        return

    # Email — opcional, mas validado se preenchido
    from utils import validar_email
    def val_email(v):
        if v == "" or validar_email(v):
            return True, v
        return False, "email inválido. Ex: nome@dominio.pt"
    email = input_campo("Email (opcional, Enter para ignorar)", val_email, obrigatorio=False)
    if email is None:
        return

    # NIF — opcional, mas validado se preenchido
    from utils import validar_nif
    def val_nif(v):
        if v == "" or validar_nif(v):
            return True, v
        return False, "NIF inválido. Deve ter exactamente 9 dígitos numéricos."
    nif = input_campo("NIF (opcional, Enter para ignorar)", val_nif, obrigatorio=False)
    if nif is None:
        return

    codigo, dados = criar_cliente(nome, contacto, email or "", nif or "")
    tratar_resultado(codigo, dados)
    pausar()


def menu_consultar_cliente():
    print("\n=== Consultar Cliente ===")
    while True:
        id_cliente = input_campo("ID do cliente")
        if id_cliente is None:
            return
        codigo, dados = consultar_cliente(id_cliente)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
        # loop → pede o ID de novo
    pausar()


def menu_pesquisar_cliente():
    print("\n=== Pesquisar Cliente ===")
    termo = input_campo("Nome ou NIF a pesquisar")
    if termo is None:
        return
    codigo, dados = pesquisar_cliente(termo)
    if codigo != 200:
        print(f"  ✖  {dados}")
    pausar()


def menu_atualizar_cliente():
    print("\n=== Editar Cliente ===")

    # ID — loop até encontrar ou cancelar
    while True:
        id_cliente = input_campo("ID do cliente a editar")
        if id_cliente is None:
            return
        codigo, dados = consultar_cliente(id_cliente)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    from utils import validar_contacto, validar_email, validar_nif
    print("  (Enter para manter o valor actual, 'x' para cancelar)\n")

    def val_contacto(v):
        if validar_contacto(v):
            return True, v
        return False, "contacto inválido. Introduza um número com 9 dígitos."

    def val_email(v):
        if v == "" or validar_email(v):
            return True, v
        return False, "email inválido. Ex: nome@dominio.pt"

    def val_nif(v):
        if v == "" or validar_nif(v):
            return True, v
        return False, "NIF inválido. Deve ter exactamente 9 dígitos numéricos."

    nome = input_campo("Nome", valor_atual=dados["nome"])
    if nome is None:
        return

    contacto = input_campo("Contacto", val_contacto, valor_atual=dados["contacto"])
    if contacto is None:
        return

    email = input_campo("Email", val_email, obrigatorio=False, valor_atual=dados["email"] or "")
    if email is None:
        return

    nif = input_campo("NIF", val_nif, obrigatorio=False, valor_atual=dados["nif"] or "")
    if nif is None:
        return

    codigo, resultado = atualizar_cliente(id_cliente,
        nome=nome, contacto=contacto, email=email, nif=nif)
    tratar_resultado(codigo, resultado)
    pausar()


def menu_remover_cliente():
    print("\n=== Remover Cliente ===")
    while True:
        id_cliente = input_campo("ID do cliente a remover")
        if id_cliente is None:
            return
        codigo, dados = consultar_cliente(id_cliente)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    if not confirmar(f"Tem a certeza que quer remover o cliente '{id_cliente}'?"):
        print("  Operação cancelada.")
        pausar()
        return

    codigo, resultado = remover_cliente(id_cliente)
    tratar_resultado(codigo, resultado)
    pausar()


# ---------- SUPERMERCADOS ----------

def menu_criar_supermercado():
    print("\n=== Novo Supermercado ===")
    from utils import validar_nif

    numero = input_campo("Número do supermercado")
    if numero is None:
        return

    morada = input_campo("Morada")
    if morada is None:
        return

    def val_nif(v):
        if validar_nif(v):
            return True, v
        return False, "NIF inválido. Deve ter exactamente 9 dígitos numéricos."

    nif = input_campo("NIF (9 dígitos)", val_nif)
    if nif is None:
        return

    codigo, dados = criar_supermercado(numero, morada, nif)
    tratar_resultado(codigo, dados)
    pausar()


def menu_consultar_supermercado():
    print("\n=== Consultar Supermercado ===")
    while True:
        id_super = input_campo("ID do supermercado")
        if id_super is None:
            return
        codigo, dados = consultar_supermercado(id_super)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_atualizar_supermercado():
    print("\n=== Editar Supermercado ===")
    from utils import validar_nif

    while True:
        id_super = input_campo("ID do supermercado a editar")
        if id_super is None:
            return
        codigo, dados = consultar_supermercado(id_super)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    print("  (Enter para manter o valor actual, 'x' para cancelar)\n")

    def val_nif(v):
        if validar_nif(v):
            return True, v
        return False, "NIF inválido. Deve ter exactamente 9 dígitos numéricos."

    numero = input_campo("Número", valor_atual=dados["numero"])
    if numero is None:
        return

    morada = input_campo("Morada", valor_atual=dados["morada"])
    if morada is None:
        return

    nif = input_campo("NIF", val_nif, valor_atual=dados["nif"])
    if nif is None:
        return

    codigo, resultado = atualizar_supermercado(id_super, numero=numero, morada=morada, nif=nif)
    tratar_resultado(codigo, resultado)
    pausar()


def menu_remover_supermercado():
    print("\n=== Remover Supermercado ===")
    while True:
        id_super = input_campo("ID do supermercado a remover")
        if id_super is None:
            return
        codigo, dados = consultar_supermercado(id_super)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    if not confirmar(f"Tem a certeza que quer remover o supermercado '{id_super}'?"):
        print("  Operação cancelada.")
        pausar()
        return

    codigo, resultado = remover_supermercado(id_super)
    tratar_resultado(codigo, resultado)
    pausar()


# ---------- CATEGORIAS ----------

def menu_criar_categoria():
    print("\n=== Nova Categoria ===")

    nome_cat = input_campo("Nome da categoria")
    if nome_cat is None:
        return

    descricao = input_campo("Descrição")
    if descricao is None:
        return

    codigo, dados = criar_categoria(nome_cat, descricao)
    tratar_resultado(codigo, dados)
    pausar()


def menu_consultar_categoria():
    print("\n=== Consultar Categoria ===")
    while True:
        id_cat = input_campo("ID da categoria")
        if id_cat is None:
            return
        codigo, dados = consultar_categoria(id_cat)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_atualizar_categoria():
    print("\n=== Editar Categoria ===")

    while True:
        id_cat = input_campo("ID da categoria a editar")
        if id_cat is None:
            return
        codigo, dados = consultar_categoria(id_cat)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    print("  (Enter para manter o valor actual, 'x' para cancelar)\n")

    nome_cat = input_campo("Nome", valor_atual=dados["nome_categoria"])
    if nome_cat is None:
        return

    descricao = input_campo("Descrição", valor_atual=dados["descricao"])
    if descricao is None:
        return

    codigo, resultado = atualizar_categoria(id_cat, nome_categoria=nome_cat, descricao=descricao)
    tratar_resultado(codigo, resultado)
    pausar()


def menu_remover_categoria():
    print("\n=== Remover Categoria ===")
    while True:
        id_cat = input_campo("ID da categoria a remover")
        if id_cat is None:
            return
        codigo, dados = consultar_categoria(id_cat)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    if not confirmar(f"Tem a certeza que quer remover a categoria '{id_cat}'?"):
        print("  Operação cancelada.")
        pausar()
        return

    codigo, resultado = remover_categoria(id_cat)
    tratar_resultado(codigo, resultado)
    pausar()


# ---------- PRODUTOS ----------

def menu_criar_produto():
    print("\n=== Novo Produto ===")
    from utils import validar_preco, validar_quantidade, validar_peso

    nome = input_campo("Nome do produto")
    if nome is None:
        return

    def val_preco(v):
        if validar_preco(v):
            return True, v
        return False, "preço inválido. Introduza um número positivo (ex: 1.99)."

    def val_qtd(v):
        if validar_quantidade(v):
            return True, v
        return False, "quantidade inválida. Introduza um número inteiro não negativo."

    def val_peso(v):
        if validar_peso(v):
            return True, v
        return False, "peso inválido. Introduza um número positivo (ex: 0.5)."

    preco = input_campo("Preço (€)", val_preco)
    if preco is None:
        return

    quantidade = input_campo("Quantidade em stock", val_qtd)
    if quantidade is None:
        return

    # ID Categoria — loop até existir ou cancelar
    listar_categorias()
    while True:
        id_cat = input_campo("ID da categoria")
        if id_cat is None:
            return
        from categoria import categoria_existe
        if categoria_existe(id_cat):
            break
        print(f"  ✖  categoria '{id_cat}' não encontrada.")

    peso = input_campo("Peso (kg)", val_peso)
    if peso is None:
        return

    codigo, dados = criar_produto(nome, preco, quantidade, id_cat, peso)
    tratar_resultado(codigo, dados)
    pausar()


def menu_consultar_produto():
    print("\n=== Consultar Produto ===")
    while True:
        id_produto = input_campo("ID do produto")
        if id_produto is None:
            return
        codigo, dados = consultar_produto(id_produto)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_listar_produtos_por_categoria():
    print("\n=== Produtos por Categoria ===")
    listar_categorias()
    while True:
        id_cat = input_campo("ID da categoria")
        if id_cat is None:
            return
        codigo, dados = listar_produtos_por_categoria(id_cat)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_atualizar_produto():
    print("\n=== Editar Produto ===")
    from utils import validar_preco, validar_quantidade, validar_peso

    while True:
        id_produto = input_campo("ID do produto a editar")
        if id_produto is None:
            return
        codigo, dados = consultar_produto(id_produto)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    print("  (Enter para manter o valor actual, 'x' para cancelar)\n")

    def val_preco(v):
        if validar_preco(v):
            return True, v
        return False, "preço inválido. Introduza um número positivo (ex: 1.99)."

    def val_qtd(v):
        if validar_quantidade(v):
            return True, v
        return False, "quantidade inválida. Introduza um número inteiro não negativo."

    def val_peso(v):
        if validar_peso(v):
            return True, v
        return False, "peso inválido. Introduza um número positivo (ex: 0.5)."

    nome = input_campo("Nome", valor_atual=dados["nome"])
    if nome is None:
        return

    preco = input_campo("Preço (€)", val_preco, valor_atual=str(dados["preco"]))
    if preco is None:
        return

    quantidade = input_campo("Stock", val_qtd, valor_atual=str(dados["quantidade_stock"]))
    if quantidade is None:
        return

    # Categoria — loop até existir ou cancelar
    while True:
        id_cat = input_campo("ID da categoria", valor_atual=dados["id_categoria"])
        if id_cat is None:
            return
        from categoria import categoria_existe
        if categoria_existe(id_cat):
            break
        print(f"  ✖  categoria '{id_cat}' não encontrada.")

    peso = input_campo("Peso (kg)", val_peso, valor_atual=str(dados["peso"]))
    if peso is None:
        return

    codigo, resultado = atualizar_produto(
        id_produto, nome=nome, preco_texto=preco,
        quantidade_texto=quantidade, id_categoria=id_cat, peso_texto=peso
    )
    tratar_resultado(codigo, resultado)
    pausar()


def menu_remover_produto():
    print("\n=== Remover Produto ===")
    while True:
        id_produto = input_campo("ID do produto a remover")
        if id_produto is None:
            return
        codigo, dados = consultar_produto(id_produto)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    if not confirmar(f"Tem a certeza que quer remover o produto '{id_produto}'?"):
        print("  Operação cancelada.")
        pausar()
        return

    codigo, resultado = remover_produto(id_produto)
    tratar_resultado(codigo, resultado)
    pausar()


# ---------- COMPRAS ----------

def menu_criar_compra():
    print("\n=== Nova Compra ===")
    from utils import validar_data, validar_preco

    # Cliente — loop até existir ou cancelar
    listar_clientes()
    while True:
        id_cliente = input_campo("ID do cliente")
        if id_cliente is None:
            return
        from cliente import cliente_existe
        if cliente_existe(id_cliente):
            break
        print(f"  ✖  cliente '{id_cliente}' não encontrado.")

    # Supermercado — loop até existir ou cancelar
    listar_supermercados()
    while True:
        id_super = input_campo("ID do supermercado")
        if id_super is None:
            return
        from supermercado import supermercado_existe
        if supermercado_existe(id_super):
            break
        print(f"  ✖  supermercado '{id_super}' não encontrado.")

    def val_data(v):
        if validar_data(v):
            return True, v
        return False, "data inválida. Utilize o formato DD/MM/AAAA (ex: 25/04/2025)."

    def val_valor(v):
        if validar_preco(v):
            return True, v
        return False, "valor inválido. Introduza um número positivo (ex: 15.99)."

    data = input_campo("Data (DD/MM/AAAA)", val_data)
    if data is None:
        return

    valor = input_campo("Valor total (€)", val_valor)
    if valor is None:
        return

    codigo, dados = criar_compra(id_cliente, id_super, data, valor)
    tratar_resultado(codigo, dados)
    pausar()


def menu_consultar_compra():
    print("\n=== Consultar Compra ===")
    while True:
        id_compra = input_campo("ID da compra")
        if id_compra is None:
            return
        codigo, dados = consultar_compra(id_compra)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_compras_por_cliente():
    print("\n=== Compras por Cliente ===")
    listar_clientes()
    while True:
        id_cliente = input_campo("ID do cliente")
        if id_cliente is None:
            return
        codigo, dados = listar_compras_por_cliente(id_cliente)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_compras_por_supermercado():
    print("\n=== Compras por Supermercado ===")
    listar_supermercados()
    while True:
        id_super = input_campo("ID do supermercado")
        if id_super is None:
            return
        codigo, dados = listar_compras_por_supermercado(id_super)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")
    pausar()


def menu_atualizar_compra():
    print("\n=== Editar Compra ===")
    from utils import validar_data, validar_preco

    while True:
        id_compra = input_campo("ID da compra a editar")
        if id_compra is None:
            return
        codigo, dados = consultar_compra(id_compra)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    print("  (Enter para manter o valor actual, 'x' para cancelar)\n")

    def val_data(v):
        if validar_data(v):
            return True, v
        return False, "data inválida. Utilize o formato DD/MM/AAAA."

    def val_valor(v):
        if validar_preco(v):
            return True, v
        return False, "valor inválido. Introduza um número positivo."

    data = input_campo("Data", val_data, valor_atual=dados["data"])
    if data is None:
        return

    valor = input_campo("Valor total (€)", val_valor, valor_atual=str(dados["valor_total"]))
    if valor is None:
        return

    codigo, resultado = atualizar_compra(id_compra, data=data, valor_total_texto=valor)
    tratar_resultado(codigo, resultado)
    pausar()


def menu_remover_compra():
    print("\n=== Remover Compra ===")
    while True:
        id_compra = input_campo("ID da compra a remover")
        if id_compra is None:
            return
        codigo, dados = consultar_compra(id_compra)
        if codigo == 200:
            break
        print(f"  ✖  {dados}")

    if not confirmar(f"Tem a certeza que quer remover a compra '{id_compra}'?"):
        print("  Operação cancelada.")
        pausar()
        return

    codigo, resultado = remover_compra(id_compra)
    tratar_resultado(codigo, resultado)
    pausar()


# ==============================
# Menus de navegação
# ==============================

def submenu_clientes():
    while True:
        limpar()
        print("""
╔══════════════════════════════╗
║         CLIENTES             ║
╠══════════════════════════════╣
║  1. Listar todos             ║
║  2. Consultar por ID         ║
║  3. Pesquisar (nome/NIF)     ║
║  4. Criar novo               ║
║  5. Editar                   ║
║  6. Remover                  ║
║  0. Voltar                   ║
╚══════════════════════════════╝""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            codigo, dados = listar_clientes()
            if codigo != 200:
                print(f"  ✖  {dados}")
            pausar()
        elif opcao == "2":
            menu_consultar_cliente()
        elif opcao == "3":
            menu_pesquisar_cliente()
        elif opcao == "4":
            menu_criar_cliente()
        elif opcao == "5":
            menu_atualizar_cliente()
        elif opcao == "6":
            menu_remover_cliente()
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")
            pausar()


def submenu_supermercados():
    while True:
        limpar()
        print("""
╔══════════════════════════════╗
║       SUPERMERCADOS          ║
╠══════════════════════════════╣
║  1. Listar todos             ║
║  2. Consultar por ID         ║
║  3. Criar novo               ║
║  4. Editar                   ║
║  5. Remover                  ║
║  0. Voltar                   ║
╚══════════════════════════════╝""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            codigo, dados = listar_supermercados()
            if codigo != 200:
                print(f"  ✖  {dados}")
            pausar()
        elif opcao == "2":
            menu_consultar_supermercado()
        elif opcao == "3":
            menu_criar_supermercado()
        elif opcao == "4":
            menu_atualizar_supermercado()
        elif opcao == "5":
            menu_remover_supermercado()
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")
            pausar()


def submenu_categorias():
    while True:
        limpar()
        print("""
╔══════════════════════════════╗
║         CATEGORIAS           ║
╠══════════════════════════════╣
║  1. Listar todas             ║
║  2. Consultar por ID         ║
║  3. Criar nova               ║
║  4. Editar                   ║
║  5. Remover                  ║
║  0. Voltar                   ║
╚══════════════════════════════╝""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            codigo, dados = listar_categorias()
            if codigo != 200:
                print(f"  ✖  {dados}")
            pausar()
        elif opcao == "2":
            menu_consultar_categoria()
        elif opcao == "3":
            menu_criar_categoria()
        elif opcao == "4":
            menu_atualizar_categoria()
        elif opcao == "5":
            menu_remover_categoria()
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")
            pausar()


def submenu_produtos():
    while True:
        limpar()
        print("""
╔══════════════════════════════╗
║          PRODUTOS            ║
╠══════════════════════════════╣
║  1. Listar todos             ║
║  2. Listar por categoria     ║
║  3. Consultar por ID         ║
║  4. Criar novo               ║
║  5. Editar                   ║
║  6. Remover                  ║
║  0. Voltar                   ║
╚══════════════════════════════╝""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            codigo, dados = listar_produtos()
            if codigo != 200:
                print(f"  ✖  {dados}")
            pausar()
        elif opcao == "2":
            menu_listar_produtos_por_categoria()
        elif opcao == "3":
            menu_consultar_produto()
        elif opcao == "4":
            menu_criar_produto()
        elif opcao == "5":
            menu_atualizar_produto()
        elif opcao == "6":
            menu_remover_produto()
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")
            pausar()


def submenu_compras():
    while True:
        limpar()
        print("""
╔══════════════════════════════╗
║          COMPRAS             ║
╠══════════════════════════════╣
║  1. Listar todas             ║
║  2. Compras de um cliente    ║
║  3. Compras de supermercado  ║
║  4. Consultar por ID         ║
║  5. Criar nova               ║
║  6. Editar                   ║
║  7. Remover                  ║
║  0. Voltar                   ║
╚══════════════════════════════╝""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            codigo, dados = listar_compras()
            if codigo != 200:
                print(f"  ✖  {dados}")
            pausar()
        elif opcao == "2":
            menu_compras_por_cliente()
        elif opcao == "3":
            menu_compras_por_supermercado()
        elif opcao == "4":
            menu_consultar_compra()
        elif opcao == "5":
            menu_criar_compra()
        elif opcao == "6":
            menu_atualizar_compra()
        elif opcao == "7":
            menu_remover_compra()
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")
            pausar()


def menu_principal():
    while True:
        limpar()
        print("""
╔══════════════════════════════╗
║      GESTÃO DE COMPRAS       ║
╠══════════════════════════════╣
║  1. Clientes                 ║
║  2. Supermercados            ║
║  3. Categorias               ║
║  4. Produtos                 ║
║  5. Compras                  ║
║  0. Sair                     ║
╚══════════════════════════════╝""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            submenu_clientes()
        elif opcao == "2":
            submenu_supermercados()
        elif opcao == "3":
            submenu_categorias()
        elif opcao == "4":
            submenu_produtos()
        elif opcao == "5":
            submenu_compras()
        elif opcao == "0":
            print("\nAté logo!\n")
            sys.exit(0)
        else:
            print("  Opção inválida.")
            pausar()


if __name__ == "__main__":
    menu_principal()
