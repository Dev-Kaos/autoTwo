""" main es el orquestador enciende la maquina y conecta los cables(inyeccion de dependencias)"""

# main.py
import flet as ft
from src.persistence.excel_repository import ExcelRepository
from src.business.report_service import ReportService
from src.presentation.main_screen import main_screen
from pathlib import Path

# Configuración rápida (Esto podría ir en src/config/settings.py)


class Config:
    ARCHIVO_ENTRADA = Path("assets/inputs/wm_order.xlsx")
    ARCHIVO_SALIDA = Path("assets/outputs/Informe_Final.xlsx")
    RUTA_CAPTURA = Path("assets/outputs/reporte.png").absolute()
    ID_GRUPO = "TU_ID_DE_GRUPO_AQUI"


def main(page: ft.Page):
    # Instanciamos las capas
    repo = ExcelRepository()
    service = ReportService(repo)

    # Cargamos la interfaz
    page.add(main_screen(page, service, Config()))


if __name__ == "__main__":
    ft.app(target=main)
