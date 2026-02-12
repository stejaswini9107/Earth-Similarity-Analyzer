import pandas as pd
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
data = pd.read_csv(
    "planets.csv",
    engine="python",
    sep=",",
    comment="#"
)
cols = ["pl_name", "pl_rade", "pl_bmasse", "pl_orbper", "st_teff"]
data = data[cols].dropna()
EARTH = {
    "pl_rade": 1.0,
    "pl_bmasse": 1.0,
    "pl_orbper": 365.0,
    "st_teff": 5778
}
def similarity_score(p):
    score = 0
    for key in EARTH:
        score += abs(p[key] - EARTH[key]) / EARTH[key]
    return round(100 / (1 + score), 2)
def find_planet(name):
    planet = data[data["pl_name"].str.lower() == name.lower()]
    if planet.empty:
        return None
    return planet.iloc[0]
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/compare")
def compare():
    name = request.args.get("planet")
    if not name:
        return jsonify({"error": "No planet name provided"})
    planet = find_planet(name)
    if planet is None:
        return jsonify({"error": "Planet not found in dataset"})
    score = similarity_score(planet)
    return jsonify({
        "planet": planet["pl_name"],
        "similarity": score,
        "radius": round(planet["pl_rade"], 2),
        "mass": round(planet["pl_bmasse"], 2),
        "orbit": round(planet["pl_orbper"], 2),
        "star_temp": int(planet["st_teff"])
    })
if __name__ == "__main__":
    app.run(debug=True)