import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Plots:
    def __init__(self, file, district): 
        self.district = district             

        dataframe = pd.read_csv(file)
        dataframe ["price_sqm_total"] = dataframe ["price"]/dataframe ["living_area"]
        self.df_complete = dataframe

        mask = self.df_complete["district"] == district
        self.df_district = self.df_complete[mask]

    @staticmethod
    def thousants_point(x: int) -> str:  
        return str('{:,}'.format(round(x)).replace(',','.'))
    
    def price_sqm (self, prediction: float, living_area: float):
        subset_district = self.df_district
        district = self.district

        average_price = round(subset_district["price_sqm_total"].mean())  


        # text prediction
        price_sqm_predict = int(prediction/living_area)
        text_pred = "Your house €" + self.thousants_point(price_sqm_predict)  + "/m²"

        # Starts setting up the histogram
                
        fig = px.histogram(subset_district,  x="price_sqm_total", 
        labels ={"price_sqm_total": f"Price per living area (€/m²) in {district}"}).update_layout(yaxis_title=f"Houses Count") 
       
        fig.add_shape(type="line", x0=average_price, x1=average_price,  yref="paper", y0=0.1, y1=0.9, line=dict(color="Green",width=2))
        fig.add_annotation(x=average_price,  y= 0,
            text=f"Average: €{average_price}/m²",
            showarrow=True,
            arrowhead=1,
            xanchor="left", 
            ax = 20,
            ay = 20
            )
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

    def pie_chart (self, feature, feature_name, home_value):

        df_room = self.df_district.groupby(feature, as_index=False).count()
        

        df_room = df_room [[feature, "district"]]
        df_room.rename(columns={"district": "Count", feature : feature_name}, inplace= True)        

        pull = df_room[feature_name] == home_value
        pull = pull * 0.1 

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

        fig.update_layout(
            # Add annotations in the center of the donut.
            annotations=[                              
                dict(
                    text="<b>{name}</b></br></br>Yours has {home_value}.".format(name=feature_name.upper(), home_value = home_value),
                 
                    # Hide the arrow that points to the [x,y] coordinate
                    showarrow=False
                
                )
            ]
        )
        return fig