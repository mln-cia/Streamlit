#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
import altair as alt
import streamlit as st
from shapely.wkt import loads
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[2]:


df = pd.read_csv('shareNow_scoringFactors_zipcode_geometry.csv')
df['geometry'] = df['geometry'].apply(lambda x: loads(x))


gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.head(3)


# In[3]:


df1 = pd.read_excel('Data Driven OOH Milano.xlsx')

df1[['latitude', 'longitude']] = df1['lat long'].str.split(',', expand=True).astype(float)
df_no_duplicates = df1.drop_duplicates(subset=['macro', 'tipologia', 'latitude', 'longitude'])



df1['latitude'] = df1['latitude'].round(1)
df1['longitude'] = df1['longitude'].round(1)

#Another Attempt

selected_scatter_columns = st.sidebar.selectbox(
    "Select Columns for Scatter Plot",
    ["macro", "tipologia"]
)

selected_intensity_column = st.sidebar.selectbox(
    "Select Intensity Column for Choropleth Map",
    ["PotentialUsers", "PotentialPicking", "Taken", "Users", "Score", "Potential"]
)

# Create the scatter plot 

scatter_fig = px.scatter_mapbox(
    df_no_duplicates,
    lat='latitude',
    lon='longitude',
    color=selected_scatter_columns,  
    color_discrete_sequence = ['#2ca02c', '#d62728','#9467bd','#1f77b4'],
    mapbox_style="carto-positron",
    zoom=10,
    opacity = 0.4,
)
scatter_fig.update_traces(marker=dict(size=3))  # To set the marker size for all points


# Create the choropleth map 
choropleth_fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry.__geo_interface__,
    locations=gdf.index,
    color=selected_intensity_column,
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=10,
    center={"lat": 45.4642, "lon": 9.1900},
    opacity=0.7,
    hover_data=["cap", selected_intensity_column]
)


#choropleth_fig.update_layout(
#    coloraxis_colorbar=dict(
#        x=0.5,  
#        y=1.17,  
#        xanchor="center",  
#        yanchor="top",  
#        lenmode="fraction",  
#        len=1.0,  
#        orientation = 'h'
#))


# Create a combined figure by overlaying the scatter plot and choropleth map figures
combined_fig1 = go.Figure()
combined_fig1.add_traces(scatter_fig.data)
combined_fig1.add_traces(choropleth_fig.data)

# Customizing the layout of the combined figure
combined_fig1.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": 45.4642, "lon": 9.1900},
    mapbox_zoom=10,
    height=700,
    width = 700,
    showlegend=True,  # to show legends for both plots
    legend=dict(x=0.001, y=0.999),  

)


#combined_fig1.update_traces(
#    marker=dict(size=3),
#    selector=dict(type='scattermapbox')
#)



# Displaying the combined figure
st.plotly_chart(combined_fig1)
st.plotly_chart(choropleth_fig)
st.plotly_chart(scatter_fig)
