function updateAnimationSpeed(horsepower) {
    // Adjust the animation duration based on horsepower
    const baseSpeed = 20; // This can be adjusted
    const newDuration = baseSpeed / horsepower + "s";
    
    const background = document.querySelector(".background");
    background.style.animationDuration = newDuration;
}

// Periodically fetch horsepower value
setInterval(() => {
    fetch('http://localhost:5000/get_horsepower')
        .then(response => {
            // Log the raw response for debugging
            return response.text().then(text => {
                console.log("Raw response:", text);  // Log raw response
                return JSON.parse(text);  // Try parsing
            });
        })
        .then(data => {
            // Logging the parsed data for further verification
            console.log("Parsed data:", data);
            console.log("Fetched data:", data);

            const horsepower = data.horsepower;

            // Display the horsepower value
            const horsepowerElem = document.getElementById('horsepowerValue');
            horsepowerElem.innerText = horsepower;

            updateAnimationSpeed(horsepower);
            
            // If horsepower is 0, pause the gif and background
            if (horsepower === 0) {
                document.getElementById("horseGif").style.animationPlayState = "paused";
                document.querySelector(".background").style.animationPlayState = "paused";
            } else {
                document.getElementById("horseGif").style.animationPlayState = "running";
                document.querySelector(".background").style.animationPlayState = "running";
            }
        })
        .catch(error => {
            console.error("Error fetching or processing horsepower:", error);
        });
}, 1000); // Check every second. Adjust as needed.


