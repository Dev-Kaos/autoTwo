import flet as ft
from src.presentation.main_screen_controller import MainScreenController


def main_screen(page: ft.Page, config_service, message_service, report_service):
    """
    VISTA PRINCIPAL: Solo contiene la estructura jerárquica de la interfaz (Layout).
    """
    # 1. Instanciar el Controlador
    controller = MainScreenController(
        page, config_service, message_service, report_service)

    # 2. DEFINICIÓN DE COMPONENTES VISUALES
    # Estos componentes se asignan al controlador para que él pueda manipular sus valores
    controller.lbl_actual_email = ft.Text(
        value=config_service.get_email() or "Sin correo",
        color="green", weight="bold", width=200
    )
    controller.lbl_actual_token = ft.Text(
        value=config_service.get_token() or "Sin clave",
        color="green", weight="bold", width=200
    )

    # Labels informativos de validación
    controller.lbl_valida_correo = ft.Text(
        value="Esperando...", color="grey", width=140)
    controller.lbl_valida_token = ft.Text(
        value="0/16", color="orange", width=140)

    # Inputs de texto vinculados a los métodos del controlador
    controller.txt_new_email = ft.TextField(
        label="Nuevo Correo", width=280,
        on_change=controller.validar_campos_credenciales
    )
    controller.txt_new_token = ft.TextField(
        label="Nueva Clave de App", password=True, can_reveal_password=True,
        width=280, on_change=controller.validar_campos_credenciales
    )

    # Cuadro multilinea para redactar el correo
    controller.txt_mensaje_correo = ft.TextField(
        label="Mensaje para el reporte",
        multiline=True, min_lines=10, width=500,
        hint_text="Redacte aquí el contenido del correo..."
    )

    # 3. CONSTRUCTORES DE ELEMENTOS REPETITIVOS
    def build_slot_row(n):
        """Crea la fila de botones (Cargar/Guardar) para cada slot de mensaje"""
        return ft.Row([
            ft.ElevatedButton(
                f"Cargar #{n}", icon=ft.Icons.DOWNLOAD,
                on_click=lambda _: controller.cargar_mensaje_slot(n), width=120
            ),
            ft.IconButton(
                icon=ft.Icons.SAVE,
                on_click=lambda _: controller.guardar_mensaje_slot(n),
                icon_color="blue"
            )
        ])

    # 4. ENSAMBLAJE DEL DISEÑO (LAYOUT)
    return ft.Column(
        [
            # Encabezado
            ft.Text("kcode - Gestión On Net Fibra", size=30, weight="bold"),
            ft.Divider(height=10),

            # SECCIÓN: Gestión de Credenciales
            ft.Row([ft.Text("Email:", width=50), controller.lbl_actual_email,
                   controller.txt_new_email, controller.lbl_valida_correo], alignment="center"),
            ft.Row([ft.Text("Clave:", width=50), controller.lbl_actual_token,
                   controller.txt_new_token, controller.lbl_valida_token], alignment="center"),
            ft.ElevatedButton("Actualizar Credenciales", icon=ft.Icons.SYNC,
                              on_click=controller.guardar_credenciales),

            ft.Divider(height=30, color="transparent"),  # Espaciador

            # SECCIÓN: Panel de Mensajería (Slots y Textbox)
            ft.Row([
                ft.Column([
                    ft.Text("Plantillas Guardadas", weight="bold"),
                    build_slot_row("1"),
                    build_slot_row("2"),
                    build_slot_row("3"),
                    ft.ElevatedButton(
                        "Limpiar Texto", icon=ft.Icons.DELETE,
                        on_click=lambda _: setattr(
                            controller.txt_mensaje_correo, "value", "") or page.update(),
                        bgcolor="red100"
                    )
                ]),
                controller.txt_mensaje_correo
            ], alignment="center", spacing=40),

            ft.Divider(height=30, color="transparent"),

            # SECCIÓN: Botón de Acción Principal
            ft.ElevatedButton(
                "EJECUTAR PROCESO COMPLETO",
                icon=ft.Icons.PLAY_ARROW, height=50,
                bgcolor="blue", color="white",
                on_click=controller.ejecutar_flujo_reporte
            )
        ],
        horizontal_alignment="center",
        scroll="always",
        spacing=10
    )
