import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

today = datetime.now()
yesterday = today - timedelta(days=1)

st.markdown("# Example Dashboard")

st.markdown("""
            ### Master Date Selectors
            """)

master_col = st.columns(2)
master_col[0].date_input(
    "Master Start Date",
    yesterday)  # date variables not connected due to dummy data
master_col[1].date_input(
    "Master End Date", today)  # date variables not connected due to dummy data

st.markdown("# ")
st.markdown("# ")

# Example Metrics
st.markdown("""
            ### Example Metrics
            """)

# Metric date controls
master_col = st.columns(2)
start_metric_input = master_col[0].date_input("Metric Start Date", yesterday)
end_metric_input = master_col[1].date_input("Metric End Date", today)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Netsales", 10, "+3.42%")  # replace absolute values

col2.metric("Orders", 10, "-0.46%")  # replace absolute values

col3.metric("AOV", 10, "+14.87%")  # replace absolute values

col4.metric("Customer Sessions", 50, "10%")  # replace absolute values

col5.metric("Conversion Rate", "0.43", "20%")  # replace absolute values

st.markdown("# ")
st.markdown("# ")

# Example Chart
st.markdown("""
            ### Example Charts
            """)

revenue_date_input = st.columns(2)

start_revenue_input = revenue_date_input[0].date_input(
    "Chart Start Date",
    yesterday)  # date variables not connected due to dummy data

end_revenue_input = revenue_date_input[1].date_input(
    "Chart End Date", today)  # date variables not connected due to dummy data

@st.cache
def get_line_chart_data():

    return pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])


df = get_line_chart_data()

st.line_chart(df)

@st.cache
def get_area_chart_data():

    return pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])


chart_data = get_area_chart_data()

st.area_chart(chart_data)

@st.cache
def get_histo():

    df = pd.DataFrame(np.random.randn(200, 1), columns=['a'])

    return np.histogram(df.a, bins=25)[0]


hist_values = get_histo()

st.bar_chart(hist_values)


st.markdown("# ")
st.markdown("# ")

# Plotly Graph
st.markdown("""
            ### Plotly Graphs
            """)


@st.cache
def get_plotly_data():

    z_data = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv'
    )
    z = z_data.values
    sh_0, sh_1 = z.shape
    x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    return x, y, z


x, y, z = get_plotly_data()

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='IRR',
                  autosize=False,
                  width=800,
                  height=800,
                  margin=dict(l=40, r=40, b=40, t=40))
st.plotly_chart(fig)

st.markdown("# ")
st.markdown("# ")


# Example Map
st.markdown("""
            ### Example Map
            """)

from streamlit_folium import folium_static

import folium

import os

import pandas as pd

m = folium.Map(location=[47, 1], zoom_start=6)

geojson_path = os.path.join("data", "departements.json")
cities_path = os.path.join("data", "lewagon_cities.csv")

for _, city in pd.read_csv(cities_path).iterrows():

    folium.Marker(
            location=[city.lat, city.lon],
            popup=city.city,
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

def color_function(feat):
    return "red" if int(feat["properties"]["code"][:1]) < 5 else "blue"

folium.GeoJson(
        geojson_path,
        name="geojson",
        style_function=lambda feat: {
            "weight": 1,
            "color": "black",
            "opacity": 0.25,
            "fillColor": color_function(feat),
            "fillOpacity": 0.25,
        },
        highlight_function=lambda feat: {
            "fillColor": color_function(feat),
            "fillOpacity": .5,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['code', 'nom'],
            aliases=['Code', 'Name'],
            localize=True
        ),
    ).add_to(m)

folium_static(m)
