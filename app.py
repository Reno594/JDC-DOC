from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    data = {}
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    raw_data = request.get_data()
    print("Contenido bruto de la solicitud:", raw_data)

    data = {key: value for key, value in request.form.items()}
    print("Datos capturados:", data)

    field_new = data.get('field_new')
    if field_new:
        proyectos_directory = 'proyectos'
        if not os.path.exists(proyectos_directory):
            os.makedirs(proyectos_directory)
        file_path = os.path.join(proyectos_directory, f"{field_new}.fop")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return redirect(url_for('results', id=field_new))
    else:
        return "No se proporcionó un valor para field_new"

@app.route('/results/<id>')
def results(id):
    proyectos_directory = 'proyectos'
    file_path = os.path.join(proyectos_directory, f"{id}.fop")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        return "Error: Archivo no encontrado", 404

    return render_template('results.html', data=data)

@app.route('/return/<id>')
def return_to_form(id):
    proyectos_directory = 'proyectos'
    file_path = os.path.join(proyectos_directory, f"{id}.fop")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        return "Error: Archivo no encontrado", 404

    return render_template('index.html', data=data)

@app.route('/files', methods=['GET'])
def list_files():
    proyectos_directory = 'proyectos'
    if not os.path.exists(proyectos_directory):
        os.makedirs(proyectos_directory)
    files = [f for f in os.listdir(proyectos_directory) if f.endswith('.fop')]
    return jsonify(files)

@app.route('/load', methods=['POST'])
def load_file():
    file = request.files['file']
    data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
































