import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Plots:
    """
    Makes plots based on predicted value of a house and its properties.
    Arguments:
    file (str): source file with dataframe of houses to build plots.
    district (str): district of the house whose value was predicted.
    """
    def __init__(self, file: str, district: str) -> None: 
        self.district = district             
        # Reads CSV with houses
        dataframe = pd.read_csv(file)
        # Create column of price/m2
        dataframe ["price_sqm_total"] = dataframe ["price"]/dataframe ["living_area"]
        # Stores unmodified df
        self.df_complete = dataframe
        # Stores df for specific district
        mask = self.df_complete["district"] == district
        self.df_district = self.df_complete[mask]

    @staticmethod
    def thousants_point(x: int) -> str:  
        """Adds point as thousant separator to a number"""
        return str('{:,}'.format(round(x)).replace(',','.'))
    
    def price_sqm (self, prediction: float, living_area: float) -> None:
        """Builds a histogram via plotly of house count versus price per sqm.
        Adds also two vertical lines:
        One with the predicted price/ m2 of the house.
        Another for the average price/sqm of the province"""
        # Dataframe about the district and district to be used
        subset_district = self.df_district
        district = self.district
        # Calculates average price of the district per sqm
        average_price = round(subset_district["price_sqm_total"].mean())  


        # Calculares price/sqm and sets up a text for the vertical line
        price_sqm_predict = int(prediction/living_area)
        text_pred = "Your house €" + self.thousants_point(price_sqm_predict)  + "/m²"

        # Starts setting up the histogram                
        fig = px.histogram(subset_district,  x="price_sqm_total", opacity = 0.7,
        labels ={"price_sqm_total": f"Price per living area (€/m²) in {district}"}).update_layout(yaxis_title=f"Houses Count") 
       
        # Add vertical line and text with a arrow for the average price of the district
        # Done this way because otherwise the texts go over each other or the axis numbers etc
        fig.add_shape(type="line", x0=average_price, x1=average_price,  yref="paper", y0=0.1, y1=0.9, line=dict(color="Green",width=2))
        fig.add_annotation(x=average_price,  y= 0,
            text=f"Average: €{average_price}/m²",
            showarrow=True,
            arrowhead=1,
            xanchor="left", 
            ax = 20,
            ay = 20
            )
        # Add vertical line with text for the prediction
        fig.add_shape(type="line", x0=price_sqm_predict, x1=price_sqm_predict,  yref="paper", y0=0.1, y1=1, line=dict(color="firebrick",width=3))
        fig.add_annotation(x=price_sqm_predict,
            text=f"Your house: €{price_sqm_predict}/m²",            
            y=1.07,
            xref="x",
            yref="paper",
            showarrow=False
            ) 
        fig.update_layout(bargap=0.2)
        
        return fig

    def pie_chart (self, feature: str, feature_name: str, home_value: int) -> None:
        """
        Makes a piechart via plotly for counting an attribute.
        The piechart has a hole in the middle and the piece realted to the house is a bit pulled out for emphasis.
        """ 
        # Makes df with that stores the counting of each value of the feature
        df_room = self.df_district.groupby(feature, as_index=False).count()        
        # Selects only the columns pertinent to the Count
        df_room = df_room [[feature, "district"]]
        # Renames them for the plot
        df_room.rename(columns={"district": "Count", feature : feature_name}, inplace= True)        
        # Finds the row of the value that is the same as the house in the prediction
        # And creates a bool series to know which piece to pull from the pie
        pull = df_room[feature_name] == home_value
        pull = pull * 0.1 
        # Starts pieplot
        fig = go.Figure(
            data=[go.Pie(labels=df_room[feature_name], 
            texttemplate="<b>%{label}</b><br>""%{percent:.1%}",
            values=df_room.Count, 
            hole=.4, 
            pull=pull,
            showlegend=False, 
            marker=dict(colors=px.colors.qualitative.Plotly),
            hovertemplate="<b>Number</b>: %{label}<br>"
              "<b>Houses Count:</b>: %{value}<br>"
              "<b>Percentage</b>: %{percent:.1%}<br>"
                        )
                ]             
        )
        # Makes the label inside the hole of the pie
        fig.update_layout(           
            annotations=[                              
                dict(
                    text="<b>{name}</b></br></br>Yours has {home_value}.".format(name=feature_name.upper(), home_value = home_value),                 
                    showarrow=False                
                )
            ]
        )
        return fig


    def charc_plot(self):
        # Select df of the district
        df = self.df_district 
        # Select only the characteristics for the plot
        df_yn = df[['has_garden', 'kitchen', 'has_terrace','has_attic', 'has_basement']]
        df_yn.replace(to_replace=0, value= "No", inplace=True)
        df_yn.replace(to_replace=1, value= "Yes", inplace=True)

        # Manually build a df to have the % of yes and no for each characteristic
        # Probably there are much better ways, but this was faster to do
        cat= ['has_garden', 'kitchen', 'has_terrace','has_attic', 'has_basement']
        category= []
        label =[]
        number = []

        for column in cat:
            category.append(column)
            category.append(column)
            yes_count = df_yn[column].value_counts()['Yes']
            no_count = df_yn[column].value_counts()['No']
            label.append("yes")
            label.append("no")
            total = yes_count + no_count
            number.append(round(yes_count *100/total, 2))
            number.append(round(no_count *100/total, 2))

        data = { "Characteristic": category, "Has" : label, "Percentage" : number}


        dataf = pd.DataFrame(data)
        # Rename the labels, because renaming in the bar plot wasnt working for mysterious reasons
        dataf.replace(to_replace="kitchen", value= "Equip. Kitchen", inplace=True)
        dataf.replace(to_replace="has_garden", value= "Garden", inplace=True)
        dataf.replace(to_replace="has_terrace", value= "Terrace", inplace=True)
        dataf.replace(to_replace="has_attic", value= "Attic", inplace=True)
        dataf.replace(to_replace="has_basement", value= "Basement", inplace=True)
        
        # Make the bar plot
        fig = px.bar(dataf, x= "Characteristic", y="Percentage", hover_data={"Percentage": True, "Has": False, "Characteristic": False },  color='Has', text = "Has" )
        fig.update_layout(showlegend=False)
        return fig
