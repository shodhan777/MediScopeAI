import shap
import numpy as np

def generate_logistic_insights(model, scaler, features, data_dict, feature_names):
    """
    Generate XAI using Logistic Regression coefficients (coef * scaled_value).
    """
    coefs = model.coef_[0]
    scaled_values = scaler.transform(features)[0]
    impacts = coefs * scaled_values
    
    return _format_insights(impacts, feature_names, data_dict)

def generate_tree_insights(model, scaler, features, data_dict, feature_names):
    """
    Generate XAI using SHAP TreeExplainer for XGBoost/Random Forest.
    """
    scaled_values = scaler.transform(features)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(scaled_values)
    
    if isinstance(shap_values, list):
        shap_values = shap_values[1] # For binary classification
        
    impacts = shap_values[0]
    
    return _format_insights(impacts, feature_names, data_dict)

def _format_insights(impacts, feature_names, data_dict):
    factors = []
    for i, impact in enumerate(impacts):
        if abs(impact) > 1e-4:
            factors.append({
                "feature": feature_names[i],
                "raw_impact": float(impact),
                "impact_abs": float(abs(impact)),
                "value": str(data_dict.get(feature_names[i], "N/A"))
            })
            
    factors = sorted(factors, key=lambda x: x['impact_abs'], reverse=True)
    top_factors = factors[:5]
    
    formatted_xai = []
    for f in top_factors:
        formatted_xai.append({
            "factor": f["feature"],
            "value": f["value"],
            "status": "Increases Risk" if f["raw_impact"] > 0 else "Decreases Risk",
            "impact": "High" if f["impact_abs"] > 0.5 else "Medium" if f["impact_abs"] > 0.1 else "Low",
            "description": f"This feature strongly contributed to the model's prediction."
        })
    return formatted_xai

def generate_cds_recommendations(disease, data_dict, prob):
    """
    Clinical Decision Support: Generate Smart Alerts and Recommendations.
    """
    alert = ""
    recommendations = []
    
    if disease == "heart":
        trestbps = float(data_dict.get("trestbps", 120))
        chol = float(data_dict.get("chol", 200))
        if prob >= 0.65 or trestbps >= 170 or chol >= 300:
            alert = "🚨 CRITICAL CLINICAL ALERT: High cardiovascular risk detected. Urgent clinical consultation recommended."
        elif prob >= 0.35 or trestbps >= 140 or chol >= 240:
            alert = "⚠️ PREVENTIVE WARNING: Moderate cardiovascular risk profile observed. Advised to schedule routine medical screening."
        else:
            alert = "🟢 FAVORABLE CARDIOVASCULAR PROFILE: Evaluated biometric parameters remain stable within low-risk thresholds."
            
        if trestbps >= 140:
            recommendations.append("Conduct consistent blood pressure monitoring (target resting systolic level < 120 mmHg).")
        if chol >= 240:
            recommendations.append("Incorporate a Mediterranean dietary structure emphasizing dietary fiber and low sodium.")
        recommendations.append("Perform a minimum of 150 minutes per week of sustained moderate aerobic physical training.")
        
    elif disease == "diabetes":
        glucose = float(data_dict.get("Glucose", 100))
        bmi = float(data_dict.get("BMI", 22))
        if prob >= 0.65 or glucose >= 200:
            alert = "🚨 CRITICAL CLINICAL ALERT: High diabetes risk detected based on metabolic parameters. Endocrine consultation recommended."
        elif prob >= 0.35 or glucose >= 140 or bmi >= 30:
            alert = "⚠️ PREVENTIVE WARNING: Moderate diabetes risk profile observed. Consider lifestyle and dietary interventions."
        else:
            alert = "🟢 FAVORABLE METABOLIC PROFILE: Blood glucose and physical parameters indicate low immediate risk."
            
        if glucose >= 140:
            recommendations.append("Monitor fasting blood glucose levels and consider HbA1c testing.")
        if bmi >= 25:
            recommendations.append("Implement weight management strategies to achieve a target BMI under 25.")
        recommendations.append("Maintain a balanced diet low in refined carbohydrates and sugars.")
        
    elif disease == "stroke":
        age = float(data_dict.get("age", 40))
        bp = float(data_dict.get("avg_glucose_level", 100))
        if prob >= 0.65 or bp >= 200:
            alert = "🚨 CRITICAL CLINICAL ALERT: Elevated stroke risk factors identified. Immediate neurological assessment is advised."
        elif prob >= 0.35 or bp >= 160 or age >= 65:
            alert = "⚠️ PREVENTIVE WARNING: Moderate stroke risk profile. Monitor cardiovascular health actively."
        else:
            alert = "🟢 FAVORABLE NEUROLOGICAL PROFILE: Stroke risk factors are within optimal bounds."
            
        recommendations.append("Control blood pressure and monitor for signs of hypertension.")
        recommendations.append("Limit alcohol consumption and completely avoid tobacco use.")
        recommendations.append("Engage in regular cardiovascular exercise to maintain vessel elasticity.")
        
    return alert, recommendations

def calculate_statistical_confidence(prob):
    """
    Calculate confidence heuristically based on distance from the decision boundary (0.5).
    """
    margin = abs(prob - 0.5)
    if margin >= 0.35: # prob > 0.85 or prob < 0.15
        return "High"
    elif margin >= 0.15: # prob > 0.65 or prob < 0.35
        return "Medium"
    else:
        return "Low"
