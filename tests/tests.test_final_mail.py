from src.business.mail_service import MailService
import os


def test_real():
    mailer = MailService()

    print("🚀 Iniciando prueba de envío con Gmail...")

    # Texto de prueba como si viniera del TextBox de Flet
    mensaje_prueba = "Hola Manuel,\n\nEste es un mensaje de prueba enviado desde kcode usando la cuenta de Google. ¡La automatización funciona!"

    # Intentar envío
    resultado = mailer.enviar_reporte(
        cuerpo_mensaje=mensaje_prueba,
        # Si ya tienes archivos en assets, puedes descomentar la siguiente línea:
        # adjuntos=["assets/reporte_captura.png"]
    )

    if resultado == True:
        print("✅ ¡ÉXITO! Revisa tu bandeja de entrada (y la de los destinatarios).")
    else:
        print(f"❌ FALLÓ: {resultado}")


if __name__ == "__main__":
    test_real()
