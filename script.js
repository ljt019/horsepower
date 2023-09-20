let backgroundPositionX = 0;
let currentSpeed = 0;
const maxHorsepower = 1.12;
let animationRunning = false;
let currentFrame = 0;
const frameWidth = 900;  // Replace with your frame width

function animateBackground() {
    if (!animationRunning) {
        return;  // Stops the loop
    }
    backgroundPositionX -= currentSpeed;
    const canvas = document.querySelector(".background");
    canvas.style.backgroundPosition = backgroundPositionX + "px 0";
    requestAnimationFrame(animateBackground);
}

function adjustBackgroundSpeed(horsepower) {
    const speedFactor = 5;
    currentSpeed = speedFactor * (horsepower / maxHorsepower);
    if (horsepower > 0) {
        animationRunning = true;
    } else {
        currentSpeed = 0;
        animationRunning = false;
    }
}

function updateHorseSprite() {
    let columns = 5; // Number of columns in the spritesheet
    let yOffset = Math.floor(currentFrame / columns) * 606; 
    let xOffset = (currentFrame % columns) * frameWidth;

    document.getElementById('horseAnimation').style.backgroundPosition = `-${xOffset}px -${yOffset}px`;
    currentFrame = (currentFrame + 1) % 6; 
}

// Periodically fetch horsepower value
setInterval(() => {
    fetch('http://localhost:5000/get_horsepower')
        .then(response => response.json())
        .then(data => {
            const horsepower = data.horsepower;
            adjustBackgroundSpeed(horsepower);

            // Display the horsepower value
            const horsepowerElem = document.getElementById('horsepowerValue');
            horsepowerElem.innerText = horsepower;
            
            // Update horse sprite
            updateHorseSprite();
        })
        .catch(error => {
            console.error("Error fetching or processing horsepower:", error);
        });
}, 1000);  // Check every second. Adjust as needed.
