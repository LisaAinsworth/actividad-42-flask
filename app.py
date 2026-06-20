from flask import Flask, render_template
import random
import socket
import re

app = Flask(__name__)

# Puerto web de Flask
WEB_PORT = 5000

# IP y puerto que muestra la APP
HOST_CELULAR = "192.168.100.231"
PORT_CELULAR = 12345


def extraer_numeros(texto):
    numeros = re.findall(r"-?\d+(?:[.,]\d+)?", texto)

    if len(numeros) >= 2:
        x = float(numeros[0].replace(",", "."))
        y = float(numeros[1].replace(",", "."))
        return x, y

    return None


def convertir_a_celda(valor):
    return int(abs(round(valor))) % 4


def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(2)
            cliente.connect((HOST_CELULAR, PORT_CELULAR))

            datos = cliente.recv(1024).decode("utf-8", errors="ignore").strip()
            print("Dato recibido desde celular:", datos)

            resultado = extraer_numeros(datos)

            if resultado:
                dato_x, dato_y = resultado
                celda_x = convertir_a_celda(dato_x)
                celda_y = convertir_a_celda(dato_y)

                return round(dato_x, 2), round(dato_y, 2), celda_x, celda_y, "App celular TCP" #Para que salgan en decimal

    except Exception as error:
        print("No se pudo leer desde la app:", error)

    # Datos de respaldo
    dato_x = random.uniform(-5, 5)
    dato_y = random.uniform(-5, 5)
    celda_x = convertir_a_celda(dato_x)
    celda_y = convertir_a_celda(dato_y)

    return round(dato_x, 2), round(dato_y, 2), celda_x, celda_y, "Simulado"


def crear_matriz(x, y):
    matriz = []

    for fila in range(4):
        nueva_fila = []

        for columna in range(4):
            if fila == y and columna == x:
                nueva_fila.append("🐾")
            elif columna == x:
                nueva_fila.append("X")
            elif fila == y:
                nueva_fila.append("Y")
            else:
                nueva_fila.append("·")

        matriz.append(nueva_fila)

    return matriz


@app.route("/")
def index():
    dato_x, dato_y, celda_x, celda_y, origen = leer_sensor()
    matriz = crear_matriz(celda_x, celda_y)

    return render_template(
        "index.html",
        datoX=dato_x,
        datoY=dato_y,
        ejeX=celda_x,
        ejeY=celda_y,
        origen=origen,
        matriz=matriz
    )


@app.route("/vista1")
def vista1():
    dato_x, dato_y, celda_x, celda_y, origen = leer_sensor()

    return render_template(
        "vista1.html",
        datoX=dato_x,
        datoY=dato_y,
        ejeX=celda_x,
        ejeY=celda_y,
        origen=origen
    )


@app.route("/vista2")
def vista2():
    dato_x, dato_y, celda_x, celda_y, origen = leer_sensor()
    matriz = crear_matriz(celda_x, celda_y)

    return render_template(
        "vista2.html",
        datoX=dato_x,
        datoY=dato_y,
        ejeX=celda_x,
        ejeY=celda_y,
        origen=origen,
        matriz=matriz
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=WEB_PORT, debug=True)
