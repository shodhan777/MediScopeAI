## 📊 Model Performance Summary

### ❤️ Heart Disease

* Best Model: Logistic Regression
* Accuracy: ~88%
* High recall and balanced performance

### 🩸 Diabetes

* Best Model: XGBoost
* Accuracy: ~70%
* Handles non-linear relationships effectively

### 🧠 Stroke

* Best Model: Logistic Regression
* Recall: ~79%
* Handles imbalanced dataset effectively

---

## ⚠️ Key Insight

Accuracy alone is not reliable for imbalanced datasets.
Models were selected based on **Recall and F1-score** to ensure proper disease detection, especially in critical healthcare scenarios.

---

## 📁 Project Structure

```
ml_service/
│
├── data/
├── models/
├── utils/
│   ├── preprocess.py
│   └── train_model.py
│
├── api/
│   └── app.py
│
├── train_heart.py
├── train_diabetes.py
├── train_stroke.py
```

---

## 🧪 How to Run

```bash
python train_heart.py
python train_diabetes.py
python train_stroke.py
```

Run API:

```bash
cd api
python app.py
```

---

## 🌐 API Endpoints

* `POST /predict/heart`
* `POST /predict/diabetes`
* `POST /predict/stroke`
* `POST /predict/all`

Each endpoint returns:

* Prediction (0/1)
* Risk Score (Probability)
* Risk Level (Low / Medium / High)

---


Endpoint:

POST
 http://127.0.0.1:5000/predict/all

Request Body:

{
  "heart": {
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
  },
  "diabetes": {
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
  },
  "stroke": {
    "gender": "Male",
    "age": 67,
    "hypertension": 1,
    "heart_disease": 1,
    "ever_married": "Yes",
    "work_type": "Private",
    "Residence_type": "Urban",
    "avg_glucose_level": 228.69,
    "bmi": 36.6,
    "smoking_status": "smokes"
  }
}