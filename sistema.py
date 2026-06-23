from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/mapache/menu")
def obtener_mapache():

    url = "http://127.0.0.1:5000/menu"

    respuesta = requests.get(url)
    data = respuesta.json()

    return jsonify(data)
@app.route("/mapache/ordenar")
def ordenar_mapache():

    url = "http://127.0.0.1:5000/ordenar"

    respuesta = requests.get(url)
    data = respuesta.json()

    return jsonify(data)
@app.route("/mapache/pagar")
def pagar_mapache():

    url = "http://127.0.0.1:5000/pagar"

    respuesta = requests.get(url)
    data = respuesta.json()

    return jsonify(data)


if __name__ == "__main__":
 app.run()
    