import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from messages import manda_mail
from absdb import calcula_tendencia

currency = 'mxn' #sacar de las variables de env  
crypto = 'bitcoin,Ripple,ethereum,dogecoin'
valor_compra = 1425000 # valor de tolerencia antes de vender - oportunidad de compra    
valor_inicial_compra = 1407508
valor_inversion_inicial = 1181.36
porcentaje_tolerancia_min = 4 # sirve pasa saber cuando comprar 1328000 y 4.5 = 1268240.0
porcentaje_ganacia_ideal = 5

def insert_record(fecha, valor): 
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
                sql_insert_query = """INSERT INTO db.`daily-operation` (`daily-operation-date`, `daily-operation-price`) VALUES (%s, %s)"""

                # Datos a insertar
                record_to_insert = (fecha, valor)

                # Ejecutar la sentencia SQL
                cursor.execute(sql_insert_query, record_to_insert)

                # Confirmar los cambios en la base de datos
                connection.commit()
                print("Record inserted successfully into current table")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# URL de la API de CoinGecko para obtener info
url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"
# Hacer la solicitud GET a la API
response = requests.get(url)




# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Convertir la respuesta JSON a un diccionario de Python
    data = response.json()
    # Obtener el precio del Bitcoin en USD
    bitcoin_price = data['bitcoin'][currency]
    print(f"El precio actual del Bitcoin es: ${bitcoin_price}")
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Usa la fecha actual, puedes cambiar esto según tus necesidades

    insert_record(fecha, bitcoin_price)
    limite_inferior = valor_compra * (1 - (porcentaje_tolerancia_min / 100))

    porcentaje_ganacia_perdida = 100 - ((valor_inicial_compra*100) / bitcoin_price)
    monto_actual = valor_inversion_inicial * (1 + (porcentaje_ganacia_perdida/100) )

    print(f"porcentaje hoy: {porcentaje_ganacia_perdida} y monto actual {monto_actual}")

    #obtener los valores de la tendencia
    arriba_del_promedio, abajo_del_promedio = calcula_tendencia(500)
    tendencia = ""
    if arriba_del_promedio > abajo_del_promedio:
        tendencia = "al alza"
    else:
        tendencia = "a la baja"
    
    #si el valor_inversion_inicial es cero no evaluar 
    if(valor_inversion_inicial != 0) :
        if(monto_actual < valor_inversion_inicial) :
            #mandar correo
            manda_mail("Bitcoin-Alerta: Perdida de dinero", f"porcentaje hoy: {porcentaje_ganacia_perdida}, monto invertido {valor_inversion_inicial} y monto actual {monto_actual}, porcentaje de registros arriba del promedio {arriba_del_promedio:.3f}% y porcentaje de registros abajo del promedio {abajo_del_promedio:.3f}%, la tendencia es {tendencia}")
        
    if(porcentaje_ganacia_perdida > porcentaje_ganacia_ideal and valor_inversion_inicial != 0) :
      manda_mail("Bitcoin Atención: puede haber ganancias.", f"porcentaje hoy: {porcentaje_ganacia_perdida}, monto invertido {valor_inversion_inicial} y monto actual {monto_actual}")
    # Obtener el precio actual
    precio_actual = bitcoin_price 
    print(f"Precio actual de Bitcoin: {precio_actual}")

    # Verificar si debes comprar

    if precio_actual < limite_inferior:

        print("Alerta-Bitcoin: El precio está por debajo del límite de tolerancia. Considera vender.")
        manda_mail("COMPRA: El precio está por debajo del margen", f"Precio actual de Bitcoin: {precio_actual} y la tendecia de los ultimos 450 registros es {tendencia}%")
    else:
          print(f"El precio está dentro del rango de tolerancia. Puedes mantener tu inversión o comprar más.:{limite_inferior}")
    # valor base y porcentaje 
     # obtner la tendencia de los ultimos 1000 registros 
     # logica de compra venta 

else:
    print("Error al hacer la solicitud a la API")
