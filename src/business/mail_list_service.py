import json
from src.config.settings import Config


class MailListService:
    def __init__(self):
        # Usamos la ruta que definimos en Config
        self.path = Config.MAIL_LIST_FILE
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """Crea el archivo JSON con una lista vacía si no existe."""
        if not self.path.exists():
            self.save_emails([])

    def get_all_emails(self):
        """Lee el archivo JSON y retorna la lista de correos."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_emails(self, lista_correos):
        """Guarda la lista de correos en el archivo JSON."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(lista_correos, f, indent=4)
