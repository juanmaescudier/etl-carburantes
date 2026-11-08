"""Transformación de cada dato (actualmente es texto)
a su tipo correspondiente (str, Decimal, datetime y None)"""

from decimal import Decimal
from datetime import datetime

COLUMNAS_DECIMALES = ("Longitud", "Latitud", "% bioalcohol", "% éster metílico")


def vacio_a_none(texto):
    """Devuelve None en el caso de que un dato no exista"""
    if not texto:
        return None
    return texto


def a_decimal(texto):
    """Devuelve None si algun dato falta
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


def transformar_estacion(estacion):
    """Devuelve un diccionario nuevo con cada valor convertido a su tipo"""
    resultado = {}
    for clave, valor in estacion.items():
        if clave.startswith("Precio") or clave in COLUMNAS_DECIMALES:
            resultado[clave] = a_decimal(valor)
        elif clave == "Toma de datos":
            resultado[clave] = a_fecha(valor)
        else:
            resultado[clave] = vacio_a_none(valor)
    return resultado


def transformar_estaciones(estaciones):
    """Devuelve la lista de las estaciones ya transformadas"""
    transformadas = []
    for estacion in estaciones:
        transformadas.append(transformar_estacion(estacion))
    return transformadas
