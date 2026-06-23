from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, FastAPI!"}
@app.get("/pregunta")
async def pregunta():
    return {"message": "esto es una pregunta?"}

@app.get("/pasteles")
async def obtener_pasteles():
    return [
        {"nombre": "chocolate", "precio": 15000},
        {"nombre": "vainilla", "precio": 12000},
        {"nombre": "red velvet", "precio": 18000}
    ]

