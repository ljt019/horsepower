# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import logging
import time

logging.basicConfig(filename='backend.log', filemode='w', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

GPIO_PIN = 14
DEBOUNCE_TIME = 5  # in milliseconds, adjust as needed

magnet_passes = 0
last_magnet_passes = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensor_read(channel):
    global magnet_passes
    magnet_passes += 1

def calculate_and_send_rpm():
    global magnet_passes, last_magnet_passes
    while True:
        time.sleep(1)  # wait for 1 second
        rpm = ((magnet_passes - last_magnet_passes) / 7) * 60  # calculate RPM
        logging.debug("RPM: " + str(rpm))
        last_magnet_passes = magnet_passes  # reset last_magnet_passes
        send_horsepower_update(rpm)  # send updated horsepower

def send_horsepower_update(rpm):
    torque = 14  # fixed at 16 foot-pounds
    horsepower = (torque * rpm) / 5252
    horsepower = round(horsepower, 2) 
    socketio.emit('horsepower_update', {'horsepower': horsepower})

GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=sensor_read, bouncetime=DEBOUNCE_TIME)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    send_horsepower_update(0)  # Send horsepower update when client connects

if __name__ == "__main__":
    try:
        socketio.start_background_task(calculate_and_send_rpm)  # start the background task
        socketio.run(app, debug=True, port=5000, host="0.0.0.0", allow_unsafe_werkzeug=True)
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
