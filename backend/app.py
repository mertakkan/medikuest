# app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseQuery import MedicalDatabase
import base64
import io

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/api/histogram', methods=['POST'])
def histogram():
    data = request.json
    attribute = data['attribute']
    values = data['values']
    personal_epsilon = data['personal_epsilon']

    db = MedicalDatabase()
    fig = db.createHistogram(attribute, values, personal_epsilon)
    db.update_epsilon(data['username'])
    db.close_connection()

    # Convert plot to a PNG image in memory
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return jsonify({'image': img_base64})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    db = MedicalDatabase()
    result = db.register(username, password)
    db.close_connection()
    return jsonify({'success': result == 1})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    db = MedicalDatabase()
    result = db.loginCheck(username, password)
    db.close_connection()
    return jsonify({'success': result == 1})


@app.route('/api/max', methods=['POST'])
def max_value():
    data = request.json
    attribute = data['attribute']
    username = data['username']  # Get the username from the request

    db = MedicalDatabase()
    personal_epsilon = db.get_epsilon(username)  # Fetch user's current epsilon
    max_val = db.maxGeneral(attribute, personal_epsilon)
    db.update_epsilon(username)
    db.close_connection()

    return jsonify({'result': max_val})


@app.route('/api/min', methods=['POST'])
def min_value():
    data = request.json
    attribute = data['attribute']
    username = data['username']

    db = MedicalDatabase()
    personal_epsilon = db.get_epsilon(username)
    min_val = db.minGeneral(attribute, personal_epsilon)
    db.update_epsilon(username)
    db.close_connection()

    return jsonify({'result': min_val})

@app.route('/api/avg', methods=['POST'])
def avg_value():
    data = request.json
    attribute = data['attribute']
    username = data['username']

    db = MedicalDatabase()
    personal_epsilon = db.get_epsilon(username)
    avg_val = db.averageGeneral(attribute, personal_epsilon)
    db.update_epsilon(username)
    db.close_connection()

    return jsonify({'result': avg_val})

@app.route('/api/totalnum', methods=['POST'])
def total_num():
    data = request.json
    attribute_type = data['attribute_type']
    smoke = data.get('smoke') 
    diabetes = data.get('diabetes')  
    blood_type = data.get('bloodType')
    username = data['username']

    db = MedicalDatabase()
    personal_epsilon = db.get_epsilon(username)

    total = None

    if attribute_type == 'Smoke':
        total = db.smokeTypeTotalNum(smoke, personal_epsilon, 0)
    elif attribute_type == 'Blood':
        total = db.bloodTypeTotalNum(blood_type, personal_epsilon, 0)
    elif attribute_type == 'Diabetes':
        total = db.diabetesTypeTotalNum(diabetes, personal_epsilon, 0)

    db.update_epsilon(username)
    
    db.close_connection()

    return jsonify({'result': total})

if __name__ == '__main__':
    app.run(debug=True)  # Runs on http://127.0.0.1:5000 by default
