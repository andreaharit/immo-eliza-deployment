import uvicorn
from typing import Annotated, Literal
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from predict import Predict
import joblib
import json


app = FastAPI()

# Initializates Basemodel with type checking
class House (BaseModel):    

    district: Annotated[str, Path(title="Name of the District where the house is.")]
    state_construction: Annotated[str, Path(title="State of the construction.")]
    living_area: Annotated[int, Path(title="Size living room sqm", gt = 17)]
    bedrooms: Annotated[int, Path(title="Number of bedrooms.", gt = 0)]
    bathrooms: Annotated[int, Path(title="Number of bathrooms.", gt = 0)]
    facades: Annotated[int, Path(title="Number of exposed façades.", gt = 0, lt = 5)]
    has_garden: Annotated[bool, Path(title="Has a garden: use true or false.")]
    has_equipped_kitchen: Annotated[bool, Path(title="Has equipped kitchen: use true or false.")]
    has_terrace: Annotated[bool, Path(title="Has at least one terrace: use true or false.")]
    has_attic: Annotated[bool, Path(title="Has an attic: use true or false.")]
    has_basement: Annotated[bool, Path(title="Has a basement: use true or false.")]
    epc: Annotated[str, Path(title="EPC score A++ to G.")]
    area_total: Annotated[int, Path(title="Size of the house sqm, must be bigger than 18sqm", gt = 17)]

    class Config:
        json_schema_extra = {
            'example': {
                'district': 'Brugge',
                'state_construction': 'GOOD',
                "living_area": 100,
                'bedrooms': 3,
                'bathrooms': 2,
                'facades': 1,
                "has_garden": False,
                "has_equipped_kitchen": True,
                'has_terrace': True,
                "has_attic": False,
                "has_basement": False,
                "epc": "A",
                "area_total": 116
            }
        }


@app.post("/predict")
def price_prediction(data: House):

    group_epc = {"A++": 9 , "A+": 8, "A": 7, "B":6, "C":5, "D":4, "E":3, "F":2, "G": 1}
    epcs = ["A++", "A+", "A", "B", "C", "D", "E", "F", "G"]   

    districts =  ["Aalst", "Antwerp", "Arlon", "Ath", "Bastogne", "Brugge", "Brussels", "Charleroi", "Dendermonde", 
"Diksmuide", "Dinant", "Eeklo", "Gent", "Halle-Vilvoorde", "Hasselt", "Huy", "Ieper", "Kortrijk", "Leuven", "Liège", 
"Maaseik", "Marche-en-Famenne", "Mechelen", "Mons", "Mouscron", "Namur", "Neufchâteau", "Nivelles", "Oostend", "Oudenaarde", 
"Philippeville", "Roeselare", "Sint-Niklaas", "Soignies", "Thuin", "Tielt", "Tongeren", "Tournai", "Turnhout", "Verviers", 
"Veurne", "Virton", "Waremme"]

    states = ["GOOD", "JUST_RENOVATED", "AS_NEW", "TO_RENOVATE", "AS_NEW", "TO_RESTORE", "TO_BE_DONE_UP"]


    data = data.dict()

    # Validations:
    if data["district"] not in districts:
        error_message = "Invalid District. Please use one of those:  " + str(districts)
        raise HTTPException(status_code=422, detail=error_message)
    if data["state_construction"] not in states:
        error_message = "Invalid state of construction. Please use one of those:  " + str(states)
        raise HTTPException(status_code=422, detail=error_message)
    if data["epc"] not in list(group_epc.keys()):
        error_message = "Invalid EPC. Please use one of those:  " + str(list(group_epc.keys()))
        raise HTTPException(status_code=422, detail=error_message)

    district = data["district"]
    state_construction = data["state_construction"]
    living_area = data["living_area"]
    bedrooms = data["bedrooms"]
    bathrooms = data["bathrooms"]
    facades = data["facades"]
    has_garden = data["has_garden"]
    has_equipped_kitchen = data["has_equipped_kitchen"]
    has_terrace = data["has_terrace"]
    has_attic = data["has_attic"]
    has_basement = data["has_basement"]
    epc_string = data["epc"]
    epc = group_epc[epc_string]
    area_total = data["area_total"]


    test = {
            "district": district,
            "state_construction": state_construction,
            "living_area": living_area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "facades": facades,
            "has_garden": has_garden,
            "kitchen": has_equipped_kitchen,
            "has_terrace": has_terrace,
            "has_attic": has_attic,
            "has_basement": has_basement,
            "epc": epc,
            "area_total": area_total
            }

    predict =  Predict(test)

    return {'prediction': round(predict.result,0)}


if __name__ == '__main__':
    uvicorn.run("api:app",reload=True)

