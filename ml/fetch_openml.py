import pandas as pd
from sklearn.datasets import fetch_openml

try:
    print("Fetching heart disease...")
    heart = fetch_openml(name='heart-statlog', version=1, as_frame=True)
    heart_df = heart.frame
    print("Heart shape:", heart_df.shape)
    print("Heart columns:", heart_df.columns.tolist())
except Exception as e:
    print("Error fetching heart:", e)

try:
    print("\nFetching kidney disease...")
    kidney = fetch_openml(name='chronic_kidney_disease', version=1, as_frame=True)
    kidney_df = kidney.frame
    print("Kidney shape:", kidney_df.shape)
    print("Kidney columns:", kidney_df.columns.tolist())
except Exception as e:
    print("Error fetching kidney:", e)

try:
    print("\nFetching liver patient...")
    liver = fetch_openml(name='ilpd', version=1, as_frame=True)
    liver_df = liver.frame
    print("Liver shape:", liver_df.shape)
    print("Liver columns:", liver_df.columns.tolist())
except Exception as e:
    print("Error fetching liver:", e)
