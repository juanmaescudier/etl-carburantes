"""Punto de entrada del proceso de ingesta"""

from etl.extraccion import crear_estaciones, leer_fecha_fichero, abrir_hoja

hoja_eess = abrir_hoja("../data/preciosEESS_es.xls")
hoja_maritimo = abrir_hoja("../data/embarcacionesPrecios_es.xls")

estaciones_eess = crear_estaciones(hoja_eess)
estaciones_maritimo = crear_estaciones(hoja_maritimo)
fecha_eess = leer_fecha_fichero(hoja_eess)
fecha_maritimo = leer_fecha_fichero(hoja_maritimo)

print(f"Estaciones terrestres: {len(estaciones_eess)}")
print(f"Estaciones marítimas: {len(estaciones_maritimo)}")
print(f"Fecha de generación del documento en GeoPortal de terrestre: {fecha_eess}")
print(f"Fecha de generación del documento en GeoPortal de marítimo: {fecha_maritimo}")
