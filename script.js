async function predictTemperature() {
    const humidity = humidityInput = document.getElementById("humidity").value;
    const wind = document.getElementById("wind").value;
    const pressure = document.getElementById("pressure").value;

    if (!humidity || !wind || !pressure) {
        alert("Please fill all fields");
        return;
    }

    document.getElementById("loader").style.display = "block";
    document.getElementById("result").style.display = "none";
    document.getElementById("predictBtn").disabled = true;

    // ⏳ 5 second futuristic delay
    setTimeout(async () => {
        try {
            // Using relative path so it automatically works locally and on Render
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    humidity: Number(humidity),
                    wind_speed: Number(wind),
                    meanpressure: Number(pressure)
                })
            });

            const data = await response.json();

            document.getElementById("loader").style.display = "none";
            document.getElementById("result").style.display = "block";
            document.getElementById("predictBtn").disabled = false;

            let resultHTML = `<h4>🌡️ Predicted Temperatures:</h4><div class="models-grid">`;
            for (const [modelName, temp] of Object.entries(data.predictions)) {
                resultHTML += `
                <div class="model-item">
                    <span class="model-name">${modelName}</span>
                    <span class="model-temp">${temp} °C</span>
                </div>`;
            }
            resultHTML += `</div>`;

            document.getElementById("result").innerHTML = resultHTML;

        } catch (error) {
            alert("❌ Error connecting to AI server");
            document.getElementById("loader").style.display = "none";
            document.getElementById("predictBtn").disabled = false;
        }
    }, 5000);
}