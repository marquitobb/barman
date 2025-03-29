class SimpleVoiceCommands:
    def __init__(self):
        self.listening = True
        print("Inicializando comandos de voz simplificados (sin PyAudio)")
    
    def listen_for_keyword(self, keyword="barman"):
        """Simula escuchar la palabra clave"""
        print(f"Di '{keyword}' para activar el asistente.")
        try:
            user_input = input("> ")
            return user_input.lower() == keyword.lower()
        except KeyboardInterrupt:
            print("\nDetección de voz interrumpida por el usuario")
            return False
    
    def listen_for_command(self):
        """Simula escuchar un comando"""
        try:
            print("Escuchando comando:")
            command = input("> ")
            return command.lower()
        except KeyboardInterrupt:
            print("\nEntrada interrumpida por el usuario")
            return None