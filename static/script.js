document.addEventListener("DOMContentLoaded", function () {

    // ---------- CHART DATA ----------
    const dataScript = document.getElementById("chart-data");
    if (!dataScript) return;

    let chartData;
    try {
        chartData = JSON.parse(dataScript.textContent || "{}");
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

    // ---------- PIE CHART ----------
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

    // ---------- LINE CHART ----------
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

    // ---------- 🔥 SUSPICIOUS IP POPUP ----------
    const alertScript = document.getElementById("alert-data");

    if (alertScript) {
        try {
            const suspicious = JSON.parse(alertScript.textContent || "[]");

            if (Array.isArray(suspicious) &&
                suspicious.length > 0 &&
                !sessionStorage.getItem("shownIPAlert")) {

                let message = "⚠️ Suspicious IP Detected\n------------------------\n";

                // Show only first 5 IPs
suspicious.slice(0, 5).forEach(ip => {
    message += `IP: ${ip[0]} | Attempts: ${ip[1]}\n`;
});

// If more than 5, show summary
if (suspicious.length > 5) {
    message += `\n+${suspicious.length - 5} more...`;
}

                alert(message);
                sessionStorage.setItem("shownIPAlert", "true");
            }

        } catch (e) {
            console.error("Alert data error:", e);
        }
    }

    // ---------- 🚨 HIGH RISK BANNER ----------
    const hasHighRisk = Array.from(document.querySelectorAll(".log-row"))
        .some(row => {
            const risk = (row.getAttribute("data-risk") || "").toUpperCase();
            return risk === "HIGH" || risk === "CRITICAL";
        });

    if (hasHighRisk && !sessionStorage.getItem("shownHighRiskAlert")) {
        const banner = document.createElement("div");

        banner.textContent = "⚠️ High Risk Attack Detected!";
        banner.style.background = "linear-gradient(90deg, red, darkred)";
        banner.style.fontWeight = "bold";
        banner.style.fontSize = "18px";
        banner.style.color = "white";
        banner.style.padding = "10px";
        banner.style.textAlign = "center";

        document.body.prepend(banner);
        sessionStorage.setItem("shownHighRiskAlert", "true");
    }

});


// ---------- 🌍 MAP FUNCTION ----------
function showLocationOnMap(ip) {

    const mapFrame = document.getElementById("mapFrame");
    const mapContainer = document.getElementById("mapContainer");

    if (!mapFrame || !mapContainer) return;

    fetch(`https://ip-api.com/json/${ip}`)
        .then(res => res.json())
        .then(data => {

            if (data.status === "success") {

                const lat = data.lat;
                const lon = data.lon;

                mapFrame.src = `https://www.google.com/maps?q=${lat},${lon}&z=5&output=embed`;

                const locationText = document.getElementById("locationText");
                if (locationText) {
                    locationText.innerHTML =
                        `Location: ${data.city}, ${data.country} <br>ISP: ${data.isp}`;
                }

                mapContainer.scrollIntoView({ behavior: "smooth" });

            } else {
                alert("Location not found");
            }

        })
        .catch(() => {
            alert("Error fetching location");
        });
}


// ---------- 🎯 ROW HIGHLIGHT ----------
function highlightRow(row) {
    document.querySelectorAll(".log-row").forEach(r => {
        r.style.background = "";
    });

    row.style.background = "#003333";
}


// ---------- 📥 DOWNLOAD CSV ----------
function downloadCSV() {
    window.location.href = "/download";
}


// ---------- 🔄 RESET ALERT FLAGS ----------
window.addEventListener("beforeunload", () => {
    sessionStorage.removeItem("shownIPAlert");
    sessionStorage.removeItem("shownHighRiskAlert");
});