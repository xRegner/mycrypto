from mysql.connector import Error
from datetime import datetime
from messages import manda_mail
from get_api_price import get_api_price, insert_record
from absdb import calcula_tendenciaV1 as calcula_tendencia


cripto = {
    "nombre": "dogecoin",
    "moneda": "mxn",
    "invertido": 290.69362363, #inversion en cripto
    "camper_mode": {
        "activo": False, #este modo es para cuando se esta vigiliando la cripto en operaciones de 1 o 2 dias
        "maximo": 55000, #umbral de ganacia
        "minimo": 53000, #umbral de perdida
    },
    "inversion_referencia": 804, #lo que pagaste por la cripto en tu moneda
    "porcentaje_ganancia": 3.2,
    "porcentaje_perdida": 0.5, #toleancia de perdida
    "notifica_perdidas": True,
    "oportunidad": 2.9 #definido por el usuario cuando se quiere comprar
}
#obtner el precio de la cripto desde la api
data = get_api_price(cripto["nombre"], cripto["moneda"])
cripto_price = data[cripto["nombre"]][ cripto["moneda"]]
fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
#Guardamos la info en la base de datos
datos_guardados = insert_record(fecha, cripto_price, cripto['nombre']) # todo mandar la moneda

#Lo que vale mi inversion en dinero
valor_actual_inversion = cripto["invertido"] * cripto_price
#print(f"El valor actual de la inversion en {cripto["nombre"]} : {valor_actual_inversion:.3f} en {cripto['moneda']}, el valor de la cripto: {cripto_price:.3f} { cripto['moneda']}")
# valor_para_comprar menos el porcentaje de tolerancia
#valor_para_comprar_menos_porcentaje = valor_para_comprar - (valor_para_comprar * (porcentaje_min_compra/100))

# calcular el porcentaje de ganancia o perdida  
porcentaje_ganacia_perdida = ((valor_actual_inversion*100) / cripto["inversion_referencia"]) - 100

arriba_del_promedio = 0
abajo_del_promedio = 0
try:
    arriba_del_promedio, abajo_del_promedio = calcula_tendencia(300, cripto["nombre"] ) #se puede parametrizar
except Error as e:
    print(f"Error al obtener los datos de la base de datos: {e}")
    arriba_del_promedio = 0
    abajo_del_promedio = 0

tendencia = ""
if arriba_del_promedio > abajo_del_promedio:
    tendencia = "al alza"
else:
    tendencia = "a la baja"
    

print(f"""El valor actual de la inversion en {cripto['nombre']} : {valor_actual_inversion:.3f} en {cripto['moneda']}, el valor de la cripto: {cripto_price:.3f} {cripto['moneda']}
          y el porcentaje con respecto a la compra base es: {porcentaje_ganacia_perdida:.3f}% 
          el porcentaje de registros arriba del promedio {arriba_del_promedio:.3f}% y porcentaje de registros 
          abajo del promedio {abajo_del_promedio:.3f}%, la tendencia es {tendencia}""")

if cripto["invertido"] != 0:
    # Si el porcentaje porcentaje_ganacia_perdida es menor a 0, y la tendencia es a la baja, enviar correo
    if porcentaje_ganacia_perdida < 0 and abajo_del_promedio > arriba_del_promedio and cripto["notifica_perdidas"]:
        manda_mail(f"Alerta-{cripto['nombre']}: Perdida de dinero", f"porcentaje hoy: {porcentaje_ganacia_perdida}, monto base invertido {cripto['inversion_referencia']} y monto actual {valor_actual_inversion}, porcentaje de registros arriba del promedio {arriba_del_promedio:.3f}% y porcentaje de registros abajo del promedio {abajo_del_promedio:.3f}%, la tendencia es {tendencia}")
        print("Alerta: Perdida de dinero")
    # si el porcentaje_ganacia_perdida es mayor al porcentaje de margen de ganancia, enviar correo
    if porcentaje_ganacia_perdida >= cripto["porcentaje_ganancia"]:
        manda_mail(f"Atención-{cripto['nombre']}: puede haber ganancias.", f"porcentaje hoy: {porcentaje_ganacia_perdida}, monto invertido  {cripto['inversion_referencia']} y monto actual {valor_actual_inversion}, la tendencia es {tendencia}")
        print(f"Atención-{cripto['nombre']}: puede haber ganancias.")
    #cuando el modo camper esta activo
    if cripto["camper_mode"]["activo"]:
        if valor_actual_inversion >= cripto["camper_mode"]["maximo"]:
            manda_mail(f"Alerta-{cripto['nombre']}: Ganancia", f"porcentaje hoy: {porcentaje_ganacia_perdida}, monto invertido  {cripto['inversion_referencia']} y monto actual {valor_actual_inversion}, la tendencia es {tendencia}")
            print(f"Alerta-{cripto['nombre']}: Ganancia")
        if valor_actual_inversion <= cripto["camper_mode"]["minimo"]:
            manda_mail(f"Alerta-{cripto['nombre']}: Perdida", f"porcentaje hoy: {porcentaje_ganacia_perdida}, monto invertido  {cripto['inversion_referencia']} y monto actual {valor_actual_inversion}, la tendencia es {tendencia}")
            print(f"Alerta-{cripto['nombre']}: Perdida")

# esta notificacion es para cuando se quiere comprar y puede no tenerse una inversion en la cripto
if cripto_price < cripto["oportunidad"]:
   manda_mail(f" Oportunidad de Compra-{cripto['nombre']}", f" El precio está por debajo del límite establecido. Considera Comprar. el Precio actual de {cripto['nombre']}: {cripto_price} y la tendecia de los ultimos registros es {tendencia}%")







