import pandas as pd
import numpy as np

MTL_FEATURES = [
    'age', 'sex_male', 'trestbps', 'chol', 'fbs', 
    'bmi', 'diabetes_pedigree', 'pregnancies', 'insulin', 'skin_thickness',
    'heart_disease_hist', 'hypertension_hist',
    'cp', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal',
    'ever_married_Yes', 'work_type_Private', 'work_type_Self-employed', 
    'Residence_type_Urban', 'smoking_status_formerly_smoked', 
    'smoking_status_never_smoked', 'smoking_status_smokes'
]

def map_heart_data(df):
    """Maps Heart Disease dataset to MTL format"""
    mtl_df = pd.DataFrame(0, index=np.arange(len(df)), columns=MTL_FEATURES)
    mtl_df['age'] = df['age']
    mtl_df['sex_male'] = df['sex']
    mtl_df['trestbps'] = df['trestbps']
    mtl_df['chol'] = df['chol']
    mtl_df['fbs'] = df['fbs']
    mtl_df['cp'] = df['cp']
    mtl_df['restecg'] = df['restecg']
    mtl_df['thalach'] = df['thalach']
    mtl_df['exang'] = df['exang']
    mtl_df['oldpeak'] = df['oldpeak']
    mtl_df['slope'] = df['slope']
    mtl_df['ca'] = df['ca']
    mtl_df['thal'] = df['thal']
    # If target is present, return it too
    target = (df['target'] > 0).astype(int).values if 'target' in df else None
    return mtl_df, target

def map_diabetes_data(df):
    """Maps Diabetes dataset to MTL format"""
    mtl_df = pd.DataFrame(0, index=np.arange(len(df)), columns=MTL_FEATURES)
    mtl_df['age'] = df['Age']
    mtl_df['trestbps'] = df['BloodPressure']
    mtl_df['bmi'] = df['BMI']
    mtl_df['diabetes_pedigree'] = df['DiabetesPedigreeFunction']
    mtl_df['pregnancies'] = df['Pregnancies']
    mtl_df['insulin'] = df['Insulin']
    mtl_df['skin_thickness'] = df['SkinThickness']
    mtl_df['fbs'] = (df['Glucose'] > 120).astype(int)
    
    target = df['Outcome'].values if 'Outcome' in df else None
    return mtl_df, target

def map_stroke_data(df):
    """Maps Stroke dataset to MTL format"""
    mtl_df = pd.DataFrame(0, index=np.arange(len(df)), columns=MTL_FEATURES)
    
    # Check if this is pre-encoded or raw
    if 'gender' in df:
        # Raw data mapping
        mtl_df['age'] = df['age']
        mtl_df['sex_male'] = (df['gender'] == 'Male').astype(int)
        mtl_df['hypertension_hist'] = df['hypertension']
        mtl_df['heart_disease_hist'] = df['heart_disease']
        mtl_df['fbs'] = (df['avg_glucose_level'] > 120).astype(int)
        mtl_df['bmi'] = df['bmi'].replace('N/A', 0).astype(float)
        mtl_df['ever_married_Yes'] = (df['ever_married'] == 'Yes').astype(int)
        mtl_df['work_type_Private'] = (df['work_type'] == 'Private').astype(int)
        mtl_df['work_type_Self-employed'] = (df['work_type'] == 'Self-employed').astype(int)
        mtl_df['Residence_type_Urban'] = (df['Residence_type'] == 'Urban').astype(int)
        mtl_df['smoking_status_formerly_smoked'] = (df['smoking_status'] == 'formerly smoked').astype(int)
        mtl_df['smoking_status_never_smoked'] = (df['smoking_status'] == 'never smoked').astype(int)
        mtl_df['smoking_status_smokes'] = (df['smoking_status'] == 'smokes').astype(int)
        target = df['stroke'].values if 'stroke' in df else None
    else:
        # Already encoded (e.g., from API payload)
        mtl_df['age'] = df.get('age', 0)
        mtl_df['sex_male'] = df.get('gender_Male', 0)
        mtl_df['hypertension_hist'] = df.get('hypertension', 0)
        mtl_df['heart_disease_hist'] = df.get('heart_disease', 0)
        mtl_df['fbs'] = int(df.get('avg_glucose_level', 0) > 120)
        mtl_df['bmi'] = df.get('bmi', 0)
        mtl_df['ever_married_Yes'] = df.get('ever_married_Yes', 0)
        mtl_df['work_type_Private'] = df.get('work_type_Private', 0)
        mtl_df['work_type_Self-employed'] = df.get('work_type_Self-employed', 0)
        mtl_df['Residence_type_Urban'] = df.get('Residence_type_Urban', 0)
        mtl_df['smoking_status_formerly_smoked'] = df.get('smoking_status_formerly smoked', 0)
        mtl_df['smoking_status_never_smoked'] = df.get('smoking_status_never smoked', 0)
        mtl_df['smoking_status_smokes'] = df.get('smoking_status_smokes', 0)
        target = None
        
    return mtl_df, target

def get_combined_dataset():
    """Loads all three datasets and combines them into one large MTL dataset."""
    heart_df = pd.read_csv('data/heart.csv')
    diabetes_df = pd.read_csv('data/diabetes.csv')
    stroke_df = pd.read_csv('data/stroke.csv')
    
    # Handle NaNs in stroke BMI
    if 'bmi' in stroke_df.columns:
        stroke_df['bmi'] = stroke_df['bmi'].replace(['N/A', '?'], np.nan).astype(float)
        stroke_df['bmi'] = stroke_df['bmi'].fillna(stroke_df['bmi'].mean())
        
    # Clean Heart and Diabetes datasets from '?'
    heart_df = heart_df.replace('?', np.nan).apply(pd.to_numeric, errors='coerce').fillna(0)
    diabetes_df = diabetes_df.replace('?', np.nan).apply(pd.to_numeric, errors='coerce').fillna(0)
    
    h_x, h_y = map_heart_data(heart_df)
    d_x, d_y = map_diabetes_data(diabetes_df)
    s_x, s_y = map_stroke_data(stroke_df)
    
    # We will structure the target as a 3-column array: [heart_target, diabetes_target, stroke_target]
    # For tasks that are missing for a sample, we use -1 as a mask value.
    h_targets = np.column_stack((h_y, np.full_like(h_y, -1), np.full_like(h_y, -1)))
    d_targets = np.column_stack((np.full_like(d_y, -1), d_y, np.full_like(d_y, -1)))
    s_targets = np.column_stack((np.full_like(s_y, -1), np.full_like(s_y, -1), s_y))
    
    X_combined = pd.concat([h_x, d_x, s_x], ignore_index=True)
    Y_combined = np.vstack([h_targets, d_targets, s_targets])
    
    return X_combined, Y_combined
