let backgroundPositionX = 0;
let currentSpeed = 0;
const maxHorsepower = 1.12;
let animationRunning = false;
let currentFrame = 0;
const frameWidth = 900;
let lastTimestamp;
const baseInterval = 70;
var idleTimer;
var isIdleScreenDisplayed = false;

function easeOutCubic(t) {
    return (--t) * t * t + 1;
}

function updateBackground() {
    if (currentSpeed > 0) {
        backgroundPositionX -= currentSpeed;
        const canvas = document.querySelector(".background");
        canvas.style.backgroundPosition = backgroundPositionX + "px 0";
    }
}

function updateHorseSprite(timestamp) {
    if (!lastTimestamp) {
        lastTimestamp = timestamp;
    }

    const deltaTime = timestamp - lastTimestamp;
    const easedHorsepower = easeOutCubic(currentSpeed / (5 * maxHorsepower));
    const frameInterval = baseInterval / easedHorsepower;

    if (deltaTime >= frameInterval) {
        let columns = 5;
        let yOffset = Math.floor(currentFrame / columns) * 606;
        let xOffset = (currentFrame % columns) * frameWidth;

        document.getElementById('horseAnimation').style.backgroundPosition = `-${xOffset}px -${yOffset}px`;
        currentFrame = (currentFrame + 1) % 6;

        lastTimestamp = timestamp;
    }
}

var audio = new Audio('static/audio/horsegallop.wav');

function update(timestamp) {
    if (animationRunning) {
        updateBackground();
        updateHorseSprite(timestamp);
        requestAnimationFrame(update);
        audio.play();
    }
}

function resetIdleTimer() {
    clearTimeout(idleTimer);
    idleTimer = setTimeout(function() {
        // Switch to idle screen if no updates for 15 seconds
        if (currentSpeed === 0) {
            window.location.href = '/idle.html';
            isIdleScreenDisplayed = true;
        }
    }, 15000); // 15 seconds
}

function adjustBackgroundSpeed(horsepower) {
    const speedFactor = 5;
    currentSpeed = speedFactor * (horsepower / maxHorsepower);
    
    if (horsepower > 0 && !animationRunning) {
        animationRunning = true;
        requestAnimationFrame(update);  // Request the next animation frame
    } else if (horsepower <= 0) {
        currentSpeed = 0;
        animationRunning = false;
        audio.pause();
        backgroundPositionX = 0;
        const canvas = document.querySelector(".background");
        canvas.style.backgroundPosition = "0 0";
    }
}

// Set up a WebSocket connection to the Raspberry Pi
var socket = new WebSocket('ws://192.168.1.198:5000/ws');

socket.onopen = function(event) {
    resetIdleTimer();
    console.log('Connected to Raspberry Pi WebSocket server.');
};

socket.onmessage = function(event) {
    const msg = JSON.parse(event.data);
    const horsepower = msg.horsepower;
    adjustBackgroundSpeed(horsepower);

    // Display the horsepower value
    const horsepowerElem = document.getElementById('horsepowerValue');
    horsepowerElem.innerText = horsepower;

    resetIdleTimer(); // Reset the idle timer on every message
};

socket.onerror = function(error) {
    console.log('WebSocket error:', error);
};

socket.onclose = function(event) {
    console.log('WebSocket connection closed.');
    clearTimeout(idleTimer); // Clear the timer when the connection is closed
};

// Initialize the animation loop
requestAnimationFrame(update);

