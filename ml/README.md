# Machine Learning Pipeline

This directory contains the machine learning foundation of the Disease Risk Predictor project.

## Workflow

1. **Dataset Loading**: 
   The Pima Indians Diabetes Dataset is automatically downloaded and loaded into a Pandas DataFrame.

2. **Data Cleaning & Preprocessing**:
   - Zero values in physiological metrics (Glucose, BloodPressure, SkinThickness, Insulin, BMI) are biologically impossible. These are treated as missing values and imputed using the median to provide robustness against outliers.
   - Features are standardized using `StandardScaler` to ensure scale-invariant models (like Logistic Regression) perform optimally.

3. **Model Selection**:
   Three models were trained and evaluated on a stratified 20% test set:
   - Logistic Regression
   - Random Forest
   - XGBoost

4. **Model Comparison Results**:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.7078 | 0.6000 | 0.5000 | 0.5455 | 0.8130 |
| **Random Forest** | **0.7792** | **0.7174** | **0.6111** | **0.6600** | **0.8179** |
| XGBoost | 0.7727 | 0.7021 | 0.6111 | 0.6535 | 0.8154 |

   *Decision: Random Forest was selected as the final model due to its superior ROC-AUC score and overall robust performance across all metrics.*

5. **Explainable AI (SHAP)**:
   The selected Random Forest model is wrapped in a `shap.TreeExplainer`. This allows us to break down every individual prediction into feature contributions (impact scores and directions), ensuring transparency in the risk assessment process.
