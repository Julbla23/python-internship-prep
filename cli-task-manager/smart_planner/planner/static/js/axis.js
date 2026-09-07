function updateLinePosition() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const currentMinutes = hours * 60 + minutes;
    const line = document.querySelector(".current-time-line");
    const warning = document.querySelector(".axis-warning");

        if (currentMinutes < 300) {
            warning.textContent = "Dzień zaczyna się o 5:00";
            line.style.display = "none";
            return;
        } else  if (currentMinutes >= 1200) {
             warning.textContent = "Dzień już się skończył";
             line.style.display = "none";
             return;
        }
    warning.textContent = "";
    line.style.display = "block";
    const pastMinutes = currentMinutes - 300;
    const percentage = pastMinutes / 900 * 100;
    line.style.top = percentage + "%";
}
updateLinePosition();
setInterval(updateLinePosition, 60000);