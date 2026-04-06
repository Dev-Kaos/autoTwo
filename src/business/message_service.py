"""@"""
import json
from src.config.settings import Config


class MessageService:
    """@"""

    def __init__(self):
        self.path = Config.MESSAGES_CONFIG_FILE
        # Inicializamos con slots vacíos por defecto
        self.messages = self._load_messages()

    def _load_messages(self):
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"1": "", "2": "", "3": ""}
        return {"1": "", "2": "", "3": ""}

    def save_message(self, slot, text):
        self.messages[str(slot)] = text
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=4)

    def get_message(self, slot):
        return self.messages.get(str(slot), "")
