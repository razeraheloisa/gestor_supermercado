# ==============================
# cliente.py
# CRUD simples para entidade Cliente
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

import logging

from utils import gerar_id_cliente, validar_contacto, validar_email, validar_nif

logger = logging.getLogger(__name__)

clientes = {}


# CREATE
def criar_cliente(nome, contacto, email="", nif=""):
    if not nome.strip():
        logging.error("Tentativa de criar cliente com nome vazio.")
        return 400, "o nome do cliente não pode estar vazio."

    if not validar_contacto(contacto):
        logging.error(f"Contacto inválido ao criar cliente: '{contacto}'.")
        return 400, "contacto inválido. Introduza um número de telefone com 9 dígitos."

    if email.strip() and not validar_email(email):
        logging.error(f"Email inválido ao criar cliente: '{email}'.")
        return 400, "email inválido. Introduza um endereço de email válido (ex: nome@dominio.pt)."

    if nif.strip() and not validar_nif(nif):
        logging.error(f"NIF inválido ao criar cliente: '{nif}'.")
        return 400, "NIF inválido. O NIF deve ter exactamente 9 dígitos numéricos."

    if nif.strip():
        for dados in clientes.values():
            if dados["nif"] == nif.strip():
                logging.warning(f"Cliente duplicado: NIF '{nif}' já existe.")
                return 409, f"já existe um cliente com o NIF '{nif}'."

    id_cliente = gerar_id_cliente()
    clientes[id_cliente] = {
        "nome": nome.strip(),
        "contacto": contacto.strip(),
        "email": email.strip(),
        "nif": nif.strip()
    }
    logging.info(f"Cliente criado com sucesso. ID: {id_cliente} | Nome: '{nome.strip()}'.")
    return 201, f"Cliente criado com sucesso. ID: {id_cliente}"


# READ (listar todos)
def listar_clientes():
    if not clientes:
        logging.error("Listagem de clientes: nenhum cliente registado.")
        return 404, "não existem clientes registados."

    logging.debug(f"Listagem de clientes: {len(clientes)} cliente(s) encontrado(s).")
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
    return 200, ""


# READ (consultar individual)
def consultar_cliente(id_cliente):
    if id_cliente not in clientes:
        logging.error(f"Cliente não encontrado: {id_cliente}.")
        return 404, f"cliente '{id_cliente}' não encontrado."

    logging.debug(f"Consulta de cliente: {id_cliente}.")
    dados = clientes[id_cliente]
    print(f"\n--- Cliente ---")
    print(f"ID:        {id_cliente}")
    print(f"Nome:      {dados['nome']}")
    print(f"Contacto:  {dados['contacto']}")
    print(f"Email:     {dados['email'] if dados['email'] else '-'}")
    print(f"NIF:       {dados['nif'] if dados['nif'] else '-'}")
    return 200, ""


# READ (pesquisar por nome ou NIF)
def pesquisar_cliente(termo):
    termo = termo.strip().lower()
    encontrados = {
        cid: d for cid, d in clientes.items()
        if termo in d["nome"].lower() or termo == d["nif"]
    }

    if not encontrados:
        logging.error(f"Pesquisa de cliente sem resultados: termo '{termo}'.")
        return 404, f"nenhum cliente encontrado com o termo '{termo}'."

    logging.debug(f"Pesquisa de cliente com termo '{termo}': {len(encontrados)} resultado(s).")
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
    return 200, ""


# UPDATE
def atualizar_cliente(id_cliente, nome=None, contacto=None, email=None, nif=None):
    if id_cliente not in clientes:
        logging.error(f"Cliente não encontrado para atualização: {id_cliente}.")
        return 404, f"cliente '{id_cliente}' não encontrado."

    if nome is not None:
        if not nome.strip():
            logging.error(f"Tentativa de atualizar cliente {id_cliente} com nome vazio.")
            return 400, "o nome não pode estar vazio."
        clientes[id_cliente]["nome"] = nome.strip()

    if contacto is not None:
        if not validar_contacto(contacto):
            logging.error(f"Contacto inválido ao atualizar cliente {id_cliente}: '{contacto}'.")
            return 400, "contacto inválido. Introduza um número de telefone com 9 dígitos."
        clientes[id_cliente]["contacto"] = contacto.strip()

    if email is not None:
        if email.strip() and not validar_email(email):
            logging.error(f"Email inválido ao atualizar cliente {id_cliente}: '{email}'.")
            return 400, "email inválido."
        clientes[id_cliente]["email"] = email.strip()

    if nif is not None:
        if nif.strip() and not validar_nif(nif):
            logging.error(f"NIF inválido ao atualizar cliente {id_cliente}: '{nif}'.")
            return 400, "NIF inválido. O NIF deve ter exactamente 9 dígitos numéricos."
        if nif.strip():
            for cid, dados in clientes.items():
                if cid != id_cliente and dados["nif"] == nif.strip():
                    logging.warning(f"Conflito de NIF ao atualizar cliente {id_cliente}: '{nif}' já existe.")
                    return 409, f"já existe um cliente com o NIF '{nif}'."
        clientes[id_cliente]["nif"] = nif.strip()

    logging.info(f"Cliente atualizado com sucesso. ID: {id_cliente}.")
    return 200, "cliente atualizado com sucesso."


# DELETE
def remover_cliente(id_cliente):
    if id_cliente not in clientes:
        logging.error(f"Cliente não encontrado para remoção: {id_cliente}.")
        return 404, f"cliente '{id_cliente}' não encontrado."

    from compra import compras
    for dados_compra in compras.values():
        if dados_compra["id_cliente"] == id_cliente:
            logging.warning(f"Tentativa de remover cliente {id_cliente} com compras associadas.")
            return 409, f"não é possível remover o cliente '{id_cliente}' porque tem compras associadas."

    del clientes[id_cliente]
    logging.info(f"Cliente removido com sucesso. ID: {id_cliente}.")
    return 200, "cliente removido com sucesso."


def cliente_existe(id_cliente):
    """Verifica se um cliente existe. Usada por compra.py."""
    existe = id_cliente in clientes
    logging.debug(f"Verificação de existência de cliente {id_cliente}: {'encontrado' if existe else 'não encontrado'}.")
    return existe
