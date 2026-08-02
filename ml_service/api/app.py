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
# HEART XAI & SIMULATION HELPERS (PHASE 5 & 6)
# =========================
def generate_heart_insights(data, prob):
    alert = ""
    trestbps = float(data.get("trestbps", 120))
    chol = float(data.get("chol", 200))
    age = float(data.get("age", 50))
    cp = int(data.get("cp", 0))
    thalach = float(data.get("thalach", 150))

    if prob >= 0.65 or trestbps >= 170 or chol >= 300:
        alert = "🚨 CRITICAL CLINICAL ALERT: High cardiovascular risk detected with significant metabolic or arterial pressure elevation. Urgent clinical consultation and ECG diagnostic evaluation are strongly recommended."
    elif prob >= 0.35 or trestbps >= 140 or chol >= 240:
        alert = "⚠️ PREVENTIVE WARNING: Moderate cardiovascular risk profile observed. Advised to schedule routine medical screening, monitor lipid profile, and adopt targeted diet and exercise interventions."
    else:
        alert = "🟢 FAVORABLE CARDIOVASCULAR PROFILE: Evaluated biometric parameters remain stable within low-risk thresholds. Continue maintaining healthy diet, hydration, and regular aerobic activity."

    xai = []

    if trestbps >= 140:
        xai.append({"factor": "Resting Blood Pressure", "value": f"{trestbps} mmHg", "status": "Hypertensive Stage", "impact": "High", "description": "Elevated systolic pressure puts severe structural strain on arterial walls and increases myocardial cardiac workload."})
    elif trestbps >= 120:
        xai.append({"factor": "Resting Blood Pressure", "value": f"{trestbps} mmHg", "status": "Pre-hypertensive", "impact": "Medium", "description": "Slightly elevated arterial pressure requiring preventive nutritional and fitness intervention."})

    if chol >= 240:
        xai.append({"factor": "Serum Cholesterol", "value": f"{chol} mg/dl", "status": "High (Hypercholesterolemia)", "impact": "High", "description": "Elevated serum lipid concentration accelerates atherosclerotic coronary plaque progression."})
    elif chol >= 200:
        xai.append({"factor": "Serum Cholesterol", "value": f"{chol} mg/dl", "status": "Borderline High", "impact": "Medium", "description": "Moderate lipid levels contributing to cumulative arterial plaque formation."})

    if cp in [0, 1, 2]:
        cp_map = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal Pain"}
        xai.append({"factor": "Chest Pain Symptoms", "value": cp_map.get(cp, "Reported Pain"), "status": "Symptomatic", "impact": "High", "description": "Reported chest discomfort suggests possible transient myocardial oxygen demand mismatch."})

    if age >= 60:
        xai.append({"factor": "Demographic Age", "value": f"{age} years", "status": "Significant Factor", "impact": "Medium", "description": "Age-related physiological reduction in vascular compliance and elasticity."})
    elif age >= 45:
        xai.append({"factor": "Demographic Age", "value": f"{age} years", "status": "Moderate Factor", "impact": "Low", "description": "Entering demographic baseline where coronary disease incidence gradually climbs."})

    if thalach <= 110:
        xai.append({"factor": "Max Heart Rate", "value": f"{thalach} bpm", "status": "Suboptimal Reserve", "impact": "Medium", "description": "Reduced maximal cardiac output and chronotropic response during physical strain."})

    if not xai:
        xai.append({"factor": "Biometric & Vital Profile", "value": "Within Reference Limits", "status": "Optimal", "impact": "Low", "description": "Primary clinical diagnostic inputs correspond with standard cardiac equilibrium."})

    recommendations = [
        "Conduct consistent blood pressure monitoring (target resting systolic level < 120 mmHg).",
        "Incorporate a Mediterranean dietary structure emphasizes dietary fiber, healthy omega fatty acids, and low sodium (< 2g/day).",
        "Perform a minimum of 150 minutes per week of sustained moderate aerobic physical training.",
        "Consult a practicing physician or cardiologist before modifying existing medication, supplements, or clinical regimens."
    ]

    return alert, xai, recommendations

def calculate_heart_prob_for(data_dict):
    features = pd.DataFrame(
        [[float(data_dict.get(f, 0)) for f in heart_features]],
        columns=heart_features
    )
    features_scaled = heart_scaler.transform(features)
    prob = heart_model.predict_proba(features_scaled)[0][1]
    return float(prob)

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
# HEART (PHASE 5 & 6 ENABLED)
# =========================
@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    data = request.json

    prob = calculate_heart_prob_for(data)
    pred = 1 if prob >= 0.5 else 0

    alert, xai, recommendations = generate_heart_insights(data, prob)

    # Core Innovation: Clinical Scenario Simulations
    untreated_data = dict(data)
    untreated_data["trestbps"] = min(float(untreated_data.get("trestbps", 120)) + 20.0, 210.0)
    untreated_data["chol"] = min(float(untreated_data.get("chol", 200)) + 45.0, 500.0)
    untreated_prob = calculate_heart_prob_for(untreated_data)

    treated_data = dict(data)
    treated_data["trestbps"] = min(float(treated_data.get("trestbps", 120)), 118.0)
    treated_data["chol"] = min(float(treated_data.get("chol", 200)), 165.0)
    treated_data["thalach"] = max(float(treated_data.get("thalach", 150)), 155.0)
    treated_prob = calculate_heart_prob_for(treated_data)

    simulation = {
        "untreated": {
            "risk_score": round(float(untreated_prob), 2),
            "risk_level": get_risk_level(untreated_prob),
            "details": "Projected 3-5 year worsening trajectory without adherence to clinical guidelines (BP +20 mmHg, Chol +45 mg/dL)"
        },
        "treated": {
            "risk_score": round(float(treated_prob), 2),
            "risk_level": get_risk_level(treated_prob),
            "details": "Projected risk reduction with optimal target treatment and lifestyle intervention (BP ≤ 118 mmHg, Chol ≤ 165 mg/dL)"
        }
    }

    return jsonify({
        "disease": "heart",
        "prediction": int(pred),
        "risk_score": round(float(prob), 2),
        "risk_level": get_risk_level(prob),
        "smart_alert": alert,
        "xai_insights": xai,
        "recommendations": recommendations,
        "simulation": simulation
    })

# =========================
# DIABETES
# =========================
@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    data = request.json

    features = pd.DataFrame(
        [[float(data.get(f, 0)) for f in diabetes_features]],
        columns=diabetes_features
    )
    features_scaled = diabetes_scaler.transform(features)
    prob = diabetes_model.predict_proba(features_scaled)[0][1]
    pred = 1 if prob >= 0.5 else 0

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
        [[float(encoded.get(f, 0)) for f in stroke_features]],
        columns=stroke_features
    )
    features_scaled = stroke_scaler.transform(features)
    prob = stroke_model.predict_proba(features_scaled)[0][1]
    pred = 1 if prob >= 0.5 else 0

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