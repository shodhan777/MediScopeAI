import pandas as pd
import numpy as np
import joblib
import torch
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, brier_score_loss

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.mtl_adapter import get_combined_dataset, MTL_FEATURES, map_heart_data, map_diabetes_data, map_stroke_data
from inference.mtl_model import get_mtl_model

def evaluate_baselines():
    metrics = {}
    datasets = {}

    heart_df = pd.read_csv('data/heart.csv')
    heart_df = heart_df.replace('?', np.nan).apply(pd.to_numeric, errors='coerce').dropna()
    h_features = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
    datasets["Heart"] = (heart_df[h_features], (heart_df['target'] > 0).astype(int))

    diabetes_df = pd.read_csv('data/diabetes.csv')
    diabetes_df = diabetes_df.replace('?', np.nan).apply(pd.to_numeric, errors='coerce').dropna()
    d_features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
    datasets["Diabetes"] = (diabetes_df[d_features], diabetes_df['Outcome'].astype(int))

    stroke_df = pd.read_csv('data/stroke.csv').drop(columns=['id'])
    stroke_df['bmi'] = pd.to_numeric(stroke_df['bmi'], errors='coerce')
    stroke_df['bmi'] = stroke_df['bmi'].fillna(stroke_df['bmi'].mean())
    s_X, s_y = map_stroke_data(stroke_df)
    datasets["Stroke"] = (s_X, s_y.astype(int))

    for disease, (X, y) in datasets.items():
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        positive_count = max(int((y_train == 1).sum()), 1)
        negative_count = max(int((y_train == 0).sum()), 1)
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
            "Random Forest": RandomForestClassifier(class_weight='balanced', n_estimators=300, random_state=42),
            "XGBoost": XGBClassifier(
                scale_pos_weight=negative_count / positive_count,
                random_state=42,
                eval_metric='logloss'
            )
        }
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            probabilities = model.predict_proba(X_test)[:, 1]
            metrics[f"{disease} ({model_name})"] = get_metrics(
                y_test, probabilities >= 0.5, probabilities
            )
    
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
