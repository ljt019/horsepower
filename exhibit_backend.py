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
pulse_times = []  # Global list to store pulse times

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_rpm():
    global pulse_times
    MAX_STORED_TIMES = 10  # Number of pulse times to store
    STOPPED_THRESHOLD = 0.02  # If average time between pulses is below this, engine is considered stopped. Adjust as needed.
    
    pulse_count = 0
    current_time = time.time()
    last_detected_time = 0  # Track time of last detected pulse in the loop

    while current_time - last_detected_time < 1:  # We'll measure for one second from the last detected pulse
        current_time = time.time()
        
        if GPIO.input(GPIO_PIN) == 0:
            pulse_count += 1
            
            # Store pulse time and maintain list length
            pulse_times.append(current_time)
            if len(pulse_times) > MAX_STORED_TIMES:
                pulse_times.pop(0)
            
            # Calculate average time between pulses
            if len(pulse_times) > 1:
                avg_time_between_pulses = (pulse_times[-1] - pulse_times[0]) / (len(pulse_times) - 1)
                if avg_time_between_pulses < STOPPED_THRESHOLD:
                    return 0
            
            last_detected_time = current_time
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
    torque = 14  # fixed at 16 foot-pounds
    horsepower = (torque * avg_rpm) / 5252

    horsepower = round(horsepower, 2)
    return jsonify({"horsepower": horsepower})

if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000, host="0.0.0.0")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
