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

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: "white" }
            }
        },
        scales: {
            x: {
                ticks: { color: "white" },
                grid: { color: "#333" }
            },
            y: {
                ticks: { color: "white" },
                grid: { color: "#333" }
            }
        }
    };

    // PIE
    const pieCanvas = document.getElementById("pieChart");
    if (pieCanvas) {
        new Chart(pieCanvas.getContext("2d"), {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ["#00ff88", "#ffaa00", "#ff3b3b"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
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
                    borderColor: "#00ffff",
                    backgroundColor: "rgba(0,255,255,0.1)",
                    tension: 0.4,
                    fill: true
                }]
            },
            options: commonOptions
        });
    }

});


// ✅ ADD YOUR FUNCTION HERE (OUTSIDE)
function showLocationOnMap(ip) {

    const mapFrame = document.getElementById("mapFrame");
    const mapContainer = document.getElementById("mapContainer");

    fetch(`http://ip-api.com/json/${ip}`)
        .then(res => res.json())
        .then(data => {

            if (data.status === "success") {

                const lat = data.lat;
                const lon = data.lon;

                mapFrame.src = `https://www.google.com/maps?q=${lat},${lon}&z=5&output=embed`;

                const locationText = document.getElementById("locationText");
                locationText.innerHTML = `Location: ${data.city}, ${data.country}`;

                mapContainer.scrollIntoView({ behavior: "smooth" });

            } else {
                alert("Location not found");
            }

        })
        .catch(() => {
            alert("Error fetching location");
        });
}
function highlightRow(row) {
    document.querySelectorAll(".log-row").forEach(r => {
        r.style.background = "";
    });

    row.style.background = "#003333";
}