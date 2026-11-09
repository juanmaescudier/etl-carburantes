"""Punto de entrada del proceso de ingesta"""

from pathlib import Path
from etl.extraccion import crear_estaciones, leer_fecha_fichero, abrir_hoja
from etl.transformacion import transformar_estaciones, a_fecha, extraer_precios

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"
RUTA_EESS = DATOS / "preciosEESS_es.xls"
RUTA_MARITIMO = DATOS / "embarcacionesPrecios_es.xls"


def main():
    """Ejecuta la creación de las estaciones y las fechas"""
    hoja_eess = abrir_hoja(RUTA_EESS)
    hoja_maritimo = abrir_hoja(RUTA_MARITIMO)

    estaciones_eess = crear_estaciones(hoja_eess)
    estaciones_maritimo = crear_estaciones(hoja_maritimo)

    estaciones_eess = transformar_estaciones(estaciones_eess, "T")
    estaciones_maritimo = transformar_estaciones(estaciones_maritimo, "M")

    fecha_eess = a_fecha(leer_fecha_fichero(hoja_eess))
    fecha_maritimo = a_fecha(leer_fecha_fichero(hoja_maritimo))

    total_precios = 0
    for estacion in estaciones_eess:
        total_precios += len(extraer_precios(estacion))
    for estacion in estaciones_maritimo:
        total_precios += len(extraer_precios(estacion))

    print(total_precios)

if __name__ == "__main__":
    main()
