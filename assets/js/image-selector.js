const images = [
    { name: "Fast and Furious", path: `${baseurl}/assets/images/fast-and-furious.jpg` },
    { name: "Harry Potter", path: `${baseurl}/assets/images/harry_potter.jpg` },
    { name: "Indiana Jones", path: `${baseurl}/assets/images/indiana_jones.jpeg` },
];

// Function to initialize a dropdown and image pairing
function initializeImageSelector(selectorId, imageId, defaultImagePath) {
    const selector = document.getElementById(selectorId);
    const image = document.getElementById(imageId);

    // Check if the selector and image exist to avoid errors
    if (!selector || !image) return;

    // Populate the dropdown
    images.forEach(img => {
        const option = document.createElement("option");
        option.value = img.path;
        option.textContent = img.name;

        // Set the default selected option based on the initial image
        if (img.path === defaultImagePath) {
            option.selected = true;
        }

        selector.appendChild(option);
    });

    // Update the image on dropdown change
    selector.addEventListener("change", function () {
        image.src = this.value;
    });
}

// Initialize for single image
initializeImageSelector("image-selector-single", "selected-image-single", `${baseurl}/assets/images/fast-and-furious.jpg`);

// Initialize for side-by-side comparison
initializeImageSelector("image-selector-left", "selected-image-left", `${baseurl}/assets/images/fast-and-furious.jpg`);
initializeImageSelector("image-selector-right", "selected-image-right", `${baseurl}/assets/images/harry_potter.jpg`);