import pymysql
import time
import threading
from flask import Flask, render_template
from notifypy import Notify

# Configuración de la base de datos
db_config = {
    'host': 'io0727.mysql.pythonanywhere-services.com',
    'user': 'io0727',
    'password': '^@k4,FB7RQ2?G_z',
    'database': 'io0727$default',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor
}

app = Flask(__name__)

def obtener_ultimo_numero():
    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MAX(numero) as max_numero FROM reporte")
            resultado = cursor.fetchone()
            return resultado['max_numero'] if resultado['max_numero'] is not None else 0

def verificar_nuevos_registros(ultimo_numero_conocido):
    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM reporte WHERE numero > %s", (ultimo_numero_conocido,))
            return cursor.fetchall()

def enviar_notificacion(registro):
    notificacion = Notify()
    notificacion.title = f"Nuevo reporte en: {registro['zona']}"
    notificacion.message = f"Hora: {registro['hora']}\nAtaque: {registro['ataco']}\nObservaciones: {registro['observaciones']}"
    notificacion.icon = "./templates/imagen_prueba.png"  # Asegúrate de que esta ruta sea válida
    notificacion.send()

def monitor():
    ultimo_numero_conocido = obtener_ultimo_numero()
    print("Monitoreando nuevos registros...")
    
    while True:
        nuevos_registros = verificar_nuevos_registros(ultimo_numero_conocido)
        for registro in nuevos_registros:
            enviar_notificacion(registro)
            ultimo_numero_conocido = registro['numero']
        
        time.sleep(3)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    threading.Thread(target=monitor, daemon=True).start()
    app.run(debug=True)
