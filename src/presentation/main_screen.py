import flet as ft
from src.presentation.main_screen_controller import MainScreenController


def main_screen(page: ft.Page, config_service, message_service, mail_list_service, report_service):
    """
    VISTA PRINCIPAL: Estructura con alineación simétrica corregida.
    """
    # 1. Instanciar el Controlador
    controller = MainScreenController(
        page, config_service, message_service, mail_list_service, report_service)

    # 2. DEFINICIÓN DE COMPONENTES VISUALES (Con anchos fijos para alinear)
    # Columna "Valores Actuales" (Ancho 220 para que quepa el correo largo de On Net)
    controller.lbl_actual_email = ft.Text(
        value=config_service.get_email() or "Sin correo",
        color="green", weight="bold", width=220
    )
    controller.lbl_actual_token = ft.Text(
        value=config_service.get_token() or "Sin clave",
        color="green", weight="bold", width=220
    )
    controller.lbl_actual_password_sso = ft.Text(
        value=config_service.get_password_sso() or "Sin SSO",
        color="green", weight="bold", width=220
    )

    # Columna "Mensajes de Validación" (Ancho 120)
    controller.lbl_valida_correo = ft.Text(
        value="Esperando...", color="grey", width=120)
    controller.lbl_valida_token = ft.Text(
        value="0/16", color="orange", width=120)
    controller.lbl_valida_sso = ft.Text(
        value="Esperando...", color="grey", width=120)

    # Inputs de texto (Ancho 280)
    controller.txt_new_email = ft.TextField(
        label="Nuevo Correo", width=280,
        on_change=controller.validar_campos_credenciales
    )
    controller.txt_new_token = ft.TextField(
        label="Nueva Clave de App", password=True, can_reveal_password=True,
        width=280, on_change=controller.validar_campos_credenciales
    )
    controller.txt_new_password_sso = ft.TextField(
        label="Nueva Clave ServiceNow", password=True, can_reveal_password=True,
        width=280, value=config_service.get_password_sso(),
        on_change=controller.validar_campos_credenciales
    )

    controller.txt_mensaje_correo = ft.TextField(
        label="Mensaje para el reporte",
        multiline=True, min_lines=10, width=500,
        hint_text="Redacte aquí el contenido del correo..."
    )

    controller.lbl_resumen_envio = ft.Text(
        value="Cargando destinatarios...", color="blue", weight="bold")
    controller.actualizar_resumen_destinatarios()

    # 3. CONSTRUCTORES DE ELEMENTOS REPETITIVOS
    def build_slot_row(n):
        return ft.Row([
            ft.ElevatedButton(f"Cargar #{n}", icon=ft.Icons.DOWNLOAD,
                              on_click=lambda _: controller.cargar_mensaje_slot(n), width=120),
            ft.IconButton(icon=ft.Icons.SAVE, on_click=lambda _: controller.guardar_mensaje_slot(
                n), icon_color="blue")
        ])

    # 4. ENSAMBLAJE DEL DISEÑO (LAYOUT CORREGIDO)
    return ft.Column(
        [
            ft.Text("kcode - Gestión On Net Fibra", size=30, weight="bold"),
            ft.Divider(height=10),

            # SECCIÓN: Gestión de Credenciales (Simétrica)
            ft.Row([
                ft.Text("Email:", width=100, weight="bold"),
                controller.lbl_actual_email,
                controller.txt_new_email,
                controller.lbl_valida_correo
            ], alignment="center", spacing=20),

            ft.Row([
                ft.Text("Token App:", width=100, weight="bold"),
                controller.lbl_actual_token,
                controller.txt_new_token,
                controller.lbl_valida_token
            ], alignment="center", spacing=20),

            ft.Row([
                ft.Text("Clave SSO:", width=100, weight="bold"),
                controller.lbl_actual_password_sso,
                controller.txt_new_password_sso,
                controller.lbl_valida_sso
            ], alignment="center", spacing=20),

            ft.ElevatedButton("Actualizar Credenciales", icon=ft.Icons.SYNC,
                              on_click=controller.guardar_credenciales),
            ft.Divider(height=30, color="transparent"),

            # Resto de la interfaz...
            ft.Row([
                ft.Column([
                    ft.Text("Plantillas Guardadas", weight="bold"),
                    build_slot_row("1"), build_slot_row(
                        "2"), build_slot_row("3"),
                    ft.ElevatedButton("Limpiar Texto", icon=ft.Icons.DELETE, on_click=lambda _: setattr(
                        controller.txt_mensaje_correo, "value", "") or page.update(), bgcolor="red100")
                ]),
                controller.txt_mensaje_correo
            ], alignment="center", spacing=40),

            ft.Divider(height=20),

            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EMAIL_OUTLINED, color="blue"),
                    controller.lbl_resumen_envio,
                    ft.ElevatedButton(
                        "Editar Destinatarios", icon=ft.Icons.EDIT, on_click=controller.abrir_ajustes_correo)
                ], alignment="center", spacing=20),
                padding=10, bgcolor=ft.Colors.GREY_50, border_radius=10
            ),

            ft.ElevatedButton("EJECUTAR PROCESO COMPLETO", icon=ft.Icons.PLAY_ARROW, height=50,
                              bgcolor="blue", color="white", on_click=controller.ejecutar_flujo_reporte)
        ],
        horizontal_alignment="center", scroll="always", spacing=10
    )
