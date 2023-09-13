from time import sleep, time
import sensor
import horsepower
import animation
from constants import SENSOR_PIN

TIME_INTERVAL = 1  # in seconds

hall_sensor = sensor.HallSensor(SENSOR_PIN)
anim = animation.Animation()

try:
    while True:
        sleep(TIME_INTERVAL)
        ticks = hall_sensor.get_and_reset_rotation_count()
        rpm = horsepower.rpm_from_sensor_ticks(ticks, TIME_INTERVAL)
        hp = horsepower.calculate_horsepower(rpm)
        anim.run_animation(hp)
except KeyboardInterrupt:
    hall_sensor.cleanup()
    pygame.quit()