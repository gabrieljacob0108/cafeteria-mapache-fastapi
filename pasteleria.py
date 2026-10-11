import os
from flask import Flask, request, jsonify, session
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")
password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["mapache"]
coleccion_pedidos = db["pasteleria"]
coleccion_tokens = db["tokens"]

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "mapache_secreto_super_seguro_123")

postres = [
    {"id": 1, "nombre": "pastel red velvet", "precio": 20000},
    {"id": 2, "nombre": "pastel de limon", "precio": 15000},
    {"id": 3, "nombre": "pastel de cafe", "precio": 1200},
    {"id": 4, "nombre": "pastel de chocolate", "precio": 3500},
    {"id": 5, "nombre": "galleta de red velvet", "precio": 2500},
    {"id": 6, "nombre": "pastel de vainilla", "precio": 1800},
    {"id": 7, "nombre": "galleta de chocolate", "precio": 1000},
    {"id": 8, "nombre": "galleta de chispas", "precio": 1500},
    {"id": 9, "nombre": "brownie", "precio": 3000},
    {"id": 10, "nombre": "milhoja", "precio": 4500}
]

toppings = [
    {"nombre": "fresas", "precio": 2000},
    {"nombre": "arequipe", "precio": 1500},
    {"nombre": "chispas", "precio": 1000},
    {"nombre": "crema", "precio": 2500},
    {"nombre": "barquillo", "precio": 3500},
    {"nombre": "galletitas", "precio": 4500}
]

@app.route("/menu", methods=["GET"])
def obtener_menu():
    return jsonify({"postres": postres, "toppings": toppings}), 200

@app.route("/carrito", methods=["GET"])
def ver_carrito():
    carrito_usuario = session.get("carrito", [])
    total = sum(item["precio_final"] for item in carrito_usuario)
    return jsonify({"carrito": carrito_usuario, "total": total}), 200

@app.route("/pedido", methods=["POST"])
def realizar_pedido():
    datos = request.get_json()
    if not datos or not datos.get("id"):
        return jsonify({}), 400

    postre = next((p for p in postres if p["id"] == datos["id"]), None)
    if not postre:
        return jsonify({}), 404

    precio_total = postre["precio"]
    topping_usado = ""

    if datos.get("topping"):
        topping_info = next((t for t in toppings if t["nombre"] == datos["topping"]), None)
        if not topping_info:
            return jsonify({}), 400
        precio_total += topping_info["precio"]
        topping_usado = datos["topping"]

    item = {
        "id": postre["id"],
        "nombre": postre["nombre"],
        "topping": topping_usado,
        "precio_final": precio_total
    }
    
    carrito_usuario = session.get("carrito", [])
    carrito_usuario.append(item)
    session["carrito"] = carrito_usuario
    
    return jsonify({"item": item, "total_items": len(carrito_usuario)}), 200

@app.route("/pagar", methods=["POST"])
def pagar_pedido():
    carrito_usuario = session.get("carrito", [])
    if not carrito_usuario:
        return jsonify({}), 400

    datos = request.get_json()
    if not datos or not datos.get("pago_usuario") or not datos.get("nombre_cliente"):
        return jsonify({}), 400

    nombre_limpio = datos["nombre_cliente"].strip().lower()
    total_cuenta = sum(item["precio_final"] for item in carrito_usuario)

    if datos["pago_usuario"] < total_cuenta:
        return jsonify({
            "total": total_cuenta,
            "faltante": total_cuenta - datos["pago_usuario"]
        }), 400

    cambio = datos["pago_usuario"] - total_cuenta

    coleccion_pedidos.insert_one({
        "cliente": nombre_limpio,
        "items": carrito_usuario,
        "total": total_cuenta
    })

    resultado_token = coleccion_tokens.find_one_and_update(
        {"nombre": nombre_limpio},
        {"$inc": {"tokens": 1}},
        upsert=True,
        return_document=True
    )
    tokens_actuales = resultado_token["tokens"]

    if tokens_actuales >= 20:
        coleccion_tokens.update_one(
            {"nombre": nombre_limpio},
            {"$set": {"tokens": 0}}
        )
        tokens_actuales = 0

    session.pop("carrito", None)

    return jsonify({
        "cliente": nombre_limpio,
        "total": total_cuenta,
        "cambio": cambio,
        "tokens_mapache": tokens_actuales
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=6001)
