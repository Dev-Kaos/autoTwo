from src.business.mail_service import MailService


def test():
    service = MailService()

    # Agregamos tu correo para probar
    service.save_emails(["manuelfernandovela@gmail.com"])

    # Enviamos sin adjuntos por ahora para ver si conecta bien
    service.enviar_reporte(
        asunto="Prueba kcode",
        cuerpo="Este es un test del servicio unificado."
    )


if __name__ == "__main__":
    test()
