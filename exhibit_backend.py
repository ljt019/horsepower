# app.py

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
CORS(app)

GPIO_PIN = 14
DEBOUNCE_TIME = 10  # in milliseconds, adjust as needed
NUM_READINGS = 2  # Number of readings to take before averaging
last_pulse_time = 0  # To counter continueous triggers (sensor stopped over magnet)

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_rpm():
    pulse_count = 0
    continuous_trigger_time = 0
    start_time = time.time()
    end_time = start_time + 1  # We'll measure for one second
    last_detected_time = 0  # Track time of last detected pulse in the loop

    while time.time() < end_time:
        current_time = time.time()

        if GPIO.input(GPIO_PIN) == 0:  # Detecting a falling edge (magnet passing by)
            # Check if the time between two consecutive pulses is greater than debounce time
            if current_time - last_detected_time > DEBOUNCE_TIME/1000:
                pulse_count += 1
            else:
                continuous_trigger_time += current_time - last_detected_time
            last_detected_time = current_time

            # If continuously triggered for more than 2 seconds, consider engine as stopped
            if continuous_trigger_time > 2:
                return 0

            time.sleep(DEBOUNCE_TIME/1000)  # Debounce for the given time
        else:
            # Reset the counter if not being continuously triggered
            continuous_trigger_time = 0

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
    torque = 14  # fixed at 16 foot-pounds
    horsepower = (torque * avg_rpm) / 5252

    horsepower = round(horsepower, 2)
    return jsonify({"horsepower": horsepower})

if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000, host="0.0.0.0")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
