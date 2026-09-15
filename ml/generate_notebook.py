import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell("# Multi-Disease AI Risk Predictor Training\nThis notebook trains models for Diabetes, Heart Disease, Chronic Kidney Disease, and Liver Disease."),
    
    nbf.v4.new_markdown_cell("## 1. Setup"),
    nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import shap

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report

BASE_DIR = os.path.dirname(os.path.abspath('__file__'))
if not os.path.basename(BASE_DIR) == 'ml':
    BASE_DIR = os.path.join(BASE_DIR, 'ml')
    
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

results = []
models_dict = {}
explainers_dict = {}
X_tests = {}
"""),

    nbf.v4.new_markdown_cell("## 2. Diabetes Model\nRetraining the existing model for consistency with the new pipeline approach (saving preprocessors appropriately)."),
    nbf.v4.new_code_cell("""df_diab = pd.read_csv(os.path.join(DATA_DIR, 'diabetes.csv'))
invalid_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
df_diab[invalid_cols] = df_diab[invalid_cols].replace(0, np.nan)
for col in invalid_cols:
    df_diab[col] = df_diab[col].fillna(df_diab[col].median())

X_diab = df_diab.drop('Outcome', axis=1)
y_diab = df_diab['Outcome']

X_train_diab, X_test_diab, y_train_diab, y_test_diab = train_test_split(X_diab, y_diab, test_size=0.2, random_state=42, stratify=y_diab)

scaler_diab = StandardScaler()
X_train_diab_scaled = pd.DataFrame(scaler_diab.fit_transform(X_train_diab), columns=X_diab.columns)
X_test_diab_scaled = pd.DataFrame(scaler_diab.transform(X_test_diab), columns=X_diab.columns)

model_diab = RandomForestClassifier(random_state=42, n_estimators=100)
model_diab.fit(X_train_diab_scaled, y_train_diab)

y_pred = model_diab.predict(X_test_diab_scaled)
y_prob = model_diab.predict_proba(X_test_diab_scaled)[:, 1]

results.append({
    'Disease': 'Diabetes',
    'Accuracy': accuracy_score(y_test_diab, y_pred),
    'Precision': precision_score(y_test_diab, y_pred),
    'Recall': recall_score(y_test_diab, y_pred),
    'F1 Score': f1_score(y_test_diab, y_pred),
    'ROC-AUC': roc_auc_score(y_test_diab, y_prob)
})

models_dict['diabetes'] = model_diab
X_tests['diabetes'] = X_test_diab_scaled
joblib.dump(scaler_diab, os.path.join(MODELS_DIR, 'diabetes_preprocessor.pkl'))
joblib.dump(model_diab, os.path.join(MODELS_DIR, 'diabetes_model.pkl'))
joblib.dump(list(X_diab.columns), os.path.join(MODELS_DIR, 'diabetes_features.pkl'))
print("Diabetes Model Trained and Saved.")
"""),

    nbf.v4.new_markdown_cell("## 3. Heart Disease Model"),
    nbf.v4.new_code_cell("""df_heart = pd.read_csv(os.path.join(DATA_DIR, 'heart.csv'))
# Drop missing values if any
df_heart = df_heart.dropna()

X_heart = df_heart.drop('target', axis=1)
y_heart = df_heart['target']

X_train_heart, X_test_heart, y_train_heart, y_test_heart = train_test_split(X_heart, y_heart, test_size=0.2, random_state=42, stratify=y_heart)

# Scaling is not strictly necessary for RF, but good for consistency
scaler_heart = StandardScaler()
X_train_heart_scaled = pd.DataFrame(scaler_heart.fit_transform(X_train_heart), columns=X_heart.columns)
X_test_heart_scaled = pd.DataFrame(scaler_heart.transform(X_test_heart), columns=X_heart.columns)

model_heart = RandomForestClassifier(random_state=42, n_estimators=100)
model_heart.fit(X_train_heart_scaled, y_train_heart)

y_pred = model_heart.predict(X_test_heart_scaled)
y_prob = model_heart.predict_proba(X_test_heart_scaled)[:, 1]

results.append({
    'Disease': 'Heart',
    'Accuracy': accuracy_score(y_test_heart, y_pred),
    'Precision': precision_score(y_test_heart, y_pred),
    'Recall': recall_score(y_test_heart, y_pred),
    'F1 Score': f1_score(y_test_heart, y_pred),
    'ROC-AUC': roc_auc_score(y_test_heart, y_prob)
})

models_dict['heart'] = model_heart
X_tests['heart'] = X_test_heart_scaled
joblib.dump(scaler_heart, os.path.join(MODELS_DIR, 'heart_preprocessor.pkl'))
joblib.dump(model_heart, os.path.join(MODELS_DIR, 'heart_model.pkl'))
joblib.dump(list(X_heart.columns), os.path.join(MODELS_DIR, 'heart_features.pkl'))
print("Heart Model Trained and Saved.")
"""),

    nbf.v4.new_markdown_cell("## 4. Kidney Disease Model\nRequires handling categorical variables and messy strings."),
    nbf.v4.new_code_cell("""df_kidney = pd.read_csv(os.path.join(DATA_DIR, 'kidney_disease.csv'))

# Clean target variable and format issues
df_kidney['classification'] = df_kidney['classification'].str.replace(r'\\t', '', regex=True).str.strip()
df_kidney['classification'] = df_kidney['classification'].map({'ckd': 1, 'notckd': 0})
df_kidney = df_kidney.dropna(subset=['classification']) # drop rows with undefined targets

# Clean string formatting issues in features
for col in ['pcv', 'wc', 'rc', 'dm', 'cad']:
    if df_kidney[col].dtype == 'object':
        df_kidney[col] = df_kidney[col].str.replace(r'\\t', '', regex=True).str.strip()

# Numeric imputation
numeric_cols = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc']
for col in numeric_cols:
    df_kidney[col] = pd.to_numeric(df_kidney[col], errors='coerce')
    df_kidney[col] = df_kidney[col].fillna(df_kidney[col].median())

# Categorical imputation & encoding
categorical_cols = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']
for col in categorical_cols:
    df_kidney[col] = df_kidney[col].fillna(df_kidney[col].mode()[0])
    
# Encode categoricals using pd.get_dummies or LabelEncoder
# Using LabelEncoder to keep feature count exactly same and simple for backend
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_kidney[col] = le.fit_transform(df_kidney[col].astype(str))
    encoders[col] = le

X_kidney = df_kidney.drop('classification', axis=1)
y_kidney = df_kidney['classification'].astype(int)

X_train_kidney, X_test_kidney, y_train_kidney, y_test_kidney = train_test_split(X_kidney, y_kidney, test_size=0.2, random_state=42, stratify=y_kidney)

scaler_kidney = StandardScaler()
X_train_kidney_scaled = pd.DataFrame(scaler_kidney.fit_transform(X_train_kidney), columns=X_kidney.columns)
X_test_kidney_scaled = pd.DataFrame(scaler_kidney.transform(X_test_kidney), columns=X_kidney.columns)

model_kidney = RandomForestClassifier(random_state=42, n_estimators=100)
model_kidney.fit(X_train_kidney_scaled, y_train_kidney)

y_pred = model_kidney.predict(X_test_kidney_scaled)
y_prob = model_kidney.predict_proba(X_test_kidney_scaled)[:, 1]

results.append({
    'Disease': 'Kidney',
    'Accuracy': accuracy_score(y_test_kidney, y_pred),
    'Precision': precision_score(y_test_kidney, y_pred, zero_division=0),
    'Recall': recall_score(y_test_kidney, y_pred, zero_division=0),
    'F1 Score': f1_score(y_test_kidney, y_pred, zero_division=0),
    'ROC-AUC': roc_auc_score(y_test_kidney, y_prob)
})

models_dict['kidney'] = model_kidney
X_tests['kidney'] = X_test_kidney_scaled
# Save preprocessor as a dict containing scaler and encoders
kidney_preprocessor = {'scaler': scaler_kidney, 'encoders': encoders}
joblib.dump(kidney_preprocessor, os.path.join(MODELS_DIR, 'kidney_preprocessor.pkl'))
joblib.dump(model_kidney, os.path.join(MODELS_DIR, 'kidney_model.pkl'))
joblib.dump(list(X_kidney.columns), os.path.join(MODELS_DIR, 'kidney_features.pkl'))
print("Kidney Model Trained and Saved.")
"""),

    nbf.v4.new_markdown_cell("## 5. Liver Disease Model\nRequires handling Gender categorical column."),
    nbf.v4.new_code_cell("""df_liver = pd.read_csv(os.path.join(DATA_DIR, 'indian_liver_patient.csv'))

# Dataset column: 1 = disease, 2 = no disease. Let's map to 1 = disease, 0 = no disease.
df_liver['Dataset'] = df_liver['Dataset'].map({1: 1, 2: 0})

# Impute missing
df_liver['Albumin_and_Globulin_Ratio'] = df_liver['Albumin_and_Globulin_Ratio'].fillna(df_liver['Albumin_and_Globulin_Ratio'].median())

# Encode Gender
df_liver['Gender'] = df_liver['Gender'].map({'Male': 1, 'Female': 0}).fillna(1) # default male if missing

X_liver = df_liver.drop('Dataset', axis=1)
y_liver = df_liver['Dataset']

X_train_liver, X_test_liver, y_train_liver, y_test_liver = train_test_split(X_liver, y_liver, test_size=0.2, random_state=42, stratify=y_liver)

scaler_liver = StandardScaler()
X_train_liver_scaled = pd.DataFrame(scaler_liver.fit_transform(X_train_liver), columns=X_liver.columns)
X_test_liver_scaled = pd.DataFrame(scaler_liver.transform(X_test_liver), columns=X_liver.columns)

model_liver = RandomForestClassifier(random_state=42, n_estimators=100)
model_liver.fit(X_train_liver_scaled, y_train_liver)

y_pred = model_liver.predict(X_test_liver_scaled)
y_prob = model_liver.predict_proba(X_test_liver_scaled)[:, 1]

results.append({
    'Disease': 'Liver',
    'Accuracy': accuracy_score(y_test_liver, y_pred),
    'Precision': precision_score(y_test_liver, y_pred),
    'Recall': recall_score(y_test_liver, y_pred),
    'F1 Score': f1_score(y_test_liver, y_pred),
    'ROC-AUC': roc_auc_score(y_test_liver, y_prob)
})

models_dict['liver'] = model_liver
X_tests['liver'] = X_test_liver_scaled
joblib.dump(scaler_liver, os.path.join(MODELS_DIR, 'liver_preprocessor.pkl'))
joblib.dump(model_liver, os.path.join(MODELS_DIR, 'liver_model.pkl'))
joblib.dump(list(X_liver.columns), os.path.join(MODELS_DIR, 'liver_features.pkl'))
print("Liver Model Trained and Saved.")
"""),

    nbf.v4.new_markdown_cell("## 6. Model Comparison"),
    nbf.v4.new_code_cell("""results_df = pd.DataFrame(results).set_index('Disease')
print(results_df.round(4).to_markdown())
"""),

    nbf.v4.new_markdown_cell("## 7. SHAP Analysis\nGenerate summary plots for each model to verify interpretability."),
    nbf.v4.new_code_cell("""for name, model in models_dict.items():
    X_test = X_tests[name]
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    if isinstance(shap_values, list):
        sv = shap_values[1]
    elif len(np.array(shap_values).shape) == 3:
        sv = shap_values[:, :, 1]
    else:
        sv = shap_values
        
    plt.figure()
    plt.title(f'SHAP Summary - {name.capitalize()} Disease')
    shap.summary_plot(sv, X_test, show=False)
    plt.savefig(os.path.join(PLOTS_DIR, f'{name}_shap_summary.png'), bbox_inches='tight')
    plt.close()
print("SHAP plots generated.")
""")
]

with open('multi_disease_training.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook multi_disease_training.ipynb created successfully.")
