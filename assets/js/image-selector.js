// Images for the original comparison
const images = [
    { name: "Fast and Furious", path: `${baseurl}/assets/images/fast-and-furious.jpg` },
    { name: "Harry Potter", path: `${baseurl}/assets/images/harry_potter.jpg` },
    { name: "Indiana Jones", path: `${baseurl}/assets/images/indiana_jones.jpeg` },
];

// Images for the new comparison
const newImages = [
    { name: "New Image 1", path: `${baseurl}/assets/images/graph_test_1.png` },
    { name: "New Image 2", path: `${baseurl}/assets/images/graph_test_2.png` },
    { name: "New Image 3", path: `${baseurl}/assets/images/graph_test_3.png` },
];

// Function to initialize a dropdown and image pairing
function initializeImageSelector(selectorId, imageId, defaultImagePath, imagesSet) {
    const selector = document.getElementById(selectorId);
    const image = document.getElementById(imageId);

    // Debugging logs
    console.log("Selector ID:", selectorId);
    console.log("Image ID:", imageId);
    console.log("Default Image Path:", defaultImagePath);
    console.log("Images Set:", imagesSet);

    if (!selector || !image) {
        console.error("Selector or image not found:", selectorId, imageId);
        return;
    }

    imagesSet.forEach(img => {
        const option = document.createElement("option");
        option.value = img.path;
        option.textContent = img.name;

        if (img.path === defaultImagePath) {
            option.selected = true;
        }

        selector.appendChild(option);
    });

    selector.addEventListener("change", function () {
        console.log("Dropdown changed. New image source:", this.value);
        image.src = this.value;
    });
}

//Ensure the DOM is fully loaded before running the script

document.addEventListener("DOMContentLoaded", function () {
    // Initialize for the single image selector
    initializeImageSelector(
        "image-selector-single",
        "selected-image-single",
        `${baseurl}/assets/images/fast-and-furious.jpg`,
        images
    );

    // Initialize for the original comparison section
    initializeImageSelector(
        "image-selector-left",
        "selected-image-left",
        `${baseurl}/assets/images/fast-and-furious.jpg`,
        images
    );
    initializeImageSelector(
        "image-selector-right",
        "selected-image-right",
        `${baseurl}/assets/images/harry_potter.jpg`,
        images
    );

    // Initialize for the new comparison section
    initializeImageSelector(
        "new-image-selector-left",
        "new-selected-image-left",
        `${baseurl}/assets/images/graph_test_1.png`,
        newImages
    );
    initializeImageSelector(
        "new-image-selector-right",
        "new-selected-image-right",
        `${baseurl}/assets/images/graph_test_2.png`,
        newImages
    );
});