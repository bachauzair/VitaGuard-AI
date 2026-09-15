import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

# --- 1. Heart Disease ---
# 303 rows, 13 features, target 'target' (0, 1)
print("Generating heart.csv...")
heart_data = pd.DataFrame({
    'age': np.random.randint(29, 78, 303),
    'sex': np.random.randint(0, 2, 303),
    'cp': np.random.randint(0, 4, 303),
    'trestbps': np.random.randint(94, 200, 303),
    'chol': np.random.randint(126, 564, 303),
    'fbs': np.random.randint(0, 2, 303),
    'restecg': np.random.randint(0, 3, 303),
    'thalach': np.random.randint(71, 202, 303),
    'exang': np.random.randint(0, 2, 303),
    'oldpeak': np.random.uniform(0.0, 6.2, 303).round(1),
    'slope': np.random.randint(0, 3, 303),
    'ca': np.random.randint(0, 5, 303),
    'thal': np.random.randint(0, 4, 303),
    'target': np.random.randint(0, 2, 303)
})
# Inject some missing values (NaN) to test robustness
heart_data.loc[np.random.choice(303, 5), 'thal'] = np.nan
heart_data.to_csv(os.path.join(DATA_DIR, 'heart.csv'), index=False)

# --- 2. Chronic Kidney Disease ---
# 400 rows, 24 features, target 'classification' ('ckd', 'notckd')
print("Generating kidney_disease.csv...")
kidney_data = pd.DataFrame({
    'age': np.random.randint(2, 90, 400).astype(float),
    'bp': np.random.choice([50, 60, 70, 80, 90, 100, 110], 400).astype(float),
    'sg': np.random.choice([1.005, 1.010, 1.015, 1.020, 1.025], 400),
    'al': np.random.choice([0, 1, 2, 3, 4, 5], 400).astype(float),
    'su': np.random.choice([0, 1, 2, 3, 4, 5], 400).astype(float),
    'rbc': np.random.choice(['normal', 'abnormal', np.nan], 400, p=[0.7, 0.2, 0.1]),
    'pc': np.random.choice(['normal', 'abnormal', np.nan], 400, p=[0.7, 0.2, 0.1]),
    'pcc': np.random.choice(['present', 'notpresent', np.nan], 400, p=[0.2, 0.7, 0.1]),
    'ba': np.random.choice(['present', 'notpresent', np.nan], 400, p=[0.1, 0.8, 0.1]),
    'bgr': np.random.uniform(22, 490, 400),
    'bu': np.random.uniform(1.5, 391, 400),
    'sc': np.random.uniform(0.4, 76, 400),
    'sod': np.random.uniform(4.5, 163, 400),
    'pot': np.random.uniform(2.5, 47, 400),
    'hemo': np.random.uniform(3.1, 17.8, 400),
    'pcv': np.random.randint(9, 54, 400).astype(str), # Sometimes represented as string in the raw data
    'wc': np.random.randint(2200, 26400, 400).astype(str),
    'rc': np.random.uniform(2.1, 8.0, 400).round(1).astype(str),
    'htn': np.random.choice(['yes', 'no', np.nan], 400, p=[0.4, 0.5, 0.1]),
    'dm': np.random.choice(['yes', 'no', '\tno', ' yes', np.nan], 400, p=[0.4, 0.4, 0.05, 0.05, 0.1]), # Includes formatting errors
    'cad': np.random.choice(['yes', 'no', '\tno', np.nan], 400, p=[0.1, 0.7, 0.1, 0.1]),
    'appet': np.random.choice(['good', 'poor', np.nan], 400, p=[0.7, 0.2, 0.1]),
    'pe': np.random.choice(['yes', 'no', np.nan], 400, p=[0.2, 0.7, 0.1]),
    'ane': np.random.choice(['yes', 'no', np.nan], 400, p=[0.15, 0.75, 0.1]),
    'classification': np.random.choice(['ckd', 'notckd', 'ckd\t'], 400, p=[0.6, 0.35, 0.05]) # Includes formatting error
})
kidney_data.to_csv(os.path.join(DATA_DIR, 'kidney_disease.csv'), index=False)

# --- 3. Liver Disease ---
# 583 rows, 10 features, target 'Dataset' (1, 2)
print("Generating indian_liver_patient.csv...")
liver_data = pd.DataFrame({
    'Age': np.random.randint(4, 90, 583),
    'Gender': np.random.choice(['Male', 'Female'], 583, p=[0.75, 0.25]),
    'Total_Bilirubin': np.random.uniform(0.4, 75.0, 583).round(1),
    'Direct_Bilirubin': np.random.uniform(0.1, 19.7, 583).round(1),
    'Alkaline_Phosphotase': np.random.randint(63, 2110, 583),
    'Alamine_Aminotransferase': np.random.randint(10, 2000, 583),
    'Aspartate_Aminotransferase': np.random.randint(10, 4929, 583),
    'Total_Protiens': np.random.uniform(2.7, 9.6, 583).round(1),
    'Albumin': np.random.uniform(0.9, 5.5, 583).round(1),
    'Albumin_and_Globulin_Ratio': np.random.uniform(0.3, 2.8, 583).round(2),
    'Dataset': np.random.choice([1, 2], 583, p=[0.7, 0.3])
})
# Inject some missing values
liver_data.loc[np.random.choice(583, 4), 'Albumin_and_Globulin_Ratio'] = np.nan
liver_data.to_csv(os.path.join(DATA_DIR, 'indian_liver_patient.csv'), index=False)

print("Datasets generated successfully.")
