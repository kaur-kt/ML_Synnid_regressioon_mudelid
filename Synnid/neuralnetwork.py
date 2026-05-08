''' Neural Network masinõppe meetod '''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

#import tensorflow as tf
#from tensorflow.keras import layers, models

import torch
import torch.nn as nn
import torch.optim as optim

'''
# Kasutades Tensorflow'd
def neuralNetworkModel(df):
	# Siin proovime Neural Network/närvivõrku ja pipeline'i

    # Tunnused ja märgendid
    X = df.drop(columns=["Sünnikaal"]) # tunnused
    y = df["Sünnikaal"] # märgend

    # Tunnused, eristame numbrilised ja kategoorilised tunnused
    numerical_features = ["Raseduskestus päevades","Ema vanus","Isa vanus"]
    cat_features = ["Ema perekonnaseis","Suitsetamine kokku","Lapse sugu"]

    # Eeltöötlus
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numerical_features), # rkendame Standardscalerit, võib proovida ka MinMaxScaler()
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features) # OneHotEncoder teisendab kategoorilised tunnused arvudeks/vektoriks
    ])
    
    # 
    X_processed = preprocessor.fit_transform(X)

    # Treening- ja testandmete ning vastavate märgendite moodustamine 
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    # Mudeli kirjeldamine
    model = models.Sequential([
        layers.Dense(64, activation="relu", input_shape(X_train.shape[1],)),
        layers.Dropout(0.2),
        layers.Dense(32, activation="relu"),
        layers.Dense(1) # väljundkiht. NB! tegu pole klassifikaatoriga, vaid regressiooniga 
        ])

    # Mudeli koostamine
    model.compile(
        optimizer = "adam",
        loss = "mse",
        metrics = ["mae"]
        )

    # Treenimine
    history = model.fit(
        X_train, y_train,
        validation_split=0.2, # 20% valideerimisandmeteks
        epochs=10,
        batch_size=32,
        verbose=2
        )

    # Hindamine
    loss, mae = model.evaluate(X_test, y_test)
    print("Test MAE: ", mae)

	return history
'''
# Kasutades PyTorch'i
def neuralNetworkModel_pt(df):

    # Tunnused ja märgendid
    X = df.drop(columns=["Sünnikaal"]) # tunnused
    y = df["Sünnikaal"] # märgend

    # Tunnused, eristame numbrilised ja kategoorilised tunnused
    numerical_features = ["Raseduskestus päevades","Ema vanus","Isa vanus","Sünnipikkus"]
    cat_features = ["Ema perekonnaseis","Suitsetamine kokku","Lapse sugu"]

    # Eeltöötlus
    preprocessor = ColumnTransformer([
        ("num", MinMaxScaler(), numerical_features), # rkendame Standardscalerit, võib proovida ka StandardScaler()/MinMaxScaler()
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features) # OneHotEncoder teisendab kategoorilised tunnused arvudeks/vektoriks
    ])
    
    # 
    X_processed = preprocessor.fit_transform(X)
    # kontroll
    #print(X_processed[:5])

    # Treening- ja testandmete ning vastavate märgendite moodustamine 
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    # Normaliseerimie märgendid
    y_mean = y_train.mean()
    y_std = y_train.std()
    y_train = (y_train - y_mean) / y_std
    y_test = (y_test - y_mean) / y_std

    # Baasjoone kontrollimne
    baseline_pred = np.mean(y_train)
    mae_baseline = np.mean(np.abs(y_test - baseline_pred))
    print("Baseline MAE:", mae_baseline)

    # Teisendame numpy massivid torchi tensoriteks
    X_train = torch.tensor(X_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1) # Siin vaja väike teisendus, kuna Torch ei suuda pandas.Series objekti üheselt tõlgendada

    # Mudeli kirjeldamine klassina
    class SynnikaalModel(nn.Module):
        def __init__(self, input_dim):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, 64),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(64, 1)
                )

        def forward(self, x):
            return self.net(x)
    
    model = SynnikaalModel(X_train.shape[1])

    # Treeningu ja valideerimisvigade salvestamine
    train_losses = []
    val_losses = []

    # Vea ja optimeerija(Adam)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    # epohhid
    epochs = 200
    # Treenimine
    for epoch in range(epochs):
        model.train()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_losses.append(loss.item())
    
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

    # Tulemuse hindamine
    model.eval()
    with torch.no_grad():
        predictions = model(X_test)
        val_loss = criterion(predictions, y_test)
        val_losses.append(val_loss.item())
        mae = torch.mean(torch.abs(predictions - y_test))
        print("MAE:", mae.item())

    
    print(f"Epoch {epoch+1}: train_loss={loss.item():.2f}, val_loss={val_loss.item():.2f}")

    plt.plot(train_losses, label="Train loss")
    plt.plot(val_losses, label="Validation loss")
    plt.legend()
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training history")
    plt.show()

    # Salvestame mudlei
    torch.save(model.state_dict(), "model.pth")

    return model, preprocessor, y_mean, y_std

def pred_synnikaal(model, preprocessor, input_dict, y_mean=None, y_std=None):
    """
    Ennustab sünnikaalu ühe või mitme näite põhjal.

    input_dict peab sisaldama:
    - Raseduskestus päevades
    - Ema vanus
    - Isa vanus
    - Sünnipikkus
    - Ema perekonnaseis
    - Lapse sugu
    - Ema suitsetamine
    """

    # 1. Dict → DataFrame
    df = pd.DataFrame([input_dict])
    print(df.dtypes)

    # 2. Preprocessing (sama mis treeningus)
    X = preprocessor.transform(df)

    # sparse → dense kui vaja
    if hasattr(X, "toarray"):
        X = X.toarray()

    # 3. Tensoriks
    X_tensor = torch.tensor(X, dtype=torch.float32)

    # 4. Ennustus
    model.eval()
    with torch.no_grad():
        pred = model(X_tensor)

    # 5. Tagasi skaalasse, kuna normaliseerisid märgendi
    pred = pred.item()

    if y_mean is not None and y_std is not None:
        pred = pred * y_std + y_mean

    return pred

def testTorchPred(model, preprocessor, y_mean, y_std):
    input_data = {
    "Raseduskestus päevades": 280,
    "Ema vanus": 30,
    "Isa vanus": 32,
    "Sünnipikkus": 52,
    "Ema perekonnaseis": "vabaabielus",
    "Suitsetamine kokku": 0,
    "Lapse sugu": "poiss",
    }
    prediction = pred_synnikaal(
        model=model,
        preprocessor=preprocessor,
        input_dict=input_data,
        y_mean=y_mean,
        y_std=y_std
        )
    
    print("Ennustatud sünnikaal PT mudeli poolt:", prediction)
    return None


