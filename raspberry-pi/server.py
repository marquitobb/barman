from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from controllers.motor_controller import MotorController

# models
from models import (
    MotorRequest,
    DrinkRequest,
    ApiResponse,
)

app = FastAPI(
    title="Barman Raspberry Pi API",
    description="API para controlar motores y relés GPIO en la Raspberry Pi",
    version="1.0.0"
)

# Inicializar controladores
motor_controller = MotorController()


@app.get("/")
async def root():
    return {"message": "Barman Raspberry Pi API activa"}

@app.post("/motors/activate", response_model=ApiResponse)
async def activate_motor(request: MotorRequest):
    """Activa un motor específico por un tiempo determinado"""
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
    """Prepara una bebida según los ingredientes recibidos"""
    try:
        success = motor_controller.process_drink_request({
            "ingredients": request.ingredients
        })

        if success:
            return {
                "success": True,
                "message": "Bebida preparada correctamente"
            }
        else:
            return {
                "success": False,
                "message": "Error al preparar la bebida"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

