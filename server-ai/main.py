import uvicorn
from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Barman Brain API",
    description="API para controlar el barman robótico usando IA",
    version="0.1.3"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)