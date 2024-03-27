import pandas as pd
import streamlit as st
from predict import Predict
import plotly.express as px
from plots.plots import Plots



def main():


    states = {
        "As new": "AS_NEW",
        "Good": "GOOD",
        "Just renovated": "JUST_RENOVATED",
        "To be done up": "TO_BE_DONE_UP",
        "To renovate": "TO_RENOVATE",
        "To restore": "TO_RESTORE"
    }

    districts =  ["Aalst", "Antwerp", "Arlon", "Ath", "Bastogne", "Brugge", "Brussels", "Charleroi", "Dendermonde", 
"Diksmuide", "Dinant", "Eeklo", "Gent", "Halle-Vilvoorde", "Hasselt", "Huy", "Ieper", "Kortrijk", "Leuven", "Liège", 
"Maaseik", "Marche-en-Famenne", "Mechelen", "Mons", "Mouscron", "Namur", "Neufchâteau", "Nivelles", "Oostend", "Oudenaarde", 
"Philippeville", "Roeselare", "Sint-Niklaas", "Soignies", "Thuin", "Tielt", "Tongeren", "Tournai", "Turnhout", "Verviers", 
"Veurne", "Virton", "Waremme"]

    epcs = {"A++": 9 , "A+": 8, "A": 7, "B":6, "C":5, "D":4, "E":3, "F":2, "G": 1}

    html = """
    <div style = "background-color: lightblue ; padding: 16px>
    <h2 style = "color: black; text-align: center;"> House Price Prediction</h2>
    </div>
    """

    st.markdown(html, unsafe_allow_html = True)

    st.write ("")

    district = st.selectbox(label = "In which district is the house located?", options = districts)
    area_total = st.number_input(label = "What is the total area of the house (m²)?", min_value = 50.0, max_value= 1500.0, step = 0.5 )
    living_area = st.number_input(label = "What is the total living area (m²)?", min_value = 50.0, max_value= 350.0, step = 0.5 )

    select_state = st.selectbox (label = "What is the state of the house?", options= list(states.keys()), index = 1)
    select_epc = st.select_slider(label ="What is the house's EPC?", options = (list(epcs.keys())), value = "A")
    bedrooms = st.slider(label = "What is the number of bedrooms?", min_value=1, max_value= 15)
    bathrooms = st.slider(label = "What is the number of bathrooms?", min_value=1, max_value= 10)
    facades = st.slider(label = "How many exposed façades?", min_value=1, max_value=4)

    st.write('Does the house have a garden?')
    has_garden = st.toggle(label = "With garden" , value=False, label_visibility="collapsed")
    if has_garden:
        st.write('It has a garden.')


    st.write('Does the house have an equipped kitchen?')
    has_equipped_kitchen = st.toggle(label = "With equipepd kitchen" , value=False, label_visibility="collapsed")
    if has_equipped_kitchen:
        st.write('It has an equipped kitchen.')

    st.write('Does the house have at least one terrace?')
    has_terrace = st.toggle(label = "With terrace" , value=False, label_visibility="collapsed")
    if has_terrace:
        st.write('It has at least one terrace.')

    st.write('Does the house have an attic?')   
    has_attic = st.toggle(label = "With attic" , value=False, label_visibility="collapsed")
    if has_attic:
        st.write('It has an attic.')

    st.write('Does the house have a basement?')   
    has_basement = st.toggle(label = "With basement" , value=False, label_visibility="collapsed")
    if has_basement:
        st.write('It has a basement.')

    data = {
            "district": district,
            "state_construction": states[select_state],
            "living_area": living_area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "facades": facades,
            "has_garden": has_garden,
            "kitchen": has_equipped_kitchen,
            "has_terrace": has_terrace,
            "has_attic": has_attic,
            "has_basement": has_basement,
            "epc": epcs[select_epc],
            "area_total": area_total
            }
        
    if st.button(label = "Predict Price"):
        predict =  Predict(data)
        st.success(f"The predicted price for your house is €{int(predict.result)}.")

        st.write (f"Your house compared to others in {district}:")

        data_plot = "./plots/cleaned_houses.csv"
        plots = Plots(file = data_plot, district = district )
        price_plot = plots.price_sqm(prediction = predict.result, living_area = living_area)
        
        st.plotly_chart(price_plot , use_container_width=True, sharing="streamlit", theme="streamlit")      

        

        # Bedroom pie
        pie_bedroom = plots.pie_chart(feature="bedrooms", feature_name="Bedrooms", home_value= bedrooms)
        st.plotly_chart(pie_bedroom , use_container_width=True, sharing="streamlit", theme="streamlit")

        # Bathroom pie
        pie_bathroom = plots.pie_chart(feature="bathrooms", feature_name="Bathrooms", home_value= bathrooms)
        st.plotly_chart(pie_bathroom , use_container_width=True, sharing="streamlit", theme="streamlit")
    
 


if __name__ == "__main__":
    main()