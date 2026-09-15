import os
import requests
import pandas as pd
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def try_download(filename, urls):
    for url in urls:
        try:
            print(f"Trying {url}...")
            res = requests.get(url)
            res.raise_for_status()
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(res.content)
            df = pd.read_csv(filepath)
            print(f"SUCCESS: {filename} downloaded. Shape: {df.shape}")
            return True
        except Exception as e:
            print(f"Failed: {e}")
    return False

heart_urls = [
    "https://raw.githubusercontent.com/rashida048/Datasets/master/heart.csv",
    "https://raw.githubusercontent.com/Sanjay-19/Heart-Disease-Prediction/master/heart.csv"
]
kidney_urls = [
    "https://raw.githubusercontent.com/subhadipml/Chronic-Kidney-Disease-Prediction/master/kidney_disease.csv",
    "https://raw.githubusercontent.com/harshit4/Chronic-Kidney-Disease/master/kidney_disease.csv",
    "https://raw.githubusercontent.com/ShubhamTiwari909/Chronic-Kidney-Disease-Prediction/master/kidney_disease.csv"
]
liver_urls = [
    "https://raw.githubusercontent.com/pik1989/IndianLiverPatient-Dataset/master/indian_liver_patient.csv",
    "https://raw.githubusercontent.com/Siddarthpi/Indian-Liver-Patient-Dataset/master/indian_liver_patient.csv"
]

try_download('heart.csv', heart_urls)
try_download('kidney_disease.csv', kidney_urls)
try_download('indian_liver_patient.csv', liver_urls)
