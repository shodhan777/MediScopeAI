import pandas as pd
import numpy as np

def clean_data(df, target_col):
    # Replace '?' with NaN
    df.replace('?', np.nan, inplace=True)

    # Convert only if possible (SAFE)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop missing
    df = df.dropna()

    # Convert target to binary
    df[target_col] = df[target_col].apply(lambda x: 1 if x > 0 else 0)

    return df