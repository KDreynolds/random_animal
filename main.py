from flask import Flask, jsonify, render_template
import sqlite3
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random-animal')
def random_animal():
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, image FROM animals")
    animals = cursor.fetchall()
    conn.close()

    random_animal = random.choice(animals)
    return jsonify({'name': random_animal[0], 'image': random_animal[1]})

if __name__ == '__main__':
    app.run(debug=True)
