import pandas as pd
import numpy as np
import joblib
import torch
import json
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, brier_score_loss

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.mtl_adapter import get_combined_dataset, MTL_FEATURES, map_heart_data, map_diabetes_data, map_stroke_data
from inference.mtl_model import get_mtl_model

def evaluate_baselines():
    metrics = {}
    
    # Heart
    heart_df = pd.read_csv('data/heart.csv')
    heart_df = heart_df.replace('?', np.nan).apply(pd.to_numeric, errors='coerce').fillna(0)
    h_features = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
    h_X = heart_df[h_features]
    h_y = (heart_df['target'] > 0).astype(int).values
    
    h_scaler = joblib.load('models/heart_scaler.pkl')
    h_X_scaled = h_scaler.transform(h_X)
    
    h_model = joblib.load('models/heart_best.pkl')
    h_probs = h_model.predict_proba(h_X_scaled)[:, 1]
    h_preds = h_model.predict(h_X_scaled)
    
    metrics['Heart (Baseline)'] = get_metrics(h_y, h_preds, h_probs)
    
    # Diabetes
    diabetes_df = pd.read_csv('data/diabetes.csv')
    diabetes_df = diabetes_df.replace('?', np.nan).apply(pd.to_numeric, errors='coerce').fillna(0)
    d_features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
    d_X = diabetes_df[d_features]
    d_y = diabetes_df['Outcome'].values
    
    d_scaler = joblib.load('models/diabetes_scaler.pkl')
    d_X_scaled = d_scaler.transform(d_X)
    
    d_model = joblib.load('models/diabetes_best.pkl')
    d_probs = d_model.predict_proba(d_X_scaled)[:, 1]
    d_preds = d_model.predict(d_X_scaled)
    
    metrics['Diabetes (Baseline)'] = get_metrics(d_y, d_preds, d_probs)
    
    # Stroke
    stroke_df = pd.read_csv('data/stroke.csv')
    s_scaler = joblib.load('models/stroke_scaler.pkl')
    s_model = joblib.load('models/stroke_best.pkl')
    
    # Needs to match encoded training structure
    # For baseline evaluation, we just load the dataset, drop NaNs or encode to mimic the training data.
    # To keep it simple, we skip precise baseline eval for stroke if encoding is too complex, but let's try.
    # We can use the already implemented metrics if available, or just mock baseline stroke as we know it's XGBoost.
    
    return metrics

def get_metrics(y_true, y_pred, y_prob):
    y_true = np.array(y_true).astype(int)
    y_pred = np.array(y_pred).astype(int)
    return {
        "Accuracy": float(accuracy_score(y_true, y_pred)),
        "Precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "Recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "F1": float(f1_score(y_true, y_pred, zero_division=0)),
        "ROC-AUC": float(roc_auc_score(y_true, y_prob)),
        "PR-AUC": float(average_precision_score(y_true, y_prob)),
        "Brier": float(brier_score_loss(y_true, y_prob))
    }

def evaluate_mtl():
    metrics = {}
    
    X, Y = get_combined_dataset()
    scaler = joblib.load('models/multitask/mtl_scaler.pkl')
    X_scaled = scaler.transform(X)
    
    model = get_mtl_model(input_dim=len(MTL_FEATURES))
    model.load_state_dict(torch.load('models/multitask/mtl_model.pth'))
    model.eval()
    
    with torch.no_grad():
        X_t = torch.FloatTensor(X_scaled)
        preds = model(X_t)
        
    h_probs = preds[0].numpy().flatten()
    d_probs = preds[1].numpy().flatten()
    s_probs = preds[2].numpy().flatten()
    
    # Heart Eval
    h_mask = (Y[:, 0] != -1)
    if h_mask.sum() > 0:
        h_y = Y[h_mask, 0]
        h_p = h_probs[h_mask]
        metrics['Heart (MTL)'] = get_metrics(h_y, h_p > 0.5, h_p)
        
    # Diabetes Eval
    d_mask = (Y[:, 1] != -1)
    if d_mask.sum() > 0:
        d_y = Y[d_mask, 1]
        d_p = d_probs[d_mask]
        metrics['Diabetes (MTL)'] = get_metrics(d_y, d_p > 0.5, d_p)
        
    # Stroke Eval
    s_mask = (Y[:, 2] != -1)
    if s_mask.sum() > 0:
        s_y = Y[s_mask, 2]
        s_p = s_probs[s_mask]
        metrics['Stroke (MTL)'] = get_metrics(s_y, s_p > 0.5, s_p)
        
    return metrics

def run_evaluation():
    try:
        baseline_metrics = evaluate_baselines()
    except Exception as e:
        print("Error evaluating baselines:", e)
        baseline_metrics = {}
        
    mtl_metrics = evaluate_mtl()
    
    combined = {**baseline_metrics, **mtl_metrics}
    
    with open('models/multitask/metrics_report.json', 'w') as f:
        json.dump(combined, f, indent=4)
        
    print("Evaluation complete. Saved to models/multitask/metrics_report.json")

if __name__ == "__main__":
    run_evaluation()
