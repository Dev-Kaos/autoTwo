import flet as ft


def main_screen(page: ft.Page, auth_service, report_service):
    # Variable fija: usuario_actual
    usuario_actual = auth_service.obtener_usuario()

    # Componentes con nombres consistentes
    lbl_status = ft.Text(
        value=f"Sesión: {usuario_actual}" if usuario_actual else "Sin sesión",
        color="blue" if usuario_actual else "red",
        size=20, weight="bold"
    )

    txt_user = ft.TextField(label="Usuario", width=280,
                            visible=not usuario_actual)
    txt_pass = ft.TextField(label="Clave", password=True,
                            width=280, visible=not usuario_actual)

    def manejar_login(e):
        if auth_service.login(txt_user.value, txt_pass.value):
            actualizar_pantalla(txt_user.value)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error de acceso"))
            page.snack_bar.open = True
            page.update()

    def manejar_logout(e):
        auth_service.logout()
        actualizar_pantalla(None)

    def actualizar_pantalla(user):
        # Usamos 'user' como variable temporal para el cambio
        lbl_status.value = f"Sesión: {user}" if user else "Sin sesión"
        lbl_status.color = "blue" if user else "red"
        txt_user.visible = not user
        txt_pass.visible = not user
        btn_login.visible = not user
        btn_logout.visible = bool(user)
        page.update()

    btn_login = ft.ElevatedButton(
        "Entrar", on_click=manejar_login, visible=not usuario_actual)
    btn_logout = ft.ElevatedButton(
        "Salir", on_click=manejar_logout, visible=bool(usuario_actual))

    return ft.Column(
        [
            ft.Text("kcode - On Net Fibra", size=30, weight="bold"),
            lbl_status,
            txt_user,
            txt_pass,
            btn_login,
            btn_logout,
            ft.Divider(),
            ft.ElevatedButton(
                "Procesar Reporte", on_click=lambda _: report_service.ejecutar_accion())
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
