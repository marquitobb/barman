from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
import os
import threading
from controllers.motor_controller import MotorController
from dotenv import load_dotenv
from telegram_api.bot import TelegramBot
from contextlib import asynccontextmanager

# models
from models import (
    MotorRequest,
    DrinkRequest,
    ApiResponse,
)

# Cargar variables de entorno
load_dotenv()

@asynccontextmanager
async def lifespan(app):
    # Código que se ejecutaba en startup_event
    global telegram_bot
    try:
        telegram_bot = TelegramBot()
        bot_thread = threading.Thread(target=telegram_bot.start)
        bot_thread.daemon = True
        bot_thread.start()
        print("Bot de Telegram iniciado correctamente")
    except Exception as e:
        print(f"Error al iniciar el bot de Telegram: {e}")
    
    yield  # Aquí la aplicación se ejecuta
    
    # Código que se ejecutaba en shutdown_event
    if telegram_bot:
        telegram_bot.stop()
        print("Bot de Telegram detenido")

# Create FastAPI application
app = FastAPI(
    title="Barman Raspberry Pi API",
    description="API para controlar motores y relés GPIO en la Raspberry Pi",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize controllers
motor_controller = MotorController()
telegram_bot = None


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