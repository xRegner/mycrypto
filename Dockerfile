FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos locales al contenedor
COPY src/ .

# Instalar la librería MySQL para Python
RUN pip install mysql-connector-python && pip install requests

# Comando para ejecutar el script Python
CMD [ "python main.py" ]