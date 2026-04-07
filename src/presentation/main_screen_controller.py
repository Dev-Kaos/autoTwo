import re
import flet as ft


class MainScreenController:
    """
    CLASE CONTROLADORA: Maneja la lógica de negocio de la interfaz.
    Actúa como puente entre la Vista (Flet) y los Servicios (JSON/Excel).
    """

    # --- ACTUALIZADO: Ahora recibe mail_list_service ---
    def __init__(self, page, config_service, message_service, mail_list_service, report_service):
        self.page = page
        self.config_service = config_service
        self.message_service = message_service
        self.mail_list_service = mail_list_service  # Servicio para la lista de correos
        self.report_service = report_service

        # --- REFERENCIAS DE UI (Vínculos con la pantalla) ---
        self.lbl_actual_email = None
        self.lbl_actual_token = None
        self.lbl_valida_correo = None
        self.lbl_valida_token = None
        self.txt_new_email = None
        self.txt_new_token = None
        self.txt_mensaje_correo = None
        self.lbl_resumen_envio = None  # Referencia para el texto de destinatarios
        self.txt_new_password_sso = None
        self.lbl_valida_sso = None

    # --- LÓGICA DE VALIDACIÓN (En tiempo real) ---
    def validar_campos_credenciales(self, e):
        """Verifica que el correo y el token de 16 dígitos sean correctos"""
        regex_correo = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        # Validar Correo Electrónico
        es_valido = bool(
            re.search(regex_correo, self.txt_new_email.value.lower()))
        self.lbl_valida_correo.value = "Correo válido" if es_valido else "Formato inválido"
        self.lbl_valida_correo.color = "green" if es_valido else "red"

        # Validar Longitud del Token (Clave de aplicación de Google)
        token_limpio = self.txt_new_token.value.replace(" ", "")
        es_token_ok = len(token_limpio) == 16
        self.lbl_valida_token.value = "Token completo" if es_token_ok else f"{len(token_limpio)}/16 dígitos"
        self.lbl_valida_token.color = "green" if es_token_ok else "orange"

        es_sso_ok = len(self.txt_new_password_sso.value.strip()) > 0

        if self.lbl_valida_sso:
            self.lbl_valida_sso.value = "Clave lista" if es_sso_ok else "Clave vacía"
            self.lbl_valida_sso.color = "green" if es_sso_ok else "red"

        self.page.update()

    # --- LÓGICA DE PERSISTENCIA (Escritura en JSON) ---
    def guardar_credenciales(self, e):
        """Toma los datos de los inputs y los envía al ConfigUserService"""
        email = self.txt_new_email.value.strip()
        token = self.txt_new_token.value.replace(" ", "")
        password_sso = self.txt_new_password_sso.value.strip()

        if self.lbl_valida_correo.color == "green" and len(token) == 16:
            self.config_service.save_credentials(email, token, password_sso)
            self.lbl_actual_email.value = email
            self.lbl_actual_token.value = token
            # Limpiar campos después de guardar
            self.txt_new_email.value = ""
            self.txt_new_token.value = ""
            self.txt_new_password_sso.value = ""
            self._notificar("Credenciales de On Net Fibra actualizadas")

    # --- LÓGICA DE PLANTILLAS (Mensajería) ---
    def cargar_mensaje_slot(self, slot):
        """Recupera el mensaje del JSON y lo pone en el cuadro de texto"""
        contenido = self.message_service.get_message(slot)
        self.txt_mensaje_correo.value = contenido
        self.page.update()
        self._notificar(f"Slot #{slot} cargado exitosamente")

    def guardar_mensaje_slot(self, slot):
        """Guarda permanentemente el texto actual en el slot seleccionado"""
        texto = self.txt_mensaje_correo.value
        self.message_service.save_message(slot, texto)
        self._notificar(f"Mensaje guardado en Slot {slot}")

    # --- NUEVA LÓGICA: GESTIÓN DE DESTINATARIOS ---

    def actualizar_resumen_destinatarios(self):
        """Refresca el texto informativo en formato vertical"""
        lista = self.mail_list_service.get_all_emails()
        cant = len(lista)

        if self.lbl_resumen_envio:
            if cant > 0:
                # Unimos los correos con un salto de línea (\n) para que se vean uno abajo del otro
                # Mostramos máximo los primeros 5 para no alargar demasiado la pantalla
                visibles = lista[:5]
                texto_vertical = "\n".join(visibles)

                if cant > 5:
                    texto_vertical += f"\n... y {cant - 5} más"

                self.lbl_resumen_envio.value = f"Enviar a:\n{texto_vertical}"
            else:
                self.lbl_resumen_envio.value = "Sin destinatarios configurados"

            self.page.update()

    def abrir_ajustes_correo(self, e):
        """Despliega el AlertDialog para agregar o quitar correos"""
        lista_visual = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)
        txt_nuevo_correo = ft.TextField(label="Nuevo correo", expand=True)

        def eliminar_correo(correo_texto):
            actuales = self.mail_list_service.get_all_emails()
            if correo_texto in actuales:
                actuales.remove(correo_texto)
                self.mail_list_service.save_emails(actuales)
                actualizar_lista_visual()
                self.actualizar_resumen_destinatarios()

        def agregar_correo(e):
            if txt_nuevo_correo.value.strip():
                actuales = self.mail_list_service.get_all_emails()
                actuales.append(txt_nuevo_correo.value.strip())
                self.mail_list_service.save_emails(actuales)
                txt_nuevo_correo.value = ""
                actualizar_lista_visual()
                self.actualizar_resumen_destinatarios()

        def actualizar_lista_visual():
            lista_visual.controls.clear()
            for correo in self.mail_list_service.get_all_emails():
                lista_visual.controls.append(
                    ft.Row([
                        ft.Text(correo, expand=True),
                        ft.IconButton(
                            ft.Icons.DELETE,
                            icon_color="red",
                            on_click=lambda _, c=correo: eliminar_correo(c)
                        )
                    ])
                )
            self.page.update()

        actualizar_lista_visual()

        dlg = ft.AlertDialog(
            title=ft.Text("Lista de Destinatarios"),
            content=ft.Column(controls=[
                lista_visual,
                ft.Row(controls=[
                    txt_nuevo_correo,
                    ft.IconButton(ft.Icons.ADD, on_click=agregar_correo)
                ]),
            ], tight=True, width=400),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: (
                    setattr(dlg, "open", False), self.page.update()
                ))
            ],
        )

        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    # --- LÓGICA DE ACCIÓN (Ejecución de Tareas) ---

    def ejecutar_flujo_reporte(self, e):
        # Recuperamos las tres piezas de información
        user_corp = self.config_service.get_email()
        token_envio = self.config_service.get_token()  # Para correos/mensajes
        pass_sso = self.config_service.get_password_sso()  # PARA SELENIUM

        if not pass_sso:
            self._notificar("⚠️ Falta la contraseña SSO en la configuración.")
            return

        # Lanzamos la descarga pasándole la contraseña de red
        self.report_service.descargar_automaticamente(user_corp, pass_sso)

    def _notificar(self, texto):
        """Helper para mostrar mensajes rápidos en la parte inferior (SnackBar)"""
        self.page.snack_bar = ft.SnackBar(ft.Text(texto))
        self.page.snack_bar.open = True
        self.page.update()
