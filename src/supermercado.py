# ==============================
# supermercado.py
# CRUD simples para entidade Supermercado
# SEM utilização de classes
# armazenamento em dicionário
# validações feitas aqui (não no main)
# ==============================

import logging

from utils import gerar_id_supermercado, validar_nif

logger = logging.getLogger(__name__)

supermercados = {}


# CREATE
def criar_supermercado(numero, morada, nif):
    if not numero.strip():
        logging.error("Tentativa de criar supermercado com número vazio.")
        return 400, "o número do supermercado não pode estar vazio."

    if not morada.strip():
        logging.error("Tentativa de criar supermercado com morada vazia.")
        return 400, "a morada não pode estar vazia."

    if not validar_nif(nif):
        logging.error(f"NIF inválido ao criar supermercado: '{nif}'.")
        return 400, "NIF inválido. O NIF deve ter exactamente 9 dígitos numéricos."

    for dados in supermercados.values():
        if dados["nif"] == nif.strip():
            logging.warning(f"Supermercado duplicado: NIF '{nif}' já existe.")
            return 409, f"já existe um supermercado com o NIF '{nif}'."

    for dados in supermercados.values():
        if dados["numero"].lower() == numero.strip().lower():
            logging.warning(f"Supermercado duplicado: número '{numero}' já existe.")
            return 409, f"já existe um supermercado com o número '{numero}'."

    id_supermercado = gerar_id_supermercado()
    supermercados[id_supermercado] = {
        "numero": numero.strip(),
        "morada": morada.strip(),
        "nif": nif.strip()
    }
    logging.info(f"Supermercado criado com sucesso. ID: {id_supermercado} | Número: '{numero.strip()}' | Morada: '{morada.strip()}'.")
    return 201, f"Supermercado criado com sucesso. ID: {id_supermercado}"


# READ (listar todos)
def listar_supermercados():
    if not supermercados:
        logging.error("Listagem de supermercados: nenhum supermercado registado.")
        return 404, "não existem supermercados registados."

    logging.debug(f"Listagem de supermercados: {len(supermercados)} supermercado(s) encontrado(s).")
    print("\n{:<8} {:<12} {:<35} {:<12}".format(
        "ID", "Número", "Morada", "NIF"
    ))
    print("-" * 70)
    for id_supermercado, dados in supermercados.items():
        print("{:<8} {:<12} {:<35} {:<12}".format(
            id_supermercado,
            dados["numero"],
            dados["morada"],
            dados["nif"]
        ))
    return 200, ""


# READ (consultar individual)
def consultar_supermercado(id_supermercado):
    if id_supermercado not in supermercados:
        logging.error(f"Supermercado não encontrado: {id_supermercado}.")
        return 404, f"supermercado '{id_supermercado}' não encontrado."

    logging.debug(f"Consulta de supermercado: {id_supermercado}.")
    dados = supermercados[id_supermercado]
    print(f"\n--- Supermercado ---")
    print(f"ID:      {id_supermercado}")
    print(f"Número:  {dados['numero']}")
    print(f"Morada:  {dados['morada']}")
    print(f"NIF:     {dados['nif']}")
    return 200, ""


# UPDATE
def atualizar_supermercado(id_supermercado, numero=None, morada=None, nif=None):
    if id_supermercado not in supermercados:
        logging.error(f"Supermercado não encontrado para atualização: {id_supermercado}.")
        return 404, f"supermercado '{id_supermercado}' não encontrado."

    if numero is not None:
        if not numero.strip():
            logging.error(f"Tentativa de atualizar supermercado {id_supermercado} com número vazio.")
            return 400, "o número não pode estar vazio."
        for sid, dados in supermercados.items():
            if sid != id_supermercado and dados["numero"].lower() == numero.strip().lower():
                logging.warning(f"Conflito de número ao atualizar supermercado {id_supermercado}: '{numero}' já existe.")
                return 409, f"já existe um supermercado com o número '{numero}'."
        supermercados[id_supermercado]["numero"] = numero.strip()

    if morada is not None:
        if not morada.strip():
            logging.error(f"Tentativa de atualizar supermercado {id_supermercado} com morada vazia.")
            return 400, "a morada não pode estar vazia."
        supermercados[id_supermercado]["morada"] = morada.strip()

    if nif is not None:
        if not validar_nif(nif):
            logging.error(f"NIF inválido ao atualizar supermercado {id_supermercado}: '{nif}'.")
            return 400, "NIF inválido. O NIF deve ter exactamente 9 dígitos numéricos."
        for sid, dados in supermercados.items():
            if sid != id_supermercado and dados["nif"] == nif.strip():
                logging.warning(f"Conflito de NIF ao atualizar supermercado {id_supermercado}: '{nif}' já existe.")
                return 409, f"já existe um supermercado com o NIF '{nif}'."
        supermercados[id_supermercado]["nif"] = nif.strip()

    logging.info(f"Supermercado atualizado com sucesso. ID: {id_supermercado}.")
    return 200, "supermercado atualizado com sucesso."


# DELETE
def remover_supermercado(id_supermercado):
    if id_supermercado not in supermercados:
        logging.error(f"Supermercado não encontrado para remoção: {id_supermercado}.")
        return 404, f"supermercado '{id_supermercado}' não encontrado."

    from compra import compras
    for dados_compra in compras.values():
        if dados_compra["id_supermercado"] == id_supermercado:
            logging.warning(f"Tentativa de remover supermercado {id_supermercado} com compras associadas.")
            return 409, f"não é possível remover o supermercado '{id_supermercado}' porque tem compras associadas."

    del supermercados[id_supermercado]
    logging.info(f"Supermercado removido com sucesso. ID: {id_supermercado}.")
    return 200, "supermercado removido com sucesso."


def supermercado_existe(id_supermercado):
    """Verifica se um supermercado existe. Usada por compra.py."""
    existe = id_supermercado in supermercados
    logging.debug(f"Verificação de existência de supermercado {id_supermercado}: {'encontrado' if existe else 'não encontrado'}.")
    return existe
