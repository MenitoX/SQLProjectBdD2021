import cx_Oracle, os
from dotenv import load_dotenv

load_dotenv()

# Realiza la conexión a oracle, retorna la conexión
def connect():
    USER = os.getenv('USER')
    PASS = os.getenv('PASS')
    URL  = os.getenv('URL')
    try:
        connection = cx_Oracle.connect(USER,PASS,URL)
    except Exception as error:
        print("Error en la conexion a la base de datos :", error)
        exit()
    else:
        print("Database version:", connection.version)
        print("Conectado con exito a la base de datos")
    finally:
        return connection

# Recibe y desconecta la conexión.
def disconnect(connection):
    try:
        connection.close()
    except Exception as error:
        print("Error al cerrar la base de datos", error)
    else:
        print("Conexión cerrada")
    finally:
        return 1