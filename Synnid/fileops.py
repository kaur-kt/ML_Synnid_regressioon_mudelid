''' Failioperatsioonidega seotud moodul '''


import pandas as pd
import joblib

def readTheFile(path):
    data = pd.read_csv(path, sep=";", na_values='?')
    df = pd.DataFrame(data)
    #checkResults(df)
    return df

def saveTheModel(model, model_name, X):
    # Lisame paketina, kus lisainfo, nagu mudel, tunnused ja versioon
    package = {
        "model": model,
        "features": X.columns.tolist(),
        "version": "1.0"
        }
    # paketi salvetamine
    joblib.dump(package, model_name)
    return None

def loadTheModel(path_to_model):
    # paketi laadimine
    package = joblib.load(path_to_model)
    # mudeli salvestamine paketist
    model = package["model"]
    return model
