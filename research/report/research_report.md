# Explainable AI for Multi-Disease Risk Assessment: A Machine Learning Approach
**Author:** AI/ML Engineer Candidate  
**Date:** September 2026

## Abstract
The application of machine learning in healthcare offers significant potential for early disease detection across various clinical domains. However, the "black box" nature of complex models often hinders clinical adoption. This study develops a comprehensive predictive system for four major conditions: Diabetes, Heart Disease, Chronic Kidney Disease (CKD), and Liver Disease. By training disease-specific Random Forest models, we achieved robust classification performance, notably reaching an ROC-AUC of 0.9993 for CKD and 0.9069 for Heart Disease. To address interpretability, SHapley Additive exPlanations (SHAP) were integrated to provide instance-level transparency. The unified models were deployed via a FastAPI backend and a dynamic cross-platform Flutter application, demonstrating a highly scalable pipeline from raw data preprocessing to a user-facing Explainable AI (XAI) platform.

## 1. Introduction
Early assessment of disease risk can significantly improve patient outcomes through prompt clinical intervention. While modern machine learning algorithms can predict these risks with high accuracy, medical applications require absolute transparency. Clinicians and users must understand the underlying physiological factors driving a prediction. This project bridges this gap by combining robust predictive modeling with Explainable AI and deploying it via a dynamically scaling mobile architecture capable of supporting multiple distinct diseases simultaneously.

## 2. Related Work
Recent literature emphasizes the necessity of interpretability in clinical decision support systems (CDSS). Lundberg and Lee (2017) introduced SHAP as a unified approach to interpreting model predictions. Subsequent studies have demonstrated the utility of SHAP in medical datasets, showing that tree-based ensembles (like Random Forests) combined with post-hoc explainers often outperform traditional linear models in both accuracy and interpretability, particularly when dealing with non-linear relationships in clinical data.

## 3. Dataset and Methodology
### 3.1 Datasets
The platform integrates four distinct public health datasets:
1. **Diabetes:** Pima Indians Dataset (768 instances, 8 features).
2. **Heart Disease:** Cleveland Heart Dataset (303 instances, 13 features).
3. **Chronic Kidney Disease:** UCI CKD Dataset (400 instances, 24 features).
4. **Liver Disease:** Indian Liver Patient Records (583 instances, 10 features).

### 3.2 Preprocessing
Each dataset required unique, rigorous preprocessing pipelines:
- **Missing Values:** Physically impossible zeros in the Diabetes dataset were treated via median imputation. The Kidney dataset required complex imputation combining median (for continuous variables) and mode (for categorical variables) strategies.
- **Categorical Encoding:** The Kidney and Liver datasets required specific encoding strategies (Label Encoding and mapping) to handle text-based clinical inputs.
- **Serialization:** All preprocessing steps were securely serialized via `joblib` into distinct dictionary objects, ensuring exact reproducibility between the training environment and the real-time FastAPI inference engine.

### 3.3 Experimental Setup
Random Forest classifiers were chosen as the baseline architecture across all four diseases due to their robustness to clinical data outliers, lack of strict scaling requirements, and excellent compatibility with `shap.TreeExplainer`. The models were evaluated using Accuracy, Precision, Recall, F1 Score, and ROC-AUC. 

## 4. Results
The model comparison yielded the following results on the test sets:

| Disease  | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| -------- | -------: | --------: | -----: | -------: | ------: |
| Diabetes |   0.7532 |    0.6538 | 0.6296 |   0.6415 |  0.8179 |
| Heart    |   0.8197 |    0.8000 | 0.8485 |   0.8235 |  0.9069 |
| Kidney   |   0.9875 |    0.9792 | 1.0000 |   0.9895 |  0.9993 |
| Liver    |   0.7436 |    0.5000 | 0.2059 |   0.2917 |  0.7412 |

The algorithms demonstrated strong discrimination capability, particularly for Chronic Kidney Disease and Heart Disease. The Liver model exhibited lower recall, indicating the dataset's inherent noise and class imbalance, serving as an excellent baseline for future algorithmic refinement.

## 5. Explainable AI Analysis
A `shap.TreeExplainer` was applied to all four Random Forest models. For local (individual) predictions, the FastAPI backend calculates exact SHAP values in real-time. The mobile application dynamically parses this 3D/2D array output to display the top three contributing factors and their directional impact on the patient's risk score (e.g., identifying that elevated Serum Creatinine is aggressively increasing a specific patient's CKD risk).

## 6. Discussion and Limitations
The system successfully demonstrates the scalable integration of complex ML modeling with accessible XAI across multiple domains. However, limitations exist:
- **Dataset Constraints:** The models are trained on specific demographic datasets (e.g., Pima Indians for Diabetes, Indian patients for Liver disease). Generalization to broader populations requires retraining on more diverse, modern datasets.
- **Clinical Validation:** This system has not undergone clinical trials and is explicitly positioned as an educational and research demonstration, not a medical diagnostic tool.

## 7. Conclusion and Future Work
This project successfully implemented an end-to-end, multi-disease explainable risk predictor. The combination of Random Forest classifiers with SHAP provides both high predictive performance and essential transparency. Future work will focus on integrating more comprehensive datasets, handling severe class imbalances (specifically in Liver disease), and conducting user studies to evaluate the effectiveness of the XAI visualizations for non-expert users.

## 8. References
1. Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *Advances in neural information processing systems*, 30.
2. UCI Machine Learning Repository. (Various Years). Heart Disease, Chronic Kidney Disease, and Indian Liver Patient Datasets.
