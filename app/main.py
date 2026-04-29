# Define una instancia app = FastAPI() y una ruta básica
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}