from constants import SENSOR_TICKS_PER_REVOLUTION, MIN_TORQUE, MAX_TORQUE, MAX_RPM

def rpm_from_sensor_ticks(ticks, time_interval):
    return (ticks / SENSOR_TICKS_PER_REVOLUTION) * (60 / time_interval)

def estimated_torque(rpm):
    # Assuming linear relation between RPM and torque for simplicity
    normalized_rpm = rpm / MAX_RPM  # Normalize between 0 and 1
    return MIN_TORQUE + (MAX_TORQUE - MIN_TORQUE) * normalized_rpm

def calculate_horsepower(rpm):
    torque = estimated_torque(rpm)
    return (torque * rpm) / 5252