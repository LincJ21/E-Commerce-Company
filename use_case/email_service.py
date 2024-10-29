import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def send_email(name: str, email: str, message: str):
    try:
        sender_email = os.getenv("EMAIL_SENDER")
        receiver_email = os.getenv("EMAIL_RECEIVER")
        password = os.getenv("EMAIL_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT"))

        # Configurar el contenido del correo
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"Mensaje de {name}"
        msg.attach(MIMEText(message, "plain"))

        # Enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Activar la conexión TLS
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        return {"message": "Correo enviado exitosamente"}

    except Exception as e:
        return {"message": f"Error al enviar el correo: {str(e)}"}


#print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))  # Verifica que se esté cargando la contraseña