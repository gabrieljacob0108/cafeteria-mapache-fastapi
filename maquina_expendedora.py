import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)
db = client["tienda"]
coleccion = db["maquina"]


class Producto:

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self, monto_disponible):
        if self.stock <= 0:
            print(f"Lo sentimos, {self.nombre} está agotado.")
            return False, 0
        if monto_disponible < self.precio:
            print(
                f"Dinero insuficiente para {self.nombre}. Cuesta ${self.precio}."
            )
            return False, 0
        self.stock -= 1
        return True, self.precio


class MaquinaGabriel:

    def __init__(self):
        datos = self.cargar_datos()
        if datos:
            self.saldo_maquina = datos["saldo_maquina"]
            self.productos_lista = [
                Producto(p["nombre"], p["precio"], p["stock"])
                for p in datos["productos_lista"]
            ]
            print("¡Bienvenido de nuevo!")
        else:
            self.saldo_maquina = 100000
            self.productos_lista = [
                Producto("Papas", 2000, 28),
                Producto("Gaseosa", 1500, 20),
                Producto("Caramelos", 1200, 12),
                Producto("Chocolate", 3500, 25),
                Producto("Galletas", 2500, 22),
                Producto("Jugo", 1800, 24),
                Producto("Agua", 1000, 18),
            ]
            self.guardar_datos()

    def cargar_datos(self):
        productos = list(coleccion.find({}, {"_id": 0}))
        return (
            {"saldo_maquina": 100000, "productos_lista": productos}
            if productos
            else None
        )

    def guardar_datos(self):
        lista_dicts = [
            {"nombre": p.nombre, "precio": p.precio, "stock": p.stock}
            for p in self.productos_lista
        ]
        coleccion.delete_many({})
        coleccion.insert_many(lista_dicts)

    def mostrar_menu(self):
        print("\n--- MENÚ DE PRODUCTOS ---")
        for i, p in enumerate(self.productos_lista, 1):
            print(f"{i}. {p.nombre} - ${p.precio} (Stock: {p.stock})")

    def condiciones(self):
        print("Bienvenido a la maquina expendedora")
        pago_usuario = 0
        intentos = 3
        while True:
            if intentos == 0:
                print(f"Muchos errores. Devolviendo: ${pago_usuario}")
                return self.saldo_maquina
            try:
                print(f"\nSaldo ingresado: ${pago_usuario}")
                entrada = (
                    input(
                        "Inserta monto (Máx 5000) o 'no' para comprar/salir: "
                    )
                    .strip()
                    .lower()
                )
                if entrada == "no":
                    break
                monto = int(entrada)
                if 0 < monto <= 5000:
                    pago_usuario += monto
                else:
                    print("Monto inválido.")
                    intentos -= 1
            except ValueError:
                print("Dígito inválido.")
                intentos -= 1
        while True:
            if intentos <= 0:
                break
            self.mostrar_menu()
            eleccion = (
                input("Escoge un número (o 'no' para salir): ").strip().lower()
            )
            if eleccion == "no":
                break
            indices = {
                str(j + 1): j for j in range(len(self.productos_lista))
            }
            if eleccion in indices:
                idx = indices[eleccion]
                prod = self.productos_lista[idx]
                exito, precio_prod = prod.vender(pago_usuario)
                if exito:
                    pago_usuario -= precio_prod
                    self.saldo_maquina += precio_prod
                    print(
                        f"¡Disfruta tu {prod.nombre}! Saldo restante: ${pago_usuario}"
                    )
                    self.guardar_datos()
                    if prod.stock < 5:
                        almacen = db["almacen"]
                        producto_almacen = almacen.find_one(
                            {"nombre": prod.nombre}
                        )
                        if producto_almacen and producto_almacen["stock"] > 10:
                            almacen.update_one(
                                {"nombre": prod.nombre},
                                {"$inc": {"stock": -10}},
                            )
                            prod.stock += 10
                            print(
                                f"⚠️ ¡Stock bajo! El almacén recargó 10 unidades de {prod.nombre}"
                            )
                else:
                    intentos -= 1
            else:
                print("Opción no válida.")
                intentos -= 1
            if (
                input("¿Quieres otro bocadillo? (si/no): ").strip().lower()
                == "no"
            ):
                break
        print(f"Tu cambio es: ${pago_usuario}")
        return self.saldo_maquina


if __name__ == "__main__":
    maquina = MaquinaGabriel()
    saldo_final = maquina.condiciones()
    print(f"Saldo total en máquina: ${saldo_final}")
    print("Ten un lindo día.")
