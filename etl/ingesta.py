"""Punto de entrada del proceso de ingesta"""

from pathlib import Path
from etl.extraccion import crear_estaciones, leer_fecha_fichero, abrir_hoja

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"
RUTA_EESS = DATOS / "preciosEESS_es.xls"
RUTA_MARITIMO = DATOS / "embarcacionesPrecios_es.xls"

hoja_eess = abrir_hoja(RUTA_EESS)
hoja_maritimo = abrir_hoja(RUTA_MARITIMO)

estaciones_eess = crear_estaciones(hoja_eess)
estaciones_maritimo = crear_estaciones(hoja_maritimo)
fecha_eess = leer_fecha_fichero(hoja_eess)
fecha_maritimo = leer_fecha_fichero(hoja_maritimo)

print(f"Estaciones terrestres: {len(estaciones_eess)}")
print(f"Estaciones marítimas: {len(estaciones_maritimo)}")
print(f"Fecha de generación del documento en GeoPortal de terrestre: {fecha_eess}")
print(f"Fecha de generación del documento en GeoPortal de marítimo: {fecha_maritimo}")
