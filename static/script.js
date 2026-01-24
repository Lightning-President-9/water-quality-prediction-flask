function runPrediction() {
    const year = document.getElementById("year").value;
    const station = document.getElementById("station").value;

    fetch(`/predict?year=${year}&station_id=${station}`)
        .then(res => {
            if (!res.ok) throw new Error("Invalid response");
            return res.json();
        })
        .then(data => {
            renderTable(data.table);

            Plotly.newPlot("radarChart", JSON.parse(data.radar));

            const gaugeDiv = document.getElementById("gaugeCharts");
            gaugeDiv.innerHTML = "";
            data.gauges.forEach(fig => {
                const d = document.createElement("div");
                gaugeDiv.appendChild(d);
                Plotly.newPlot(d, JSON.parse(fig));
            });

            const bulletDiv = document.getElementById("bulletCharts");
            bulletDiv.innerHTML = "";
            data.bullets.forEach(fig => {
                const d = document.createElement("div");
                bulletDiv.appendChild(d);
                Plotly.newPlot(d, JSON.parse(fig));
            });
        })
        .catch(err => {
            console.error(err);
            alert("Prediction failed. Check inputs.");
        });
}

function renderTable(rows) {
    let html = `
    <table class="data-table">
        <tr>
            <th>Pollutant</th>
            <th>Predicted</th>
            <th>Limit</th>
            <th>Status</th>
        </tr>`;

    rows.forEach(r => {
        const status = r.Predicted > r.Limit ? "Unsafe" : "Safe";
        const cls = status === "Unsafe" ? "bad" : "good";
        html += `
        <tr>
            <td>${r.Pollutant}</td>
            <td>${r.Predicted.toFixed(2)}</td>
            <td>${r.Limit}</td>
            <td class="${cls}">${status}</td>
        </tr>`;
    });

    html += "</table>";
    document.getElementById("table").innerHTML = html;
}