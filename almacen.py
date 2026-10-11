import os
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["tienda"]
coleccion = db["almacen"]

def cargar_existencias():
    return list(coleccion.find({}))

def verificar_y_recargar_automatico(producto):
    UMBRAL_MINIMO = 4
    CANTIDAD_RECARGA = 15

    if producto["stock"] <= UMBRAL_MINIMO:
        producto["stock"] += CANTIDAD_RECARGA
        coleccion.update_one(
            {"_id": producto["_id"]},
            {"$set": {"stock": producto["stock"]}}
        )

def actualizar_un_solo_producto(producto):
    coleccion.update_one(
        {"_id": producto["_id"]},
        {"$set": {"stock": producto["stock"]}}
    )

def pedir_cantidad(mensaje):
    try:
        cantidad = int(input().strip())
        if cantidad <= 0:
            return None
        return cantidad
    except ValueError:
        return None

def gestionar_almacen():
    productos = cargar_existencias()

    if not productos:
        inventario_inicial = [
            {"nombre": "Papas", "stock": 28000, "categoria": "maquina"},
            {"nombre": "Gaseosa", "stock": 20000, "categoria": "maquina"},
            {"nombre": "Caramelos", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Chocolate", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Galletas", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Jugo", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Agua", "stock": 30000, "categoria": "maquina"},
            {"nombre": "bolsa de papas*12", "stock": 30000, "categoria": "supermercado"},
            {"nombre": "caja de jugo*12", "stock": 20000, "categoria": "supermercado"},
            {"nombre": "harina*16", "stock": 20000, "categoria": "supermercado"},
            {"nombre": "cafe molido*10", "stock": 20000, "categoria": "supermercado"},
            {"nombre": "aceite*15", "stock": 22000, "categoria": "supermercado"},
            {"nombre": "pastillas de panela*30", "stock": 23000, "categoria": "supermercado"},
            {"nombre": "pastillas de chocolate*30", "stock": 20000, "categoria": "supermercado"},
            {"nombre": "botellas de agua*16", "stock": 20000, "categoria": "supermercado"},
            {"nombre": "pan de molde*12", "stock": 22000, "categoria": "supermercado"},
            {"nombre": "arroz 1kg*20", "stock": 40000, "categoria": "supermercado"},
            {"nombre": "galletas de soda*6paquetes", "stock": 21000, "categoria": "supermercado"},
            {"nombre": "leche entera*8", "stock": 30000, "categoria": "supermercado"},
            {"nombre": "empaques de brownie*15", "stock": 15000, "categoria": "supermercado"},
            {"nombre": "galletas de red velvet", "stock": 30000, "categoria": "supermercado"},
            {"nombre": "postres de red velvet", "stock": 20000, "categoria": "supermercado"},
        ]
        coleccion.insert_many(inventario_inicial)
        productos = cargar_existencias()

    indices = {str(i + 1): i for i in range(len(productos))}

    while True:
        for k, idx in indices.items():
            prod = productos[idx]
            if prod["categoria"] == "supermercado":
                print(f"{k} {prod['stock']}")

        for k, idx in indices.items():
            prod = productos[idx]
            if prod["categoria"] == "maquina":
                print(f"{k} {prod['stock']}")

        opcion = input().strip()

        if opcion == "3":
            return

        if opcion not in ["1", "2"]:
            continue

        eleccion = input().strip()

        if eleccion not in indices:
            continue

        prod = productos[indices[eleccion]]

        if opcion == "1":
            if prod["stock"] <= 0:
                continue

            cantidad = pedir_cantidad("")
            if cantidad is None:
                continue

            if cantidad <= prod["stock"]:
                prod["stock"] -= cantidad
                actualizar_un_solo_producto(prod)
                verificar_y_recargar_automatico(prod)

        elif opcion == "2":
            cantidad = pedir_cantidad("")
            if cantidad is None:
                continue

            prod["stock"] += cantidad
            actualizar_un_solo_producto(prod)

        continuar = input().strip().lower()
        if continuar != "si":
            return

if __name__ == "__main__":
    gestionar_almacen()
