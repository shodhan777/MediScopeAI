from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import torch
import json
import os
import sys

# Allow importing from parent directory for MTL modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing.mtl_adapter import map_heart_data, map_diabetes_data, map_stroke_data
from inference.mtl_model import get_mtl_model
from explainability.explainer import MTLExplainer
from explainability.baseline_explainer import (
    generate_logistic_insights,
    generate_tree_insights,
    generate_cds_recommendations,
    calculate_statistical_confidence
)
from uncertainty.estimator import get_mc_dropout_uncertainty, calculate_confidence
from calibration.calibrator import calibrate_prediction
from inference.selective_predictor import apply_selective_prediction

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
# (Phase 5/6 Heart Insights removed in favor of baseline_explainer)
# =========================

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

    features_df = pd.DataFrame([[float(data.get(f, 0)) for f in heart_features]], columns=heart_features)
    xai = generate_logistic_insights(heart_model, heart_scaler, features_df, data, heart_features)
    alert, recommendations = generate_cds_recommendations("heart", data, prob)
    confidence = calculate_statistical_confidence(prob)

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
        "confidence": confidence,
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

    xai = generate_tree_insights(diabetes_model, diabetes_scaler, features, data, diabetes_features)
    alert, recommendations = generate_cds_recommendations("diabetes", data, prob)
    confidence = calculate_statistical_confidence(prob)

    return jsonify({
        "disease": "diabetes",
        "prediction": int(pred),
        "risk_score": round(float(prob), 2),
        "risk_level": get_risk_level(prob),
        "confidence": confidence,
        "smart_alert": alert,
        "xai_insights": xai,
        "recommendations": recommendations
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

    xai = generate_logistic_insights(stroke_model, stroke_scaler, features, encoded, stroke_features)
    alert, recommendations = generate_cds_recommendations("stroke", data, prob)
    confidence = calculate_statistical_confidence(prob)

    return jsonify({
        "disease": "stroke",
        "prediction": int(pred),
        "risk_score": round(float(prob), 2),
        "risk_level": get_risk_level(prob),
        "confidence": confidence,
        "smart_alert": alert,
        "xai_insights": xai,
        "recommendations": recommendations
    })

def calculate_simulation_probability(disease, data):
    if disease == "heart":
        return calculate_heart_prob_for(data)

    if disease == "diabetes":
        features = pd.DataFrame(
            [[float(data.get(f, 0)) for f in diabetes_features]],
            columns=diabetes_features
        )
        scaled = diabetes_scaler.transform(features)
        return float(diabetes_model.predict_proba(scaled)[0][1])

    if disease == "stroke":
        encoded = encode_stroke_input(data)
        features = pd.DataFrame(
            [[float(encoded.get(f, 0)) for f in stroke_features]],
            columns=stroke_features
        )
        scaled = stroke_scaler.transform(features)
        return float(stroke_model.predict_proba(scaled)[0][1])

    raise ValueError(f"Unsupported disease: {disease}")

@app.route("/simulate/<disease>", methods=["POST"])
def simulate_risk(disease):
    payload = request.json or {}
    baseline = payload.get("baseline", payload)
    scenarios = payload.get("scenarios", {})

    if not isinstance(baseline, dict) or not isinstance(scenarios, dict):
        return jsonify({"error": "baseline and scenarios must be JSON objects"}), 400

    try:
        baseline_probability = calculate_simulation_probability(disease, baseline)
        results = {
            "baseline": {
                "risk_score": round(baseline_probability, 4),
                "risk_level": get_risk_level(baseline_probability),
                "risk_change": 0
            }
        }

        for name, changes in scenarios.items():
            if not isinstance(changes, dict):
                return jsonify({"error": f"Scenario '{name}' must be a JSON object"}), 400
            scenario_data = {**baseline, **changes}
            probability = calculate_simulation_probability(disease, scenario_data)
            results[name] = {
                "risk_score": round(probability, 4),
                "risk_level": get_risk_level(probability),
                "risk_change": round(probability - baseline_probability, 4),
                "changes": changes
            }

        return jsonify({"disease": disease, "results": results})
    except (KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

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
            "risk_level": get_risk_level(h_prob),
            "confidence": calculate_statistical_confidence(h_prob)
        },
        "diabetes": {
            "risk_score": round(float(d_prob), 2),
            "risk_level": get_risk_level(d_prob),
            "confidence": calculate_statistical_confidence(d_prob)
        },
        "stroke": {
            "risk_score": round(float(s_prob), 2),
            "risk_level": get_risk_level(s_prob),
            "confidence": calculate_statistical_confidence(s_prob)
        }
    })

# =========================
# RESEARCH (MTL & TRUSTWORTHY AI)
# =========================

mtl_scaler = None
mtl_model = None
explainer = None

def init_research_models():
    global mtl_scaler, mtl_model, explainer
    if mtl_model is None:
        try:
            mtl_scaler = joblib.load("../models/multitask/mtl_scaler.pkl")
            mtl_model = get_mtl_model(27)
            mtl_model.load_state_dict(torch.load("../models/multitask/mtl_model.pth"))
            mtl_model.eval()
            explainer = MTLExplainer(model_path="../models/multitask/mtl_model.pth")
        except Exception as e:
            print(f"Research models not initialized: {e}")

@app.route("/research/metrics", methods=["GET"])
def get_research_metrics():
    try:
        with open("../models/multitask/metrics_report.json", "r") as f:
            metrics = json.load(f)
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": "Metrics not found", "details": str(e)}), 404

@app.route("/predict/research/all", methods=["POST"])
def predict_research_all():
    init_research_models()
    if mtl_model is None:
        return jsonify({"error": "MTL model not available"}), 503
        
    data = request.json
    
    # 1. Preprocessing Adapter
    h_df = pd.DataFrame([data.get("heart", {})])
    d_df = pd.DataFrame([data.get("diabetes", {})])
    s_df = pd.DataFrame([data.get("stroke", {})])
    
    h_x, _ = map_heart_data(h_df)
    d_x, _ = map_diabetes_data(d_df)
    s_encoded = encode_stroke_input(data.get("stroke", {}))
    s_x, _ = map_stroke_data(s_encoded)
    
    # Combine (for a joint prediction, we assume the patient has all these features,
    # so we merge the vectors into one patient profile).
    combined_x = h_x.copy()
    for col in d_x.columns:
        if d_x[col].iloc[0] != 0: combined_x[col] = d_x[col]
    for col in s_x.columns:
        if s_x[col].iloc[0] != 0: combined_x[col] = s_x[col]
        
    x_scaled = mtl_scaler.transform(combined_x)
    x_tensor = torch.FloatTensor(x_scaled)
    
    # 2. Prediction
    with torch.no_grad():
        preds = mtl_model(x_tensor)
        h_prob_raw = preds[0].item()
        d_prob_raw = preds[1].item()
        s_prob_raw = preds[2].item()
        
    # 3. Calibration
    h_prob = calibrate_prediction(h_prob_raw)
    d_prob = calibrate_prediction(d_prob_raw)
    s_prob = calibrate_prediction(s_prob_raw)
    
    # 4. Uncertainty Estimation (MC Dropout)
    uncertainty = get_mc_dropout_uncertainty(mtl_model, x_tensor, n_iterations=20)
    
    # 5. Explainability (SHAP)
    # Using background of zeroes for quick SHAP baseline in prototype
    h_factors = explainer.explain(x_tensor, 'heart')
    d_factors = explainer.explain(x_tensor, 'diabetes')
    s_factors = explainer.explain(x_tensor, 'stroke')
    
    def process_disease(disease_name, prob, uncert, factors):
        conf_level = calculate_confidence(uncert['std'])
        selective = apply_selective_prediction(prob, conf_level)
        return {
            "risk_score": round(prob, 2),
            "confidence": conf_level,
            "uncertainty_std": round(uncert['std'], 3),
            "abstained": selective['abstained'],
            "status_message": selective['message'],
            "top_factors": factors
        }
        
    return jsonify({
        "heart": process_disease("heart", h_prob, uncertainty['heart'], h_factors),
        "diabetes": process_disease("diabetes", d_prob, uncertainty['diabetes'], d_factors),
        "stroke": process_disease("stroke", s_prob, uncertainty['stroke'], s_factors)
    })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)