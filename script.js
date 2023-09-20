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

// Fetch horsepower value periodically
setInterval(() => {
    fetch('http://localhost:5000/get_horsepower')
        .then(response => response.json())
        .then(data => {
            const horsepower = data.horsepower;
            adjustBackgroundSpeed(horsepower);

            // Display the horsepower value
            const horsepowerElem = document.getElementById('horsepowerValue');
            horsepowerElem.innerText = horsepower;
        })
        .catch(error => {
            console.error("Error fetching or processing horsepower:", error);
        });
}, 1000);