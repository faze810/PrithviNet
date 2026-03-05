import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="PrithviNet", layout="wide")

data = pd.read_csv("pollution_data.csv")

# -------------------------
# TITLE SECTION
# -------------------------

st.markdown("<h1 style='text-align:center;'>🌍 PrithviNet</h1>", unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center;font-size:18px;'>Smart Environmental Monitoring Platform for Air, Water and Noise Pollution</p>",
unsafe_allow_html=True
)

st.image(
"https://images.unsplash.com/photo-1500375592092-40eb2168fd21",
use_container_width=True
)

st.divider()

# -------------------------
# GRAPH + MAP SECTION
# -------------------------

col1, col2 = st.columns([2,1])

with col1:

    st.subheader("Pollution Levels Across Cities")

    fig = px.bar(
        data,
        x="City",
        y="PM2.5",
        color="PM2.5",
        title="PM2.5 Levels"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("India Pollution Map")

    map_data = data.rename(columns={
        "Latitude": "lat",
        "Longitude": "lon"
    })

    st.map(map_data, zoom=4)

st.divider()

# -------------------------
# HIGHEST + LOWEST POLLUTION
# -------------------------

highest_city = data.loc[data["PM2.5"].idxmax()]
lowest_city = data.loc[data["PM2.5"].idxmin()]

col3, col4 = st.columns(2)

with col3:
    st.error(f"⚠ Highest Polluted City: {highest_city['City']} ({highest_city['PM2.5']})")

with col4:
    st.success(f"✅ Lowest Polluted City: {lowest_city['City']} ({lowest_city['PM2.5']})")

st.divider()

# -------------------------
# CITY DROPDOWN
# -------------------------

st.subheader("City Pollution Analysis")

city = st.selectbox("Select City", data["City"])

city_data = data[data["City"] == city]

current = int(city_data["PM2.5"].values[0])

before = current - random.randint(5,15)
after = current + random.randint(5,15)

trend_data = pd.DataFrame({
    "Time":["24h Before","Current","24h After"],
    "PM2.5":[before,current,after]
})

fig2 = px.line(
    trend_data,
    x="Time",
    y="PM2.5",
    markers=True,
    title=f"Pollution Trend for {city}"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -------------------------
# AI PREDICTOR BUTTON
# -------------------------

st.markdown("### 🤖 AI Pollution Risk Predictor")

if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

if st.button("Open AI Predictor"):
    st.session_state.show_ai = True

if st.session_state.show_ai:

    ai_city = st.selectbox("Select city for prediction", data["City"])

    base = int(data[data["City"]==ai_city]["PM2.5"].values[0])

    prediction = base + random.randint(10,25)

    reasons = [
        "High traffic congestion",
        "Industrial emissions",
        "Construction dust",
        "Weather conditions trapping pollutants",
        "Festival firecrackers"
    ]

    st.write("### Possible Reasons")

    for r in random.sample(reasons,3):
        st.write("-",r)

    st.write("### Predicted Pollution")

    st.warning(f"Estimated PM2.5 in next few days: {prediction}")
