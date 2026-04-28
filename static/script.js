document.addEventListener("DOMContentLoaded", function () {

    const dataScript = document.getElementById("chart-data");
    if (!dataScript) return;

    let chartData;
    try {
        chartData = JSON.parse(dataScript.textContent);
    } catch {
        console.error("Invalid JSON data");
        return;
    }

    const labels = chartData.labels || [];
    const values = chartData.values || [];

    // PIE
    const pieCanvas = document.getElementById("pieChart");
    if (pieCanvas) {
        new Chart(pieCanvas.getContext("2d"), {
            type: "pie",
            data: {
                labels,
                datasets: [{
                    data: values,
                    backgroundColor: labels.map(() =>
                        `hsl(${Math.random() * 360}, 70%, 50%)`
                    )
                }]
            }
        });
    }

    // LINE
    const lineCanvas = document.getElementById("lineChart");
    if (lineCanvas) {
        new Chart(lineCanvas.getContext("2d"), {
            type: "line",
            data: {
                labels: ["12PM", "2PM", "4PM", "6PM", "8PM"],
                datasets: [{
                    label: "Attack Trend",
                    data: [10, 30, 50, 40, 60],
                    borderColor: "cyan",
                    fill: false
                }]
            }
        });
    }

});