"""El código importa las librerías necesarias y establece una instacia Flask
con dos rutas: una que renderiza la plantilla principal y otra que gestiona
las interacciones del usuario con el modelo. La app también informa al usuario
si el servidor extá experimentado tráfico para que consulte más tade."""

#Importamos los módulos y librerías necesarios
import os
import json
from flask import Flask, render_template, request, jsonify
import openai
from openai.error import RateLimitError

#Inicializamos una nueva applicación Flask
app = Flask(__name__)

#Establecemos la API key como una variable de entorno para evitar exponer la clave.
openai.organization = "org-hLGkFR4WcNN8UTIkbKVwP3MQ"

openai.api_key = "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"

#Ruta hacia la página principal

#Define la ruta raíz para la aplicación
@app.route('/')
#Esta función se llama cuando se accede a la ruta raíz.
def index():
    return render_template('index.html') #Renderiza la platilla

@app.route("/adios")

def goodbye():
    return render_template("adios.html")

#Ruta para interactuar con la API
@app.route('/gpt', methods=['GET', 'POST']) #Define la ruta y permite solicitudes POST y GET

#Se llama a esta función cuando se accede a la ruta '/gpt'
def gpt():
    user_input = request.args.get('user_input') if request.method == 'GET' else request.form['user_input'] #Recupera la entrada del usuario según la forma de los datos
    messages = [{"role": "user", "content": user_input}] #Crea una lista de mensajes conteniendo un solo mensaje con la entrada del usuario

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        content = response.choices[0].message["content"]
    except RateLimitError:
        content = "El servidor está experimentando un alto volumen de peticiones. Vuelva a intentarlo más tarde."

    return jsonify(content=content) #Devuelve el contenido como en formato JSON

if __name__ == '__main__':
    app.run(port=5000)


