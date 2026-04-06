import flet as ft
import re
from src.business.config_user_service import ConfigUserService


def main_screen(page: ft.Page, config_service: ConfigUserService, report_service):

    # 1. Datos iniciales del JSON
    current_email = config_service.get_email()
    current_token = config_service.get_token()

    # Labels de "Actual" (antes de los campos)
    lbl_actual_email = ft.Text(
        value=current_email if current_email else "Sin correo guardado",
        color="green" if current_email else "red",
        weight="bold", width=200
    )

    lbl_actual_token = ft.Text(
        value=current_token if current_token else "Sin clave guardada",
        color="green" if current_token else "red",
        weight="bold", width=200
    )

    # 2. Labels de Validación / Estado (frente a los campos, a la derecha)
    lbl_valida_correo = ft.Text(value="Esperando...", color="grey", width=140)
    lbl_valida_token = ft.Text(value="0/16", color="orange", width=140)

    def validar_interfaz(e):
        # Validación de Correo (Regex)
        regex_correo = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex_correo, txt_new_email.value.lower()):
            lbl_valida_correo.value = "Correo válido"
            lbl_valida_correo.color = "green"
        else:
            lbl_valida_correo.value = "Formato inválido"
            lbl_valida_correo.color = "red"

        # Validación de Token (Conteo de 16 caracteres)
        token_limpio = txt_new_token.value.replace(" ", "")
        largo = len(token_limpio)
        if largo == 16:
            lbl_valida_token.value = "Token completo"
            lbl_valida_token.color = "green"
        else:
            lbl_valida_token.value = f"{largo}/16 dígitos"
            lbl_valida_token.color = "orange"

        page.update()

    # 3. Campos de entrada
    txt_new_email = ft.TextField(
        label="Nuevo Correo Remitente",
        width=280,
        on_change=validar_interfaz
    )

    txt_new_token = ft.TextField(
        label="Nueva Clave de Google",
        password=True,
        can_reveal_password=True,
        width=280,
        on_change=validar_interfaz
    )

    def handle_save(e):
        email = txt_new_email.value.strip()
        token = txt_new_token.value.replace(" ", "")
        print("funciona")
        if lbl_valida_correo.color == "green" and len(token) == 16:
            config_service.save_credentials(email, token)

            # Actualizamos labels de "Actual"
            lbl_actual_email.value = email
            lbl_actual_email.color = "green"
            lbl_actual_token.value = token
            lbl_actual_token.color = "green"

            # Limpiamos campos
            txt_new_email.value = ""
            txt_new_token.value = ""
            lbl_valida_correo.value = "Actualizado"
            lbl_valida_token.value = "Actualizado"

            page.snack_bar = ft.SnackBar(
                ft.Text("Configuración de On Net Fibra guardada"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Verifique los campos en rojo/naranja"))
            page.snack_bar.open = True
            page.update()

    # Estructura de Filas: [Texto Fijo] + [Estado Guardado] + [Campo Nuevo] + [Validación]
    row_user = ft.Row(
        [ft.Text("Email:", width=50), lbl_actual_email,
         txt_new_email, lbl_valida_correo],
        alignment=ft.MainAxisAlignment.CENTER
    )

    row_pass = ft.Row(
        [ft.Text("Clave:", width=50), lbl_actual_token,
         txt_new_token, lbl_valida_token],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.Column(
        [
            ft.Text("kcode - Automatización On Net Fibra",
                    size=30, weight="bold"),
            ft.Divider(height=20),
            row_user,
            row_pass,
            ft.ElevatedButton(
                "Guardar y Actualizar Datos",
                icon=ft.Icons.SAVE,
                on_click=handle_save
            ),
            ft.Divider(height=40),
            ft.ElevatedButton(
                "Iniciar Procesamiento de Reportes",
                icon=ft.Icons.PLAY_ARROW,
                on_click=lambda _: report_service.ejecutar_accion()
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
