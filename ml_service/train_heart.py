import pandas as pd
from utils.preprocess import clean_data
from utils.train_model import train_pipeline

print("Loading Heart dataset...")

df = pd.read_csv("data/heart.csv")

df = clean_data(df, "target")

train_pipeline(df, "target", "heart")