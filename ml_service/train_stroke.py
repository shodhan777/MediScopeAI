import pandas as pd
from utils.preprocess import clean_data
from utils.train_model import train_pipeline

print("Loading Stroke dataset...")

df = pd.read_csv("data/stroke.csv")

# =========================
# SPECIAL CLEANING
# =========================

# Drop ID column
df = df.drop(columns=["id"])

# Fix BMI properly (NO inplace)
df["bmi"] = df["bmi"].fillna(df["bmi"].mean())

# Convert categorical → numeric FIRST
df = pd.get_dummies(df, drop_first=True)

# DEBUG (VERY IMPORTANT)
print("After encoding:")
print(df.head())

# =========================
# CLEAN (NOW SAFE)
# =========================
df = clean_data(df, "stroke")

# =========================
# TRAIN
# =========================
train_pipeline(df, "stroke", "stroke")