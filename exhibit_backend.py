# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import logging

logging.basicConfig(filename='backend.log', filemode='w', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

GPIO_PIN = 14
DEBOUNCE_TIME = 10  # in milliseconds, adjust as needed

magnet_passes = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensor_read(channel):
    global magnet_passes
    magnet_passes += 0.5
    send_horsepower_update()

def send_horsepower_update():
    torque = 14  # fixed at 16 foot-pounds
    rpm = calculate_rpm()
    horsepower = (torque * rpm) / 5252
    horsepower = round(horsepower, 2)
    socketio.emit('horsepower_update', {'horsepower': horsepower})

def calculate_rpm(number_of_magnets=7):
    global magnet_passes
    rpm = (magnet_passes / number_of_magnets) * 60
    magnet_passes = 0  # Reset magnet_passes after calculating RPM
    logging.debug("RPM: " + str(rpm))
    return rpm

GPIO.add_event_detect(GPIO_PIN, GPIO.BOTH, callback=sensor_read, bouncetime=DEBOUNCE_TIME)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    send_horsepower_update()  # Send horsepower update when client connects

if __name__ == "__main__":
    try:
        socketio.run(app, debug=True, port=5000, host="0.0.0.0", allow_unsafe_werkzeug=True)
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
