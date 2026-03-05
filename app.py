import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PrithviNet", layout="wide")

data = pd.read_csv("pollution_data.csv")

# ---------------------------
# Pollution Causes
# ---------------------------

city_pollution_causes = {
"Delhi":["Vehicular emissions","Crop burning","Construction dust","Industrial pollution"],
"Mumbai":["Heavy traffic","Construction dust","Humidity trapping pollutants"],
"Kolkata":["Coal industries","Traffic congestion","Industrial emissions"],
"Chennai":["Vehicle pollution","Industrial zones"],
"Bangalore":["Traffic congestion","Urban construction"],
"Hyderabad":["Urban traffic","Construction dust"],
"Pune":["Rapid urbanization","Vehicle density"],
"Ahmedabad":["Industrial emissions","Vehicle pollution"],
"Lucknow":["Crop burning impact","Traffic pollution"],
"Jaipur":["Dust storms","Vehicle emissions"],
"Bhopal":["Industrial zones","Traffic pollution"],
"Patna":["Construction dust","Vehicle pollution"],
"Ranchi":["Industrial activities","Coal burning"],
"Bhubaneswar":["Urban growth","Traffic pollution"],
"Raipur":["Steel industries","Mining dust"],
"Indore":["Urban traffic","Construction"],
"Chandigarh":["Vehicle density"],
"Shimla":["Tourism traffic"],
"Dehradun":["Urban growth"],
"Gangtok":["Tourism traffic"],
"Guwahati":["Traffic congestion"],
"Imphal":["Urbanization"],
"Aizawl":["Urban vehicles"],
"Itanagar":["Traffic"],
"Shillong":["Tourism vehicles"],
"Agartala":["Urban growth"],
"Mysore":["Traffic"],
"Coimbatore":["Industries"],
"Thiruvananthapuram":["Traffic"],
"Panaji":["Tourism traffic"]
}

# ---------------------------
# Title
# ---------------------------

st.markdown("<h1 style='text-align:center;'>🌍 PrithviNet</h1>", unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center;font-size:18px;'>AI Environmental Monitoring Platform for Air, Water and Noise Pollution</p>",
unsafe_allow_html=True
)

st.divider()

# ---------------------------
# BAR GRAPH + MAP
# ---------------------------

col1, col2 = st.columns([2,1])

with col1:

    st.subheader("Pollution Levels Across Cities")

    fig = px.bar(
        data,
        x="City",
        y="PM2.5",
        color="PM2.5",
        height=450
    )

    fig.update_traces(width=0.4)

    fig.update_layout(
        xaxis_tickangle=-60
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("India Pollution Map")

    map_data = data.copy()

    map_data = map_data.rename(columns={
        "Latitude": "lat",
        "Longitude": "lon"
    })

    map_data = map_data[["lat", "lon"]]

    st.map(map_data)

st.divider()

# ---------------------------
# Highest & Lowest Pollution
# ---------------------------

highest = data.loc[data["PM2.5"].idxmax()]
lowest = data.loc[data["PM2.5"].idxmin()]

col3, col4 = st.columns(2)

with col3:
    st.error(f"⚠ Highest Pollution: {highest['City']} ({highest['PM2.5']})")

with col4:
    st.success(f"✅ Lowest Pollution: {lowest['City']} ({lowest['PM2.5']})")

st.divider()

# ---------------------------
# City Analysis
# ---------------------------

st.subheader("City Pollution Analysis")

city = st.selectbox("Select City", data["City"])

city_data = data[data["City"] == city]

current = int(city_data["PM2.5"].values[0])

before = int(current * 0.9)
after = int(current * 1.1)

trend = pd.DataFrame({
"Time":["Before 24h","Current","After 24h"],
"PM2.5":[before,current,after]
})

fig2 = px.bar(
trend,
x="Time",
y="PM2.5",
color="Time",
title=f"Pollution Trend for {city}"
)

st.plotly_chart(fig2,use_container_width=True)

st.divider()

# ---------------------------
# AI Pollution Assistant
# ---------------------------

st.markdown("### 🤖 AI Pollution Assistant")

city_ai = st.selectbox("Select City for AI Analysis", data["City"], key="ai")

base = int(data[data["City"]==city_ai]["PM2.5"].values[0])

prediction = int(base * 1.08)

st.markdown("#### Possible Causes")

causes = city_pollution_causes.get(city_ai,
["Traffic congestion","Industrial emissions","Construction dust"])

for c in causes:
    st.write("•", c)

st.markdown("#### AI Prediction")

st.warning(f"Estimated PM2.5 in next few days: {prediction}")
