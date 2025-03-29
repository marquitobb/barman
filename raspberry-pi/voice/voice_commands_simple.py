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
            
    def listen_audio(self, timeout=None, phrase_limit=None):
        """Función compatible con la interfaz de VoiceCommands pero usando entrada por teclado"""
        print("Ingresa el texto (simula audio captado por micrófono):")
        try:
            user_input = input("> ")
            # Devuelve algo que simule un objeto de audio, pero que contenga el texto
            return SimpleAudio(user_input)
        except KeyboardInterrupt:
            print("\nEntrada interrumpida por el usuario")
            return None
    
    def recognize_speech(self, audio):
        """Extrae el texto del objeto SimpleAudio"""
        if audio is None:
            return None
        return audio.text.lower()
        
class SimpleAudio:
    """Clase simple para simular un objeto de audio con texto"""
    def __init__(self, text):
        self.text = text