import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)
db = client["tienda"]
coleccion_maquina = db["maquina"]
coleccion_estado = db["maquina_estado"] 


class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self, monto_disponible):
        if self.stock <= 0:
            return False, 0
        if monto_disponible < self.precio:
            return False, 0
        self.stock -= 1
        return True, self.precio


class MaquinaGabriel:
    def __init__(self):
        estado_bd = coleccion_estado.find_one({"config": "principal"})
        if estado_bd:
            self.saldo_maquina = estado_bd["saldo_maquina"]
        else:
            self.saldo_maquina = 100000
            coleccion_estado.update_one(
                {"config": "principal"},
                {"$set": {"saldo_maquina": self.saldo_maquina}},
                upsert=True
            )

        productos_bd = list(coleccion_maquina.find({}))
        if productos_bd:
            self.productos_lista = [
                Producto(p["nombre"], p["precio"], p["stock"])
                for p in productos_bd
            ]
        else:
            productos_iniciales = [
                {"nombre": "Papas", "precio": 2000, "stock": 28},
                {"nombre": "Gaseosa", "precio": 1500, "stock": 20},
                {"nombre": "Caramelos", "precio": 1200, "stock": 12},
                {"nombre": "Chocolate", "precio": 3500, "stock": 25},
                {"nombre": "Galletas", "precio": 2500, "stock": 22},
                {"nombre": "Jugo", "precio": 1800, "stock": 24},
                {"nombre": "Agua", "precio": 1000, "stock": 18},
            ]
            coleccion_maquina.insert_many(productos_iniciales)
            self.productos_lista = [
                Producto(p["nombre"], p["precio"], p["stock"])
                for p in productos_iniciales
            ]

    def actualizar_producto_en_bd(self, producto: Producto):
        coleccion_maquina.update_one(
            {"nombre": producto.nombre},
            {"$set": {"stock": producto.stock}}
        )

    def actualizar_saldo_en_bd(self):
        coleccion_estado.update_one(
            {"config": "principal"},
            {"$set": {"saldo_maquina": self.saldo_maquina}}
        )

    def mostrar_menu(self):
        for i, p in enumerate(self.productos_lista, 1):
            print(f"{i} {p.nombre} {p.precio} {p.stock}")

    def condiciones(self):
        pago_usuario = 0
        intentos = 3
        
        while True:
            if intentos == 0:
                return self.saldo_maquina
            try:
                entrada = input().strip().lower()
                if entrada == "no":
                    break
                monto = int(entrada)
                if 0 < monto <= 5000:
                    pago_usuario += monto
                else:
                    intentos -= 1
            except ValueError:
                intentos -= 1
                
        while True:
            if intentos <= 0:
                break
            self.mostrar_menu()
            eleccion = input().strip().lower()
            if eleccion == "no":
                break
                
            indices = {str(j + 1): j for j in range(len(self.productos_lista))}
            if eleccion in indices:
                idx = indices[eleccion]
                prod = self.productos_lista[idx]
                
                exito, precio_prod = prod.vender(pago_usuario)
                if exito:
                    pago_usuario -= precio_prod
                    self.saldo_maquina += precio_prod
                    
                    self.actualizar_producto_en_bd(prod)
                    self.actualizar_saldo_en_bd()
                    
                    if prod.stock < 5:
                        almacen = db["almacen"]
                        producto_almacen = almacen.find_one({"nombre": prod.nombre})
                        
                        if producto_almacen and producto_almacen.get("stock", 0) > 10:
                            almacen.update_one(
                                {"nombre": prod.nombre},
                                {"$inc": {"stock": -10}}
                            )
                            prod.stock += 10
                            self.actualizar_producto_en_bd(prod)
                else:
                    intentos -= 1
            else:
                intentos -= 1
                
            if input().strip().lower() == "no":
                break
                
        return self.saldo_maquina


if __name__ == "__main__":
    maquina = MaquinaGabriel()
    saldo_final = maquina.condiciones()

    print(f"Saldo total en máquina: ${saldo_final}")
    print("Ten un lindo día.")
