import mysql.connector
from mysql.connector import Error


def calcula_tendencia(_limit) :
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu contenedor está en otra dirección
            database='db',
            user='user',
            password='password'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Crear la sentencia SQL
            sql_insert_query = f"""
                                        WITH ultimos_registros AS (
                                        SELECT `daily-operation-price`
                                            FROM db.`daily-operation`
                                            ORDER BY `daily-operation-date` DESC
                                            LIMIT {_limit}
                                        ),
                                        promedio AS (
                                            SELECT AVG(`daily-operation-price`) AS promedio_venta
                                            FROM ultimos_registros
                                        )
                                        SELECT 
                                            SUM(CASE WHEN ur.`daily-operation-price` > p.promedio_venta THEN 1 ELSE 0 END) AS arriba_del_promedio,
                                            SUM(CASE WHEN ur.`daily-operation-price` < p.promedio_venta THEN 1 ELSE 0 END) AS abajo_del_promedio
                                        FROM ultimos_registros ur, promedio p;
                                    """



            # Ejecutar la sentencia SQL
            cursor.execute(sql_insert_query)

            resultados = cursor.fetchone()
            arriba_del_promedio, abajo_del_promedio = resultados

            #sacamos el promedio de los valores cuando _limit = 100%

            total = arriba_del_promedio + abajo_del_promedio
            arriba_del_promedio = (arriba_del_promedio/total)*100
            abajo_del_promedio = (abajo_del_promedio/total)*100

            #arriba_del_promedio = (arriba_del_promedio/_limit)*100
            #abajo_del_promedio = (abajo_del_promedio/_limit)*100


            return arriba_del_promedio, abajo_del_promedio

            # Muestra los resultados con solo tres decimales
            print(f"El {arriba_del_promedio:.3f}% de los últimos {_limit} registros están arriba del promedio")
            print(f"El {abajo_del_promedio:.3f}% de los últimos {_limit} registros están abajo del promedio")
    
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def calcula_tendencia_ethereum(_limit) :
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu contenedor está en otra dirección
            database='db',
            user='user',
            password='password'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Crear la sentencia SQL
            sql_insert_query = f"""
                                        WITH ultimos_registros AS (
                                        SELECT `daily-operation-price`
                                            FROM db.`daily-operation_ethereum`
                                            ORDER BY `daily-operation-date` DESC
                                            LIMIT {_limit}
                                        ),
                                        promedio AS (
                                            SELECT AVG(`daily-operation-price`) AS promedio_venta
                                            FROM ultimos_registros
                                        )
                                        SELECT 
                                            SUM(CASE WHEN ur.`daily-operation-price` > p.promedio_venta THEN 1 ELSE 0 END) AS arriba_del_promedio,
                                            SUM(CASE WHEN ur.`daily-operation-price` < p.promedio_venta THEN 1 ELSE 0 END) AS abajo_del_promedio
                                        FROM ultimos_registros ur, promedio p;
                                    """



            # Ejecutar la sentencia SQL
            cursor.execute(sql_insert_query)

            resultados = cursor.fetchone()
            arriba_del_promedio, abajo_del_promedio = resultados

            #sacamos el promedio de los valores cuando _limit = 100%

            total = arriba_del_promedio + abajo_del_promedio
            arriba_del_promedio = (arriba_del_promedio/total)*100
            abajo_del_promedio = (abajo_del_promedio/total)*100

            return arriba_del_promedio, abajo_del_promedio

    
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def calcula_tendencia_solana(_limit) :
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu contenedor está en otra dirección
            database='db',
            user='user',
            password='password'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Crear la sentencia SQL
            sql_insert_query = f"""
                                        WITH ultimos_registros AS (
                                        SELECT `daily-operation-price`
                                            FROM db.`daily-operation_solana`
                                            ORDER BY `daily-operation-date` DESC
                                            LIMIT {_limit}
                                        ),
                                        promedio AS (
                                            SELECT AVG(`daily-operation-price`) AS promedio_venta
                                            FROM ultimos_registros
                                        )
                                        SELECT 
                                            SUM(CASE WHEN ur.`daily-operation-price` > p.promedio_venta THEN 1 ELSE 0 END) AS arriba_del_promedio,
                                            SUM(CASE WHEN ur.`daily-operation-price` < p.promedio_venta THEN 1 ELSE 0 END) AS abajo_del_promedio
                                        FROM ultimos_registros ur, promedio p;
                                    """



            # Ejecutar la sentencia SQL
            cursor.execute(sql_insert_query)

            resultados = cursor.fetchone()
            arriba_del_promedio, abajo_del_promedio = resultados

            #sacamos el promedio de los valores cuando _limit = 100%

            arriba_del_promedio = (arriba_del_promedio/_limit)*100
            abajo_del_promedio = (abajo_del_promedio/_limit)*100


            return arriba_del_promedio, abajo_del_promedio

    
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

