class AuthService:
    # 1. El Constructor: "Conectando con el almacén"
    def __init__(self, repo):
        """
        Al nacer, el servicio recibe el 'repo' (AuthRepository).
        No sabe SI es un JSON o una DB, solo sabe que ese objeto 
        tiene el poder de guardar y leer datos.
        """
        self.repo = repo

    # 2. La Verificación: "¿Quién está ahí?"
    def obtener_usuario(self):
        """
        Esta parte se usa apenas abres la app.
        """
        # Le pide al repositorio los datos crudos del archivo
        datos = self.repo.get_data()

        # Revisa si en el archivo dice que hay alguien conectado
        if datos.get("conectado") == True:
            return datos.get("usuario")  # Devuelve "Manuel"

        return None  # Si no hay nadie, devuelve Nada

    # 3. La Acción: "El Intento de Entrada"
    def login(self, user, password):
        """
        Aquí es donde aplicas las reglas de negocio del SENA o de On Net.
        """
        # Regla de oro: Solo entra si coincide con esto
        # (Más adelante esto podría ser una lista de usuarios)
        if user == "manuel" and password == "1234":

            # Si es correcto, le ordena al repo que lo escriba en el disco
            self.repo.save_data({
                "usuario": user,
                "conectado": True
            })
            return True  # Avisa a la Interfaz: "¡Déjalo pasar!"

        return False  # Avisa a la Interfaz: "Error, datos falsos"

    # 4. La Salida: "Cerrar la sesión"
    def logout(self):
        """Limpia el rastro del usuario en el archivo."""
        self.repo.save_data({
            "usuario": None,
            "conectado": False
        })
