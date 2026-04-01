# src/presentation/main_screen.py
import flet as ft


def main_screen(page: ft.Page, report_service, config):
    def on_click_enviar(e):
        try:
            progress_bar.visible = True
            page.update()

            report_service.generar_y_enviar_reporte(
                config.ARCHIVO_ENTRADA,
                config.ARCHIVO_SALIDA,
                config.RUTA_CAPTURA,
                config.ID_GRUPO
            )

            page.snack_bar = ft.SnackBar(ft.Text("¡Reporte enviado al grupo!"))
            page.snack_bar.open = True
        except Exception as ex:
            print(f"Error: {ex}")
        finally:
            progress_bar.visible = False
            page.update()

    btn_enviar = ft.ElevatedButton(
        "Generar y Enviar Reporte", on_click=on_click_enviar)
    progress_bar = ft.ProgressBar(width=400, color="green", visible=False)

    return ft.Column([
        ft.Text("Panel de Control AUTOONE", size=30, weight="bold"),
        btn_enviar,
        progress_bar
    ])
