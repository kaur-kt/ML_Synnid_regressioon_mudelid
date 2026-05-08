''' Masinõppe meetod Gradient Boosting '''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import sys
import joblib

from fileops import saveTheModel, loadTheModel

save_model_name_gb = "synnimudel_gb.pkl"

def gradientBoostingModel(df):
    # Siin proovime Gradient Boosting ja pipeline'i

    print("--- Gradient Boosting meetodiga mudeli koostamine ja treenimine ---")

    # Tunnused ja märgendid
    X = df.drop(columns=["Sünnikaal"])
    y = df["Sünnikaal"]

    # Tunnused, eristame numbrilised ja kategoorilised tunnused
    numerical_features = ["Raseduskestus päevades","Ema vanus","Isa vanus"]
    cat_features = ["Ema perekonnaseis","Suitsetamine kokku","Lapse sugu"]

    # Eeltöötlus
    preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features) # OneHotEncoder teisendab kategoorilised tunnused arvudeks/vektoriks
    ]
)
    # Mudel, mittelineaarsete seoste õppimine
    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
        )

    # Toru/pipeline moodustamine
    pipeline = Pipeline(steps=[
        ("preprocessing", preprocessor),
        ("model", model)
        ])

    # Treening- ja testandmete ning vastavate märgendite moodustamine 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Mudeli treenimine
    pipeline.fit(X_train, y_train)

    # Testime
    y_pred = pipeline.predict(X_test)

    print(y_pred)

    # Hindame mudelit
    mse_kaal = mean_squared_error(y_test, y_pred)
    rmse_kaal = np.sqrt(mse_kaal)

    r2_kaal = r2_score(y_test, y_pred)

    print("Gradient Boosting")
    print(f"RMSE: {rmse_kaal:.2f}")
    print(f"R2: {r2_kaal:.3f}") # seletab mudeli sünnikaalu varieeruvust, mida kõrgem 0'st seda parem, 0=keskmine

    # Salvestame mudeli
    saveTheModel(pipeline, save_model_name_gb, X)

    return pipeline, X_train, y_train, X_test, y_test, X

