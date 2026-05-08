''' Random Forest mudeli tuunimine '''


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
from fileops import saveTheModel

save_model_name_rf = "synnimudel_rf.pkl"

def tuneTheModel(pipeline, X_train, y_train, X_test, y_test, X):
    # Tuunime parameetreid ja otsime parimat mudelit
    param_grid = {
     "model__estimator__n_estimators": [100, 200],
     "model__estimator__max_depth": [None, 10, 20],
     "model__estimator__min_samples_split": [2, 5],
     "model__estimator__min_samples_leaf": [1, 2],
     "model__estimator__max_features": [ "sqrt",  "log2"]
     }
    
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring= "neg_root_mean_squared_error",
        n_jobs=-1,
        verbose=2
        )

    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print("Parimad parameetrid:")
    print(grid_search.best_params_)

    y_pred_best = best_model.predict(X_test)

    # Hindame parimat mudelit
    #rmse_kaal = mean_squared_error(y_test["Sünnikaal"], y_pred[:, 0], squared=False) # Uus versioon funktsioonist, kuid mul ei tööta
    mse_kaal_best = mean_squared_error(y_test["Sünnikaal"], y_pred_best[:, 0])
    rmse_kaal_best = np.sqrt(mse_kaal_best)

    mse_pikkus_best = mean_squared_error(y_test["Sünnipikkus"], y_pred_best[:, 1])
    rmse_pikkus_best = np.sqrt(mse_pikkus_best)
    #rmse_pikkus = mean_squared_error(y_test["Sünnipikkus"], y_pred[:, 1], squared=False) # Uus versioon funktsioonist, kuid mul ei tööta

    #r2_kaal = r2_score(y_test["Sünnikaal"], y_pred_best[:, 0])
    #r2_pikkus = r2_score(y_test["Sünnipikkus"], y_pred_best[:, 1])

        # Mudeli kvaliteedinäitajate väljaprintimine
    print("Tuunitud Random Forest:")
    print(f"Kaal (parim) RMSE: {rmse_kaal_best:.2f}")
    print(f"Pikkus (parim) RMSE:: {rmse_pikkus_best:.2f}")
    #print(f"Kaal R2: {r2_kaal:.3f}")
    #print(f"Pikkus R2: {r2_pikkus:.3f}")

    #print("Kaal (parim) RMSE:", rmse_kaal_best)
    #print("Pikkus (parim) RMSE:", rmse_pikkus_best)
    #print("Kaal R2:", r2_kaal)
    #print("Pikkus R2:", r2_kaal)

    # Uurimine , mis mõjutab sünnikaalu
    rf_model_kaal = best_model.named_steps["model"].estimators_[0]
    importances = rf_model_kaal.feature_importances_

    # Peale OneHotEncoding tunnuste saamine
    feature_names = best_model.named_steps["preprocessing"].get_feature_names_out()

    # Tabeli koostamine
    feat_imp = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
        }).sort_values(by="importance", ascending=False)

    print(feat_imp.head(10))

    # Visualiseerimine
    feat_imp.head(10).plot(
        kind="barh",
        x="feature",
        y="importance",
        legend=False
        )

    plt.gca().invert_yaxis()
    plt.title("Top tunnused sünnikaalu prognoosimisel")
    plt.show()

    # Salvestame mudeli tulevastele põlvedele :)
    saveTheModel(best_model, save_model_name_rf, X)
    
    return best_model

