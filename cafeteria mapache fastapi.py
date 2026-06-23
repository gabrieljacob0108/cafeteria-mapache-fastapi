import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["mapache"]
coleccion_ventas = db["cafeteria"]
coleccion_tokens = db["tokens"]

app = FastAPI()
carrito = []
saldo_mapache = 100000
total_cuenta = 0
lleva_sorpresa_mapache = False
lleva_cola_anillada = False

class Orden(BaseModel):
    id: int
    nombre_cliente: Optional[str] = "anonimo"

bebidas = [
    {"id": 1, "nombre": "cafe sencillo", "precio": 2200, "categoria": "bebida"},
    {"id": 2, "nombre": "cafe con leche", "precio": 2500, "categoria": "bebida"},
    {"id": 3, "nombre": "capuccino", "precio": 3200, "categoria": "bebida"},
    {"id": 4, "nombre": "chocolate caliente", "precio": 2500, "categoria": "bebida"},
    {"id": 5, "nombre": "sorpresa mapache", "precio": 18500, "categoria": "bebida"},
    {"id": 6, "nombre": "te helado", "precio": 7500, "categoria": "bebida"},
    {"id": 7, "nombre": "chocolate con malvadiscos", "precio": 10000, "categoria": "bebida"},
    {"id": 8, "nombre": "botella de agua", "precio": 1500, "categoria": "bebida"},
    {"id": 9, "nombre": "yogurt", "precio": 3000, "categoria": "bebida"},
    {"id": 10, "nombre": "expreso", "precio": 3500, "categoria": "bebida"}
]

postres = [
    {"id": 11, "nombre": "pastel red velvet", "precio": 20000, "categoria": "postre"},
    {"id": 12, "nombre": "pastel de limon", "precio": 15000, "categoria": "postre"},
    {"id": 13, "nombre": "pastel de cafe", "precio": 1200, "categoria": "postre"},
    {"id": 14, "nombre": "pastel de chocolate", "precio": 35000, "categoria": "postre"},
    {"id": 15, "nombre": "3 galletas de red velvet", "precio": 25000, "categoria": "postre"},
    {"id": 16, "nombre": "pastel de vainilla", "precio": 22000, "categoria": "postre"},
    {"id": 17, "nombre": "3 galletas de chocolate", "precio": 20000, "categoria": "postre"},
    {"id": 18, "nombre": "3 galletas de chispas", "precio": 15000, "categoria": "postre"},
    {"id": 19, "nombre": "postre de cola anillada", "precio": 30000, "categoria": "postre"},
    {"id": 20, "nombre": "milhoja", "precio": 4500, "categoria": "postre"}
]

menu_completo = bebidas + postres

@app.get("/menu")
def obtener_menu():
    return {"bebidas": bebidas, "postres": postres}

@app.get("/carrito")
def ver_carrito():
    return {"carrito": carrito, "total": sum(i["precio"] for i in carrito)}

@app.post("/ordenar")
def ordenar(orden: Orden):
    for eleccion in menu_completo:
        if eleccion["id"] == orden.id:
            carrito.append(eleccion)
            return {"mensaje": "orden agregada", "producto": eleccion, "carrito": carrito}
    raise HTTPException(status_code=404, detail="Eleccion no encontrada")

class Pago(BaseModel):
    nombre_cliente: Optional[str] = "anonimo"
    dinero_ingresado: int

@app.post("/pagar")
def pagar(pago: Pago):
    global saldo_mapache, total_cuenta, lleva_sorpresa_mapache, lleva_cola_anillada

    if not carrito:
        raise HTTPException(status_code=400, detail="Carrito vacío")

    total_carrito = sum(item["precio"] for item in carrito)

    if pago.dinero_ingresado < total_carrito:
        raise HTTPException(
            status_code=400, 
            detail= f"Dinero insuficiente. Total: {total_carrito}, Ingresado: {pago.dinero_ingresado}"
        )

    cambio = pago.dinero_ingresado - total_carrito
    nombre_limpio = pago.nombre_cliente.strip().lower()
    
    for eleccion in carrito:
        saldo_mapache += eleccion["precio"]
        total_cuenta += eleccion["precio"]
        
        if eleccion["nombre"] == "sorpresa mapache":
            lleva_sorpresa_mapache = True
        if eleccion["nombre"] == "postre de cola anillada":
            lleva_cola_anillada = True

        coleccion_ventas.insert_one({
            "cliente": nombre_limpio,
            "producto": eleccion["nombre"],
            "precio": eleccion["precio"],
            "categoria": eleccion["categoria"]
        })

    cliente = coleccion_tokens.find_one({"nombre": nombre_limpio})
    if cliente:
        coleccion_tokens.update_one(
            {"nombre": nombre_limpio},
            {"$inc": {"tokens": 1}}
        )
        tokens_actuales = coleccion_tokens.find_one({"nombre": nombre_limpio})["tokens"]
    else:
        coleccion_tokens.insert_one({"nombre": nombre_limpio, "tokens": 1})
        tokens_actuales = 1

    premio = "Sigue acumulando 🦝"
    if tokens_actuales >= 20:
        premio = "¡PELUCHE MAPACHE! 🦝"
        coleccion_tokens.update_one({"nombre": nombre_limpio}, {"$set": {"tokens": 0}})
        tokens_actuales = 0
    elif tokens_actuales >= 10:
        premio = "¡5% descuento!"
    elif tokens_actuales >= 5:
        premio = "¡Postre gratis!"

    carrito.clear()

    return {
        "mensaje": "pago realizado exitosamente",
        "total_cuenta": total_carrito,
        "dinero_recibido": pago.dinero_ingresado,
        "cambio_devuelto": cambio,
        "saldo_cafeteria": saldo_mapache,
        "total_historico_pagado": total_cuenta,
        "nombre_cliente": nombre_limpio,
        "tokens_mapache": tokens_actuales,
        "premio": premio
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
