""" src/config/settings.py """
from pathlib import Path


class Config:
    """ Rutas base usando Pathlib para que funcione en Windows y Linux"""
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    INPUT_FILE = BASE_DIR / "assets" / "inputs" / "wm_order.xlsx"
    OUTPUT_FILE = BASE_DIR / "assets" / "outputs" / "Informe_Final.xlsx"
    SCREENSHOT_PATH = BASE_DIR / "assets" / "outputs" / "reporte.png"

    # Datos de conexión o IDs
    WHATSAPP_GROUP_ID = "TU_ID_DE_GRUPO_REAL"
