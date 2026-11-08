"""Extracción de los precios de carburantes del Ministerio para la Transición Ecológica y el Reto Demográfico.

Lee ficheros .xls de estaciones terrestres y marítimas descargados del Geoportal, convierte cada
estación en un diccionario
"""

import xlrd

def abrir_hoja(ruta):
    """Abre el fichero .xls de la ruta indicada y devuelve su primera hoja"""
    libro = xlrd.open_workbook(ruta)
    hoja = libro.sheet_by_index(0)
    return hoja


def buscar_cabecera(hoja, columna_clave="Provincia"):
    """Esta función devuelve el número de la fila que contiene columna_clave.

    Se busca la fila que corresponde a las cabeceras en lugar de fijar una porque
    el Ministerio inserta metadatos encima y en el futuro se podrían modificar.
    Si ninguna fila contiene columna_clave devuelve None
    """
    for i in range(hoja.nrows):
        if columna_clave in hoja.row_values(i):
            return i
    return None


def limpiar_textos(textos):
    """Esta función devuelve los textos limpios en forma de lista.

    Quita espacios y tabuladores, y deja un solo espacio donde había
    varios seguidos. Todos los valores deben de ser texto.
    """
    lista_limpia = []
    for texto in textos:
        limpio = " ".join(texto.split())
        lista_limpia.append(limpio)
    return lista_limpia


def crear_estaciones(hoja):
    """Devuelve una lista con un diccionario por estación.

    Se asignan valores a las cabeceras almacenandolos en un diccionario.
    Lanza ValueError si no encuentra cabecera.
    Las columnas sin nombre se descartan.
    """
    estaciones = []
    fila_cabecera = buscar_cabecera(hoja)

    if fila_cabecera is None:
        raise ValueError("No se encuentra la cabecera: ninguna fila contiene 'Provincia'. ¿Ha cambiado el formato del fichero del Ministerio?")

    cabecera_limpia = limpiar_textos(hoja.row_values(fila_cabecera))
    for i in range(fila_cabecera + 1, hoja.nrows):
        fila = limpiar_textos(hoja.row_values(i))
        estacion = {}
        for nombre, valor in zip(cabecera_limpia, fila):
            if nombre:  # las marítimas traen una columna sin nombre, la descartamos
                estacion[nombre] = valor
        estaciones.append(estacion)
    return estaciones


def leer_fecha_fichero(hoja):
    """Devuelve la fecha y hora en formato texto en que el Ministerio generó el fichero.

    Se busca la fila donde se encuentre la clave 'Fecha:' y una vez en esa fila
    se accede al dato de su derecha
    """
    fila_fecha = buscar_cabecera(hoja, "Fecha:")
    if fila_fecha is None:
        raise ValueError("No se encuentra la fecha del fichero: ninguna fila contiene 'Fecha:'. ¿Ha cambiado el formato del fichero del Ministerio?")
    fila = hoja.row_values(fila_fecha)
    fecha = fila[1]
    return fecha
