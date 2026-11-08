"""Transformación de cada dato (actualmente es texto)
a su tipo correspondiente (str, Decimal, datetime y None)"""

from decimal import Decimal
from datetime import datetime


def vacio_a_none(texto):
    """Devuelve None en el caso de que un dato no exista"""
    if not texto:
        return None
    return texto


def a_decimal(texto):
    """Devuelce None si algun dato falta
    y si no devuelve el numero en decimal
    """
    if not texto:
        return None
    return Decimal(texto.replace(",", "."))


def a_fecha(texto):
    """Devuelve None si algun dato falta
    y si no devuelve el dato en formato datetime
    """
    if not texto:
        return None
    return datetime.strptime(texto, "%d/%m/%Y %H:%M")
