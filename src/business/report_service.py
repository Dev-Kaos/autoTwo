"""El "Director de Orquesta". Une la persistencia con el dominio y la mensajería."""

# src/business/report_service.py
import pywhatkit as kit
import dataframe_image as dfi
from datetime import datetime
from src.domain.logic import formatear_tiempo_legible


class ReportService:
    def __init__(self, repository):
        self.repo = repository

    def generar_y_enviar_reporte(self, ruta_in, ruta_out, ruta_img, receiver_id):
        # 1. Obtener datos (Persistence)
        df = self.repo.leer_ordenes(ruta_in)

        # 2. Procesar (Business Logic)
        df['Actualizado'] = pd.to_datetime(df['Actualizado'])
        df['tiempo_transcurrido'] = datetime.now() - df['Actualizado']
        df = df.sort_values(by='tiempo_transcurrido', ascending=False)
        df['tiempo_transcurrido_legible'] = df['tiempo_transcurrido'].apply(
            formatear_tiempo_legible)

        # 3. Guardar Excel (Persistence)
        self.repo.guardar_reporte(df, ruta_out)

        # 4. Generar Imagen y Enviar (Integración)
        columnas_foto = ["Número", "Nombre",
                         "Ubicación", "tiempo_transcurrido_legible"]
        df_snapshot = df[columnas_foto].head(10)
        dfi.export(df_snapshot, str(ruta_img))

        mensaje = f"Reporte automático generado a las {datetime.now().strftime('%H:%M')}"

        # Aquí enviamos al grupo o persona usando el ID
        kit.sendwhats_image(receiver=receiver_id, img_path=str(
            ruta_img), caption=mensaje, wait_time=35)
