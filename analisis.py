import re


def menciona(descripcion, palabra):
    """
    ¿Esta descripción menciona esa habilidad?

    Busca la palabra entera, no un pedazo adentro de otra. Es lo que evita
    contar "maintain" como si dijera "AI", o "excellent" como si dijera
    "Excel".
    """
    if not descripcion:
        return False
    patron = r"\b" + re.escape(palabra) + r"\b"
    return re.search(patron, descripcion, re.IGNORECASE) is not None
