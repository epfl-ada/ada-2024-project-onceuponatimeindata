// Iframes for the selector
const iframes = [
    { name: "Absolute - Box office per year", path: `${baseurl}/results/box_office_absolute.html` },
    { name: "Average - Box office per year", path: `${baseurl}/results/average_box_office_revenue.html` },
];

// Function to initialize a dropdown and iframe pairing
function initializeIframeSelector(selectorId, iframeId, defaultIframePath, iframesSet) {
    const selector = document.getElementById(selectorId);
    const iframe = document.getElementById(iframeId);

    if (!selector || !iframe) {
        console.error("Selector or iframe not found:", selectorId, iframeId);
        return;
    }

    // Populate the dropdown
    iframesSet.forEach(frame => {
        const option = document.createElement("option");
        option.value = frame.path;
        option.textContent = frame.name;

        if (frame.path === defaultIframePath) {
            option.selected = true;
        }

        selector.appendChild(option);
    });

    // Set initial iframe source
    iframe.src = defaultIframePath;

    // Update iframe on dropdown change
    selector.addEventListener("change", function () {
        iframe.src = this.value;
    });
}

// Ensure the DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", function () {
    initializeIframeSelector(
        "iframe-selector",       // Dropdown ID
        "selected-iframe",       // Iframe ID
        `${baseurl}/results/box_office_absolute.html`, // Default iframe path
        iframes                 // Set of iframes
    );
});