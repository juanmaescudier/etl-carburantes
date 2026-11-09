import os
import pymysql
from dotenv import load_dotenv


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

        Los carburantes salen de la cabecera de Precios. El diccionario se usa
        después para obtener el carburante_id de cada gasolinera.
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


def cargar(estaciones_eess, estaciones_maritimo):
    """Carga todas las estaciones en MySQL en una única transacción."""
    estaciones = estaciones_eess + estaciones_maritimo
    conexion = conectar_mysql()
    try:
        ids_empresas = cargar_empresas(conexion, estaciones)
        ids_carburantes = cargar_carburantes(conexion, estaciones)
        print(f"Empresas: {len(ids_empresas)} | Carburantes: {len(ids_carburantes)}")
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
