import uvicorn
from fastapi import FastAPI
from api.routes import router
from db.database import init_db
import threading
import os
from dotenv import load_dotenv
from telegram_api import TelegramBot

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Barman Brain API",
    description="API para controlar el barman robótico usando IA",
    version="0.1.4"
)

telegram_bot = None

@app.get("/barman")
async def root():
    return {"message": "Welcome to the Barman Brain API!"}

# Inicializar la base de datos al arrancar la aplicación
@app.on_event("startup")
async def startup_db_client():
    # Inicializar la base de datos
    init_db()
    print("Base de datos inicializada")

    # Inicializar el bot de Telegram si el token está presente
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        try:

            global telegram_bot
            telegram_bot = TelegramBot()

            # Iniciar el bot en un hilo separado
            bot_thread = threading.Thread(target=telegram_bot.start)
            bot_thread.daemon = True
            bot_thread.start()

            print("Bot de Telegram iniciado en un hilo separado")
        except Exception as e:
            print(f"Error al iniciar el bot de Telegram: {e}")
    else:
        print("No se encontró el token de Telegram. El bot no se iniciará.")

# Detener el bot de Telegram al cerrar la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    global telegram_bot
    if telegram_bot:
        telegram_bot.stop()
        print("Bot de Telegram detenido")

app.include_router(router, prefix="/barman")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)