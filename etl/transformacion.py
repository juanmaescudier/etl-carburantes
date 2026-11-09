"""Transformación de cada dato (actualmente es texto)
a su tipo correspondiente (str, Decimal, datetime y None)"""

from decimal import Decimal
from datetime import datetime

COLUMNAS_DECIMALES = ("Longitud", "Latitud", "% bioalcohol", "% éster metílico")
EMPRESA_DESCONOCIDA = "DESCONOCIDA"
TIPOS_VENTA = {"P": "Venta al público en general"}


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


def transformar_estacion(estacion, tipo):
    """Devuelve un diccionario nuevo con cada valor convertido a su tipo.

    Añade la clave "tipo" con el valor recibido ("T" terrestre, "M" marítima).
    Los rótulos vacíos pasan a EMPRESA_DESCONOCIDA y las siglas de
    tipo de venta se traducen con TIPOS_VENTA."""
    resultado = {"tipo": tipo}
    for clave, valor in estacion.items():
        if clave.startswith("Precio") or clave in COLUMNAS_DECIMALES:
            resultado[clave] = a_decimal(valor)
        elif clave == "Toma de datos":
            resultado[clave] = a_fecha(valor)
        elif clave == "Rótulo":
            if valor:
                resultado[clave] = valor
            else:
                resultado[clave] = EMPRESA_DESCONOCIDA
        elif clave == "Tipo venta":
            resultado[clave] = TIPOS_VENTA.get(valor, valor)
        else:
            resultado[clave] = vacio_a_none(valor)
    return resultado


def transformar_estaciones(estaciones, tipo):
    """Devuelve la lista de estaciones transformadas, todas con el tipo indicado ("T" o "M")."""
    transformadas = []
    for estacion in estaciones:
        transformadas.append(transformar_estacion(estacion, tipo))
    return transformadas


def extraer_precios(estacion):
    """Devuelve una lista de tuplas (carburante, precio) de una estación.

        Solo incluye los carburantes con precio. El nombre del carburante es
        el de la columna sin el prefijo "Precio ".
        """
    precios = []
    for clave, valor in estacion.items():
        if clave.startswith("Precio") and valor is not None:
            nombre = clave.removeprefix("Precio ")
            precios.append((nombre, valor))
    return precios
