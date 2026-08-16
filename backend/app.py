"""
app.py
Flask API for the Employee Salary Prediction project.

Run with:  python app.py
Make sure salary_model.pkl (and the .pkl option files) already exist —
run train_model.py first if they don't.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # allows the HTML/JS frontend (opened as a local file) to call this API

# Load the trained model and dropdown options once, at startup
model = joblib.load("salary_model.pkl")
education_levels = joblib.load("education_levels.pkl")
job_roles = joblib.load("job_roles.pkl")
cities = joblib.load("cities.pkl")


@app.route("/options", methods=["GET"])
def get_options():
    """Returns the valid dropdown values, built from the training CSV."""
    return jsonify({
        "education_levels": education_levels,
        "job_roles": job_roles,
        "cities": cities
    })


@app.route("/predict", methods=["POST"])
def predict():
    """Takes experience/education/job_role/city and returns a predicted salary."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No input data received"}), 400

    try:
        experience = float(data["experience"])
        education = data["education"]
        job_role = data["job_role"]
        city = data["city"]
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Missing or invalid fields"}), 400

    # Build a single-row DataFrame matching the training column names/order
    input_df = pd.DataFrame([{
        "Experience_Years": experience,
        "Education_Level": education,
        "Job_Role": job_role,
        "City": city
    }])

    prediction = model.predict(input_df)[0]

    return jsonify({"predicted_salary": round(float(prediction), 2)})


if __name__ == "__main__":
    app.run(debug=False, port=5000)