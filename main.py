""" main es el orquestador enciende la maquina y conecta los cables(inyeccion de dependencias)"""
from pathlib import Path
import flet as ft
from src.persistence.auth_repository import AuthRepository
from src.business.auth_service import AuthService
from src.business.report_service import ReportService
from src.business.message_service import MessageService
from src.presentation.main_screen import main_screen
# _____
from src.business.config_user_service import ConfigUserService


def main(page: ft.Page):
    """
    Configura el entorno de la aplicación Flet y ensambla las capas de software.

    Esta función inicializa la ventana principal, define los parámetros
    visuales base (tema, título) y conecta el servicio de lógica de negocio
    con la interfaz de usuario (main_screen).

    Args:
        page (ft.Page): La instancia de la página principal proporcionada por Flet.
    """
    # 1. Configuración de la ventana
    page.title = "kcode - Automatización"
    page.theme_mode = ft.ThemeMode.DARK

    # 2. Persistencia
    repo = AuthRepository(Path("data/session.json"))

    # 3. Servicios
    auth_service = AuthService(repo)
    report_service = ReportService()
    config_user_service = ConfigUserService()
    message_service = MessageService()

    # 4. Carga de la interfaz
    # Le pasamos el servicio a la pantalla para que puedan interactuar
    page.add(main_screen(page, config_user_service,
             message_service, report_service,))

    # _____________________________________________________________________________________________


if __name__ == "__main__":
    ft.app(target=main)  # type:ignore
