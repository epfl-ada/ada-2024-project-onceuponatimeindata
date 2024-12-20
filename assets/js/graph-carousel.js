document.addEventListener("DOMContentLoaded", function () {
    const graphFrame = document.getElementById("graph-frame");
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");
    const playPauseButton = document.getElementById("play-pause-button");
  
    const graphs = [
      `${baseurl}/results/revenu/revenu1.html`,
      `${baseurl}/results/revenu/revenu2.html`,
      `${baseurl}/results/revenu/revenu3.html`,
      `${baseurl}/results/revenu/revenu4.html`,
      `${baseurl}/results/revenu/revenu5.html`,
    ];
  
    let currentIndex = 0;
    let isPlaying = false;
    let intervalId = null;
  
    function showGraph(index) {
      if (index >= 0 && index < graphs.length) {
        graphFrame.src = graphs[index];
        currentIndex = index;
      }
    }
  
    prevButton.addEventListener("click", () => {
      const newIndex = (currentIndex - 1 + graphs.length) % graphs.length;
      showGraph(newIndex);
    });
  
    nextButton.addEventListener("click", () => {
      const newIndex = (currentIndex + 1) % graphs.length;
      showGraph(newIndex);
    });
  
    playPauseButton.addEventListener("click", () => {
      if (isPlaying) {
        clearInterval(intervalId);
        playPauseButton.textContent = "Play";
      } else {
        intervalId = setInterval(() => {
          const newIndex = (currentIndex + 1) % graphs.length;
          showGraph(newIndex);
        }, 1000);
        playPauseButton.textContent = "Pause";
      }
      isPlaying = !isPlaying;
    });
  
    // Initialize the first graph
    showGraph(0);
  });