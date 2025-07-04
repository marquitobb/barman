from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import json
import os
from db.crud import get_all_motors, get_motor_by_device

class OllamaAgent:
    def __init__(self, model="gemma3"):
        self.llm = Ollama(model=model)
        # Cargar base de conocimiento de recetas
        self.recipes_data = self._load_recipe_knowledge()

    def _load_recipe_knowledge(self):
        """Carga el archivo JSON con las recetas base"""
        try:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   "data", "drink_recipes.json")
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando recetas: {e}")
            # Devolver un diccionario vacío si hay error
            return {"base_drinks": {}}

    def generate_drink_instructions(self, drink_name: str):
        """Genera instrucciones para preparar una bebida usando Ollama y base de conocimiento."""
        # Obtenemos los motores disponibles de la base de datos
        available_motors = get_all_motors()

        # Creamos una lista de ingredientes disponibles para el prompt
        available_ingredients = []
        for motor in available_motors:
            available_ingredients.append(f"{motor['content']} (device: {motor['device']})")

        ingredients_text = "\n- ".join(available_ingredients)

        # Convertir recetas base a formato texto para el prompt
        recipes_text = json.dumps(self.recipes_data, indent=2, ensure_ascii=False)

        prompt = PromptTemplate(
            input_variables=["drink_name", "ingredients", "recipes"],
            template="""Genera instrucciones detalladas para preparar un {drink_name} usando los siguientes ingredientes disponibles:
            - {ingredients}

            Usa como referencia esta base de conocimiento de recetas:
            {recipes}

            Si el usuario pidió una bebida que está en la base de conocimiento:
            1. IMPORTANTE: Usa ÚNICAMENTE los ingredientes disponibles en la lista de arriba
            2. NO sustituyas ingredientes no disponibles por otros diferentes
            3. Si un ingrediente no está disponible, simplemente omítelo y ajusta los porcentajes
            4. Los porcentajes deben sumar siempre 100%
            5. Si llegan a pedir la bebida cargada ya sea de tequila o whisky, se debe ajustar el porcentaje de soda para que sume 100% pero con mayor cantidad de tequila o whisky

            Si la bebida no está en la base de conocimiento, usa la receta más similar como referencia siguiendo las mismas reglas.

            Las instrucciones deben estar en formato JSON y seguir esta estructura:
            {{
                "name": "Nombre de la bebida",
                "description": "Descripción breve (menciona si es una versión adaptada por falta de ingredientes)",
                "ingredients": [
                    {{"name": "Tequila", "percentage": 40.0, "device": "relay_one"}},
                    {{"name": "Limón", "percentage": 20.0, "device": "relay_two"}},
                    {{"name": "Soda (Squirt)", "percentage": 40.0, "device": "relay_three"}}
                ]
            }}

            Usa sólo los ingredientes exactamente como aparecen en la lista de arriba.
            Para cada ingrediente, asigna el dispositivo (device) correcto según la lista anterior.
            """
        )

        result = self.llm.invoke(prompt.format(
            drink_name=drink_name,
            ingredients=ingredients_text,
            recipes=recipes_text
        ))

        # Extraer el JSON de la respuesta
        try:
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            json_str = result[json_start:json_end]
            print("response json------------------>")
            print(json_str)
            return json.loads(json_str)
        except:
            # Fallback en caso de error
            return {
                "name": drink_name,
                "description": f"Receta para {drink_name}",
                "ingredients": [
                    {"name": available_motors[0]['content'], "percentage": 40.0, "device": available_motors[0]['device']},
                    {"name": available_motors[1]['content'], "percentage": 20.0, "device": available_motors[1]['device']},
                ]
            }

    def process_command(self, command_text: str):
        """Procesa un comando en lenguaje natural."""
        # Obtenemos los motores disponibles de la base de datos
        available_motors = get_all_motors()
        
        # Creamos una lista de ingredientes disponibles para el prompt
        available_ingredients = []
        for motor in available_motors:
            available_ingredients.append(f"{motor['content']} (device: {motor['device']})")
        
        ingredients_text = "\n- ".join(available_ingredients)
        
        prompt = f"""
        Como asistente de barman, interpreta el siguiente comando:
        "{command_text}"
        
        Los ingredientes disponibles son:
        - {ingredients_text}
        
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