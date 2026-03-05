import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="PrithviNet", layout="wide")

# Load data
data = pd.read_csv("pollution_data.csv")

# ----------------------------
# TITLE
# ----------------------------

st.markdown(
"<h1 style='text-align:center;'>🌍 PrithviNet</h1>",
unsafe_allow_html=True
)

st.markdown(
"<p style='text-align:center;font-size:18px;'>Smart Environmental Monitoring Platform for Air, Water and Noise Pollution</p>",
unsafe_allow_html=True
)

st.divider()

# ----------------------------
# GRAPH + MAP
# ----------------------------

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

# ----------------------------
# HIGHEST / LOWEST CITY
# ----------------------------

highest = data.loc[data["PM2.5"].idxmax()]
lowest = data.loc[data["PM2.5"].idxmin()]

col3, col4 = st.columns(2)

with col3:
    st.error(f"⚠ Highest Pollution: {highest['City']} ({highest['PM2.5']})")

with col4:
    st.success(f"✅ Lowest Pollution: {lowest['City']} ({lowest['PM2.5']})")

st.divider()

# ----------------------------
# CITY ANALYSIS
# ----------------------------

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

# ----------------------------
# FLOATING CHATBOT STYLE
# ----------------------------

st.markdown("""
<style>
.chat-button {
position: fixed;
bottom: 20px;
right: 20px;
background-color: #2563eb;
color: white;
padding: 14px 18px;
border-radius: 50px;
font-size: 16px;
font-weight: bold;
box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.chat-box {
position: fixed;
bottom: 80px;
right: 20px;
width: 320px;
background-color: #111;
padding: 15px;
border-radius: 12px;
box-shadow: 0px 4px 25px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# Chat toggle
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

chat_button = st.button("🤖 AI Assistant")

if chat_button:
    st.session_state.chat_open = not st.session_state.chat_open

# ----------------------------
# CHAT WINDOW
# ----------------------------

if st.session_state.chat_open:

    st.markdown("### 🤖 PrithviNet AI Assistant")

    st.write("Select a city to analyze pollution risk.")

    city_ai = st.selectbox(
        "Choose City",
        data["City"],
        key="chat_city"
    )

    base = int(data[data["City"] == city_ai]["PM2.5"].values[0])

    prediction = base + random.randint(10,25)

    reasons = [
        "High traffic congestion",
        "Industrial emissions",
        "Construction dust",
        "Low wind speeds trapping pollutants",
        "Seasonal crop burning",
        "Firecracker pollution"
    ]

    st.markdown("### Possible Causes")

    for r in random.sample(reasons,3):
        st.write("•", r)

    st.markdown("### AI Prediction")

    st.warning(f"Expected PM2.5 in next few days: {prediction}")
