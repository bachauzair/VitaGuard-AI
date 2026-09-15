import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import shap

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_FILE = os.path.join(DATA_DIR, 'diabetes.csv')

def load_and_preprocess_data():
    """Reproduces the exact preprocessing pipeline from Day 1."""
    df = pd.read_csv(DATA_FILE)
    
    invalid_zero_features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[invalid_zero_features] = df[invalid_zero_features].replace(0, np.nan)
    
    for feature in invalid_zero_features:
        df[feature] = df[feature].fillna(df[feature].median())
        
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    # Notice we keep X_train and X_test as DataFrames with feature names for SHAP and XGBoost
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X.columns)
    
    # Save the scaler
    scaler_path = os.path.join(MODELS_DIR, 'scaler.joblib')
    joblib.dump(scaler, scaler_path)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Trains and compares multiple machine learning models."""
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'XGBoost': XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    }
    
    results = []
    trained_models = {}
    
    plt.figure(figsize=(10, 8))
    
    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)
        trained_models[name] = model
        
        # Predict
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc = roc_auc_score(y_test, y_prob)
        
        results.append({
            'Model': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1 Score': f1,
            'ROC-AUC': roc
        })
        
        # ROC Curve
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        plt.plot(fpr, tpr, label=f'{name} (AUC = {roc:.3f})')
        
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - Model Comparison')
    plt.legend()
    plt.savefig(os.path.join(PLOTS_DIR, 'roc_curves_comparison.png'))
    plt.close()
    
    results_df = pd.DataFrame(results).set_index('Model')
    print("\n--- Model Comparison Table ---")
    print(results_df.round(4))
    
    # Model Selection Logic
    # We prioritize ROC-AUC for class separation and F1 Score as it balances Precision and Recall
    # which is important in medical datasets with some imbalance.
    best_model_name = results_df['ROC-AUC'].idxmax()
    print(f"\nSelected Best Model: {best_model_name} (based on highest ROC-AUC)")
    
    return trained_models[best_model_name], best_model_name

def implement_shap(model, X_train, X_test, model_name):
    """Implements SHAP explainability on the best model."""
    print(f"\n--- Implementing SHAP for {model_name} ---")
    
    # Depending on the model type, use the appropriate SHAP explainer
    if isinstance(model, RandomForestClassifier) or isinstance(model, XGBClassifier):
        explainer = shap.TreeExplainer(model)
    else:
        explainer = shap.LinearExplainer(model, X_train)
        
    # Calculate SHAP values for the test set
    shap_values = explainer.shap_values(X_test)
    
    # For binary classification in some tree models (like RandomForest), shap_values might be a list or 3D array
    if isinstance(shap_values, list):
        shap_values_for_class_1 = shap_values[1] # We care about the positive class (Diabetes)
    elif len(np.array(shap_values).shape) == 3:
        shap_values_for_class_1 = shap_values[:, :, 1]
    else:
        shap_values_for_class_1 = shap_values

    # SHAP Summary Plot
    plt.figure()
    shap.summary_plot(shap_values_for_class_1, X_test, show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'shap_summary_plot.png'), bbox_inches='tight')
    plt.close()
    print(f"SHAP summary plot saved to {PLOTS_DIR}")
    
    # Explain an Individual Prediction
    # Let's pick a high-risk instance from the test set for demonstration
    y_prob = model.predict_proba(X_test)[:, 1]
    high_risk_index = np.argmax(y_prob)
    
    instance = X_test.iloc[[high_risk_index]]
    instance_shap = shap_values_for_class_1[high_risk_index]
    
    # Create the structured JSON response as required
    feature_names = X_test.columns
    contributions = []
    
    for i, feature in enumerate(feature_names):
        impact = float(instance_shap[i])
        if abs(impact) > 0.01: # Filter out near-zero impacts for clarity
            contributions.append({
                "name": feature,
                "impact": abs(impact),
                "direction": "increasing" if impact > 0 else "decreasing"
            })
            
    # Sort by absolute impact descending
    contributions = sorted(contributions, key=lambda x: x['impact'], reverse=True)
    
    print("\n--- Individual Prediction Explanation (JSON) ---")
    print(json.dumps(contributions[:3], indent=2)) # Top 3 contributing factors

def main():
    print("Starting Day 2: Model Comparison and Explainable AI...")
    
    X_train_scaled, X_test_scaled, y_train, y_test, scaler = load_and_preprocess_data()
    
    best_model, best_model_name = train_and_evaluate_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Save the best model
    best_model_path = os.path.join(MODELS_DIR, 'best_model.joblib')
    joblib.dump(best_model, best_model_path)
    print(f"\nBest model saved to {best_model_path}")
    
    # SHAP integration
    implement_shap(best_model, X_train_scaled, X_test_scaled, best_model_name)
    
    print("\nDay 2 Complete.")

if __name__ == "__main__":
    main()
