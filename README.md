# Horsepower Exhibit with Raspberry Pi

A web-based visualization of engine RPM and calculated horsepower using a Raspberry Pi and a Hall effect sensor.

## Overview

This project uses a Raspberry Pi to read RPM values from an engine via a Hall effect sensor. The RPM values are then used to calculate and display the engine's horsepower on a web-based interface. The interface also features a visually appealing representation with a horse animation that dynamically changes based on the RPM/horsepower.

## Features

- **Real-time RPM Readings**: Utilizes the GPIO pins on a Raspberry Pi to get real-time RPM readings from an engine.
- **Horsepower Calculation**: Based on the RPM and a constant torque value, the horsepower of the engine is calculated and displayed.
- **Dynamic Horse Animation**: The web interface displays a horse animation that changes its speed based on the current RPM/horsepower.

## Prerequisites

- **Hardware**:
  - Raspberry Pi (with Raspbian OS installed).
  - Hall effect sensor.
  - Engine with 7 magnets for the sensor.
- **Software**:
  - Flask web framework.
  - Python GPIO library for Raspberry Pi.

## Setup

1. Connect the Hall effect sensor to the Raspberry Pi's GPIO pin 14.
2. Ensure all software dependencies are installed:

   `pip install flask RPi.GPIO flask_cors`

## Getting Started

1. **Clone the repository and navigate to the directory**:
    `git clone https://github.com/Sci-Port/Horsepower.git`
   `cd Horsepower`

3. **Run the Flask app**:
    `
    python app.py
    `

## Usage

1. Start the engine.
2. Navigate to `http://[Raspberry Pi IP Address]:5000` on a web browser.
3. Observe the real-time horsepower value and horse animation on the web interface.

## Author
**Lucien Thomas** | [GitHub](https://github.com/LucienJamesT) | 📧 lucienjamest22@gmail.com | Feel free to contact me with any questions
