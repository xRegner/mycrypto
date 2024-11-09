import mysql.connector
from statistics import mode, StatisticsError
from collections import Counter
from mysql.connector import Error

def obtener_datos():
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
            cursor.execute("SELECT * FROM db.`daily-operation_solana`")  # Cambia "valor" y "tu_tabla" según tu esquema
            resultados = cursor.fetchall()
            
            return [resultado[1] for resultado in resultados]  # Devuelve solo los valores

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

# Obtener datos de MySQL
data = obtener_datos()

# Calcular la moda
if data:
    try:
        moda = mode(data)
    except StatisticsError:
        count_data = Counter(data)
        moda = count_data.most_common(1)[0][0]  # Primer elemento más común
           #calculamos la probabilidad que los siguientes numeros sean mayores a la moda
    probabilidad = 0
    for i in range(0,len(data)):
        if data[i] > moda:
            probabilidad += 1
    probabilidad = probabilidad/len(data)

    print(f'La moda es: {moda} y la probabilidad de que los siguientes numeros sean mayores a la moda es: {probabilidad}')

else:
    print("No se obtuvieron datos.")