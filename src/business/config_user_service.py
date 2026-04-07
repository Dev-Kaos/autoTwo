import json
import os
from src.config.settings import Config


class ConfigUserService:
    """Configura los métodos para determinar el correo, el token de envío y la clave SSO"""

    def __init__(self):
        self.path = Config.USER_CONFIG_FILE
        self.config = self._load_config()

    def _load_config(self):
        """Carga los datos del JSON o retorna valores vacíos si no existe."""
        default_config = {"email": "", "token": "", "password_sso": ""}
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Combinamos con default para asegurar que password_sso exista si el JSON es viejo
                    return {**default_config, **data}
            except (json.JSONDecodeError, IOError):
                return default_config
        return default_config

    def save_credentials(self, email, token, password_sso):
        """Guarda el correo, el token de envío y la clave de acceso SSO."""
        self.config = {
            "email": email,
            "token": token,
            "password_sso": password_sso
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get_email(self):
        return self.config.get("email", "")

    def get_token(self):
        """Este es tu token original (App Password / API)"""
        return self.config.get("token", "")

    def get_password_sso(self):
        """Esta es la contraseña de red para el login de ServiceNow"""
        return self.config.get("password_sso", "")

    def is_configured(self):
        """Verifica si los campos esenciales tienen datos."""
        return bool(self.config.get("email") and self.config.get("token") and self.config.get("password_sso"))
