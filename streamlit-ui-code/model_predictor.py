import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib


CREDIT_RISK_MODEL_PATH = 'artifacts/model_data.joblib'

# Load the model and its components
model_data = joblib.load(CREDIT_RISK_MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']

def create_model_input(age, income, loan_amount, loan_tenure_months,
                       avg_dpd_per_delinquency, delinquency_ratio,
                       credit_utilization_ratio, num_open_accounts,
                       residence_type, loan_purpose, loan_type):


    loan_to_income = loan_amount / income if income > 0 else 0

    # Build input dictionary with dynamic one-hot encoding for categorical variables
    input_data = {
        "age": age,
        "loan_tenure_months": loan_tenure_months,
        "number_of_open_accounts": num_open_accounts,
        "credit_utilization_ratio": credit_utilization_ratio,
        "loan_to_income": loan_to_income,
        "delinquency_ratio": delinquency_ratio,
        "avg_dpd_per_delinquency": avg_dpd_per_delinquency,

        # One-hot encode categorical variables dynamically
        f"residence_type_{residence_type}": 1,
        f"loan_purpose_{loan_purpose}": 1,
        f"loan_type_{loan_type}": 1,
    }

    # Convert to DataFrame
    df = pd.DataFrame([input_data])

    # Add missing columns from training features (fill with 0)
    for col in features:
        if col not in df.columns:
            df[col] = 0.0

    for col in cols_to_scale:
        if col not in df.columns:
            df[col] = 0.0

    # Scale numeric columns as per training
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    return df[features]

# Function to calculate credit score and rating

def calculate_credit_score(input_df, base_score=300, scale_length=600):
    # Predict default probability using trained model
    probability = model.predict_proba(input_df)[0][1]

    # Convert probability to credit score
    credit_score = int(base_score + (1 - probability) * scale_length)

    # Assign rating based on credit score
    if credit_score < 500:
        rating = "Poor"
    elif credit_score < 650:
        rating = "Average"
    elif credit_score < 750:
        rating = "Good"
    else:
        rating = "Excellent"

    return probability, credit_score, rating

def predict(age, income, loan_amount, loan_tenure_months,
            avg_dpd_per_delinquency, delinquency_ratio,
            credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):

    # Prepare model-ready input
    input_df = create_model_input(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_delinquency, delinquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    # Calculate probability, credit score, and rating
    return calculate_credit_score(input_df)
