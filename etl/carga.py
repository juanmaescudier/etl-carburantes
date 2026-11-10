"""Carga de las estaciones transformadas en MySQL.

Todas las inserciones van en una única conexión y una única transacción:
si algo falla, se deshace la carga entera.
"""

import os
import pymysql
from dotenv import load_dotenv


SQL_GASOLINERA = """
    INSERT INTO gasolinera (
        empresa_id, tipo, provincia, municipio, localidad, codigo_postal,
        direccion, margen, latitud, longitud, fecha_toma_datos, horario,
        tipo_venta, rem, tipo_servicio, pct_bioalcohol, pct_ester_metilico
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def conectar_mysql():
    """Carga el .env y devuelve una conexión a MySQL con el usuario de la aplicación."""
    load_dotenv()

    conexion = pymysql.connect(
        host="localhost",
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
    )
    return conexion


def cargar_empresas(conexion, estaciones):
    """Inserta las empresas sin repetir y devuelve un diccionario {nombre: id}.

    Los nombres salen del Rótulo de cada estación. El diccionario se usa
    después para obtener el empresa_id de cada gasolinera.
    """
    nombres = set()
    for estacion in estaciones:
        nombres.add(estacion["Rótulo"])

    with conexion.cursor() as cursor:
        for nombre in nombres:
            cursor.execute("INSERT INTO empresa (nombre) VALUES (%s)", (nombre,))

        cursor.execute("SELECT id, nombre FROM empresa")
        ids = {}
        for id_, nombre in cursor.fetchall():
            ids[nombre] = id_

    return ids


def cargar_carburantes(conexion, estaciones):
    """Inserta los carburantes sin repetir y devuelve un diccionario {carburante: id}.

    Los nombres salen de las columnas "Precio ..." de las estaciones, sin el
    prefijo. Incluye también los carburantes que ninguna gasolinera vende.
    El diccionario se usa después para obtener el carburante_id de cada precio.
    """
    nombres = set()
    for estacion in estaciones:
        for clave in estacion:
            if clave.startswith("Precio"):
                nombres.add(clave.removeprefix("Precio "))

    with conexion.cursor() as cursor:
        for nombre in nombres:
            cursor.execute("INSERT INTO carburante (nombre) VALUES (%s)", (nombre,))

        cursor.execute("SELECT id, nombre FROM carburante")
        ids = {}
        for id_, carburante in cursor.fetchall():
            ids[carburante] = id_

    return ids


def cargar_gasolineras(conexion, estaciones, ids_empresas):
    """Inserta las gasolineras y devuelve la lista de sus id.

    La lista va en el mismo orden que estaciones: ids[i] es el id que MySQL
    ha asignado a estaciones[i]. Se obtiene con cursor.lastrowid justo
    después de cada INSERT, porque ningún campo de la gasolinera es único.
    Las columnas que las marítimas no traen se leen con .get() y quedan a NULL.
    """
    with conexion.cursor() as cursor:
        ids = []
        for estacion in estaciones:
            valores = (
                ids_empresas[estacion["Rótulo"]],
                estacion["tipo"],
                estacion["Provincia"],
                estacion["Municipio"],
                estacion["Localidad"],
                estacion["Código postal"],
                estacion["Dirección"],
                estacion.get("Margen"),
                estacion["Latitud"],
                estacion["Longitud"],
                estacion.get("Toma de datos"),
                estacion["Horario"],
                estacion["Tipo venta"],
                estacion["Rem."],
                estacion.get("Tipo servicio"),
                estacion.get("% bioalcohol"),
                estacion.get("% éster metílico"),
            )
            cursor.execute(SQL_GASOLINERA, valores)
            ids.append(cursor.lastrowid)
        return ids


def cargar(estaciones_eess, estaciones_maritimo):
    """Carga todas las estaciones en MySQL en una única transacción."""
    estaciones = estaciones_eess + estaciones_maritimo
    conexion = conectar_mysql()
    try:
        ids_empresas = cargar_empresas(conexion, estaciones)
        ids_carburantes = cargar_carburantes(conexion, estaciones)
        ids_gasolineras = cargar_gasolineras(conexion, estaciones, ids_empresas)
        print(f"Empresas: {len(ids_empresas)} | Carburantes: {len(ids_carburantes)} "
              f"| Gasolineras: {len(ids_gasolineras)}")
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
