import pandas as pd
import json
import joblib
import warnings





class Predict:
    def __init__(self, data):
        #Supress warnin "has feature names, but StandardScaler was fitted without feature names"
        #Since it doesnt affect the calculation
        
        warnings.filterwarnings("ignore")

        categorical = ["district","state_construction"]

        X = pd.DataFrame(data, index=[0])
  


        # Encodes new data with saved encoding from train set
        encoder = '../pickle_files/encoding.pkl'
        loaded_enc = joblib.load(encoder)

        enctransform = loaded_enc.transform(X[categorical])
        X = pd.concat([X, enctransform], axis = 1).drop(categorical, axis = 1)



        # Scales new data with saved scaler from train set
        scaler = '../pickle_files/scaler.pkl'
        loaded_scaler = joblib.load(scaler)
        X = loaded_scaler.transform(X)


        # Loads and use model to predict new price
        model = '../pickle_files/forest.pkl'
        loaded_model = joblib.load(model)
     
    
        self.result = loaded_model.predict(X)[0]
        

