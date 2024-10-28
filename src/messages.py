#manda email en la compra y venta

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuraciones
smtp_server = 'smtp.gmail.com'  # Cambia esto según tu proveedor de correo
port = 587  # Para TLS
sender_email = 'killabout69@gmail.com'
password = 'wapj sten fusy fvhv'  # Considera usar un método más seguro para almacenar contraseñas
receiver_email = 'familiabntznun@gmail.com'

# Crear el mensaje

# Cuerpo del correo


def manda_mail(mensaje, _body): 
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email

    body = _body
    message.attach(MIMEText(body, 'plain'))
    try:
        # agrega la fecha en el asunto del correo
        message['Subject'] = mensaje + " " + datetime.now().strftime('%Y-%m-%d')
        #message['Subject'] = mensaje
        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Usar TLS
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print('Correo enviado con éxito')
    except Exception as e:
        print(f'Error al enviar el correo: {e}')
