import joblib
import json
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def train_pipeline(df, target_col, model_prefix):
    print(f"\n🚀 Training {model_prefix} model...")

    X = df.drop(target_col, axis=1)
    y = df[target_col]

    # 🔥 Show class distribution
    print("\n📊 Class Distribution:")
    print(y.value_counts())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # 🔥 Improved models for imbalance
    models = {
        "logistic": LogisticRegression(max_iter=1000, class_weight='balanced'),
        "random_forest": RandomForestClassifier(class_weight='balanced'),
        "xgboost": XGBClassifier(scale_pos_weight=10)
    }

    results = {}
    trained_models = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)

        results[name] = {
            "accuracy": acc,
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0)
        }

        # 🔥 Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n{name.upper()} Confusion Matrix:\n{cm}")

        trained_models[name] = model

        # Save model
        joblib.dump(model, f"models/{model_prefix}_{name}.pkl")

    # Save scaler
    joblib.dump(scaler, f"models/{model_prefix}_scaler.pkl")

    # Best model
    best_model_name = max(results, key=lambda x: results[x]["recall"])
    best_model = trained_models[best_model_name]

    joblib.dump(best_model, f"models/{model_prefix}_best.pkl")

    # Save results
    with open(f"models/{model_prefix}_results.json", "w") as f:
        json.dump(results, f, indent=4)

    # 🔥 Print results cleanly
    print("\n📊 Model Performance:")
    for model, metrics in results.items():
        print(f"\n{model.upper()}")
        for key, value in metrics.items():
            print(f"{key}: {value:.4f}")

    print(f"\n🏆 Best Model: {best_model_name.upper()}")
    print(f"\n✅ {model_prefix} training completed!")