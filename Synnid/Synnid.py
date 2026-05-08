''' Sündide andmestiku puhastamine, analüüs ja mitmete sünnikaalu ennustamise regressioni mudelite loomine ning treenimine. Loodud mudelite võrdlus. '''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import sys
#import shap
import joblib

import matplotlib.patheffects as path_effects
from randomforest import randomForestModel
from gradientboosting import gradientBoostingModel
from fileops import readTheFile, saveTheModel, loadTheModel
from visuaalanalyys import analysisTheData
from tuunirandomforest import tuneTheModel
from neuralnetwork import neuralNetworkModel_pt, testTorchPred



# Alates 37 nädalast loetakse norm raseduspikkuseks (37nädalat x 7päeva)
NORM_RASEDUSKESTUS = 259

#plt.use('TkAgg')  # või 'Agg' kui ei taha akent

path = 'synnid.csv' # toorandmete fail
save_model_name_rf = "synnimudel_rf.pkl" # fail treenitud Random Forest mudeli salvestamisks
save_model_name_gb = "synnimudel_gb.pkl" # fail treenitud Gradient Boosting mudeli salvestamisks


def cleanUpRawData(df):
    checkResults(df)
    df.dropna(inplace=True) # read, kus väärtus puudub, eemaldame
    print("--- Puuduvate andmete kontroll peale eemaldamisi ---")
    print(df.isna().sum()) # uus kontroll
    return df

def checkResults(df):
    print("--- Esimesed kirjed ---")
    print(df.head())
    print("--- Puuduvad andmed summeerituna tunnuste kaupa ---")
    print(df.isna().sum())
    print("--- Andmestiku info, tunnused, andmetüübid jm ---")
    print(df.info())
    return None

def showParameterPairs(df):
    print("--- Paarikaupa hajuvusdiagrammid ---")
    sns.set(style="whitegrid")
    sns.pairplot(
        df,
        vars=["Sünnikaal","Raseduskestus päevades","Ema vanus","Isa vanus","Sünnipikkus"],
        y_vars=["Sünnikaal"],
        diag_kind="hist",
        #kind="reg",
        height=3
        )
    plt.suptitle("Paarikaupa hajuvusdiagrammid (pairplot)", y=1.02)
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule
    return None

def showCorrMatrix(df):
    # korrelatasiooni maatriks
    print("--- Korrelatasiooni maatriks ---")
    numeric_df = df[["Sünnikaal","Raseduskestus päevades","Ema vanus","Isa vanus","Sünnipikkus"]] # valime tulbad,
    corr = numeric_df.corr() # arvutame korrelatsioonimaatriksi
    sns.heatmap(corr, annot=True, cmap="coolwarm") # hiitmap
    plt.title("Korrelatsioon numbriliste suuruste vahel")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule
    return None

def transformTheData(df):
    print("--- Teisendame ja täiendame andmestikku ---")
    # Teisendame kombineerime kaks eraldi tulpa kokku raseduskestuseks päevades
    df["Raseduskestus päevades"] = (df["Raseduskestus nädalad"] * 7) + df["Raseduskestus päevad"]
    # Vanemate vanusevahe
    df["Vanusevahe"] = df["Isa vanus"] - df["Ema vanus"]
    # Loomulik sünnitus, siin on meil võimalus käsitsi muuta vastavat mäppingut, kui peaks olema soov
    df["Loomulik sünnitus"] = df["Sünnitusviis"].map({
        "Loomulikul teel": 1,
        "Vaakumsünnitus": 0,
        "Tangsünnitus": 0,
        "Plaaniline keisrilõige": 0,
        "Erakorraline keisrilõige": 0,
        "Hädakeisrilõige": 0,
        "Keisrilõige pärast ebaõnnestunud vaakumsünnitust": 0
        }) # kodeerimine
    # Suitsetamine igas vormis
    df["Suitsetamine kokku"] = df["Suitsetamine"].map({
        "ei suitsetanud": 0,
        "lõpetas suitsetamise raseduse esimesel trimestril": 1,
        "suitsetas": 1,
        "andmed puuduvad": 0 # NB! Siin peab kaaluma mingitel juhtudel nende ridade väljaarvamise andmestikust
        }) # Seejärel kodeerimine
    df["Suitsetamine kokku"] = df["Suitsetamine kokku"].replace({0: "Mittesuitsetaja", 1:"Suitsetaja"}) # Asendame kategoorilised numbrilised väärtused tekstilisetga
    return df

def modelWorks():

    return None

def testLoadModel(model):
    print("--- Random Forest meetodiga ennustame sünnikaalu ja sünnipikkust ---")
    uued_andmed = pd.DataFrame({
        "Raseduskestus päevades": [259],
        "Ema vanus": [30],
        "Isa vanus": [32],
        "Ema perekonnaseis": ["abielus"],
        "Lapse sugu": ["tüdruk"],
        "Suitsetamine kokku": [0] # täpsustada
        })
    prognoos = model.predict(uued_andmed)
    
    print("Sünnikaal (prognoos):", prognoos[0][0])
    print("Sünnipikkus (prognoos):", prognoos[0][1])
    return None

def predPregCurve(model):
    print("--- Random Forest meetodiga ennustame sünnikaalu ja sünnipikkust ---")
    baas = 175 # see on nii 25 rasedusnädal, sealt alustame sünnikaalu prognoosimist
    tulemused = []
    for number in range(25):
        kestus = baas + (5 * number)
        uued_andmed = pd.DataFrame({
            "Raseduskestus päevades": [kestus], # arvutamine iga 5 päeva järel
            "Ema vanus": [30],
            "Isa vanus": [32],
            "Ema perekonnaseis": ["abielus"],
            "Lapse sugu": ["tüdruk"],
            "Suitsetamine kokku": ["Mittesuitsetaja"] # täpsustada
            })
        prognoos = model.predict(uued_andmed)
        #print("Raseduskestus: ", baas + (5 * number))
        print("Sünnikaal (prognoos):", round(prognoos[0][0], 2))
        print("Sünnipikkus (prognoos):", round(prognoos[0][1], 2))
        tulemused.append({
            "Raseduskestus päevades": kestus,
            "Sünnikaal": round(prognoos[0][0], 2),
            "Sünnipikkus": round(prognoos[0][1], 2)
            })

    # Dataframe tegemine
    df = pd.DataFrame(tulemused)
    #print(df.head())
    # Graafiku joonistamine
    plt.plot(df["Raseduskestus päevades"], df["Sünnikaal"], c="green")
    plt.xlabel("Raseduskestus päevades")
    plt.ylabel("Sünnikaal")
    plt.title("Raseduskestus vs sünnikaal")
    plt.show()
    #print(df.head())
    return df

def predPregCurve_gb(model):
    print("--- Gradient Boosting meetodiga ennustame sünnikaalu ---")
    baas = 175 # see on nii 25 rasedusnädal
    tulemused = []
    for number in range(25):
        kestus = baas + (5 * number)
        uued_andmed = pd.DataFrame({
            "Raseduskestus päevades": [kestus], # arvutamine iga 5 päeva järel
            "Ema vanus": [30],
            "Isa vanus": [32],
            "Ema perekonnaseis": ["abielus"],
            "Lapse sugu": ["tüdruk"],
            "Suitsetamine kokku": ["Mittesuitsetaja"] # täpsustada
            })
        prognoos = model.predict(uued_andmed)
        #print("Raseduskestus: ", baas + (5 * number))
        print("Sünnikaal (prognoos):", round(prognoos[0], 2))
        #print("Sünnipikkus (prognoos):", round(prognoos[0][1], 2))
        tulemused.append({
            "Raseduskestus päevades": kestus,
            "Sünnikaal": round(prognoos[0], 2),
            #"Sünnipikkus": round(prognoos[0][1], 2)
            })

    # Dataframe tegemine
    df = pd.DataFrame(tulemused)
    #print(df.head())
    # Graafiku joonistamine
    plt.plot(df["Raseduskestus päevades"], df["Sünnikaal"], c="green")
    plt.xlabel("Raseduskestus päevades")
    plt.ylabel("Sünnikaal")
    plt.title("Raseduskestus vs sünnikaal")
    plt.show()
    #print(df.head())
    return df

def compTrends(df, df_predicted):
    print("--- Võrdleme treenitud mudeli poolt ennustatut reaalse andmestikuga (lisatud trendijoon) ---")
    plt.figure(figsize=(8,5))
    # Taust: algne dataset (punktid + trendijoon)
    sns.regplot(
        data=df,
        x="Raseduskestus päevades",
        y="Sünnikaal",
        scatter_kws={"alpha": 0.4},
        line_kws={"color": "red", "label": "Trend (lineaarne)"}
        )
    # Treenitud mudeli ennustuste joone peale joonistamine
    sns.lineplot(
        data=df_predicted,
        x="Raseduskestus päevades",
        y="Sünnikaal",
        color="blue",
        label="Mudeli prognoos"
        )
    plt.xlabel("Raseduskestus (päevades)")
    plt.ylabel("Sünnikaal")
    plt.title("Võrdlus: mudel vs pärisandmed")
    plt.legend()
    plt.show()

    return None



def main():
    print("--- Main alustab ---")
    # Loeme failist
    data = readTheFile(path)
    # Esmane andmete töötlus ja puhastus
    df = cleanUpRawData(data)
    # Teisene andmete töötlus ja täiendamine 
    df = transformTheData(df)
    # Võrdleme tunnuspaaride kaupa andmeid
    showParameterPairs(df)
    # Korrelatsioonimaatriks
    showCorrMatrix(df)
    # Andmete analüüs
    analysisTheData(df) 
    #model, preprocessor, y_mean, y_std = neuralNetworkModel_pt(df)
    #testTorchPred(model, preprocessor, y_mean, y_std)
    
    # Mudeli loomine ja käivitamine, RF
    pipeline, X_train, y_train, X_test, y_test, X = randomForestModel(df)
    # Parameetrite tuunimine ja parima parameetritega mudeli leidmine
    #best_model = tuneTheModel(pipeline, X_train, y_train, X_test, y_test, X) # kommenteerime hetkel välja

    #print(df.info())
    
    # print()
    
    # Salvestatud mudeli testimine
    loaded_model = loadTheModel(save_model_name_rf)
    # Prognoosimine laetud mudeli abil
    testLoadModel(loaded_model)
    # test2
    df_predicted = predPregCurve(loaded_model)
    compTrends(df, df_predicted)

    pipeline_gb, X_train_gb, y_train_gb, X_test_gb, y_test_gb, X_gb = gradientBoostingModel(df)
    #testLoadModel(pipeline_gb)
    df_predicted_gb = predPregCurve_gb(pipeline_gb)
    compTrends(df, df_predicted_gb)
    


if __name__ == '__main__':
    main()

