import requests

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint, payload):
    print(f"Testing {endpoint}...")
    try:
        res = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        res.raise_for_status()
        print(f"SUCCESS: {res.json()}")
    except Exception as e:
        print(f"FAILED {endpoint}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

diabetes_data = {
    "Pregnancies": 1,
    "Glucose": 85,
    "BloodPressure": 66,
    "SkinThickness": 29,
    "Insulin": 45,
    "BMI": 26.6,
    "DiabetesPedigreeFunction": 0.351,
    "Age": 31
}

heart_data = {
    "age": 52,
    "sex": 1,
    "cp": 0,
    "trestbps": 125,
    "chol": 212,
    "fbs": 0,
    "restecg": 1,
    "thalach": 168,
    "exang": 0,
    "oldpeak": 1.0,
    "slope": 2,
    "ca": 2,
    "thal": 3
}

kidney_data = {
    "age": 48.0,
    "bp": 80.0,
    "sg": 1.020,
    "al": 1.0,
    "su": 0.0,
    "rbc": "normal",
    "pc": "normal",
    "pcc": "notpresent",
    "ba": "notpresent",
    "bgr": 121.0,
    "bu": 36.0,
    "sc": 1.2,
    "sod": 138.0,
    "pot": 4.4,
    "hemo": 15.4,
    "pcv": "44",
    "wc": "7800",
    "rc": "5.2",
    "htn": "yes",
    "dm": "yes",
    "cad": "no",
    "appet": "good",
    "pe": "no",
    "ane": "no"
}

liver_data = {
    "Age": 65,
    "Gender": 0,
    "Total_Bilirubin": 0.7,
    "Direct_Bilirubin": 0.1,
    "Alkaline_Phosphotase": 187.0,
    "Alamine_Aminotransferase": 16.0,
    "Aspartate_Aminotransferase": 18.0,
    "Total_Protiens": 6.8,
    "Albumin": 3.3,
    "Albumin_and_Globulin_Ratio": 0.9
}

print("Testing /diseases endpoint...")
try:
    res = requests.get(f"{BASE_URL}/diseases")
    res.raise_for_status()
    print("SUCCESS: /diseases")
except Exception as e:
    print(f"FAILED /diseases: {e}")

test_endpoint("/predict/diabetes", diabetes_data)
test_endpoint("/predict/heart", heart_data)
test_endpoint("/predict/kidney", kidney_data)
test_endpoint("/predict/liver", liver_data)
