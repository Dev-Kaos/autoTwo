import pandas as pd
import os
from datetime import datetime
from pathlib import Path


class DataProcessorService:
    def __init__(self, ruta_descargas=None):
        self.ruta_descargas = ruta_descargas or Path(
            os.path.expanduser("~")) / "Downloads"

    def _formatear_tiempo(self, td: pd.Timedelta) -> str:
        """Convierte un Timedelta en formato legible (Días, HH:MM)."""
        if pd.isnull(td):
            return "Sin datos"
        dias = td.days
        horas = td.components.hours
        minutos = td.components.minutes
        return f"{dias} días, {horas:02d}:{minutos:02d}"

    def obtener_archivo_reciente(self):
        """Busca el último Excel de ServiceNow descargado."""
        archivos = list(self.ruta_descargas.glob(
            "sn_customerservice_case*.xlsx"))
        if not archivos:
            return None
        return max(archivos, key=os.path.getmtime)

    def procesar_casos_sin_avance(self):
        """Lee el Excel, calcula tiempos y devuelve un DataFrame listo para el reporte."""
        archivo = self.obtener_archivo_reciente()
        if not archivo:
            print("❌ No se encontró el archivo para procesar.")
            return None

        try:
            print(f"⚙️ Procesando: {archivo.name}")
            # Leemos la hoja 'Page 1' como estaba en tu código anterior
            df = pd.read_excel(archivo)

            # 1. Selección de columnas críticas (ajustadas a tu captura)
            columnas = ["Número", "Creado",
                        "Grupo de asignación", "Ubicación", "Actualizado"]
            df_filtrado = df[columnas].copy()

            # 2. Cálculos de tiempo
            df_filtrado['Actualizado'] = pd.to_datetime(
                df_filtrado['Actualizado'])
            # Calculamos la diferencia contra el momento actual
            df_filtrado['tiempo_transcurrido'] = datetime.now() - \
                df_filtrado['Actualizado']

            # 3. Ordenar por el más antiguo (el que lleva más tiempo sin actualizar)
            df_filtrado = df_filtrado.sort_values(
                by='tiempo_transcurrido', ascending=False)

            # 4. Crear columna legible para la imagen de WhatsApp
            df_filtrado['tiempo_transcurrido_legible'] = df_filtrado['tiempo_transcurrido'].apply(
                self._formatear_tiempo)

            print(
                f"✅ Procesamiento completado. {len(df_filtrado)} casos analizados.")
            print(df_filtrado)
            return df_filtrado

        except Exception as e:
            print(f"❌ Error al procesar datos: {e}")
            return None
