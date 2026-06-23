from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["tienda"]
coleccion = db["almacen"]


def cargar_existencias():
    productos = list(coleccion.find({}, {"_id": 0}))
    return productos if productos else None

def guardar_existencias(lista_productos):
    coleccion.delete_many({})
    coleccion.insert_many(lista_productos)

def pedir_cantidad(mensaje):
    try:
        cantidad = int(input(mensaje).strip())

        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0.")
            return None

        return cantidad

    except ValueError:
        print("Cantidad inválida. Ingresa un número.")
        return None


def gestionar_almacen():
    datos_guardados = cargar_existencias()

    if datos_guardados:
        productos = datos_guardados
        print("¡Datos del almacén cargados exitosamente!")
    else:
        productos = [
            # Máquina Expendedora
            {"nombre": "Papas", "stock": 28000, "categoria": "maquina"},
            {"nombre": "Gaseosa", "stock": 20000, "categoria": "maquina"},
            {"nombre": "Caramelos", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Chocolate", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Galletas", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Jugo", "stock": 30000, "categoria": "maquina"},
            {"nombre": "Agua", "stock": 30000, "categoria": "maquina"},
            # Supermercado
            {
                "nombre": "bolsa de papas*12",
                "stock": 30000,
                "categoria": "supermercado",
            },
            {
                "nombre": "caja de jugo*12",
                "stock": 20000,
                "categoria": "supermercado",
            },
            {
                "nombre": "harina*16",
                "stock": 20000,
                "categoria": "supermercado",
            },
            {
                "nombre": "cafe molido*10",
                "stock": 20000,
                "categoria": "supermercado",
            },
            {"nombre": "aceite*15", "stock": 22000, "categoria": "supermercado"},
            {
                "nombre": "pastillas de panela*30",
                "stock": 23000,
                "categoria": "supermercado",
            },
            {
                "nombre": "pastillas de chocolate*30",
                "stock": 20000,
                "categoria": "supermercado",
            },
            {
                "nombre": "botellas de agua*16",
                "stock": 20000,
                "categoria": "supermercado",
            },
            {
                "nombre": "pan de molde*12",
                "stock": 22000,
                "categoria": "supermercado",
            },
            {
                "nombre": "arroz 1kg*20",
                "stock": 40000,
                "categoria": "supermercado",
            },
            {
                "nombre": "galletas de soda*6paquetes",
                "stock": 21000,
                "categoria": "supermercado",
            },
            {
                "nombre": "leche entera*8",
                "stock": 30000,
                "categoria": "supermercado",
            },
            {
                "nombre": "empaques de brownie*15",
                "stock": 15000,
                "categoria": "supermercado",
            },
            {
                "nombre": "galletas de red velvet",
                "stock": 30000,
                "categoria": "supermercado",
            },
            {
                "nombre": "postres de red velvet",
                "stock": 20000,
                "categoria": "supermercado",
            },
        ]
        print("Iniciando nuevo inventario de almacén.")
        guardar_existencias(productos)

    indices = {str(i + 1): i for i in range(len(productos))}

    while True:
        print("\n--- INVENTARIO DE ALMACÉN ---")
        print("\n SUPERMERCADO:")
        for k in indices:
            producto = productos[indices[k]]
            if producto["categoria"] == "supermercado":
                print(f"{k}. {producto['nombre']} - Stock: {producto['stock']}")

        print("\n MÁQUINA EXPENDEDORA:")
        for k in indices:
            producto = productos[indices[k]]
            if producto["categoria"] == "maquina":
                print(f"{k}. {producto['nombre']} - Stock: {producto['stock']}")

        print("\n--- OPCIONES ---")
        print("1. Preparar salida de producto")
        print("2. Cargar stock al almacén")
        print("3. Salir")

        opcion = input("\n¿Qué deseas hacer?: ").strip().lower()

        if opcion == "3" or opcion == "no":
            guardar_existencias(productos)
            print("Datos guardados. Saliendo del almacén.")
            return

        if opcion not in ["1", "2"]:
            print("Opción inválida.")
            continue

        eleccion = input("\nSeleccione el número del producto: ").strip().lower()

        if eleccion not in indices:
            print("Código inválido. Selecciona un número válido.")
            continue

        idx = indices[eleccion]
        prod = productos[idx]

        print(f"\nProducto seleccionado: {prod['nombre']}")
        print(f"Stock actual: {prod['stock']} unidades.")

        if opcion == "1":
            if prod["stock"] <= 0:
                print("Sin stock.")
                continue

            cantidad = pedir_cantidad(
                "¿Cuántas unidades deseas preparar para salida?: "
            )

            if cantidad is None:
                continue

            if cantidad > prod["stock"]:
                print("No hay suficiente stock en almacén.")
            else:
                prod["stock"] -= cantidad
                print(
                    f"Salida preparada. Quedan {prod['stock']} unidades en almacén."
                )
                guardar_existencias(productos)

        elif opcion == "2":
            cantidad = pedir_cantidad(
                "¿Cuántas unidades deseas cargar al almacén?: "
            )

            if cantidad is None:
                continue

            prod["stock"] += cantidad
            print(
                f"Stock cargado correctamente. Ahora hay {prod['stock']} unidades de {prod['nombre']}."
            )
            guardar_existencias(productos)

        while True:
            continuar = (
                input("\n¿Quieres gestionar otro producto? (si/no): ")
                .strip()
                .lower()
            )

            if continuar == "si":
                break
            elif continuar == "no":
                guardar_existencias(productos)
                print("Datos guardados. Saliendo del almacén.")
                return
            else:
                print("Escribe únicamente 'si' o 'no'.")


gestionar_almacen()
