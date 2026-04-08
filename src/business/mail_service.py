# src/business/mail_service.py
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


class MailService:
    def __init__(self):
        # Rutas a tus archivos de datos en la carpeta /data
        self.root_path = Path(__file__).resolve().parent.parent.parent
        self.user_data_path = self.root_path / "data" / "user_data.json"
        self.mail_list_path = self.root_path / "data" / "mail_list_data.json"

        # Configuración fija para Gmail
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def enviar_reporte(self, cuerpo_mensaje, adjuntos=None):
        """
        Lee credenciales y destinatarios de los JSON y envía el correo.
        """
        try:
            # 1. Leer credenciales (tu Gmail y el Token de 16 dígitos)
            with open(self.user_data_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                sender_email = user_data.get("email")
                sender_token = user_data.get("token")

            # 2. Leer destinatarios
            with open(self.mail_list_path, "r", encoding="utf-8") as f:
                destinatarios = json.load(f)

            if not all([sender_email, sender_token, destinatarios]):
                return "⚠️ Error: Revisa que el email, token y destinatarios estén guardados."

            # 3. Construir el mensaje
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ", ".join(destinatarios)
            msg['Subject'] = "📊 Reporte de Casos On Net Fibra"
            msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

            # 4. Adjuntar archivos (Excel/Imagen)
            if adjuntos:
                for ruta in adjuntos:
                    p = Path(ruta)
                    if p.exists():
                        with open(p, "rb") as f:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition",
                                        f"attachment; filename={p.name}")
                        msg.attach(part)

            # 5. Envío SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_token)
                server.send_message(msg)

            return True

        except Exception as e:
            return f"❌ Error: {str(e)}"
