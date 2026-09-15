import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    print("Health Check:", response.json())

def test_predict():
    payload = {
        "Pregnancies": 6,
        "Glucose": 148,
        "BloodPressure": 72,
        "SkinThickness": 35,
        "Insulin": 79,
        "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627,
        "Age": 50
    }
    response = client.post("/predict", json=payload)
    if response.status_code != 200:
        print("Error Response:", response.text)
    assert response.status_code == 200
    print("Predict Response:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health()
    test_predict()
    print("All backend tests passed successfully!")
