import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from shapely.geometry import Point
from streamlit_folium import folium_static
import scipy.spatial.distance as dist


import io
import streamlit as st
import os
import pandas as pd
import numpy as np

# absolute path to this file
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
# absolute path of directory_of_interest
dir_of_interest = os.path.join(PARENT_DIR, "resources")

DATA_PATH = os.path.join(dir_of_interest, "data", "cleaned_open_pubs.csv")
#st.title(":green[Pub Data Info]")

#st.header(':red[DataFrame]')

df = pd.read_csv(DATA_PATH)

# Page Title
st.title("Find the Nearest Pub")

# User Input for Latitude and Longitude
user_lat = st.number_input("Enter your Latitude:")
user_lon = st.number_input("Enter your Longitude:")

# Calculate Distance
df["distance"] = df.apply(lambda row: dist.euclidean((user_lat, user_lon), (row["latitude"], row["longitude"])), axis=1)

# Get 5 Nearest Pubs
nearest_pubs = df.sort_values(by=["distance"]).head(5)

# Display Nearest Pubs on Map
if not nearest_pubs.empty:
    pub_map = folium.Map(location=[nearest_pubs["latitude"].mean(), nearest_pubs["longitude"].mean()], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(pub_map)

    # Add Markers to Map
    for idx, row in nearest_pubs.iterrows():
        folium.Marker(location=[row["latitude"], row["longitude"]],
                      tooltip=row["name"],
                      popup=row["address"],
                      icon=None).add_to(marker_cluster)

    # Display Map
    st.write("5 Nearest Pubs:")
    folium_static(pub_map)

    # Display Nearest Pubs in DataFrame
    st.write(nearest_pubs[["name", "address", "postcode", "local_authority", "distance"]])
else:
    st.warning("No pubs found.")
