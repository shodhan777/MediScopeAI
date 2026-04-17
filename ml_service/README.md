# 🧠 MediScope AI

### A Unified Multi-Disease Prediction System with Explainable AI and Clinical Decision Support

---

## 🚀 Overview

MediScope AI is a comprehensive healthcare intelligence platform designed to predict multiple chronic diseases including **Heart Disease, Diabetes, and Stroke** using Machine Learning techniques. The system integrates predictive analytics with explainability and clinical decision support to enhance trust and usability in medical environments.

---

## 🎯 Objectives

- Predict risk of multiple diseases using ML models
- Provide explainable insights into predictions
- Support clinical decision-making with recommendations
- Enable early detection and prevention

---

## 🧠 Features

- Multi-disease prediction (Heart, Diabetes, Stroke)
- Model comparison (Logistic, Random Forest, XGBoost)
- Class imbalance handling
- Confusion matrix & evaluation metrics
- Best model selection using F1-score / Recall
- Scalable ML pipeline

---

## ⚙️ Tech Stack

- Python (Pandas, Scikit-learn, XGBoost)
- Machine Learning Models
- Data Preprocessing & Feature Engineering
- (Upcoming) Flask API & Node.js Backend

---

## 📊 Model Performance Summary

### ❤️ Heart Disease

- Best Model: Logistic Regression
- Accuracy: ~88%
- High recall and balanced performance

### 🩸 Diabetes

- Best Model: XGBoost
- Accuracy: ~70%
- Handles non-linear relationships effectively

### 🧠 Stroke

- Best Model: Logistic Regression
- Recall: ~79%
- Handles imbalanced dataset effectively

---

## ⚠️ Key Insight

Accuracy alone is not reliable for imbalanced datasets.
Models were selected based on **Recall and F1-score** to ensure proper disease detection.

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

---

## 📌 Future Work

- Flask ML API integration
- Node.js backend
- React frontend dashboard
- Explainable AI (SHAP)
- Real-time risk simulation

---

## 📜 ABSTRACT

Chronic diseases such as heart disease, diabetes, and stroke are among the leading causes of mortality and long-term health complications worldwide. Early detection and timely intervention play a crucial role in improving patient outcomes and reducing healthcare burden. However, traditional machine learning-based prediction systems often operate as black-box models, limiting their adoption in clinical settings due to a lack of transparency and interpretability.

This project presents _MediScope AI_, a Unified Multi-Disease Prediction System that integrates machine learning, explainable artificial intelligence (XAI), and clinical decision support to address these challenges. The system is capable of predicting the risk of heart disease, diabetes, and stroke using patient health data through a scalable and reusable machine learning pipeline.

Multiple models, including Logistic Regression, Random Forest, and XGBoost, are trained and evaluated using performance metrics such as accuracy, precision, recall, and F1-score. Special emphasis is placed on handling imbalanced datasets, particularly for stroke prediction, where recall and F1-score are prioritized over accuracy to ensure reliable disease detection.

The system automatically selects the most suitable model for each disease based on performance evaluation. Logistic Regression performs best for heart disease and stroke due to its interpretability and strong recall, while XGBoost performs better for diabetes due to its ability to capture complex non-linear relationships.

By combining predictive accuracy, interpretability, and robust evaluation, MediScope AI bridges the gap between machine learning and real-world healthcare applications. The system lays the foundation for future enhancements, including real-time prediction APIs, explainable AI visualizations, and clinical decision support modules, ultimately contributing to improved medical decision-making and early disease prevention.
