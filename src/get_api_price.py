import requests
from datetime import datetime
import mysql.connector
from mysql.connector import Error

def get_api_price(cripto, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies={currency}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def insert_record(fecha, valor, cripto): 
    try:
            # Conectar a la base de datos MySQL
            connection = mysql.connector.connect(
                host='db',  # Cambia esto si tu contenedor está en otra dirección
                database='db',
                user='user',
                password='password'
            )

            if connection.is_connected():
                cursor = connection.cursor()

                # Crear la sentencia SQL
                sql_insert_query = f"""INSERT INTO db.`daily-operation_{cripto}` (`daily-operation-date`, `daily-operation-price`) VALUES (%s, %s)"""

                # Datos a insertar
                record_to_insert = (fecha, valor)

                # Ejecutar la sentencia SQL
                cursor.execute(sql_insert_query, record_to_insert)

                # Confirmar los cambios en la base de datos
                connection.commit()
                return True

    except Error as e:
        return False
    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            cursor.close()
            connection.close()

