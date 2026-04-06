import re
import flet as ft


class MainScreenController:
    """
    CLASE CONTROLADORA: Maneja la lógica de negocio de la interfaz.
    Actúa como puente entre la Vista (Flet) y los Servicios (JSON/Excel).
    """

    def __init__(self, page, config_service, message_service, report_service):
        self.page = page
        self.config_service = config_service
        self.message_service = message_service
        self.report_service = report_service

        # --- REFERENCIAS DE UI (Vínculos con la pantalla) ---
        self.lbl_actual_email = None
        self.lbl_actual_token = None
        self.lbl_valida_correo = None
        self.lbl_valida_token = None
        self.txt_new_email = None
        self.txt_new_token = None
        self.txt_mensaje_correo = None

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

        self.page.update()

    # --- LÓGICA DE PERSISTENCIA (Escritura en JSON) ---
    def guardar_credenciales(self, e):
        """Toma los datos de los inputs y los envía al ConfigUserService"""
        email = self.txt_new_email.value.strip()
        token = self.txt_new_token.value.replace(" ", "")

        if self.lbl_valida_correo.color == "green" and len(token) == 16:
            self.config_service.save_credentials(email, token)
            self.lbl_actual_email.value = email
            self.lbl_actual_token.value = token
            # Limpiar campos después de guardar
            self.txt_new_email.value = ""
            self.txt_new_token.value = ""
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

    # --- LÓGICA DE ACCIÓN (Ejecución de Tareas) ---
    def ejecutar_flujo_reporte(self, e):
        """Dispara la lógica de procesamiento de Pandas en el ReportService"""
        self._notificar("Iniciando procesamiento de reportes...")
        self.report_service.ejecutar_accion()

    def _notificar(self, texto):
        """Helper para mostrar mensajes rápidos en la parte inferior (SnackBar)"""
        self.page.snack_bar = ft.SnackBar(ft.Text(texto))
        self.page.snack_bar.open = True
        self.page.update()
