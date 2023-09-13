import RPi.GPIO as GPIO

class HallSensor:
    def __init__(self, pin):
        self.pin = pin
        self.rotation_count = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._rotation_detected)

    def _rotation_detected(self, channel):
        self.rotation_count += 1

    def get_and_reset_rotation_count(self):
        count = self.rotation_count
        self.rotation_count = 0
        return count

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
