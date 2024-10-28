# use_case/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def send_email(name: str, email: str, message: str):
    try:
        sender_email = os.getenv("EMAIL_SENDER")  # Correo del remitente
        receiver_email = os.getenv("EMAIL_RECEIVER")  # Correo del destinatario
        password = os.getenv("EMAIL_PASSWORD")  # Contraseña obtenida de la variable de entorno

        # Configurar el contenido del correo
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"Mensaje de {name}"

        msg.attach(MIMEText(message, "plain"))

        # Enviar el correo
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        return {"message": "Correo enviado exitosamente"}

    except Exception as e:
        return {"message": f"Error al enviar el correo: {str(e)}"}
#print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))  # Verifica que se esté cargando la contraseña