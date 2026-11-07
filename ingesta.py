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

fila_cabecera_eess = buscar_cabecera(hoja_eess)
fila_cabecera_maritimo = buscar_cabecera(hoja_maritimo)

def limpiar_textos(textos):
    lista_limpia = []
    for n in textos:
        limpio = " ".join(n.split())
        lista_limpia.append(limpio)
    return lista_limpia

cabeceras_limpias_eess = limpiar_textos(hoja_eess.row_values(fila_cabecera_eess))
print(repr(cabeceras_limpias_eess))
cabeceras_limpias_maritimo = limpiar_textos(hoja_maritimo.row_values(fila_cabecera_maritimo))
print(repr(cabeceras_limpias_maritimo))

primera_fila = limpiar_textos(hoja_eess.row_values(fila_cabecera_eess + 1))

primera_estacion = dict(zip(cabeceras_limpias_eess, primera_fila))
print(primera_estacion)

estaciones_eess = []

for i in range(fila_cabecera_eess + 1, hoja_eess.nrows):
    fila = limpiar_textos(hoja_eess.row_values(i))
    estacion = dict(zip(cabeceras_limpias_eess, fila))
    estaciones_eess.append(estacion)

print(len(estaciones_eess))
print(estaciones_eess[0])
print(estaciones_eess[-1])