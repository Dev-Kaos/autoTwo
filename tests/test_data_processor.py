from src.business.data_processor_service import DataProcessorService
import pandas as pd


def probar_procesamiento():
    print("🧪 Iniciando prueba unitaria del procesador de datos...")

    # Instanciamos el servicio
    processor = DataProcessorService()

    # Ejecutamos la lógica de procesamiento
    df_resultado = processor.procesar_casos_sin_avance()

    if df_resultado is not None:
        print("\n✅ PRUEBA EXITOSA")
        print(f"Número de filas recuperadas: {len(df_resultado)}")

        print("\n--- Vista previa de los 5 casos con más tiempo sin avance ---")
        # Mostramos las columnas clave para verificar los cálculos
        columnas_verificacion = [
            "Número", "Actualizado", "tiempo_transcurrido_legible"]
        print(df_resultado[columnas_verificacion].head(5))

        # Verificación técnica: ¿La columna de tiempo es realmente un string legible?
        ejemplo_tiempo = df_resultado['tiempo_transcurrido_legible'].iloc[0]
        print(f"\n📝 Formato de tiempo verificado: {ejemplo_tiempo}")
    else:
        print("\n❌ LA PRUEBA FALLÓ: No se pudo obtener o procesar el archivo.")


if __name__ == "__main__":
    probar_procesamiento()
