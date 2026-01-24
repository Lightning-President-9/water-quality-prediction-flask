from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# LOAD MODEL
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

POLLUTANTS = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
LIMITS = {
    'O2': 5,
    'NO3': 10,
    'NO2': 0.1,
    'SO4': 250,
    'PO4': 0.1,
    'CL': 250
}

# ROUTES
@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/predict", methods=["GET"])
def predict():
    # READ QUERY PARAMS (GET)
    year = request.args.get("year", type=int)
    station_id = request.args.get("station_id", type=int)

    # VALIDATION
    if year is None or station_id is None:
        return jsonify({"error": "Missing parameters"}), 400

    if year < 1000 or year > 9999:
        return jsonify({"error": "Year must be 4 digits"}), 400

    if station_id < 1 or station_id > 22:
        return jsonify({"error": "Station ID must be between 1 and 22"}), 400

    # MODEL INPUT
    X = pd.DataFrame({
        "year": [year],
        "id": [str(station_id)]
    })

    X = pd.get_dummies(X, columns=["id"])

    for col in model_cols:
        if col not in X.columns:
            X[col] = 0

    X = X[model_cols]

    # PREDICTION
    try:
        prediction = model.predict(X)[0]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    df = pd.DataFrame({
        "Pollutant": POLLUTANTS,
        "Predicted": prediction,
        "Limit": [LIMITS[p] for p in POLLUTANTS]
    })

    # RADAR (NORMALIZED)
    df["Normalized"] = df["Predicted"] / df["Limit"]

    radar_fig = px.line_polar(
        df,
        r="Normalized",
        theta="Pollutant",
        line_close=True,
        range_r=[0, 2],
        title="Normalized Radar (Predicted / Limit)"
    )

    radar_fig.update_traces(fill="toself", line_color="red")
    radar_fig.update_layout(
        paper_bgcolor="#0d1117",
        polar=dict(bgcolor="#0d1117"),
        font=dict(color="white")
    )

    # GAUGES & BULLETS
    gauges = []
    bullets = []

    for _, r in df.iterrows():
        # Gauge
        g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=r["Predicted"],
            title={"text": r["Pollutant"]},
            gauge={
                "axis": {"range": [0, r["Limit"] * 2]},
                "bar": {"color": "red" if r["Predicted"] > r["Limit"] else "blue"},
                "steps": [
                    {"range": [0, r["Limit"]], "color": "#9ef79e"},
                    {"range": [r["Limit"], r["Limit"] * 2], "color": "#ff8a80"}
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "value": r["Limit"]
                }
            }
        ))
        g.update_layout(height=250, paper_bgcolor="#0d1117", font=dict(color="white"))
        gauges.append(g.to_json())

        # Bullet
        b = go.Figure()
        b.add_bar(x=[r["Limit"] * 3], y=[r["Pollutant"]],
                  orientation="h", marker=dict(color="#e0e0e0"), showlegend=False)
        b.add_bar(x=[r["Limit"]], y=[r["Pollutant"]],
                  orientation="h", marker=dict(color="#9ef79e"), showlegend=False)
        b.add_scatter(x=[r["Predicted"]], y=[r["Pollutant"]],
                      mode="markers",
                      marker=dict(size=12, color="red" if r["Predicted"] > r["Limit"] else "blue"),
                      name="Predicted",
                      showlegend=True
                      )
        b.update_layout(
            xaxis=dict(range=[0, r["Limit"] * 3]),
            height=120,
            margin=dict(l=60, r=20, t=20, b=20),
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(color="white")
        )
        bullets.append(b.to_json())

    # RESPONSE
    return jsonify({
        "table": df[["Pollutant", "Predicted", "Limit"]].to_dict("records"),
        "radar": radar_fig.to_json(),
        "gauges": gauges,
        "bullets": bullets
    })

# MAIN
if __name__ == "__main__":
    app.run(debug=True)