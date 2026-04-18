from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODELS
# =========================
heart_model = joblib.load("../models/heart_best.pkl")
diabetes_model = joblib.load("../models/diabetes_best.pkl")
stroke_model = joblib.load("../models/stroke_best.pkl")

heart_scaler = joblib.load("../models/heart_scaler.pkl")
diabetes_scaler = joblib.load("../models/diabetes_scaler.pkl")
stroke_scaler = joblib.load("../models/stroke_scaler.pkl")

# =========================
# FEATURE ORDER
# =========================
heart_features = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal"
]

diabetes_features = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

stroke_features = list(stroke_scaler.feature_names_in_)

# =========================
# RISK LEVEL
# =========================
def get_risk_level(prob):
    if prob < 0.3:
        return "Low"
    elif prob < 0.7:
        return "Medium"
    else:
        return "High"

# =========================
# STROKE ENCODER
# =========================
def encode_stroke_input(data):
    encoded = {}

    # Numerical
    encoded["age"] = data["age"]
    encoded["hypertension"] = data["hypertension"]
    encoded["heart_disease"] = data["heart_disease"]
    encoded["avg_glucose_level"] = data["avg_glucose_level"]
    encoded["bmi"] = data["bmi"]

    # Binary
    encoded["gender_Male"] = 1 if data["gender"] == "Male" else 0
    encoded["ever_married_Yes"] = 1 if data["ever_married"] == "Yes" else 0
    encoded["Residence_type_Urban"] = 1 if data["Residence_type"] == "Urban" else 0

    # Work type
    for wt in ["Private", "Self-employed", "Govt_job"]:
        encoded[f"work_type_{wt}"] = 1 if data["work_type"] == wt else 0

    # Smoking
    for sm in ["formerly smoked", "never smoked", "smokes"]:
        encoded[f"smoking_status_{sm}"] = 1 if data["smoking_status"] == sm else 0

    return encoded

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "MediScope AI ML API Running"

# =========================
# HEART
# =========================
@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    data = request.json

    features = pd.DataFrame(
    [[data[f] for f in heart_features]],
    columns=heart_features
)

    features = heart_scaler.transform(features)

    pred = heart_model.predict(features)[0]
    prob = heart_model.predict_proba(features)[0][1]

    return jsonify({
        "disease": "heart",
        "prediction": int(pred),
        "risk_score": round(float(prob), 2),
        "risk_level": get_risk_level(prob)
    })

# =========================
# DIABETES
# =========================
@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    data = request.json

    features = pd.DataFrame(
    [[data[f] for f in heart_features]],
    columns=heart_features
)

    pred = diabetes_model.predict(features)[0]
    prob = diabetes_model.predict_proba(features)[0][1]

    return jsonify({
        "disease": "diabetes",
        "prediction": int(pred),
        "risk_score": round(float(prob), 2),
        "risk_level": get_risk_level(prob)
    })

# =========================
# STROKE (SMART INPUT)
# =========================
@app.route("/predict/stroke", methods=["POST"])
def predict_stroke():
    data = request.json

    encoded = encode_stroke_input(data)

    features = pd.DataFrame(
    [[data[f] for f in heart_features]],
    columns=heart_features
)

    pred = stroke_model.predict(features)[0]
    prob = stroke_model.predict_proba(features)[0][1]

    return jsonify({
        "disease": "stroke",
        "prediction": int(pred),
        "risk_score": round(float(prob), 2),
        "risk_level": get_risk_level(prob)
    })

# =========================
# 🔥 UNIFIED API
# =========================
@app.route("/predict/all", methods=["POST"])
def predict_all():
    data = request.json

    # HEART
    h_feat = np.array([data["heart"][f] for f in heart_features]).reshape(1, -1)
    h_feat = heart_scaler.transform(h_feat)
    h_prob = heart_model.predict_proba(h_feat)[0][1]

    # DIABETES
    d_feat = np.array([data["diabetes"][f] for f in diabetes_features]).reshape(1, -1)
    d_feat = diabetes_scaler.transform(d_feat)
    d_prob = diabetes_model.predict_proba(d_feat)[0][1]

    # STROKE
    s_encoded = encode_stroke_input(data["stroke"])
    s_feat = np.array([s_encoded.get(f, 0) for f in stroke_features]).reshape(1, -1)
    s_feat = stroke_scaler.transform(s_feat)
    s_prob = stroke_model.predict_proba(s_feat)[0][1]

    return jsonify({
        "heart": {
            "risk_score": round(float(h_prob), 2),
            "risk_level": get_risk_level(h_prob)
        },
        "diabetes": {
            "risk_score": round(float(d_prob), 2),
            "risk_level": get_risk_level(d_prob)
        },
        "stroke": {
            "risk_score": round(float(s_prob), 2),
            "risk_level": get_risk_level(s_prob)
        }
    })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)