from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
CORS(app)

db = TinyDB('db.json')
tabla_patentes = db.table('patentes')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['POST'])
def agregar_patente():
    data = request.json
    patente = data.get('patente')
    hora_ingreso = data.get('horaIngreso')

    if patente and hora_ingreso:
        tabla_patentes.insert({
            'patente': patente,
            'horaIngreso': hora_ingreso
        })
        return jsonify({'status': 'ok'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

@app.route('/listar', methods=['GET'])
def listar_patentes():
    registros = tabla_patentes.all()
    return jsonify(registros)

@app.route('/eliminar', methods=['POST'])
def eliminar_patente():
    data = request.json
    patente = data.get('patente')

    if patente:
        Patente = Query()
        tabla_patentes.remove(Patente.patente == patente)
        return jsonify({'status': 'ok'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Patente no especificada'}), 400

if __name__ == '__main__':
    app.run(debug=True)
