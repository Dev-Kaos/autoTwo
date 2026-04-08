import pandas as pd
import dataframe_image as dfi
import pywhatkit as kit
from datetime import datetime
from pathlib import Path
import os


class NotificationService:
    def __init__(self, id_grupo="J3BhNzzFU2EKjJDEPYceWg"):
        self.id_grupo = id_grupo
        # Guardamos la captura en la carpeta assets de tu ASUS A15
        # self.base_path = Path(__file__).parent.parent
        self.root_path = Path(__file__).resolve().parent.parent.parent

        self.ruta_captura = self.root_path / "assets" / "reporte_captura.png"

    def generar_imagen_reporte(self, df):
        """Convierte las primeras filas del DataFrame en una imagen elegante."""
        try:
            # Seleccionamos columnas seguras (las que suelen estar en ServiceNow)
            # Si los nombres cambian, solo ajustamos esta lista
            cols = [c for c in ["Número", "Nombre", "Ubicación",
                                "tiempo_transcurrido_legible"] if c in df.columns]
            df_snapshot = df[cols].head(10)

            # Estilo On Net Fibra (Verde)
            df_styled = df_snapshot.style.set_table_styles(
                [{'selector': 'th', 'props': [
                    ('background-color', '#4CAF50'),
                    ('color', 'white'),
                    ('font-family', 'Arial'),
                    ('text-align', 'center')]}]
            ).hide(axis="index")

            # Exportar a PNG
            dfi.export(df_styled, str(self.ruta_captura))
            print(f"📸 Captura generada en: {self.ruta_captura}")
            return True
        except Exception as e:
            print(f"❌ Error al generar imagen: {e}")
            return False

    def enviar_whatsapp(self, mensaje=None):
        """Abre WhatsApp Web y envía la imagen al grupo."""
        try:
            ahora = datetime.now().strftime('%d/%m %H:%M')
            if not mensaje:
                mensaje = f"🤖 kcode: Reporte de casos sin avances actualizado ({ahora})."

            print("🚀 Abriendo WhatsApp Web... ¡No muevas el mouse!")

            # Usamos wait_time=20 para dar tiempo a que cargue en tu red de 300Mbps
            kit.sendwhats_image(
                receiver=self.id_grupo,
                img_path=str(self.ruta_captura),
                caption=mensaje,
                wait_time=20,
                tab_close=True  # Cierra la pestaña después de enviar
            )
            print("✅ Reporte enviado exitosamente.")
            return True
        except Exception as e:
            print(f"❌ Error en el envío de WhatsApp: {e}")
            return False
