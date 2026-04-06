"""config_user_service"""
import json
import os
from src.config.settings import Config


class ConfigUserService:
    """Configuraa los metodos para determinar el correo y el codigo"""

    def __init__(self):
        self.path = Config.USER_CONFIG_FILE
        self.config = self._load_config()

    def _load_config(self):
        """Carga los datos del JSON o retorna valores vacíos si no existe."""
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"email": "", "token": ""}
        return {"email": "", "token": ""}

    def save_credentials(self, email, token):
        """Guarda el correo y el token de 16 dígitos en el archivo local."""
        self.config = {"email": email, "token": token}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get_email(self):
        return self.config.get("email", "")

    def get_token(self):
        return self.config.get("token", "")

    def is_configured(self):
        """Verifica si ambos campos tienen datos."""
        return bool(self.config.get("email") and self.config.get("token"))
