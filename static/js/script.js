let backgroundPositionX = 0;
let currentSpeed = 0;
const maxHorsepower = 1.12;
let animationRunning = false;
let currentFrame = 0;
const frameWidth = 900;
let lastTimestamp;
const baseInterval = 70;

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

// Set up a Socket.IO connection
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Define a handler for 'horsepower_update' messages
socket.on('horsepower_update', function(msg) {
    const horsepower = msg.horsepower;
    adjustBackgroundSpeed(horsepower);

    // Display the horsepower value
    const horsepowerElem = document.getElementById('horsepowerValue');
    horsepowerElem.innerText = horsepower;
});

// Optionally send a 'get_horsepower' message to the server to request an initial horsepower update
socket.emit('get_horsepower');

// Initialize the animation loop
requestAnimationFrame(update);
