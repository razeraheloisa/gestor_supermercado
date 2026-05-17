# ==============================
# cliente.py
# CRUD simples para entidade Cliente
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_cliente, validar_contacto, validar_email, validar_nif
import json
import os


clientes = {}
FICHEIRO_CLIENTES = "clientes.json"

# ==============================
# Persistência
# ==============================

def guardar_clientes():
    with open(FICHEIRO_CLIENTES, "w", encoding="utf-8") as ficheiro:
        json.dump(clientes, ficheiro, indent=4, ensure_ascii=False)


def carregar_clientes():
    global clientes

    if os.path.exists(FICHEIRO_CLIENTES):
        with open(FICHEIRO_CLIENTES, "r", encoding="utf-8") as ficheiro:
            clientes = json.load(ficheiro)
    else:
        clientes = {}



# CREATE
def criar_cliente(nome, contacto, email="", nif=""):
    carregar_clientes()
    if not nome.strip():
        return 400, "o nome do cliente não pode estar vazio."

    if not validar_contacto(contacto):
        return 400, "contacto inválido. Introduza um número de telefone com 9 dígitos."

    if email.strip() and not validar_email(email):
        return 400, "email inválido. Introduza um endereço de email válido (ex: nome@dominio.pt)."

    if nif.strip() and not validar_nif(nif):
        return 400, "NIF inválido. O NIF deve ter exactamente 9 dígitos numéricos."

    if nif.strip():
        for dados in clientes.values():
            if dados["nif"] == nif.strip():
                return 409, f"já existe um cliente com o NIF '{nif}'."

    id_cliente = gerar_id_cliente()
    clientes[id_cliente] = {
        "nome": nome.strip(),
        "contacto": contacto.strip(),
        "email": email.strip(),
        "nif": nif.strip()
    }
    guardar_clientes()
    return 201, clientes[id_cliente]


# READ (listar todos)
def listar_clientes():
    carregar_clientes()
    if not clientes:
        return 404, "não existem clientes registados."

    print("\n{:<8} {:<25} {:<12} {:<25} {:<12}".format(
        "ID", "Nome", "Contacto", "Email", "NIF"
    ))
    print("-" * 85)
    for id_cliente, dados in clientes.items():
        print("{:<8} {:<25} {:<12} {:<25} {:<12}".format(
            id_cliente,
            dados["nome"],
            dados["contacto"],
            dados["email"] if dados["email"] else "-",
            dados["nif"] if dados["nif"] else "-"
        ))
    return 200, clientes


# READ (consultar individual)
def consultar_cliente(id_cliente):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, f"cliente '{id_cliente}' não encontrado."

    dados = clientes[id_cliente]
    print(f"\n--- Cliente ---")
    print(f"ID:        {id_cliente}")
    print(f"Nome:      {dados['nome']}")
    print(f"Contacto:  {dados['contacto']}")
    print(f"Email:     {dados['email'] if dados['email'] else '-'}")
    print(f"NIF:       {dados['nif'] if dados['nif'] else '-'}")
    return 200, dados


# READ (pesquisar por nome ou NIF)
def pesquisar_cliente(termo):
    carregar_clientes()
    termo = termo.strip().lower()
    encontrados = {
        cid: d for cid, d in clientes.items()
        if termo in d["nome"].lower() or termo == d["nif"]
    }

    if not encontrados:
        return 404, f"nenhum cliente encontrado com o termo '{termo}'."

    print("\n{:<8} {:<25} {:<12} {:<25} {:<12}".format(
        "ID", "Nome", "Contacto", "Email", "NIF"
    ))
    print("-" * 85)
    for id_cliente, dados in encontrados.items():
        print("{:<8} {:<25} {:<12} {:<25} {:<12}".format(
            id_cliente,
            dados["nome"],
            dados["contacto"],
            dados["email"] if dados["email"] else "-",
            dados["nif"] if dados["nif"] else "-"
        ))
    return 200, encontrados


# UPDATE
def atualizar_cliente(id_cliente, nome=None, contacto=None, email=None, nif=None):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, f"cliente '{id_cliente}' não encontrado."

    if nome is not None:
        if not nome.strip():
            return 400, "o nome não pode estar vazio."
        clientes[id_cliente]["nome"] = nome.strip()

    if contacto is not None:
        if not validar_contacto(contacto):
            return 400, "contacto inválido. Introduza um número de telefone com 9 dígitos."
        clientes[id_cliente]["contacto"] = contacto.strip()

    if email is not None:
        if email.strip() and not validar_email(email):
            return 400, "email inválido."
        clientes[id_cliente]["email"] = email.strip()

    if nif is not None:
        if nif.strip() and not validar_nif(nif):
            return 400, "NIF inválido. O NIF deve ter exactamente 9 dígitos numéricos."
        if nif.strip():
            for cid, dados in clientes.items():
                if cid != id_cliente and dados["nif"] == nif.strip():
                    return 409, f"já existe um cliente com o NIF '{nif}'."
        clientes[id_cliente]["nif"] = nif.strip()
    guardar_clientes()
    return 200, clientes[id_cliente]


# DELETE
def remover_cliente(id_cliente):
    carregar_clientes()
    if id_cliente not in clientes:
        return 404, f"cliente '{id_cliente}' não encontrado."

    from compra import compras
    for dados_compra in compras.values():
        if dados_compra["id_cliente"] == id_cliente:
            return 409, f"não é possível remover o cliente '{id_cliente}' porque tem compras associadas."

    del clientes[id_cliente]
    guardar_clientes()
    return 200, id_cliente

def cliente_existe(id_cliente):
    carregar_clientes()
    """Verifica se um cliente existe. Usada por compra.py."""
    return id_cliente in clientes
