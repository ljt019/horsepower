# app.py

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(filename='backend.log', filemode='w', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)


GPIO_PIN = 14
DEBOUNCE_TIME = 10  # in milliseconds, adjust as needed
RPM_SAMPLE_SIZE = 2  # Number of readings to take before averaging

last_pulse_time = 0  # To counter continueous triggers (sensor stopped over magnet)
pulse_times = []  # Global list to store pulse times

logging.info("-------------------CONSTANTS-------------------")
logging.info(f"GPIO_PIN: {GPIO_PIN}, DEBOUNCE_TIME: {DEBOUNCE_TIME}, RPM_SAMPLE_SIZE: {RPM_SAMPLE_SIZE}")

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def initialize_rpm_variables():
    pulse_count = 0
    current_time = time.time()
    last_detected_time = 0
    return pulse_count, current_time, last_detected_time

def update_pulse_times(pulse_times, current_time, MAX_STORED_TIMES):
    pulse_times.append(current_time)
    if len(pulse_times) > MAX_STORED_TIMES:
        pulse_times.pop(0)
    return pulse_times

def calculate_average_pulse_interval(pulse_times):
    if len(pulse_times) > 1:
        return (pulse_times[-1] - pulse_times[0]) / (len(pulse_times) - 1)
    return None

def is_engine_stopped(avg_time_between_pulses, STOPPED_THRESHOLD):
    return avg_time_between_pulses < STOPPED_THRESHOLD if avg_time_between_pulses is not None else False

def calculate_rpm(pulse_count):
    return (pulse_count / 7) * 60

logging.info("-------------------Measured RPM-------------------")
def get_rpm(GPIO_PIN, DEBOUNCE_TIME, MAX_STORED_TIMES=10, STOPPED_THRESHOLD=0.1):
    global pulse_times  
    pulse_count, current_time, last_detected_time = initialize_rpm_variables()

    while current_time - last_detected_time < 1:
        current_time = time.time()
        
        try:
            if GPIO.input(GPIO_PIN) == 0:
                pulse_count += 1
                pulse_times = update_pulse_times(pulse_times, current_time, MAX_STORED_TIMES)
                
                avg_time_between_pulses = calculate_average_pulse_interval(pulse_times)
                if is_engine_stopped(avg_time_between_pulses, STOPPED_THRESHOLD):
                    logging.info("Detected engine as stopped.")
                    return 0
                
                last_detected_time = current_time
                time.sleep(DEBOUNCE_TIME / 1000)
        except Exception as e:
            logging.info("-------------------Errors-------------------")
            logging.error(f"An error occurred: {e}")
    
    rpm = calculate_rpm(pulse_count)
    logging.debug(f"Detected RPM: {rpm}")
    return rpm


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_horsepower", methods=["GET"])
def get_horsepower():
    total_rpm = 0

    for _ in range(RPM_SAMPLE_SIZE):
        total_rpm += get_rpm()
        time.sleep(0.1)  # Sleep a bit between readings

    avg_rpm = total_rpm / RPM_SAMPLE_SIZE
    torque = 14  # fixed at 16 foot-pounds
    horsepower = (torque * avg_rpm) / 5252

    horsepower = round(horsepower, 2)
    return jsonify({"horsepower": horsepower})

if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000, host="0.0.0.0")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
