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


def comprobar_conexion(conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM empresa")
            print(f"Empresas en la base de datos: {cursor.fetchone()[0]}")
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()