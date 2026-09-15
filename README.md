# VitaGuard AI: Explainable Disease Risk Predictor 🧬

![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

**VitaGuard AI** is a comprehensive, end-to-end digital health platform designed to assess the risk of chronic illnesses, including diabetes, heart disease, chronic kidney disease, and liver disease. Built with a full-stack architecture, it features a cross-platform Flutter mobile application, a scalable Python FastAPI backend, and robust machine learning models. 

Crucially, the platform integrates **SHapley Additive exPlanations (SHAP)** to provide **Explainable AI (XAI)** insights, transforming black-box predictions into transparent, clinical factor analyses. The application includes dynamic multilingual support, persistent assessment history, and professional PDF report generation, demonstrating a complete integration of modern software engineering and clinical AI.

---

## 🌟 Key Features

* **Explainable AI (XAI):** Predicts risk levels using advanced machine learning models (Random Forest/Gradient Boosting) and visualizes the exact clinical drivers (e.g., Glucose, Blood Pressure) using SHAP values.
* **Dynamic Multi-Lingual Engine:** A Python backend translation matrix serves the entire UI—including dynamic diagnostic forms, hints, and results—instantly in **English, Spanish, French, and Urdu**.
* **Glassmorphic UI Design:** A stunning, modern dark-mode Flutter interface utilizing advanced blur filters and sleek animations.
* **Persistent Patient History:** All AI assessments are serialized and saved securely to local device storage for immediate recall.
* **Professional Medical Export:** One-tap PDF generation that creates a printable, localized medical report summarizing the risk factors and SHAP visual insights.

---

## 🏗 Architecture & Technical Stack

This system is architected as a decoupled, microservices-oriented application. 
1. **Machine Learning (`ml/`):** Utilizes `scikit-learn` to train and serialize predictive models. Explainability is achieved via the `shap` library, calculating feature importance values dynamically.
2. **REST API Backend (`backend/`):** Built with `FastAPI`, providing high-performance, asynchronous endpoints. It handles model inference and serves dynamic UI configurations, utilizing an in-memory translation matrix to support instant localization.
3. **Mobile Client (`mobile/disease_risk_app/`):** A responsive Flutter mobile application. It features a dynamic form engine that constructs diagnostic interfaces directly from the backend's schema. State management and API integrations allow for real-time risk assessment and SHAP value visualization using `fl_chart`.

---

## 🚀 Getting Started

To run this project locally, you will need to start both the Python FastAPI backend and the Flutter mobile application.

### 1. Start the Backend
Navigate to the backend directory and install the dependencies:
```bash
cd backend
pip install -r requirements.txt
```
Start the Uvicorn server:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Configure the Mobile App
Open `mobile/disease_risk_app/lib/api_service.dart`. You must point the Flutter app to where your backend is running.
- **For Emulator Testing:** Set it to `http://10.0.2.2:8000` (Android) or `http://127.0.0.1:8000` (iOS).
- **For Physical Device:** Change it to your computer's local Wi-Fi IPv4 address (e.g., `http://192.168.1.5:8000`).

### 3. Run the Flutter App
Navigate to the mobile app directory and fetch packages:
```bash
cd mobile/disease_risk_app
flutter pub get
```
Run the application on your connected device or emulator:
```bash
flutter run
```

---

## 📸 Application Screenshots

*(Upload and add your screenshots here before publishing!)*
* `<img src="path/to/home_screen.png" width="200" />`
* `<img src="path/to/form_screen.png" width="200" />`
* `<img src="path/to/result_screen.png" width="200" />`
* `<img src="path/to/history_screen.png" width="200" />`

---

## 🔮 Limitations and Future Work
A primary limitation of the current system is its reliance on static, pre-trained scikit-learn models, which do not adapt to new patient data over time (lack of continuous learning). Furthermore, the clinical datasets utilized for training may contain inherent demographic biases, potentially affecting prediction accuracy across diverse populations. 

Future work should focus on implementing **federated learning** to improve models while maintaining patient privacy. Additionally, rigorous clinical validation against real-world electronic health records (EHR) and expanding the integration of FHIR (Fast Healthcare Interoperability Resources) standards would be essential before formal clinical deployment. 

---
*Keywords: Explainable AI (XAI), SHAP (SHapley Additive exPlanations), Clinical Decision Support Systems (CDSS), Predictive Modeling, Digital Health, Mobile Health (mHealth), FastAPI, Flutter, Machine Learning Interpretability, Multilingual Architecture.*
