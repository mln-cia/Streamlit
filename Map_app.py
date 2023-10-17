import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import plotly.express as px

# Defining a function to generate the choropleth map
def generate_choropleth_map(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.ms-excel":
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        if 'geometry' in df.columns:
            df['geometry'] = df['geometry'].apply(lambda x: loads(x))
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
            gdf = gdf.drop('Unnamed: 0', axis=1)
            df = df.drop('Unnamed: 0', axis=1)
        else:
            st.warning("The uploaded file does not contain a 'geometry' column.")
            return

        excluded_columns = ['cap', 'geometry']
        available_intensity_columns = [col for col in df.columns if col not in excluded_columns]

        st.sidebar.header("Choropleth Map Options")
        selected_intensity_column = st.sidebar.selectbox(
            "Select Intensity Column for Choropleth Map",
            available_intensity_columns,
        )

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
            hover_data=["cap", selected_intensity_column],
            height = 900,
            width = 900,
        )

        st.plotly_chart(choropleth_fig)

# Main Streamlit app code
uploaded_file = st.file_uploader("Upload your DataFrame file (CSV or Excel)", type=["csv", "xlsx"])
st.write('Your choropleth map:')
generate_choropleth_map(uploaded_file)
