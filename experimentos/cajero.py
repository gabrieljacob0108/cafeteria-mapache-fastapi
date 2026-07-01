import json

def cargar_datos():
    try:
        with open("banco_data..json", "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def guardar_datos(saldo, stock_actual):
    datos = {
        "saldou": saldo,
       
    }
    with open("banco_data.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

datos_viejos = cargar_datos()

if datos_viejos:
    saldou = datos_viejos["saldou"]
   
    print("¡Bienvenido de nuevo! Datos de la máquina cargados.")
else:
    saldou = 0
intentos = 3

def modulo_deposito(saldo_actual):
    entrada = input("Inserta valor de monto: ")
    monto = int(entrada)
    if monto <= 0:
        print("Cantidad inválida")
        return saldo_actual, False
    
    nuevo_saldo = saldo_actual + monto
    print("Saldo actual:", nuevo_saldo)
    return nuevo_saldo, True

def modulo_retiro(saldo_actual):
    entrada = input("Inserta valor de monto a retirar: ")
    monto = int(entrada)
    if monto > saldo_actual:
        print("Saldo insuficiente")
        return saldo_actual, False
    
    nuevo_saldo = saldo_actual - monto
    print("transaccion realizada. Saldo restante:", nuevo_saldo)
    return nuevo_saldo, True

def mostrar_menu():
    print("1. deposito | 2. retiro| 3.vista de saldo")

def condiciones(saldou, intentos):
     
    while True:
        if intentos == 0:
            print("Demasiados intentos fallidos. Devolviendo dinero:", saldou)
            return saldou
            
        mostrar_menu()
        eleccion = input("Escoge un número (o escribe 'no' para salir): ")
        
        if eleccion == "no":
            print("Tu cambio es:", saldou, "\nten un lindo dia")
            return saldou
            
        try:
            if eleccion == "1":
                saldou, exito = modulo_deposito(saldou)
                if not exito: intentos -= 1
                
            elif eleccion == "2":
                saldou, exito = modulo_retiro(saldou)
                if not exito: intentos -= 1
                
            elif eleccion == "3":
                print("Tu saldo es:", saldou)
                
            else:
                print("Opción no válida")
                intentos -= 1
                
        except ValueError:
            print("Dígito inválido")
            intentos -= 1

saldo_final = condiciones(saldou, intentos)
print("Saldo final:", saldo_final)
