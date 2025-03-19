from fastapi import APIRouter, HTTPException
from .models import Command, DrinkInstructions, DrinkRequest, DrinkResponse, Ingredient
from agents.ollama_agent import OllamaAgent
from db.crud import get_all_motors, get_motor_by_device, update_motor_content, update_motor_level, reset_motor_level
from .models import Motor, MotorUpdate

router = APIRouter()
ollama_agent = OllamaAgent()

@router.post("/commands")
async def process_command(command: Command):
    try:
        # El agente procesa el comando en lenguaje natural
        result = ollama_agent.process_command(command.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/drink", response_model=DrinkResponse)
async def analyze_drink(request: DrinkRequest):
    try:
        # Extraer el nombre de la bebida del texto
        drink_text = request.text

        # Usar el agente para analizar la bebida
        result = ollama_agent.generate_drink_instructions(drink_text)

        # Ya no necesitamos convertir steps a ingredients, solo usar directamente
        return DrinkResponse(
            success=True,
            message="Bebida analizada correctamente",
            name=result["name"],
            description=result["description"],
            ingredients=result["ingredients"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/motors", response_model=list[Motor])
async def get_motors():
    """Obtiene todos los motores y su contenido"""
    try:
        motors = get_all_motors()
        return motors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/motors/{device}", response_model=Motor)
async def get_motor(device: str):
    """Obtiene un motor específico por su dispositivo (relay_one, relay_two, etc.)"""
    try:
        motor = get_motor_by_device(device)
        if not motor:
            raise HTTPException(status_code=404, detail=f"Motor con dispositivo {device} no encontrado")
        return motor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/motors/{device}", response_model=Motor)
async def update_motor(device: str, motor_data: MotorUpdate):
    """Actualiza el contenido de un motor"""
    try:
        success = update_motor_content(device, motor_data.content)
        if not success:
            raise HTTPException(status_code=404, detail=f"Motor con dispositivo {device} no encontrado")
        return get_motor_by_device(device)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/motors/{device}/refill")
async def refill_motor(device: str):
    """Rellena un motor a su capacidad máxima"""
    try:
        success = reset_motor_level(device)
        if not success:
            raise HTTPException(status_code=404, detail=f"Motor con dispositivo {device} no encontrado")
        return {"message": f"Motor {device} rellenado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
