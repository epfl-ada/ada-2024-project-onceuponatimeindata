document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const currentMode = localStorage.getItem("darkMode");

    // Apply saved mode
    if (currentMode === "enabled") {
        document.body.classList.add("dark-mode");
    }

    // Set initial button text based on the mode
    toggleButton.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";

    // Toggle dark mode on button click
    toggleButton.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        const isDarkMode = document.body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", isDarkMode ? "enabled" : "disabled");

        // Update the button text
        toggleButton.textContent = isDarkMode ? "☀️" : "🌙";
    });
});