# Belgian house market, ML deployment 👩‍💻

## Project context 📝

This is the fourth part of a project that aims to create a machine learning model to predict the selling price of houses in Belgium.

Previous stages were:

- Scrapping the data from the real state website [Immoweb](https://www.immoweb.be/). See [repository](https://github.com/niels-demeyer/immo-eliza-scraping-scrapegoat).
- Analysing the data for business insights. See [repository](https://github.com/Yanina-Andriienko/immo-eliza-scrapeGOATS-analysis).
- Building and evaluating a ML model via regression. See [repository](https://github.com/andreaharit/05-immoeliza-ml-Andrea).

And now we are deploying those models in two ways: via FastAPI and Streamlit.

## Table of Contents

- [Usage: FastAPI](#fastapi)
- [Usage: Streamlit](#streamlit)
- [Model](#model)
- [File structure](#structure)
- [Timeline](#timeline)

## Usage 🛠

<a id="fastapi"></a>
### FastAPI 🚀

This is the [link](https://immo-eliza-deployment-o9qq.onrender.com/docs) for the FastAPI docs.

For prediction, please send a post request with a json to the following [website](https://immo-eliza-deployment-o9qq.onrender.com/predict) with the following format:

    data = {
      "area_total": int,
      "bathrooms": int,
      "bedrooms": int,
      "district": str,
      "epc": str,
      "facades": str,
      "has_attic": bool,
      "has_basement": bool,
      "has_equipped_kitchen": bool,
      "has_garden": bool,
      "has_terrace": bool,
      "living_area": bool,
      "state_construction": str
    }

The API will return a json with the predicted price in euros:

    {
      "prediction": int
    }
    
The [API docs](https://immo-eliza-deployment-o9qq.onrender.com/docs) contain further explanations and constraints about the parameters.

<a id="streamlit"></a> 

### Streamlit 🖱️
This is the [link](https://immo-eliza-deployment-1-rhgt.onrender.com/) for the webapp with an user interface for inputting data.
The app calculates the price based on the user input and displays some plots comparing the house with other metrics in the same districts.


<div style="max-height: 300px;">
    <img src="img\streamlit_example.jpg" alt="Streamlit app" style="width: auto; height: 300px;">
</div>

<a id="model"></a>
## Model 🤖

The chosen model for deployment is simplified version of the models built in the previous stage since we are aiming for a better user experience. 
The final model metrics in the test set are:

|   R2 |	RMSE (€) | MAE (€)|
| ----- | ------- | ---------- |
| 0.68 | 81274.5 | 61009.4 |

<a id="structure"></a>
## File structure 🗃️

    ├── img
    ├── FastAPI
    │   ├── picke_files
    │   │    ├── encoding.pkl
    │   │    ├── forest.pkl
    │   │    └── scaler.pkl
    │   ├── Dockerfile
    │   ├── description.py
    │   ├── predict.py
    │   ├── app.py
    │   └── requirements.txt
    ├── streamlit
    │   ├── plots
    │   │    ├── cleaned_houses.csv
    │   │    └── plots.py
    │   ├── house_streamlit.py
    │   └── requirements.txt
    └── README.md

#### FastAPI:

- The picke file folders contains the files for the preprocessing and the model `forest.pkl`.
- `description.py` is the README loaded into FastAPI docs.
- `predict.py` runs the preprocessing and prediction pipeline (making use of the picke files) for the json sent to the API.
- `app.py` contains the code to build the API. 


#### Streamlit:

- The plots file contains:

    - `cleaned_houses.csv`, the scrapped info from houses collected on the previous steps of this project. It is used to make the plots into the streamlit app to compare the results of a predicted house with others in the same district. 

    - `plots.py` which contain the code to build the histogram and piechart.
- `house_streamlit.py` is the code to build the Streamlit app itself.


The `requirements.txt` between the API and Streamlit differ in scope so they were separated.
️
<a id="timeline"></a>

## Timeline 📅

This project took 5 days to be completed.
