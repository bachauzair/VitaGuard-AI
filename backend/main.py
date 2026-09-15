from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import shap
from translations import translations
import os

app = FastAPI(title="Multi-Disease AI Risk Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'ml', 'models')

# Load Artifacts
def load_artifacts(prefix):
    try:
        model = joblib.load(os.path.join(MODELS_DIR, f"{prefix}_model.pkl"))
        prep = joblib.load(os.path.join(MODELS_DIR, f"{prefix}_preprocessor.pkl"))
        feats = joblib.load(os.path.join(MODELS_DIR, f"{prefix}_features.pkl"))
        # Using TreeExplainer
        explainer = shap.TreeExplainer(model)
        return model, prep, feats, explainer
    except Exception as e:
        print(f"Error loading {prefix} models: {e}")
        return None, None, None, None

models = {}
preprocessors = {}
features = {}
explainers = {}

for disease in ['diabetes', 'heart', 'kidney', 'liver']:
    m, p, f, e = load_artifacts(disease)
    models[disease] = m
    preprocessors[disease] = p
    features[disease] = f
    explainers[disease] = e


# Pydantic Schemas
class DiabetesData(BaseModel):
    Pregnancies: int = Field(..., ge=0)
    Glucose: float = Field(..., gt=0)
    BloodPressure: float = Field(..., gt=0)
    SkinThickness: float = Field(..., gt=0)
    Insulin: float = Field(..., gt=0)
    BMI: float = Field(..., gt=0)
    DiabetesPedigreeFunction: float = Field(..., gt=0)
    Age: int = Field(..., gt=0)

class HeartData(BaseModel):
    age: int = Field(..., gt=0)
    sex: int = Field(..., description="1 = male; 0 = female")
    cp: int = Field(..., description="Chest pain type (0-3)")
    trestbps: float = Field(...)
    chol: float = Field(...)
    fbs: int = Field(..., description="Fasting blood sugar > 120 (1=true, 0=false)")
    restecg: int = Field(...)
    thalach: float = Field(...)
    exang: int = Field(..., description="Exercise induced angina (1=yes, 0=no)")
    oldpeak: float = Field(...)
    slope: int = Field(...)
    ca: int = Field(...)
    thal: int = Field(...)

class KidneyData(BaseModel):
    age: float = Field(...)
    bp: float = Field(...)
    sg: float = Field(...)
    al: float = Field(...)
    su: float = Field(...)
    rbc: str = Field(...)
    pc: str = Field(...)
    pcc: str = Field(...)
    ba: str = Field(...)
    bgr: float = Field(...)
    bu: float = Field(...)
    sc: float = Field(...)
    sod: float = Field(...)
    pot: float = Field(...)
    hemo: float = Field(...)
    pcv: float = Field(...)
    wc: float = Field(...)
    rc: float = Field(...)
    htn: str = Field(...)
    dm: str = Field(...)
    cad: str = Field(...)
    appet: str = Field(...)
    pe: str = Field(...)
    ane: str = Field(...)

class LiverData(BaseModel):
    Age: int = Field(...)
    Gender: int = Field(..., description="1 = Male, 0 = Female")
    Total_Bilirubin: float = Field(...)
    Direct_Bilirubin: float = Field(...)
    Alkaline_Phosphotase: float = Field(...)
    Alamine_Aminotransferase: float = Field(...)
    Aspartate_Aminotransferase: float = Field(...)
    Total_Protiens: float = Field(...)
    Albumin: float = Field(...)
    Albumin_and_Globulin_Ratio: float = Field(...)


@app.get("/diseases")
def get_diseases(lang: str = "en"):
    config = [
            {
                "id": "diabetes",
                "name": "Diabetes",
                "description": "Predict the risk of developing diabetes.",
                "endpoint": "/predict/diabetes",
                "fields": [
                    {"name": "Pregnancies", "label": "Pregnancies", "type": "number", "hint": "Number of times pregnant"},
                    {"name": "Glucose", "label": "Glucose Level", "type": "number", "hint": "Plasma glucose concentration"},
                    {"name": "BloodPressure", "label": "Blood Pressure", "type": "number", "hint": "Diastolic blood pressure (mm Hg)"},
                    {"name": "SkinThickness", "label": "Skin Thickness", "type": "number", "hint": "Triceps skin fold thickness (mm)"},
                    {"name": "Insulin", "label": "Insulin", "type": "number", "hint": "2-Hour serum insulin (mu U/ml)"},
                    {"name": "BMI", "label": "BMI", "type": "number", "hint": "Body mass index"},
                    {"name": "DiabetesPedigreeFunction", "label": "Diabetes Pedigree", "type": "number", "hint": "Diabetes pedigree function"},
                    {"name": "Age", "label": "Age", "type": "number", "hint": "Age in years"}
                ]
            },
            {
                "id": "heart",
                "name": "Heart Disease",
                "description": "Predict the risk of developing heart disease.",
                "endpoint": "/predict/heart",
                "fields": [
                    {"name": "age", "label": "Age", "type": "number", "hint": "Age in years"},
                    {"name": "sex", "label": "Gender", "type": "select", "options": [{"label": "Male", "value": 1}, {"label": "Female", "value": 0}]},
                    {"name": "cp", "label": "Chest Pain Type", "type": "select", "options": [{"label": "Typical Angina", "value": 0}, {"label": "Atypical Angina", "value": 1}, {"label": "Non-anginal Pain", "value": 2}, {"label": "Asymptomatic", "value": 3}]},
                    {"name": "trestbps", "label": "Resting Blood Pressure", "type": "number", "hint": "Resting blood pressure (mm Hg)"},
                    {"name": "chol", "label": "Serum Cholestoral", "type": "number", "hint": "Serum cholestoral in mg/dl"},
                    {"name": "fbs", "label": "Fasting Blood Sugar > 120", "type": "select", "options": [{"label": "True", "value": 1}, {"label": "False", "value": 0}]},
                    {"name": "restecg", "label": "Resting ECG Results", "type": "select", "options": [{"label": "Normal", "value": 0}, {"label": "ST-T wave abnormality", "value": 1}, {"label": "Left ventricular hypertrophy", "value": 2}]},
                    {"name": "thalach", "label": "Max Heart Rate", "type": "number", "hint": "Maximum heart rate achieved"},
                    {"name": "exang", "label": "Exercise Induced Angina", "type": "select", "options": [{"label": "Yes", "value": 1}, {"label": "No", "value": 0}]},
                    {"name": "oldpeak", "label": "ST Depression", "type": "number", "hint": "ST depression induced by exercise"},
                    {"name": "slope", "label": "Slope of Peak ST Segment", "type": "select", "options": [{"label": "Upsloping", "value": 0}, {"label": "Flat", "value": 1}, {"label": "Downsloping", "value": 2}]},
                    {"name": "ca", "label": "Major Vessels Colored by Flourosopy", "type": "number", "hint": "Number of major vessels (0-4)"},
                    {"name": "thal", "label": "Thalassemia", "type": "select", "options": [{"label": "Normal", "value": 1}, {"label": "Fixed Defect", "value": 2}, {"label": "Reversable Defect", "value": 3}]}
                ]
            },
            {
                "id": "kidney",
                "name": "Chronic Kidney Disease",
                "description": "Predict the risk of chronic kidney disease.",
                "endpoint": "/predict/kidney",
                "fields": [
                    {"name": "age", "label": "Age", "type": "number", "hint": "Age in years"},
                    {"name": "bp", "label": "Blood Pressure", "type": "number", "hint": "Blood pressure"},
                    {"name": "sg", "label": "Specific Gravity", "type": "select", "options": [{"label": "1.005", "value": 1.005}, {"label": "1.010", "value": 1.010}, {"label": "1.015", "value": 1.015}, {"label": "1.020", "value": 1.020}, {"label": "1.025", "value": 1.025}]},
                    {"name": "al", "label": "Albumin", "type": "select", "options": [{"label": "0", "value": 0}, {"label": "1", "value": 1}, {"label": "2", "value": 2}, {"label": "3", "value": 3}, {"label": "4", "value": 4}, {"label": "5", "value": 5}]},
                    {"name": "su", "label": "Sugar", "type": "select", "options": [{"label": "0", "value": 0}, {"label": "1", "value": 1}, {"label": "2", "value": 2}, {"label": "3", "value": 3}, {"label": "4", "value": 4}, {"label": "5", "value": 5}]},
                    {"name": "rbc", "label": "Red Blood Cells", "type": "select", "options": [{"label": "Normal", "value": "normal"}, {"label": "Abnormal", "value": "abnormal"}]},
                    {"name": "pc", "label": "Pus Cell", "type": "select", "options": [{"label": "Normal", "value": "normal"}, {"label": "Abnormal", "value": "abnormal"}]},
                    {"name": "pcc", "label": "Pus Cell Clumps", "type": "select", "options": [{"label": "Present", "value": "present"}, {"label": "Not Present", "value": "notpresent"}]},
                    {"name": "ba", "label": "Bacteria", "type": "select", "options": [{"label": "Present", "value": "present"}, {"label": "Not Present", "value": "notpresent"}]},
                    {"name": "bgr", "label": "Blood Glucose Random", "type": "number", "hint": "mgs/dl"},
                    {"name": "bu", "label": "Blood Urea", "type": "number", "hint": "mgs/dl"},
                    {"name": "sc", "label": "Serum Creatinine", "type": "number", "hint": "mgs/dl"},
                    {"name": "sod", "label": "Sodium", "type": "number", "hint": "mEq/L"},
                    {"name": "pot", "label": "Potassium", "type": "number", "hint": "mEq/L"},
                    {"name": "hemo", "label": "Hemoglobin", "type": "number", "hint": "gms"},
                    {"name": "pcv", "label": "Packed Cell Volume", "type": "number", "hint": "volume"},
                    {"name": "wc", "label": "White Blood Cell Count", "type": "number", "hint": "cells/cumm"},
                    {"name": "rc", "label": "Red Blood Cell Count", "type": "number", "hint": "millions/cmm"},
                    {"name": "htn", "label": "Hypertension", "type": "select", "options": [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]},
                    {"name": "dm", "label": "Diabetes Mellitus", "type": "select", "options": [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]},
                    {"name": "cad", "label": "Coronary Artery Disease", "type": "select", "options": [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]},
                    {"name": "appet", "label": "Appetite", "type": "select", "options": [{"label": "Good", "value": "good"}, {"label": "Poor", "value": "poor"}]},
                    {"name": "pe", "label": "Pedal Edema", "type": "select", "options": [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]},
                    {"name": "ane", "label": "Anemia", "type": "select", "options": [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]}
                ]
            },
            {
                "id": "liver",
                "name": "Liver Disease",
                "description": "Predict the risk of liver disease.",
                "endpoint": "/predict/liver",
                "fields": [
                    {"name": "Age", "label": "Age", "type": "number", "hint": "Age in years"},
                    {"name": "Gender", "label": "Gender", "type": "select", "options": [{"label": "Male", "value": 1}, {"label": "Female", "value": 0}]},
                    {"name": "Total_Bilirubin", "label": "Total Bilirubin", "type": "number", "hint": "mg/dL"},
                    {"name": "Direct_Bilirubin", "label": "Direct Bilirubin", "type": "number", "hint": "mg/dL"},
                    {"name": "Alkaline_Phosphotase", "label": "Alkaline Phosphotase", "type": "number", "hint": "IU/L"},
                    {"name": "Alamine_Aminotransferase", "label": "Alamine Aminotransferase", "type": "number", "hint": "IU/L"},
                    {"name": "Aspartate_Aminotransferase", "label": "Aspartate Aminotransferase", "type": "number", "hint": "IU/L"},
                    {"name": "Total_Protiens", "label": "Total Proteins", "type": "number", "hint": "g/dL"},
                    {"name": "Albumin", "label": "Albumin", "type": "number", "hint": "g/dL"},
                    {"name": "Albumin_and_Globulin_Ratio", "label": "A/G Ratio", "type": "number", "hint": "Albumin and Globulin Ratio"}
                ]
            }
        ]
        
    if lang in translations:
        t = translations[lang]
        for disease in config:
            disease['name'] = t.get(disease['name'], disease['name'])
            disease['description'] = t.get(disease['description'], disease['description'])
            for field in disease['fields']:
                field['label'] = t.get(field['label'], field['label'])
                if 'hint' in field:
                    field['hint'] = t.get(field['hint'], field['hint'])
                if 'options' in field:
                    for opt in field['options']:
                        opt['label'] = t.get(opt['label'], opt['label'])
                        
    return {"diseases": config}

def get_risk_level(prob: float) -> str:
    if prob < 0.33:
        return "Low Risk"
    elif prob < 0.66:
        return "Medium Risk"
    else:
        return "High Risk"

def extract_shap(shap_values, feature_names):
    # TreeExplainer outputs either 1D, 2D or 3D arrays depending on the model formulation
    # For binary classification RF it is usually [N, F, 2] or [N, F] depending on exact sklearn/shap version.
    if isinstance(shap_values, list):
        sv = shap_values[1][0]
    elif len(np.array(shap_values).shape) == 3:
        sv = shap_values[0, :, 1]
    elif len(np.array(shap_values).shape) == 2:
        sv = shap_values[0]
    else:
        sv = shap_values
    
    impacts = []
    for i, feature in enumerate(feature_names):
        val = float(sv[i])
        impacts.append({
            "name": feature,
            "impact": abs(val),
            "direction": "increasing" if val > 0 else "decreasing"
        })
        
    # Sort and take top 3
    impacts.sort(key=lambda x: x["impact"], reverse=True)
    return impacts[:3]

def process_prediction(disease: str, input_df: pd.DataFrame):
    if models[disease] is None:
        raise HTTPException(status_code=500, detail=f"{disease.capitalize()} model not found.")
        
    model = models[disease]
    prep = preprocessors[disease]
    feats = features[disease]
    explainer = explainers[disease]
    
    # Reorder columns to match training exactly
    input_df = input_df[feats]
    
    # Preprocess
    if disease == 'kidney':
        scaler = prep['scaler']
        encoders = prep['encoders']
        
        # Apply encoders to categorical columns
        for col, encoder in encoders.items():
            if col in input_df.columns:
                # Need to handle unseen labels gracefully, but assuming valid inputs here
                input_df[col] = encoder.transform(input_df[col].astype(str))
                
        # Scale
        scaled_array = scaler.transform(input_df)
        X_scaled = pd.DataFrame(scaled_array, columns=feats)
    else:
        # Standard scaler only
        scaled_array = prep.transform(input_df)
        X_scaled = pd.DataFrame(scaled_array, columns=feats)
        
    # Predict
    prob = model.predict_proba(X_scaled)[0][1]
    
    # SHAP
    shap_values = explainer.shap_values(X_scaled)
    top_factors = extract_shap(shap_values, feats)
    
    return {
        "risk_level": get_risk_level(prob),
        "confidence_percentage": round(float(prob * 100), 1),
        "top_factors": top_factors
    }


@app.post("/predict/diabetes")
def predict_diabetes(data: DiabetesData):
    input_df = pd.DataFrame([data.model_dump()])
    return process_prediction('diabetes', input_df)

@app.post("/predict/heart")
def predict_heart(data: HeartData):
    input_df = pd.DataFrame([data.model_dump()])
    return process_prediction('heart', input_df)

@app.post("/predict/kidney")
def predict_kidney(data: KidneyData):
    input_dict = data.model_dump()
    # convert string numbers back to string explicitly where needed if any
    input_df = pd.DataFrame([input_dict])
    return process_prediction('kidney', input_df)

@app.post("/predict/liver")
def predict_liver(data: LiverData):
    input_df = pd.DataFrame([data.model_dump()])
    return process_prediction('liver', input_df)
