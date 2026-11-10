"""Punto de entrada del proceso de ingesta.

Orquesta las tres fases del ETL: extrae las estaciones de los dos ficheros
del Ministerio, las transforma y las carga en MySQL.

Se ejecuta desde la raíz del proyecto con: python -m etl.ingesta
"""

from pathlib import Path
from etl.extraccion import crear_estaciones, leer_fecha_fichero, abrir_hoja
from etl.transformacion import transformar_estaciones, a_fecha
from etl.carga import cargar

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"
RUTA_EESS = DATOS / "preciosEESS_es.xls"
RUTA_MARITIMO = DATOS / "embarcacionesPrecios_es.xls"


def main():
    """Ejecuta el ETL completo: extracción, transformación y carga.

    Lee los dos ficheros (estaciones terrestres y marítimas), transforma
    sus filas marcando cada estación con su tipo ("T" o "M") y las carga
    en la base de datos. Al terminar muestra la fecha en que el Ministerio
    generó los datos, que es la misma en los dos ficheros.
    """
    hoja_eess = abrir_hoja(RUTA_EESS)
    hoja_maritimo = abrir_hoja(RUTA_MARITIMO)

    estaciones_eess = crear_estaciones(hoja_eess)
    estaciones_maritimo = crear_estaciones(hoja_maritimo)

    estaciones_eess = transformar_estaciones(estaciones_eess, "T")
    estaciones_maritimo = transformar_estaciones(estaciones_maritimo, "M")

    fecha_extraccion = a_fecha(leer_fecha_fichero(hoja_eess))

    cargar(estaciones_eess, estaciones_maritimo)

    print(
        "Fecha de extracción de los datos del Geoportal:",
        fecha_extraccion.strftime("%d/%m/%Y %H:%M"),
    )


if __name__ == "__main__":
    main()
