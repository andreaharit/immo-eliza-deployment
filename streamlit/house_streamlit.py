import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import plotly.express as px
from plots.plots import Plots
import requests



def main():



    # Initializes data for dropdown menus

    #State of construction, dict makes options prettier
    states = {
        "As new": "AS_NEW",
        "Good": "GOOD",
        "Just renovated": "JUST_RENOVATED",
        "To be done up": "TO_BE_DONE_UP",
        "To renovate": "TO_RENOVATE",
        "To restore": "TO_RESTORE"
    }
    # Belgian provinces
    districts =  ["Aalst", "Antwerp", "Arlon", "Ath", "Bastogne", "Brugge", "Brussels", "Charleroi", "Dendermonde", 
"Diksmuide", "Dinant", "Eeklo", "Gent", "Halle-Vilvoorde", "Hasselt", "Huy", "Ieper", "Kortrijk", "Leuven", "Liège", 
"Maaseik", "Marche-en-Famenne", "Mechelen", "Mons", "Mouscron", "Namur", "Neufchâteau", "Nivelles", "Oostend", "Oudenaarde", 
"Philippeville", "Roeselare", "Sint-Niklaas", "Soignies", "Thuin", "Tielt", "Tongeren", "Tournai", "Turnhout", "Verviers", 
"Veurne", "Virton", "Waremme"]

    epcs = ["A++", "A+", "A", "B", "C", "D", "E", "F", "G"]

    # Writes app header with html
    html = """
    <div style = "background-color: rgb(255, 75, 75); padding: 10px; box-sizing: border-box;
    border-radius: 15px;">
    <h2 style = "color: white; text-align: center;"> House Price Prediction 🏠</h2>
    </div>  
    """
    st.markdown(html, unsafe_allow_html = True)
    st.write ("")

    # Begins selection tools
    district = st.selectbox(label = "In which district is the house located?", options = districts)
    area_total = st.number_input(label = "What is the land area of the house (m²)?", value = 100, min_value = 50, max_value= 1500, step = 1)
    living_area = st.number_input(label = "What is the total living area (m²)?", value = 100, min_value = 50, max_value= 350, step = 1 )
    select_state = st.selectbox (label = "What is the state of the house?", options= list(states.keys()), index = 1)
    select_epc = st.select_slider(label ="What is the house's EPC?", options = epcs, value = "A")
    bedrooms = st.slider(label = "What is the number of bedrooms?", min_value=1, max_value= 15)
    bathrooms = st.slider(label = "What is the number of bathrooms?", min_value=1, max_value= 10)
    facades = st.slider(label = "How many exposed façades?", min_value=1, max_value=4)

    # For boolean variables
    # Divides them into columns for better redability 
    col_1, col_2 = st.columns(2)

    with col_1:
        # Makes a border into the column
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,):        

            # Starts the toggle buttoms with text confirmation of choice
            st.write('Does the house have a garden?')
            has_garden = st.toggle(label = "With garden" , value=False, label_visibility="collapsed")
            if has_garden:
                st.write('It has a garden.')

            
            st.write('Does the house have at least one terrace?')
            has_terrace = st.toggle(label = "With terrace" , value=False, label_visibility="collapsed")
            if has_terrace:
                st.write('It has at least one terrace.')

            st.write('Does the house have an attic?')   
            has_attic = st.toggle(label = "With attic" , value=False, label_visibility="collapsed")
            if has_attic:
                st.write('It has an attic.')

    # Second column of toggles 
    with col_2:
        # Makes border for the column
        with stylable_container(
        key="container_with_border_2",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,):

            # Start toggles
            st.write('Does the house have an equipped kitchen?')
            has_equipped_kitchen = st.toggle(label = "With equipepd kitchen" , value=False, label_visibility="collapsed")
            if has_equipped_kitchen:
                st.write('It has an equipped kitchen.')


            st.write('Does the house have a basement?')   
            has_basement = st.toggle(label = "With basement" , value=False, label_visibility="collapsed")
            if has_basement:
                st.write('It has a basement.')

    # Builts json data to sent to API
    data = {
            "district": district,
            "state_construction": states[select_state],
            "living_area": living_area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "facades": facades,
            "has_garden": has_garden,
            "has_equipped_kitchen": has_equipped_kitchen,
            "has_terrace": has_terrace,
            "has_attic": has_attic,
            "has_basement": has_basement,
            "epc": select_epc,
            "area_total": area_total
            }

    #Starts button to run prediction


    
    if st.button(label = "Predict Price", use_container_width = True, type="primary"):
        # Send post request to API with json
        URL = "https://immo-eliza-deployment-o9qq.onrender.com/predict"
        r = requests.post(URL, json = data)
        result = r.json()
        predict = result["prediction"]
        # Prints the result from the API    
        st.success(f"The predicted price for your house is €{int(predict)}.")


        # Starts interesting plots for the case
        st.divider()
        # Sub header to announce the plots with a custom HTML
        html = """
    <div style = "background-color: rgb(255, 75, 75); padding: 10px; box-sizing: border-box;
    border-radius: 15px;">
    <h4 style = "color: white; text-align: center;"> Your house compared to others in {district}</h4>
    </div>  
    """.format(district=district)
        st.markdown(html, unsafe_allow_html = True)
        st.write ("")

        # Prepare plots from class in plots.py        
        data_plot = "./plots/cleaned_houses.csv"
        plots = Plots(file = data_plot, district = district )

        # Puts plots into a container with tabs for better UX
        with st.container():
            tab1, tab2= st.tabs(["Price/living Area", "Rooms distribution"])
            with tab1:
                # Plot for price and living area via plotly
                price_plot = plots.price_sqm(prediction = predict, living_area = living_area)                
                st.plotly_chart(price_plot , use_container_width=True, sharing="streamlit", theme="streamlit") 
            with tab2:
                # Plot two pie charts one in each column  
                col1, col2 = st.columns(2)

                with col1: 
                    # Bedroom piechart
                    pie_bedroom = plots.pie_chart(feature="bedrooms", feature_name="Bedrooms", home_value= bedrooms)
                    st.plotly_chart(pie_bedroom , use_container_width=True, sharing="streamlit", theme="streamlit")
                with col2:
                    # Bathroom piechart
                    pie_bathroom = plots.pie_chart(feature="bathrooms", feature_name="Bathrooms", home_value= bathrooms)
                    st.plotly_chart(pie_bathroom , use_container_width=True, sharing="streamlit", theme="streamlit")
        
    


if __name__ == "__main__":
    main()