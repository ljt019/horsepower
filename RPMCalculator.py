import RPi.GPIO as GPIO
import logging

logging.basicConfig(filename='rpm.log', filemode='w', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

GPIO_PIN = 14
DEBOUNCE_TIME = 10  # in milliseconds, adjust as needed

magnet_passes = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensor_read(channel):
    global magnet_passes
    magnet_passes += 0.5

GPIO.add_event_detect(GPIO_PIN, GPIO.BOTH, callback=sensor_read, bouncetime=DEBOUNCE_TIME)

def calculate_rpm(number_of_magnets = 7):
    global magnet_passes
    return (magnet_passes / number_of_magnets) * 60

def get_rpm():
    global magnet_passes
    rpm = calculate_rpm()
    magnet_passes = 0
    return rpm
