from fastapi import APIRouter, HTTPException
from .models import Command, DrinkInstructions
from agents.ollama_agent import OllamaAgent

router = APIRouter()
ollama_agent = OllamaAgent()

@router.get("/drinks/{drink_name}", response_model=DrinkInstructions)
async def get_drink_instructions(drink_name: str):
    try:
        # Aquí el agente de IA generaría las instrucciones para preparar la bebida
        instructions = ollama_agent.generate_drink_instructions(drink_name)
        return instructions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/commands")
async def process_command(command: Command):
    try:
        # El agente procesa el comando en lenguaje natural
        result = ollama_agent.process_command(command.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))