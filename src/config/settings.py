""" src/config/settings.py """
from pathlib import Path


class Config:
    """ Rutas base usando Pathlib para que funcione en Windows y Linux """
    # Sube 3 niveles: config -> src -> autoTwo
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # --- NUEVA RUTA PARA EL USUARIO ---
    USER_CONFIG_FILE = BASE_DIR / "data" / "user_data.json"

    # Tus rutas existentes
    INPUT_FILE = BASE_DIR / "assets" / "inputs" / "wm_order.xlsx"
    OUTPUT_FILE = BASE_DIR / "assets" / "outputs" / "Informe_Final.xlsx"
    SCREENSHOT_PATH = BASE_DIR / "assets" / "outputs" / "reporte.png"

    WHATSAPP_GROUP_ID = "TU_ID_DE_GRUPO_REAL"
