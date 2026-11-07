import xlrd

libro_eess = xlrd.open_workbook("data/preciosEESS_es.xls")
libro_maritimo = xlrd.open_workbook("data/embarcacionesPrecios_es.xls")

hoja_eess = libro_eess.sheet_by_index(0)
hoja_maritimo = libro_maritimo.sheet_by_index(0)

def buscar_cabecera(hoja, columna_clave="Provincia"):
    for i in range(hoja.nrows):
        if columna_clave in hoja.row_values(i):
            return i
    return None

def limpiar_textos(textos):
    lista_limpia = []
    for n in textos:
        limpio = " ".join(n.split())
        lista_limpia.append(limpio)
    return lista_limpia

def crear_estaciones(hoja):
    estaciones = []
    fila_cabecera = buscar_cabecera(hoja)
    cabecera_limpia = limpiar_textos(hoja.row_values(fila_cabecera))
    for i in range(fila_cabecera + 1, hoja.nrows):
        fila = limpiar_textos(hoja.row_values(i))
        estacion = dict(zip(cabecera_limpia, fila))
        estaciones.append(estacion)
    return estaciones

estaciones_eess = crear_estaciones(hoja_eess)
estaciones_maritimo = crear_estaciones(hoja_maritimo)
