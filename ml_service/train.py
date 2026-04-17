import pandas as pd
import numpy as np
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("🚀 Starting training pipeline...")

# =========================
# LOAD DATA
# =========================
print("\nLoading dataset...")
df = pd.read_csv("data/heart.csv")
print("Dataset loaded!")

# =========================
# DATA CLEANING
# =========================
print("\nCleaning data...")

# Replace '?' with NaN
df.replace('?', np.nan, inplace=True)

# Convert all to numeric
df = df.apply(pd.to_numeric)

# Drop missing values
df = df.dropna()

# Convert target to binary
df["target"] = df["target"].apply(lambda x: 1 if x > 0 else 0)

print("Data cleaning completed!")

# =========================
# FEATURE SPLIT
# =========================
X = df.drop("target", axis=1)
y = df["target"]

# =========================
# SCALING
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# =========================
# MODELS
# =========================
models = {
    "logistic": LogisticRegression(max_iter=1000),
    "random_forest": RandomForestClassifier(),
    "xgboost": XGBClassifier()
}

results = {}
trained_models = {}

# =========================
# TRAINING LOOP
# =========================
for name, model in models.items():
    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    results[name] = {
        "accuracy": acc,
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred)
    }

    trained_models[name] = model

    # Save individual model
    joblib.dump(model, f"models/heart_{name}.pkl")

# =========================
# SAVE SCALER
# =========================
joblib.dump(scaler, "models/scaler.pkl")

# =========================
# FIND BEST MODEL
# =========================
best_model_name = max(results, key=lambda x: results[x]["accuracy"])
best_model = trained_models[best_model_name]

joblib.dump(best_model, "models/heart_best.pkl")

# =========================
# PRINT RESULTS
# =========================
print("\n📊 Model Performance:")

for model, metrics in results.items():
    print(f"\n{model.upper()}")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

print(f"\n🏆 Best Model: {best_model_name.upper()}")

# =========================
# SAVE RESULTS
# =========================
with open("models/heart_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ Training completed successfully!")