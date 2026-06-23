import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)
db = client["tienda"]
coleccion = db["supermercado"]
saldo_col = db["saldo_supermercado"]


def cargar_datos():
    productos = list(coleccion.find({}, {"_id": 0}))
    saldo_doc = saldo_col.find_one({}, {"_id": 0})
    saldo = saldo_doc["saldo"] if saldo_doc else 100000
    return {"productos": productos, "saldo": saldo} if productos else None


def guardar_datos(saldo, productos):
    coleccion.delete_many({})
    coleccion.insert_many(productos)
    saldo_col.delete_many({})
    saldo_col.insert_one({"saldo": saldo})


datos_viejos = cargar_datos()

if datos_viejos:
    productos_lista = datos_viejos["productos"]
    saldo_tienda = datos_viejos["saldo"]
    print("¡Bienvenido de nuevo!")
else:
    saldo_tienda = 100000
    productos_lista = [...]
    guardar_datos(saldo_tienda, productos_lista)

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
    guardar_datos(saldo_tienda, productos_lista)
    print("¡Bienvenido de nuevo! ")

print("bienvenido a tiendas gabriel amigo!")
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
    print("\n--- MENÚ DE PRODUCTOS ---")
    for i, p in enumerate(productos_lista, 1):
        print(f"{i}. {p['nombre']} - ${p['precio']} (Stock: {p['stock']})")


def condiciones(
    saldo_tienda, pago_comprador, carrito, total_cuenta, productos_lista
):
    while True:
        mostrar_menu()
        try:
            eleccion = input("\nEscoge un numero: ").strip().lower()
            indices = {str(i + 1): i for i in range(len(productos_lista))}

            if eleccion in indices:
                idx = indices[eleccion]
                prod = productos_lista[idx]

                if prod["nombre"] in variantes:
                    print(f"\n¿Qué tipo de {prod['nombre']} quieres?")
                    opciones = variantes[prod["nombre"]]
                    for i, v in enumerate(opciones, 1):
                        print(f"{i}. {v['nombre']} - ${v['precio']}")

                    try:
                        eleccion_variante = int(
                            input("Escoge una opción: ").strip()
                        )
                        if 1 <= eleccion_variante <= len(opciones):
                            variante_elegida = opciones[eleccion_variante - 1]
                            prod = {
                                "nombre": variante_elegida["nombre"],
                                "precio": variante_elegida["precio"],
                                "stock": prod["stock"],
                            }
                        else:
                            print(
                                "Opción inválida, se agrega la versión normal."
                            )
                    except ValueError:
                        print("Dato inválido, se agrega la versión normal.")

                if prod["stock"] <= 0:
                    print("Sin stock")
                    continue

                cantidad_input = (
                    input(f"¿Cuántos de {prod['nombre']} necesitas? (Max 4): ")
                    .strip()
                    .lower()
                )
                cantidad = int(cantidad_input)

                if 0 < cantidad <= 4 and cantidad <= prod["stock"]:
                    productos_lista[idx]["stock"] -= cantidad
                    carrito.append(f"{cantidad}x {prod['nombre']}")
                    total_cuenta += prod["precio"] * cantidad
                    print(f"Agregaste {cantidad} de {prod['nombre']}")

                    if productos_lista[idx]["stock"] < 5:
                        almacen = db["almacen"]
                        producto_almacen = almacen.find_one(
                            {"nombre": productos_lista[idx]["nombre"]}
                        )
                        if producto_almacen and producto_almacen["stock"] > 10:
                            almacen.update_one(
                                {"nombre": productos_lista[idx]["nombre"]},
                                {"$inc": {"stock": -10}},
                            )
                            productos_lista[idx]["stock"] += 10
                            print(
                                f" ¡Stock bajo! El almacén recargó 10 unidades de {productos_lista[idx]['nombre']}"
                            )
                else:
                    print("Cantidad inválida o supera el stock/límite.")
            else:
                print("Opción no válida.")

            respuesta = input("¿Seguir comprando? (si/no): ").strip().lower()
            if respuesta == "no":
                break
            elif respuesta != "si":
                print("Respuesta inválida, escribe 'si' o 'no'")
                break
        except ValueError:
            print("Dato inválido.")

    if total_cuenta > 0:
        print(f"\nTotal a pagar: ${total_cuenta}")
        while pago_comprador < total_cuenta:
            try:
                dinero_raw = (
                    input(
                        f"Faltan ${total_cuenta - pago_comprador}. Ingresa dinero: "
                    )
                    .strip()
                    .lower()
                )
                if dinero_raw == "no":
                    break
                dinero = int(dinero_raw)
                if dinero > 0:
                    pago_comprador += dinero
                else:
                    print("Monto inválido.")
            except ValueError:
                print("Dato inválido.")

        cambio = pago_comprador - total_cuenta
        saldo_tienda += pago_comprador
        saldo_tienda -= cambio
        print(f"\nTu cambio: ${cambio}")

    return saldo_tienda


saldo_tienda = condiciones(
    saldo_tienda, pago_comprador, carrito, total_cuenta, productos_lista
)
guardar_datos(saldo_tienda, productos_lista)

print(f"Saldo final tienda: ${saldo_tienda}")
print("¡Datos guardados! Gracias por su compra.")
