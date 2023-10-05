# app.py

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from RPMCalculator import get_rpm
import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(filename='backend.log', filemode='w', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")

# Function to calculate and emit horsepower
def send_horsepower():
    torque = 14  # fixed at 16 foot-pounds
    horsepower = (torque * get_rpm()) / 5252
    horsepower = round(horsepower, 2)
    socketio.emit('horsepower_update', {'horsepower': horsepower})

# SocketIO event handler for when client connects
@socketio.on('connect')
def handle_connect():
    send_horsepower()  # Send horsepower update when client connects

# SocketIO event handler for when client requests horsepower
@socketio.on('get_horsepower')
def handle_get_horsepower():
    send_horsepower()  # Send horsepower update in response to client request

# Main entry point
if __name__ == "__main__":
    try:
        socketio.run(app, debug=True, port=5000, host="0.0.0.0")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
