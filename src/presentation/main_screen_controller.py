import re
import flet as ft
import threading


class MainScreenController:
    """
    CLASE CONTROLADORA: Maneja la lógica de negocio de la interfaz.
    Actúa como puente entre la Vista (Flet) y los Servicios (JSON/Excel).
    """

    def __init__(self, page, config_service, message_service, mail_list_service, report_service, data_processor_service):
        self.page = page
        self.config_service = config_service
        self.message_service = message_service
        self.mail_list_service = mail_list_service
        self.report_service = report_service
        self.data_processor_service = data_processor_service

        # --- REFERENCIAS DE UI ---
        self.lbl_actual_email = None
        self.lbl_actual_token = None
        self.lbl_valida_correo = None
        self.lbl_valida_token = None
        self.txt_new_email = None
        self.txt_new_token = None
        self.txt_mensaje_correo = None
        self.lbl_resumen_envio = None
        self.txt_new_password_sso = None
        self.lbl_valida_sso = None
        self.btn_ejecutar = None

    # --- LÓGICA DE VALIDACIÓN ---
    def validar_campos_credenciales(self, e):
        regex_correo = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        es_valido = bool(
            re.search(regex_correo, self.txt_new_email.value.lower()))
        self.lbl_valida_correo.value = "Correo válido" if es_valido else "Formato inválido"
        self.lbl_valida_correo.color = "green" if es_valido else "red"

        token_limpio = self.txt_new_token.value.replace(" ", "")
        es_token_ok = len(token_limpio) == 16
        self.lbl_valida_token.value = "Token completo" if es_token_ok else f"{len(token_limpio)}/16 dígitos"
        self.lbl_valida_token.color = "green" if es_token_ok else "orange"

        es_sso_ok = len(self.txt_new_password_sso.value.strip()) > 0
        if self.lbl_valida_sso:
            self.lbl_valida_sso.value = "Clave lista" if es_sso_ok else "Clave vacía"
            self.lbl_valida_sso.color = "green" if es_sso_ok else "red"
        self.page.update()

    # --- LÓGICA DE PERSISTENCIA ---
    def guardar_credenciales(self, e):
        email = self.txt_new_email.value.strip()
        token = self.txt_new_token.value.replace(" ", "")
        password_sso = self.txt_new_password_sso.value.strip()

        if self.lbl_valida_correo.color == "green" and len(token) == 16:
            self.config_service.save_credentials(email, token, password_sso)
            self.lbl_actual_email.value = email
            self.lbl_actual_token.value = token
            self.txt_new_email.value = ""
            self.txt_new_token.value = ""
            self.txt_new_password_sso.value = ""
            self._notificar("Credenciales actualizadas correctamente")

    # --- LÓGICA DE PLANTILLAS ---
    def cargar_mensaje_slot(self, slot):
        contenido = self.message_service.get_message(slot)
        self.txt_mensaje_correo.value = contenido
        self.page.update()
        self._notificar(f"Slot #{slot} cargado")

    def guardar_mensaje_slot(self, slot):
        texto = self.txt_mensaje_correo.value
        self.message_service.save_message(slot, texto)
        self._notificar(f"Mensaje guardado en Slot {slot}")

    # --- GESTIÓN DE DESTINATARIOS ---
    def actualizar_resumen_destinatarios(self):
        lista = self.mail_list_service.get_all_emails()
        cant = len(lista)
        if self.lbl_resumen_envio:
            if cant > 0:
                visibles = lista[:5]
                texto_vertical = "\n".join(visibles)
                if cant > 5:
                    texto_vertical += f"\n... y {cant - 5} más"
                self.lbl_resumen_envio.value = f"Enviar a:\n{texto_vertical}"
            else:
                self.lbl_resumen_envio.value = "Sin destinatarios"
            self.page.update()

    def abrir_ajustes_correo(self, e):
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
            correo = txt_nuevo_correo.value.strip()
            if correo:
                actuales = self.mail_list_service.get_all_emails()
                actuales.append(correo)
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
                        ft.IconButton(ft.Icons.DELETE, icon_color="red",
                                      on_click=lambda _, c=correo: eliminar_correo(c))
                    ])
                )
            self.page.update()

        actualizar_lista_visual()
        dlg = ft.AlertDialog(
            title=ft.Text("Destinatarios"),
            content=ft.Column([
                lista_visual,
                ft.Row([txt_nuevo_correo, ft.IconButton(
                    ft.Icons.ADD, on_click=agregar_correo)])
            ], tight=True, width=400),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: (
                setattr(dlg, "open", False), self.page.update()))]
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    # --- EJECUCIÓN DEL FLUJO ---
    def ejecutar_flujo_reporte(self, e):
        def hilo_proceso():
            try:
                self._notificar("🚀 Iniciando descarga ServiceNow...")
                user_corp = self.config_service.get_email()
                pass_sso = self.config_service.get_password_sso()

                if not pass_sso:
                    self._notificar("❌ Falta contraseña SSO")
                    return

                # PASO 1: Descarga
                self.report_service.descargar_automaticamente(
                    user_corp, pass_sso)

                # PASO 2: Procesamiento
                self._notificar("📊 Procesando Excel...")
                self.data_processor_service.procesar_archivo()

                # PASO 3: Notificaciones finales
                self._notificar("📧 Enviando reportes...")
                self.enviar_notificaciones_finales()

                self._notificar("✅ Proceso kcode terminado")
            except Exception as ex:
                self._notificar(f"❌ Error: {ex}")
            finally:
                if self.btn_ejecutar:
                    self.btn_ejecutar.disabled = False
                self.page.update()

        if self.btn_ejecutar:
            self.btn_ejecutar.disabled = True
        self.page.update()
        threading.Thread(target=hilo_proceso, daemon=True).start()

    def enviar_notificaciones_finales(self):
        cuerpo_final = self.txt_mensaje_correo.value
        from src.business.mail_service import MailService
        mailer = MailService()
        archivos = [
            "assets/outputs/reporte_captura.png",
            "assets/inputs/sn_customerservice_case.xlsx"
        ]
        return mailer.enviar_reporte(
            cuerpo_mensaje=cuerpo_final,
            asunto="📊 Reporte Automatizado - On Net Fibra",
            adjuntos=archivos
        )

    def enviar_notificacion_correo(self, e=None):
        mensaje_ui = self.txt_mensaje_correo.value
        from src.business.mail_service import MailService
        mailer = MailService()
        return mailer.enviar_reporte(
            cuerpo_mensaje=mensaje_ui,
            adjuntos=["assets/outputs/reporte_captura.png",
                      "assets/inputs/sn_customerservice_case.xlsx"]
        )

    # def _notificar(self, texto):
    #     self.page.snack_bar = ft.SnackBar(ft.Text(texto))
    #     self.page.snack_bar.open = True
    #     self.page.update()
    def _notificar(self, texto):
        """Muestra mensajes en la parte inferior de la app de forma segura"""
        print(
            # Para que al menos lo veas en la consola
            f"[DEBUG KCODE]: {texto}")

        # 1. Creamos el SnackBar con configuración de visibilidad clara
        snack = ft.SnackBar(
            content=ft.Text(texto, color="white"),
            bgcolor="blue_grey_900",
            duration=3000,  # 3 segundos
            action="OK"
        )

        # 2. Se lo asignamos a la página
        self.page.snack_bar = snack

        # 3. Lo abrimos
        self.page.snack_bar.open = True

        # 4. Refrescamos la página (VITAL)
        self.page.update()
