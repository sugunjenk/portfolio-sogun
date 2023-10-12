import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client["DB_NAME"]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    # Dapatkan data dari permintaan POST
    data = request.get_json()
    name = data['name']
    email = data['email']
    message = data['message']

    # Simpan data ke database MongoDB
    messages = db.messages
    new_message = {
        'name': name,
        'email': email,
        'message': message
    }
    messages.insert_one(new_message)

    # Anda dapat memberikan respons ke klien jika diperlukan
    response = {'message': 'Pesan telah berhasil disimpan ke database.'}
    return jsonify(response)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
