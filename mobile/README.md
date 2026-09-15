# AI-Powered Disease Risk Predictor - Mobile App

This directory contains the Flutter application for the Disease Risk Predictor.

## Features
- **Cross-Platform:** Built with Flutter, capable of compiling to iOS, Android, and Web.
- **Professional UI/UX:** Clean, modern, and intuitive design tailored for health tech applications.
- **Real-Time Inference:** Communicates with the FastAPI backend to provide instant risk assessments.
- **Explainable AI Visualization:** Parses and beautifully displays the JSON SHAP values, showing users exactly which health metrics (e.g., Glucose, BMI) impacted their result and in which direction.

## Setup Instructions

1. **Prerequisites:** Ensure you have the [Flutter SDK](https://docs.flutter.dev/get-started/install) installed.

2. **Navigate to the mobile directory:**
   ```bash
   cd disease-risk-predictor/mobile/disease_risk_app
   ```

3. **Install dependencies:**
   ```bash
   flutter pub get
   ```

4. **Run the Application:**
   ```bash
   flutter run
   ```
   *Note: Make sure your FastAPI backend is running. If you are using an Android Emulator, you may need to change `baseUrl` in `lib/api_service.dart` to `http://10.0.2.2:8000`.*
