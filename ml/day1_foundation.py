import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_FILE = os.path.join(DATA_DIR, 'diabetes.csv')

# Ensure directories exist
for directory in [DATA_DIR, PLOTS_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)

def download_dataset():
    """Downloads the Pima Indians Diabetes Dataset if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        print("Downloading Pima Indians Diabetes Dataset...")
        url = "https://raw.githubusercontent.com/npradaschnor/Pima-Indians-Diabetes-Dataset/master/diabetes.csv"
        response = requests.get(url)
        response.raise_for_status()
        with open(DATA_FILE, 'wb') as f:
            f.write(response.content)
        print(f"Dataset downloaded to {DATA_FILE}")
    else:
        print(f"Dataset already exists at {DATA_FILE}")

def main():
    # 1. Dataset Loading
    download_dataset()
    df = pd.read_csv(DATA_FILE)
    
    print("\n--- Initial Data Inspection ---")
    print(df.head())
    print("\nDataset Shape:", df.shape)
    
    # 2. Data Cleaning & Missing/Invalid-Value Handling
    # Physiological measurements of 0 are impossible and represent missing data
    # Features where 0 is invalid: Glucose, BloodPressure, SkinThickness, Insulin, BMI
    # Pregnancies can be 0. DiabetesPedigreeFunction and Age are never 0 in this dataset.
    invalid_zero_features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    
    print("\n--- Missing Value Handling ---")
    print("Zeros before replacement:\n", (df[invalid_zero_features] == 0).sum())
    
    # Replace 0s with NaN for appropriate handling
    df[invalid_zero_features] = df[invalid_zero_features].replace(0, np.nan)
    
    # Impute missing values with the median of each column
    # Decision: Median is used because it is robust to outliers, which are present in features like Insulin and SkinThickness.
    for feature in invalid_zero_features:
        df[feature] = df[feature].fillna(df[feature].median())
        
    print("\nZeros after imputation:\n", (df[invalid_zero_features] == 0).sum())
    print("Missing values after imputation:\n", df.isnull().sum())
    
    # 3. Exploratory Data Analysis & Statistical Understanding
    print("\n--- Statistical Summary ---")
    print(df.describe())
    
    # Target distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Outcome', data=df)
    plt.title("Distribution of Outcome (Diabetes vs No Diabetes)")
    plt.savefig(os.path.join(PLOTS_DIR, 'target_distribution.png'))
    plt.close()
    
    # Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Feature Correlation Heatmap")
    plt.savefig(os.path.join(PLOTS_DIR, 'correlation_heatmap.png'))
    plt.close()
    
    # 4. Feature/Target Separation
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # 5. Train/Test Split
    # Stratified split ensures the proportion of Outcomes remains consistent in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"\nTrain set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
    
    # 6. Appropriate Preprocessing
    # Standard scaling is crucial for models like Logistic Regression to ensure all features are on the same scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler for inference and future model comparisons
    scaler_path = os.path.join(MODELS_DIR, 'scaler.joblib')
    joblib.dump(scaler, scaler_path)
    print(f"\nScaler saved to {scaler_path}")
    
    # 7. Logistic Regression Training
    print("\n--- Training Baseline Logistic Regression ---")
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # 8. Evaluation Metrics
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_prob)
    
    print("\n--- Baseline Model Metrics (Logistic Regression) ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc:.4f}")
    
    # 9. Confusion Matrix & Visualization
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Diabetes', 'Diabetes'])
    disp.plot(cmap='Blues')
    plt.title("Logistic Regression Confusion Matrix")
    plt.savefig(os.path.join(PLOTS_DIR, 'logreg_confusion_matrix.png'))
    plt.close()
    
    # 10. Save Results
    model_path = os.path.join(MODELS_DIR, 'logreg_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    print("\nDay 1 ML Foundation complete. Plots and models have been generated in their respective directories.")

if __name__ == "__main__":
    main()
