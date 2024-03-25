description = """
## Predict

You will receive a integer number that is the price predicted for a house in euros.

You can send a json file, or input it directly via /docs with the following keys:


- **'area_total'**: integer bigger than 18. In sqm. Total area of the house.
- **'living_area'**: integer bigger than 18. In sqm. Living area of the house.
- **'bedrooms'**: integer, at least 1. Number of bedrooms available.
- **'bathrooms'**: integer, at least 1. Number of bathrooms available.
- **'facades'**: integer, from 1 to 4. Exposed façades of the house.
- **'has_garden'**: boolean. 1 or true if there is a garden. 0 or false if not.
- **'has_equipped_kitchen'**: boolean. 1 or true if the kitchen has some level of equippement. 0 or false if it's empty.
- **'has_terrace'**: boolean. 1 or true if there is at least one terrace. 0 or false if not.
- **'has_attic'**: boolean. 1 or true if there is an attic. 0 or false if not.
- **'has_basement'**: boolean. 1 or true if there is an basement. 0 or false if not.
- **'epc'**: string. Regarding the energy performance certificate of the house. 

    Must be one of the following values (case sensitive):
    
    ["A++", "A+", "A", "B", "C", "D", "E", "F", "G"]

- **'state_construction'**: string. Regarding the state of the construction of the house.

    Must be one of the following values (case sensitive): 

    ["GOOD", "JUST_RENOVATED", "AS_NEW", "TO_RENOVATE", "AS_NEW", "TO_RESTORE", "TO_BE_DONE_UP"]

- **'district'**: string. District where the house is located.

    Must be one of the following values (case sensitive):
    
    ["Aalst", "Antwerp", "Arlon", "Ath", "Bastogne", "Brugge", "Brussels", "Charleroi", "Dendermonde", "Diksmuide", "Dinant", "Eeklo", "Gent", "Halle-Vilvoorde", "Hasselt", "Huy", "Ieper", "Kortrijk", "Leuven", "Liège", "Maaseik", "Marche-en-Famenne", "Mechelen", "Mons", "Mouscron", "Namur", "Neufchâteau", "Nivelles", "Oostend", "Oudenaarde", "Philippeville", "Roeselare", "Sint-Niklaas", "Soignies", "Thuin", "Tielt", "Tongeren", "Tournai", "Turnhout", "Verviers", "Veurne", "Virton", "Waremme"]
    
### Errors

- 422 Error: Unprocessable Entity: Invalid or missing input that can't be computed by the Machine Learning model. Please refer to the documentation above.

"""