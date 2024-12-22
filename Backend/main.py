from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd
import numpy as np

#creation de l'application
app = FastAPI()

# charger le modèle
model = joblib.load("scoring_credit.pkl")

# Définir le schéma de données attendu
class InputData(BaseModel):
    age: int
    credit_amount: float
    duration: int
    housing: str  # "free", "own", "rent"
    saving_accounts: str  # "little", "moderate", "quite rich", "rich"


@app.post("/predict")
def predict(data : InputData):
    # Conversion des colonnes catégoriques Housing
    housing_free = 1 if data.housing == "free" else 0
    housing_own = 1 if data.housing == "own" else 0
    housing_rent = 1 if data.housing == "rent" else 0

    # Conversion des colonnes catégoriques Saving accounts
    saving_little = 1 if data.saving_accounts == "little" else 0
    saving_moderate = 1 if data.saving_accounts == "moderate" else 0
    saving_quite_rich = 1 if data.saving_accounts == "quite rich" else 0
    saving_rich = 1 if data.saving_accounts == "rich" else 0


    # Construire la liste des features dans le bon ordre
    features = np.array([
        data.age,
        data.credit_amount,
        data.duration,
        housing_free,
        housing_own,
        housing_rent,
        saving_little,
        saving_moderate,
        saving_quite_rich,
        saving_rich
    ]).reshape(1, -1)
    print(features)

    # Faire la prédiction
    prediction = model.predict(features)

    # Convertir la prédiction en type natif
    prediction_value = prediction[0] if isinstance(prediction[0], (int, float, bool)) else prediction[0].item()

    return {"prediction":prediction_value}