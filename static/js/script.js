let backgroundPositionX = 0;
let currentSpeed = 0;
const maxHorsepower = 1.12;
let animationRunning = false;
let currentFrame = 0;
let animationRequested = false;
let horseAnimationInterval = null;
const frameWidth = 900;

function easeOutCubic(t) {
    return (--t) * t * t + 1;
}

function animateBackground() {
    if (!animationRunning) {
        animationRequested = false;
        return;
    }

    if (currentSpeed > 0) {
        backgroundPositionX -= currentSpeed;
        const canvas = document.querySelector(".background");
        canvas.style.backgroundPosition = backgroundPositionX + "px 0";
    }

    if (animationRequested) {
        requestAnimationFrame(animateBackground);
    }
}

function adjustBackgroundSpeed(horsepower) {
    const speedFactor = 5;
    currentSpeed = speedFactor * (horsepower / maxHorsepower);
    
    if (horsepower > 0 && !animationRunning) {
        animationRunning = true;
        animationRequested = true;
        animateBackground();
        updateHorseSpriteInterval(horsepower);
    } else if (horsepower <= 0) {
        currentSpeed = 0;
        animationRunning = false;
        backgroundPositionX = 0;
        const canvas = document.querySelector(".background");
        canvas.style.backgroundPosition = "0 0";
    }
}

function updateHorseSprite() {
    let columns = 5;
    let yOffset = Math.floor(currentFrame / columns) * 606;
    let xOffset = (currentFrame % columns) * frameWidth;

    document.getElementById('horseAnimation').style.backgroundPosition = `-${xOffset}px -${yOffset}px`;
    currentFrame = (currentFrame + 1) % 6;
}

function updateHorseSpriteInterval(horsepower) {
    // Clear existing interval
    if (horseAnimationInterval) {
        clearInterval(horseAnimationInterval);
    }

    const baseInterval = 1000;
    const easedHorsepower = easeOutCubic(horsepower / maxHorsepower);
    const newInterval = baseInterval / easedHorsepower;

    horseAnimationInterval = setInterval(updateHorseSprite, newInterval);
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
