document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed - Carousel initialization started.");

    const carousel = document.querySelector(".carousel");
    const images = Array.from(carousel.querySelectorAll("img"));

    console.log("Carousel element found:", carousel);
    console.log("Images found in carousel:", images);

    // Clone images for seamless effect
    const totalImages = images.length;
    images.forEach((img) => {
        const clone = img.cloneNode(true);
        carousel.appendChild(clone);
    });

    // Set up scrolling variables
    let scrollInterval;
    const scrollSpeed = 2; // Adjust speed (pixels per interval)

    const seamlessScroll = () => {
        // Reset to the middle of the scroll to create the illusion of infinite scrolling
        if (carousel.scrollLeft >= carousel.scrollWidth - carousel.clientWidth) {
            console.log("Reached the end. Resetting to the middle for seamless loop.");
            carousel.scrollLeft = carousel.scrollWidth / 2 - carousel.clientWidth;
        } else if (carousel.scrollLeft <= 0) {
            console.log("Reached the beginning. Resetting to the middle for seamless loop.");
            carousel.scrollLeft = carousel.scrollWidth / 2;
        }
    };

    // Start scrolling
    const startScroll = (direction) => {
        console.log("Starting scroll in direction:", direction);

        stopScroll(); // Stop any existing interval
        scrollInterval = setInterval(() => {
            const scrollAmount = direction === "left" ? -scrollSpeed : scrollSpeed;
            carousel.scrollLeft += scrollAmount;

            // Handle seamless looping
            seamlessScroll();

            console.log("Current scrollLeft:", carousel.scrollLeft);
        }, 16); // ~60fps
    };

    const stopScroll = () => {
        console.log("Stopping scroll.");
        clearInterval(scrollInterval);
    };

    // Mouse hover logic for direction
    const carouselContainer = document.querySelector(".carousel-container");
    console.log("Carousel container found:", carouselContainer);

    carouselContainer.addEventListener("mousemove", (event) => {
        const x = event.clientX - carouselContainer.getBoundingClientRect().left;
        console.log("Mouse position (relative to container):", x);

        if (x < carouselContainer.clientWidth / 2) {
            console.log("Mouse is on the left side. Scrolling left.");
            startScroll("left");
        } else {
            console.log("Mouse is on the right side. Scrolling right.");
            startScroll("right");
        }
    });

    carouselContainer.addEventListener("mouseleave", () => {
        console.log("Mouse left the carousel container. Stopping scroll.");
        stopScroll();
    });

    // Set initial position to the middle for seamless effect
    carousel.scrollLeft = carousel.scrollWidth / 2 - carousel.clientWidth;

    console.log("Carousel initialization completed.");
});