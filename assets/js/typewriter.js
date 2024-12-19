// function to animate text typewriter effect

document.addEventListener("DOMContentLoaded", function () {
    const typewriterLinks = document.querySelectorAll(".typewriter");

    typewriterLinks.forEach(link => {
        const text = link.getAttribute("data-title");
        link.textContent = ""; // Clear initial text
        let index = 0;

        function type() {
            if (index < text.length) {
                link.textContent += text.charAt(index);
                index++;
                setTimeout(type, 100); // Adjust typing speed here (100ms per letter)
            }
        }

        type();
    });
});

