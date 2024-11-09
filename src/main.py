from analisis import analisis
from get_api_price import get_api_price, insert_record
import json
from datetime import datetime


data_from_json = None 
with open('/app/data_cripto.json') as f:
    data_from_json = json.load(f) 

cripto_string = ""
cripto_monedas = "" 
for cripto in data_from_json:
    cripto_string += f"""{cripto["nombre"]},"""
    cripto_monedas += f"""{cripto["moneda"]},""" # no repetir la moneda

data_from_api = get_api_price(cripto_string, cripto_monedas)
print(data_from_api)
for cripto in data_from_json:
    #obtener del api el precio de la cripto y el currency
    cripto_price = data_from_api[cripto["nombre"]][ cripto["moneda"]]

    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    datos_guardados = insert_record(fecha, cripto_price, cripto['nombre']) 

    if(cripto["activo"]):
        analisis(cripto, cripto_price)
