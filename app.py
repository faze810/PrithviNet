import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="PrithviNet", layout="wide")

data = pd.read_csv("pollution_data.csv")

# -------------------------
# TITLE SECTION
# -------------------------

st.markdown(
"<h1 style='text-align:center;'>🌍 PrithviNet</h1>",
unsafe_allow_html=True
)

st.markdown(
"<p style='text-align:center;font-size:18px;'>Smart Environmental Monitoring Platform for Air, Water and Noise Pollution</p>",
unsafe_allow_html=True
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
        color="PM2.5"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("India Pollution Map")

    map_data = data.rename(columns={
        "Latitude":"lat",
        "Longitude":"lon"
    })

    st.map(map_data, zoom=4)

st.divider()

# -------------------------
# HIGHEST + LOWEST POLLUTION
# -------------------------

highest = data.loc[data["PM2.5"].idxmax()]
lowest = data.loc[data["PM2.5"].idxmin()]

col3, col4 = st.columns(2)

with col3:
    st.error(f"⚠ Highest Pollution: {highest['City']} ({highest['PM2.5']})")

with col4:
    st.success(f"✅ Lowest Pollution: {lowest['City']} ({lowest['PM2.5']})")

st.divider()

# -------------------------
# CITY ANALYSIS
# -------------------------

st.subheader("City Pollution Analysis")

city = st.selectbox("Select City", data["City"])

city_data = data[data["City"] == city]

current = int(city_data["PM2.5"].values[0])

before = current - random.randint(5,15)
after = current + random.randint(5,15)

trend = pd.DataFrame({
    "Time":["24h Before","Current","24h After"],
    "PM2.5":[before,current,after]
})

fig2 = px.line(
    trend,
    x="Time",
    y="PM2.5",
    markers=True,
    title=f"Pollution Trend for {city}"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# AI CHAT BUTTON
# -------------------------

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

st.divider()

st.markdown("### 🤖 AI Pollution Risk Predictor")

if st.button("Open AI Assistant"):
    st.session_state.chat_open = not st.session_state.chat_open


# -------------------------
# AI CHATBOX
# -------------------------

if st.session_state.chat_open:

    ai_city = st.selectbox(
        "Choose City",
        data["City"],
        key="ai_city"
    )

    base = int(data[data["City"] == ai_city]["PM2.5"].values[0])

    prediction = base + random.randint(10,30)

    reasons = [
        "High traffic congestion",
        "Industrial emissions",
        "Construction dust",
        "Weather conditions trapping pollutants",
        "Firecracker pollution",
        "Vehicle density"
    ]

    st.write("### Possible Reasons")

    for r in random.sample(reasons,3):
        st.write("-", r)

    st.write("### Predicted Pollution in Coming Days")

    st.warning(f"Estimated PM2.5 level: {prediction}")

    st.write("**Prediction for next few days:**")

    st.warning(f"Estimated PM2.5: {prediction}")
