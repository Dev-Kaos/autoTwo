""" En este auth se carga el correo y la contraseña generada para enviar los correos"""
import json
from pathlib import Path


class AuthRepository:
    """Crea el Json con el correo y agrega la clave para enviar los smtp"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        # Si la carpeta no existe (ej. 'data/'), la creamos
        self.file_path.parent.mkdir(exist_ok=True)
        # Si el archivo no existe, creamos uno con valores por defecto
        if not self.file_path.exists():
            self.save_data({"usuario": None, "conectado": False})

    def get_data(self) -> dict[str, object]:
        """Lee el JSON y lo convierte en un diccionario de Python."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"usuario": None, "conectado": False}

    def save_data(self, data: dict[str, object]):
        """Toma un diccionario y lo escribe físicamente en el JSON."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
