# Horsepower Exhibit Documentation

This documentation provides a comprehensive overview of the Horsepower Exhibit project, a web-based interactive application that visualizes horsepower using physical interaction through a Raspberry Pi, a hall effect sensor, and web technologies.

## Table of Contents

- [Introduction](#introduction)
- [System Overview](#system-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [Troubleshooting](#troubleshooting)
- [Author](#author)


## Introduction

The Horsepower Exhibit is an interactive project designed to teach and visualize the concept of horsepower. Users interact with a physical device connected to a Raspberry Pi, which in turn communicates the calculated horsepower to a web application. The web app visually represents this horsepower through a dynamic horse animation and moving background.

## System Overview

### Components

1. **Host Computer Server (Go):**
    
    - `./main.go`: Hosts the files in the static directory.
2. **Web Frontend (HTML, CSS, JS):**
    
    - HTML: `index.html` (main page), `idle.html` (idle screen).
    - CSS: `styles.css` for styling.
    - JavaScript: `script.js` for dynamic functionalities, processing the animations and animation speed from the sensor data
3. **Raspberry Pi & Sensor Setup:**
    
    - `raspPiDataCollectionWebSocket.go`: Raspberry Pi script for collecting sensor data and calculating horsepower.
    - Raspberry Pi connected to a sensor for input data.

### Architecture

- **Backend:** Written in Go, running on a Host Computer and Raspberry Pi.
- **Frontend:** HTML/CSS/JavaScript, served by the Go server, running in a web browser.
- **Communication:** WebSocket for real-time data exchange between the Raspberry Pi and the web frontend.

## Installation

### Prerequisites

- Raspberry Pi with GPIO access.
- Necessary sensors and hardware connected to the Raspberry Pi.

### Setup Steps

1. **Server Setup:**
    
    - Clone the repository to your server.
    - Run the `./main.exe`
1. **Raspberry Pi Setup:**
    
    - Set up the Raspberry Pi with the appropriate sensors.
    - Clone the repository to your server.
    - Run the `./piWebsocket/main.exe`
## Usage

1. **Accessing the Web Application:**
    
    - Open a web browser and navigate to the server's IP address with port `8080` (e.g., `http://<server-ip>:8080`).  *Note: `http://localhost:8080`*
2. **Interacting with the Exhibit:**
    
    - Turn the crank or interact with the sensor connected to the Raspberry Pi.
    - Watch the web application's visual response in real-time.

## Code Overview

### `./main.go`

- Serves static files and templates.
- Defines the root path handler.

### `./piWebsocket/main.go`

- Reads sensor data from Raspberry Pi GPIO.
- Calculates RPM and horsepower.
- Sends data over WebSocket.

### HTML Files (`index.html`, `idle.html`)

- Define the structure of the web pages.

### `styles.css`

- Styles for the web pages and animations.

### `script.js`

- Handles WebSocket communications.
- Animates the horse sprite and background.
- Manages idle screen transitions.

## Troubleshooting

- **WebSocket Connection Issues:** Ensure the server and Raspberry Pi are on the same network and the WebSocket URL is correct.
- **Animation Not Working:** Check if the JavaScript file is correctly linked in the HTML files and no errors are present in the console.

## Author
**Lucien Thomas** | [GitHub](https://github.com/LucienJamesT) | 📧 lucienjamest22@gmail.com | Feel free to contact me with any questions
