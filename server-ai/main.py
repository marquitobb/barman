import uvicorn
from fastapi import FastAPI
from api.routes import router
from db.database import init_db
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Barman Brain API",
    description="API para controlar el barman robótico usando IA",
    version="0.1.4"
)

@app.get("/barman")
async def root():
    return {"message": "Welcome to the Barman Brain API!"}

# Inicializar la base de datos al arrancar la aplicación
@app.on_event("startup")
async def startup_db_client():
    # Inicializar la base de datos
    init_db()
    print("Base de datos inicializada")

app.include_router(router, prefix="/barman")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)