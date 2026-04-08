from src.business.notification_service import NotificationService
import pandas as pd


def probar_envio():
    # Creamos datos de prueba (falsos) para ver si la imagen se genera bien
    data = {
        "Número": ["CS001", "CS002"],
        "Nombre": ["Falla Masiva", "Corte Fibra"],
        "Ubicación": ["Bogotá", "Medellín"],
        "tiempo_transcurrido_legible": ["2 días", "5 horas"]
    }
    df_test = pd.DataFrame(data)

    notifier = NotificationService()

    print("1. Generando imagen...")
    if notifier.generar_imagen_reporte(df_test):
        print("2. Enviando a WhatsApp...")
        # NOTA: Esto abrirá tu navegador. Asegúrate de estar logueado en WhatsApp Web.
        notifier.enviar_whatsapp()


if __name__ == "__main__":
    probar_envio()
