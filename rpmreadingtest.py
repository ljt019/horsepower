import RPi.GPIO as GPIO
import time

# Setup
GPIO_PIN = 14  # Change to the pin number you are using
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback function to run when an edge is detected
def edge_detected(channel):
    print(f'Edge detected on channel {channel}')

# Add event detection for both rising and falling edges
GPIO.add_event_detect(GPIO_PIN, GPIO.BOTH, callback=edge_detected)

try:
    while True:  # Keep the script running
        time.sleep(0.1)  # Reduce CPU usage

except KeyboardInterrupt:
    print('Script terminated by user')

finally:
    GPIO.cleanup()  # Clean up GPIO pins
