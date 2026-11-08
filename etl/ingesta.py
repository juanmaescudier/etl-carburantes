"""Punto de entrada del proceso de ingesta"""

from pathlib import Path
from etl.extraccion import crear_estaciones, leer_fecha_fichero, abrir_hoja

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
    fecha_eess = leer_fecha_fichero(hoja_eess)
    fecha_maritimo = leer_fecha_fichero(hoja_maritimo)


if __name__ == "__main__":
    main()
