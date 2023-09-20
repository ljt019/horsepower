# app.py

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/get_horsepower", methods=["GET"])
def get_horsepower():
    
    horsepower = .6
    
    if horsepower > 1.12:
        horsepower = 1.12
    
    return jsonify({"horsepower": horsepower})

if __name__ == "__main__":
    app.run(debug=True, port=5000)