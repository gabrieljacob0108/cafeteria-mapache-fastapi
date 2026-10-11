import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

db = client["mapache"]
coleccion_ventas = db["cafeteria"]
coleccion_tokens = db["tokens"]
saldo_col = db["saldo_cafeteria"] 

app = FastAPI(title="Cafetería Mapache API")

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

menu_dict = {item["id"]: item for item in (bebidas + postres)}

class ContenidoPago(BaseModel):
    nombre_cliente: Optional[str] = ""
    productos_ids: List[int] = Field(..., min_length=1)
    dinero_ingresado: int

@app.get("/menu")
def obtener_menu():
    return {"bebidas": bebidas, "postres": postres}

@app.post("/pagar", status_code=status.HTTP_200_OK)
def pagar(pago: ContenidoPago):
    nombre_limpio = pago.nombre_cliente.strip().lower()
    
    items_a_comprar = []
    total_carrito = 0
    
    for pid in pago.productos_ids:
        if pid not in menu_dict:
            raise HTTPException(status_code=404)
        producto = menu_dict[pid]
        items_a_comprar.append(producto)
        total_carrito += producto["precio"]

    datos_cliente = coleccion_tokens.find_one({"nombre": nombre_limpio})
    tokens_previos = datos_cliente["tokens"] if datos_cliente else 0
    
    aplicó_descuento = False
    if 10 <= tokens_previos < 20:
        total_carrito = int(total_carrito * 0.95)
        aplicó_descuento = True

    if pago.dinero_ingresado < total_carrito:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    ventas_db = []
    for eleccion in items_a_comprar:
        ventas_db.append({
            "cliente": nombre_limpio,
            "producto": eleccion["nombre"],
            "precio": eleccion["precio"],
            "categoria": eleccion["categoria"]
        })
        
    if ventas_db:
        coleccion_ventas.insert_many(ventas_db)

    if tokens_previos >= 20:
        coleccion_tokens.update_one({"nombre": nombre_limpio}, {"$set": {"tokens": 1}}, upsert=True)
        tokens_actuales = 1
    else:
        coleccion_tokens.update_one({"nombre": nombre_limpio}, {"$inc": {"tokens": 1}}, upsert=True)
        tokens_actuales = tokens_previos + 1

    saldo_col.update_one({}, {"$inc": {"saldo_total_tienda": total_carrito}}, upsert=True)
    saldo_doc = saldo_col.find_one({})
    saldo_actual_tienda = saldo_doc.get("saldo_total_tienda", total_carrito) if saldo_doc else total_carrito

    return {
        "total_cuenta_cobrado": total_carrito,
        "descuento_aplicado": aplicó_descuento,
        "dinero_recibido": pago.dinero_ingresado,
        "cambio_devuelto": pago.dinero_ingresado - total_carrito,
        "saldo_historico_cafeteria": saldo_actual_tienda,
        "nombre_cliente": nombre_limpio,
        "tokens_mapache_actuales": tokens_actuales
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
