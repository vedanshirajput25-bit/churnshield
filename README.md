"""
ChurnShield - ML Churn Prediction Model
Uses RFM analysis + Random Forest to predict customer churn risk.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime


def compute_rfm(df: pd.DataFrame, reference_date: str = None) -> pd.DataFrame:
    if reference_date:
        today = datetime.strptime(reference_date, "%Y-%m-%d")
    else:
        today = datetime.today()

    df = df.copy()
    df["last_order_date"] = pd.to_datetime(df["last_order_date"], format="mixed", dayfirst=False)
    df["last_order_date"] = df["last_order_date"].dt.tz_localize(None)

    df["recency"]   = (today - df["last_order_date"]).dt.days
    df["frequency"] = df["num_orders"]
    df["monetary"]  = df["total_spend"]

    scaler = MinMaxScaler(feature_range=(1, 5))
    df["R_score"] = (scaler.fit_transform(df[["recency"]]) * -1 + 6).clip(1, 5)
    df["F_score"] = scaler.fit_transform(df[["frequency"]]).clip(1, 5)
    df["M_score"] = scaler.fit_transform(df[["monetary"]]).clip(1, 5)
    df["rfm_score"] = 0.4 * df["R_score"] + 0.3 * df["F_score"] + 0.3 * df["M_score"]
    return df


def label_churn(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    def get_risk(days):
        if days >= 46:   return "High"
        elif days >= 21: return "Medium"
        else:            return "Low"
    df["churn_risk"]  = df["recency"].apply(get_risk)
    df["churn_label"] = df["churn_risk"].map({"High": 2, "Medium": 1, "Low": 0})
    return df


FEATURES = ["R_score", "F_score", "M_score", "rfm_score", "recency", "frequency", "monetary"]

def train_model(df: pd.DataFrame):
    X = df[FEATURES]
    y = df["churn_label"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model


def generate_retention_message(row) -> str:
    name = str(row.get("customer_name", "Customer")).split()[0]
    risk = row.get("churn_risk", "Low")
    if risk == "High":
        return (f"Namaste {name} ji! Aapko humari yaad aa rahi thi! "
                f"Aapke liye special 20% discount: WELCOME{name[:3].upper()}20. Aaj hi order karein!")
    elif risk == "Medium":
        return (f"Hi {name}! We have exciting new arrivals just for you. "
                f"Use code SAVE10 for 10% off your next order!")
    else:
        return (f"Hi {name}! Thank you for being a loyal customer. "
                f"As a VIP member, enjoy FREE shipping on your next order. Code: VIPSHIP")


def predict_churn(df: pd.DataFrame):
    df = compute_rfm(df, reference_date="2026-05-09")
    df = label_churn(df)
    model = train_model(df)
    proba = model.predict_proba(df[FEATURES])
    if 2 in model.classes_:
        high_idx = list(model.classes_).index(2)
        df["churn_probability"] = (proba[:, high_idx] * 100).round(1)
    else:
        df["churn_probability"] = 0.0
    df["retention_message"] = df.apply(generate_retention_message, axis=1)
    return df, model
