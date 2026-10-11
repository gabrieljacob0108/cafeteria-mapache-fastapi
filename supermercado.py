import os
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)
db = client["tienda"]
coleccion = db["supermercado"]
saldo_col = db["saldo_supermercado"]

def cargar_datos():
    productos = list(coleccion.find({}))
    saldo_doc = saldo_col.find_one({"config": "contabilidad"})
    saldo = saldo_doc["saldo"] if saldo_doc else 100000
    return {"productos": productos, "saldo": saldo} if productos else None

def guardar_datos_iniciales(saldo, productos):
    coleccion.insert_many(productos)
    saldo_col.update_one(
        {"config": "contabilidad"},
        {"$set": {"saldo": saldo}},
        upsert=True
    )

def sincronizar_inventario_y_saldo(saldo, productos):
    operaciones = [
        UpdateOne({"nombre": p["nombre"]}, {"$set": {"stock": p["stock"], "precio": p["precio"]}}, upsert=True)
        for p in productos
    ]
    if operaciones:
        coleccion.bulk_write(operaciones)
    
    saldo_col.update_one(
        {"config": "contabilidad"},
        {"$set": {"saldo": saldo}},
        upsert=True
    )

datos_existentes = cargar_datos()

if datos_existentes:
    productos_lista = datos_existentes["productos"]
    saldo_tienda = datos_existentes["saldo"]
else:
    saldo_tienda = 100000
    productos_lista = [
        {"nombre": "bolsa de papas*12", "precio": 20000, "stock": 30},
        {"nombre": "caja de jugo*12", "precio": 18000, "stock": 19},
        {"nombre": "harina*16", "precio": 15000, "stock": 16},
        {"nombre": "cafe molido*10", "precio": 14500, "stock": 10},
        {"nombre": "aceite*15", "precio": 12000, "stock": 22},
        {"nombre": "pastillas de panela*30", "precio": 12000, "stock": 23},
        {"nombre": "pastillas de chocolate*30", "precio": 32500, "stock": 18},
        {"nombre": "botellas de agua*16", "precio": 10000, "stock": 20},
        {"nombre": "pan de molde*12", "precio": 11500, "stock": 12},
        {"nombre": "arroz 1kg*20", "precio": 50800, "stock": 40},
        {"nombre": "galletas de soda*6paquetes", "precio": 10500, "stock": 21},
        {"nombre": "leche entera*8", "precio": 20200, "stock": 30},
    ]
    guardar_datos_iniciales(saldo_tienda, productos_lista)

pago_comprador = 0
carrito = []
total_cuenta = 0

variantes = {
    "leche entera*8": [
        {"nombre": "leche entera*8", "precio": 20200},
        {"nombre": "leche con chocolate*8", "precio": 22000},
        {"nombre": "leche deslactosada*8", "precio": 25000},
    ],
    "caja de jugo*12": [
        {"nombre": "jugo de naranja*12", "precio": 18000},
        {"nombre": "jugo de manzana*12", "precio": 18000},
        {"nombre": "jugo de mango*12", "precio": 18000},
        {"nombre": "jugo de mora*12", "precio": 18000},
        {"nombre": "jugo de pera*12", "precio": 18000},
        {"nombre": "jugo de arandano*12", "precio": 20000},
    ],
}

def mostrar_menu():
    for i, p in enumerate(productos_lista, 1):
        print(f"{i} {p['nombre']} {p['precio']} {p['stock']}")

def condiciones(saldo_tienda, pago_comprador, carrito, total_cuenta, productos_lista):
    while True:
        mostrar_menu()
        try:
            eleccion = input().strip().lower()
            if eleccion == 'no':
                break
                
            indices = {str(i + 1): i for i in range(len(productos_lista))}

            if eleccion in indices:
                idx = indices[eleccion]
                prod_original = productos_lista[idx]
                prod_actual = prod_original.copy()

                if prod_original["nombre"] in variantes:
                    opciones = variantes[prod_original["nombre"]]
                    for i, v in enumerate(opciones, 1):
                        print(f"{i} {v['nombre']} {v['precio']}")

                    try:
                        eleccion_variante = int(input().strip())
                        if 1 <= eleccion_variante <= len(opciones):
                            variante_elegida = opciones[eleccion_variante - 1]
                            prod_actual["nombre"] = variante_elegida["nombre"]
                            prod_actual["precio"] = variante_elegida["precio"]
                    except ValueError:
                        pass

                if prod_original["stock"] <= 0:
                    continue

                cantidad_input = input().strip()
                cantidad = int(cantidad_input)

                if 0 < cantidad <= 4 and cantidad <= prod_original["stock"]:
                    productos_lista[idx]["stock"] -= cantidad
                    carrito.append(f"{cantidad}x {prod_actual['nombre']}")
                    total_cuenta += prod_actual["precio"] * cantidad

                    if productos_lista[idx]["stock"] < 5:
                        almacen = db["almacen"]
                        producto_almacen = almacen.find_one({"nombre": prod_original["nombre"]})
                        if producto_almacen and producto_almacen.get("stock", 0) > 10:
                            almacen.update_one(
                                {"nombre": prod_original["nombre"]},
                                {"$inc": {"stock": -10}}
                            )
                            productos_lista[idx]["stock"] += 10

            respuesta = input().strip().lower()
            if respuesta == "no":
                break
        except ValueError:
            pass

    if total_cuenta > 0:
        for item in carrito:
            print(f"{item}")
        
        while pago_comprador < total_cuenta:
            try:
                dinero_raw = input().strip().lower()
                if dinero_raw == "no":
                    return saldo_tienda
                dinero = int(dinero_raw)
                if dinero > 0:
                    pago_comprador += dinero
            except ValueError:
                pass

        saldo_tienda += total_cuenta

    return saldo_tienda

if __name__ == "__main__":
    saldo_tienda = condiciones(saldo_tienda, pago_comprador, carrito, total_cuenta, productos_lista)
    sincronizar_inventario_y_saldo(saldo_tienda, productos_lista)
