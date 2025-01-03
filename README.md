# Horsepower Exhibit

This documentation provides an overview of the Horsepower Exhibit project, implemented in Rust using the Macroquad game framework. The application visualizes horsepower through a dynamic horse animation and scrolling background, receiving data via UDP from an external source.

## Table of Contents

- [Introduction](#introduction)
- [System Overview](#system-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

## Introduction

The Horsepower Exhibit is an interactive visualization of horsepower using a Rust-based application. It receives real-time horsepower data via UDP and animates a horse sprite and scrolling background based on the input values. The application is built using the Macroquad game framework for graphics and Rodio for audio.

## System Overview

### Components

1. **Rust Application:**
   - Receives UDP packets containing horsepower, RPM, and torque data
   - Animates horse sprite and background based on input
   - Plays galloping sound effect synchronized with animation

2. **External Data Source:**
   - Sends UDP packets to the application on port 3450
   - Expected packet format: 3 f32 values (horsepower, RPM, torque)

### Architecture

- **Graphics:** Macroquad framework for 2D rendering
- **Audio:** Rodio for sound effects
- **Data Processing:** UDP socket for real-time data reception
- **Animation:** Frame-based sprite animation with smooth interpolation

## Installation

### Prerequisites

- Rust 1.65+ installed
- Cargo package manager

### Setup Steps

1. Clone the repository
2. Install dependencies:
   ```bash
   cargo build
   ```
3. Place assets in the `assets/` directory:
   - Background: `background/HorseRace.png`
   - Horse frames: `horse/frame_0.png` to `horse/frame_5.png`
   - Audio: `audio/horsegallop.wav`

4. Run the application:
   ```bash
   cargo run
   ```

## Usage

1. Start the application
2. Ensure the data source is sending UDP packets to port 3450
3. The application will:
   - Display a fullscreen window with the visualization
   - Animate the horse and background based on received horsepower values
   - Show current horsepower value on screen
   - Play galloping sound effect when horsepower > 0

## Code Structure

### Main Components

- `main.rs`: Entry point, handles UDP communication and main loop
- `background.rs`: Manages scrolling background animation
- `horse.rs`: Handles horse sprite animation
- `data_smoother.rs`: Implements data smoothing for stable visualization

### Key Features

- Smooth interpolation of horsepower values
- Configurable animation speeds
- Automatic scaling for different screen resolutions
- Data smoothing for stable visualization

## Configuration

The application can be configured through constants in `main.rs`:

- `BACKGROUND_SPEED_FACTOR`: Controls background scroll speed
- `HORSE_SPEED_FACTOR`: Controls horse animation speed
- `INTERPOLATION_DURATION`: Time for horsepower value interpolation

## Troubleshooting

- **No Animation:** Verify UDP packets are being sent to the correct port
- **No Sound:** Check OpenAL installation and audio file path
- **Performance Issues:** Reduce window size or optimize assets

## Author
**Lucien Thomas** | [GitHub](https://github.com/ljt019) | 📧 lucienjamest22@gmail.com | Feel free to contact me with any questions