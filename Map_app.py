#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import geopandas as gpd
import altair as alt
import streamlit as st
from shapely.wkt import loads
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# In[ ]:

#df = pd.DataFrame()

uploaded_file = st.file_uploader("Upload your DataFrame file (CSV or Excel)", type=["csv", "xlsx"])



if uploaded_file is not None:
    if uploaded_file.type == "application/vnd.ms-excel":
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

     
# Creating a GeoDataFrame from the DataFrame 
df['geometry'] = df['geometry'].apply(lambda x: loads(x))
gdf = gpd.GeoDataFrame(df, geometry='geometry')

gdf = gdf.drop('Unnamed: 0', axis=1)
df = df.drop('Unnamed: 0', axis=1)

# Creating sidebars for the choropleth map
excluded_columns = ['cap', 'geometry']
available_intensity_columns = [col for col in df.columns if col not in excluded_columns] 

# Creating sidebars for the choropleth map
st.sidebar.header("Choropleth Map Options")
selected_intensity_column = st.sidebar.selectbox(
        "Select Intensity Column for Choropleth Map",available_intensity_columns,
)

# Creating the choropleth map 
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


# Displaying the choropleth map
st.plotly_chart(choropleth_fig)
        

        


