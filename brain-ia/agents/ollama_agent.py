from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import json

class OllamaAgent:
    def __init__(self, model="llama3.2"):
        self.llm = Ollama(model=model)
        
    def generate_drink_instructions(self, drink_name: str):
        """Genera instrucciones para preparar una bebida usando Ollama."""
        prompt = PromptTemplate(
            input_variables=["drink_name"],
            template="""Genera instrucciones detalladas para preparar un {drink_name}.
            Las instrucciones deben estar en formato JSON y seguir esta estructura:
            {{
                "name": "Nombre de la bebida",
                "description": "Descripción breve",
                "steps": [
                    {{"device": "relay_one", "duration": 2.5, "description": "Agregar 50ml de ron"}},
                    {{"device": "relay_two", "duration": 1.0, "description": "Agregar 25ml de limón"}}
                ]
            }}
            """
        )

        result = self.llm.invoke(prompt.format(drink_name=drink_name))

        # Extraer el JSON de la respuesta
        try:
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            json_str = result[json_start:json_end]
            return json.loads(json_str)
        except:
            # Fallback en caso de error
            return {
                "name": drink_name,
                "description": f"Receta para {drink_name}",
                "steps": [
                    {"device": "relay_one", "duration": 3.0, "description": "Ingrediente principal"},
                    {"device": "relay_two", "duration": 2.0, "description": "Mezclador"}
                ]
            }
    
    def process_command(self, command_text: str):
        """Procesa un comando en lenguaje natural."""
        prompt = f"""
        Como asistente de barman, interpreta el siguiente comando:
        "{command_text}"
        
        Responde con un JSON que incluya la acción a realizar.
        """
        
        result = self.llm.invoke(prompt)
        
        # Similar a la función anterior, extraer el JSON
        try:
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            json_str = result[json_start:json_end]
            return json.loads(json_str)
        except:
            return {"action": "unknown", "message": "No pude entender el comando"}