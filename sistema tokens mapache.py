from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["mapache"]

coleccion_tokens = db["tokens"]
coleccion_historial = db["historial_canjes"]

app = FastAPI()

class Cliente(BaseModel):
    nombre: str

class Canjeo(BaseModel):
    nombre: str
    tokens_a_canjear: int

@app.post("/cliente")
def crear_cliente(cliente: Cliente):
    nombre_limpio = cliente.nombre.strip().lower()
    
    existe = coleccion_tokens.find_one({"nombre": nombre_limpio})
    if existe:
        raise HTTPException(status_code=400, detail="Cliente ya existe")
    coleccion_tokens.insert_one({"nombre": nombre_limpio, "tokens": 0})
    return {"mensaje": f"Cliente {nombre_limpio} registrado", "tokens": 0}

@app.get("/tokens/{nombre}")
def ver_tokens(nombre: str):
    nombre_limpio = nombre.strip().lower()
    
    cliente = coleccion_tokens.find_one({"nombre": nombre_limpio}, {"_id": 0})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    tokens = cliente["tokens"]
    premio = "Sigue acumulando 🦝"
    if tokens >= 20:
        premio = "¡PELUCHE MAPACHE! 🦝"
    elif tokens >= 10:
        premio = "¡5% descuento!"
    elif tokens >= 5:
        premio = "¡Postre gratis!"
    
    return {"cliente": nombre_limpio, "tokens": tokens, "premio_disponible": premio}

@app.get("/clientes")
def ver_clientes():
    clientes = list(coleccion_tokens.find({}, {"_id": 0}))
    return {"clientes": clientes}

@app.post("/canjear")
def canjear_tokens(canje: Canjeo):
    nombre_limpio = canje.nombre.strip().lower()
    
    cliente = coleccion_tokens.find_one({"nombre": nombre_limpio})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if cliente["tokens"] < canje.tokens_a_canjear:
        raise HTTPException(status_code=400, detail=f"Tokens insuficientes. Tienes: {cliente['tokens']}")
    
    nuevos_tokens = cliente["tokens"] - canje.tokens_a_canjear
    coleccion_tokens.update_one(
        {"nombre": nombre_limpio},
        {"$inc": {"tokens": -canje.tokens_a_canjear}}
    )
    coleccion_historial.insert_one({
        "nombre": nombre_limpio,
        "tokens_canjeados": canje.tokens_a_canjear,
        "fecha": datetime.now()
    })
    return {"mensaje": "Canje exitoso", "tokens_restantes": nuevos_tokens}

@app.get("/historial")
def ver_historial(nombre: Optional[str] = None):
    filtro = {"nombre": nombre.strip().lower()} if nombre else {}
    historial = list(coleccion_historial.find(filtro, {"_id": 0}))
    return {"historial": historial}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
