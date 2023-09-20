# app.py

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
CORS(app)

GPIO_PIN = 14
DEBOUNCE_TIME = 10  # in milliseconds, adjust as needed
NUM_READINGS = 5  # Number of readings to take before averaging

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_rpm():
    pulse_count = 0
    start_time = time.time()
    end_time = start_time + 1  # We'll measure for one second

    while time.time() < end_time:
        if GPIO.input(GPIO_PIN) == 0:  # Detecting a falling edge (magnet passing by)
            pulse_count += 1
            time.sleep(DEBOUNCE_TIME/1000)  # Debounce for the given time

    rpm = (pulse_count / 7) * 60  # Calculate RPM
    return rpm

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_horsepower", methods=["GET"])
def get_horsepower():
    total_rpm = 0

    for _ in range(NUM_READINGS):
        total_rpm += get_rpm()
        time.sleep(0.1)  # Sleep a bit between readings

    avg_rpm = total_rpm / NUM_READINGS
    torque = 16  # fixed at 16 foot-pounds
    horsepower = (torque * avg_rpm) / 5252

    return jsonify({"horsepower": horsepower})

if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000, host="0.0.0.0")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
