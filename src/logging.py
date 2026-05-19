# ==============================
# logging_config.py
# Configuração central do logging
# Importar no main.py antes de qualquer outro módulo
# ==============================

import logging


def configurar_logging(nivel=logging.DEBUG, ficheiro="app.log"):
    """
    Configura o logging global da aplicação.

    Formato de saída:
        2026-05-19 14:32:01 - ERROR - Supermercado não encontrado: S015

    Parâmetros:
        nivel    - Nível mínimo de log (default: DEBUG; em produção usar INFO ou WARNING)
        ficheiro - Nome do ficheiro onde os logs são gravados (default: app.log)
    """
    formato = "%(asctime)s - %(levelname)s - %(message)s"
    data_formato = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=nivel,
        format=formato,
        datefmt=data_formato,
        handlers=[
            logging.FileHandler(ficheiro, encoding="utf-8"),
            logging.StreamHandler()          # também imprime na consola
        ]
    )
