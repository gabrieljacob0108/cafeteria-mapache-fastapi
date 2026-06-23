from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

cliente_mongo = MongoClient("mongodb://localhost:27017/")
db = cliente_mongo["sistema_tokens"]

coleccion_tokens = db["clientes"]
coleccion_historial = db["historial_canjes"]

class Cliente(BaseModel):
    nombre: str

class Canjeo(BaseModel):
    nombre: str
    tokens_a_canjear: int

@app.post("/cliente")
def crear_cliente(cliente: Cliente):
    existe = coleccion_tokens.find_one({"nombre": cliente.nombre})
    if existe:
        raise HTTPException(status_code=400, detail="Cliente ya existe")
    
    coleccion_tokens.insert_one({"nombre": cliente.nombre, "tokens": 100})
    return {"mensaje": f"Cliente {cliente.nombre} registrado", "tokens": 100}

@app.get("/tokens/{nombre}")
def ver_tokens(nombre: str):
    cliente = coleccion_tokens.find_one({"nombre": nombre}, {"_id": 0})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.get("/clientes")
def ver_clientes():
    clientes = list(coleccion_tokens.find({}, {"_id": 0}))
    return {"clientes": clientes} 

@app.post("/canjear")
def canjear_tokens(canje: Canjeo):
    cliente = coleccion_tokens.find_one({"nombre": canje.nombre})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    if cliente["tokens"] < canje.tokens_a_canjear:
        raise HTTPException(status_code=400, detail=f"Tokens insuficientes. Tienes: {cliente['tokens']}")
    
    nuevos_tokens = cliente["tokens"] - canje.tokens_a_canjear
    coleccion_tokens.update_one({"nombre": canje.nombre}, {"$set": {"tokens": nuevos_tokens}})
    
    registro_historial = {
        "nombre": canje.nombre,
        "tokens_canjeados": canje.tokens_a_canjear,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    coleccion_historial.insert_one(registro_historial)
    
    return {
        "mensaje": "Canje exitoso", 
        "tokens_restantes": nuevos_tokens
    }

@app.get("/historial")
def ver_historial(nombre: Optional[str] = None):
    filtro = {"nombre": nombre} if nombre else {}
    historial = list(coleccion_historial.find(filtro, {"_id": 0}))
    return {"historial": historial}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
