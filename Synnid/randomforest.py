''' Masinõppe meetod Random Forest '''


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
#path = 'synnid.csv'
save_model_name_rf = "synnimudel_rf.pkl"
save_model_name_gb = "synnimudel_gb.pkl"

def randomForestModel(df):

    # Siin proovime Random Forrest ja pipeline'i, miks viimane:
    #   puuduvate väärtuste automaatne käsitlemine
    #   kategooriate õigesti kodeerimine
    #   numbriliste väärtuste skaleerimine
    #  uute andmetega töötamine, otse 
    #  andmelekete vältimine

    print("--- Random Forest meetodiga mudeli koostamine ja treenimine ---")
          
    # Tunnused ja märgendid
    X = df.drop(columns=["Sünnikaal","Sünnipikkus"])
    y = df[["Sünnikaal","Sünnipikkus"]]

    print(df.head())
    print(X)

    # Tunnused, eristame numbrilised ja kategoorilised tunnused
    num_features = ["Raseduskestus päevades","Ema vanus","Isa vanus"]
    cat_features = ["Ema perekonnaseis","Suitsetamine kokku","Lapse sugu"] # kas lisada ka [Sünnitusviis]?

    # Toru/Pipeline, moodustame numbrilise
    numerical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")), # kui peaks siiski leiduma tühje välju, siis imputeerime, nt mediaanväärtused
        ("scaler", StandardScaler()) # Kasutame skaalerit , kas StandardScaler või MinMaxScaler
        ])
    # Toru/Pipeline, moodustame kategoorilise
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")), # kui peaks siiski leiduma tühje välju, siis imputeerime, nt popimad väärtused
        ("onehot", OneHotEncoder(handle_unknown="ignore")) # onhotenkooder, käsitsi kodeerimst pole siis vaja, tundmatuid ignoreerimie
        ])

    # Paneme torud kokku :)
    preprocessor = ColumnTransformer([
        ("num", numerical_pipeline, num_features),
        ("cat", cat_pipeline, cat_features)
        ])
    # Loome mudeli, siin kasutame vräpperit, sisuliselt kaks mudelit ühes, et saada kahte väljundit, nb! sõltumatut väljundit
    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))

    # Koostame lõpliku ja täieliku toru, elik mudeli
    pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("model", model)
        ])
    # Treening- ja testandmete ning vastavate märgendite moodustamine 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treenimine
    pipeline.fit(X_train, y_train)

    # Testimine
    y_pred = pipeline.predict(X_test)

    #print(y_pred) # ennustuste kontroll välaprint

    # Hindame mudelit. Mudeli kvaliteedinäitajate arvutamine
    #rmse_kaal = mean_squared_error(y_test["Sünnikaal"], y_pred[:, 0], squared=False) # mul vist vana versioon, siin see ei tööta ja läeb sis ringiga
    mse_kaal = mean_squared_error(y_test["Sünnikaal"], y_pred[:, 0])
    rmse_kaal = np.sqrt(mse_kaal)

    mse_pikkus = mean_squared_error(y_test["Sünnipikkus"], y_pred[:, 1])
    rmse_pikkus = np.sqrt(mse_pikkus)
    #rmse_pikkus = mean_squared_error(y_test["Sünnipikkus"], y_pred[:, 1], squared=False) # sama laul, mul se põrsas ei toeta seda

    r2_kaal = r2_score(y_test["Sünnikaal"], y_pred[:, 0])
    r2_pikkus = r2_score(y_test["Sünnipikkus"], y_pred[:, 1])

    # Mudeli kvaliteedinäitajate väljaprintimine
    print("Random Forest")
    print(f"Kaal RMSE: {rmse_kaal:.2f}")
    print(f"Pikkus RMSE: {rmse_pikkus:.2f}")
    print(f"Kaal R2: {r2_kaal:.3f}")
    print(f"Pikkus R2: {r2_pikkus:.3f}")

    # Salvestame mudeli tulevastele põlvedele :)
    saveTheModel(pipeline, save_model_name_rf, X)

    return pipeline, X_train, y_train, X_test, y_test, X
