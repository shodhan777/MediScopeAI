import pandas as pd
from utils.preprocess import clean_data
from utils.train_model import train_pipeline

print("Loading Diabetes dataset...")

df = pd.read_csv("data/diabetes.csv")

df = clean_data(df, "Outcome")

train_pipeline(df, "Outcome", "diabetes")