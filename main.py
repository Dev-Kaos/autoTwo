import flet as ft
from src.presentation.main_screen import main_screen
from src.business.config_user_service import ConfigUserService
from src.business.message_service import MessageService
from src.business.mail_list_service import MailListService  # <--- IMPORTAR EL NUEVO
from src.business.report_service import ReportService


def main(page: ft.Page):
    page.title = "kcode - On Net Fibra"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "always"
    # 1. Instanciar TODOS los servicios
    config_service = ConfigUserService()
    message_service = MessageService()
    mail_list_service = MailListService()  # <--- CREAR LA INSTANCIA
    report_service = ReportService()

    # 2. Cargar la pantalla pasando los 5 argumentos en el orden correcto
    page.add(
        main_screen(
            page,
            config_service,
            message_service,
            mail_list_service,  # <--- AGREGAR AQUÍ
            report_service
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
