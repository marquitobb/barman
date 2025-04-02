import uvicorn
import sys
from server import app

def main():
    # Verificar si se desea un modo específico
    api_port = 8080
    api_host = "0.0.0.0"
    
    # Comprobar si se especificó un puerto diferente
    if "--port" in sys.argv:
        try:
            port_index = sys.argv.index("--port") + 1
            api_port = int(sys.argv[port_index])
        except (ValueError, IndexError):
            print("Error al especificar el puerto. Usando puerto por defecto 8080.")
    
    print(f"Iniciando API REST en {api_host}:{api_port}...")
    print("Presiona Ctrl+C para detener el servidor.")
    
    # Iniciar el servidor FastAPI
    uvicorn.run(app, host=api_host, port=api_port)

# Punto de entrada principal
if __name__ == "__main__":
    main()