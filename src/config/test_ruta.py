"""Archivo para probar el funcionamiento de las rutas"""
from pathlib import Path

# La línea "mágica"
BASE_DIR = Path(__file__).resolve().parent.parent.parent

print("--- PRUEBA DE RUTA ---")
print(f"Archivo actual: {__file__}")
print(f"Ruta Raíz (BASE_DIR): {BASE_DIR}")
print(f"¿Existe la carpeta assets?: {(BASE_DIR / 'assets').exists()}")
