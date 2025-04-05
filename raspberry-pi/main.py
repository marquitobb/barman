from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
from controllers.motor_controller import MotorController

# models
from models import (
    MotorRequest,
    DrinkRequest,
    ApiResponse,
)

# Create FastAPI application
app = FastAPI(
    title="Barman Raspberry Pi API",
    description="API para controlar motores y relés GPIO en la Raspberry Pi",
    version="1.0.0"
)

# Initialize controllers
motor_controller = MotorController()


@app.get("/")
async def root():
    return {"message": "Barman Raspberry Pi API activa"}


@app.post("/motors/activate", response_model=ApiResponse)
async def activate_motor(request: MotorRequest):
    """Activates a specific motor for a determined time"""
    try:
        motor_controller.activate_motor(request.device, request.duration)
        return {
            "success": True,
            "message": f"Motor {request.device} activado por {request.duration} segundos"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/drink", response_model=ApiResponse)
async def make_drink(request: DrinkRequest):
    """Prepares a drink according to the received ingredients"""
    try:
        success = motor_controller.process_drink_request({
            "ingredients": request.ingredients
        })
        if success:
            return {
                "success": True,
                "message": "Bebida preparada correctamente"
            }
        return {
            "success": False,
            "message": "Error al preparar la bebida"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    # Check if a specific mode is desired
    api_port = 8080
    api_host = "0.0.0.0"

    # Check if a different port was specified
    if "--port" in sys.argv:
        try:
            port_index = sys.argv.index("--port") + 1
            api_port = int(sys.argv[port_index])
        except (ValueError, IndexError):
            print("Error al especificar el puerto. Usando puerto por defecto 8080.")

    print(f"Iniciando API REST en {api_host}:{api_port}...")
    print("Presiona Ctrl+C para detener el servidor.")

    # Start FastAPI server
    uvicorn.run(app, host=api_host, port=api_port)


# Main entry point
if __name__ == "__main__":
    main()