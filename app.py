import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PrithviNet", layout="wide")

st.title("🌍 PrithviNet Environmental Monitoring Platform")

st.markdown("AI-powered monitoring system for **Air, Water and Noise pollution**.")

# Load data
data = pd.read_csv("pollution_data.csv")

# ---- Dashboard ----
st.header("📊 Pollution Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Highest PM2.5", data["PM2.5"].max())
col2.metric("Average Noise", round(data["Noise"].mean(),2))
col3.metric("Average Water pH", round(data["Water_pH"].mean(),2))

st.divider()

# ---- Charts ----
st.subheader("Air Pollution Levels")

fig = px.bar(data, x="City", y="PM2.5", color="PM2.5",
             title="PM2.5 Levels Across Cities")

st.plotly_chart(fig, use_container_width=True)

# ---- Map ----
st.subheader("🗺 Pollution Map")

st.map(data[["Latitude","Longitude"]])

# ---- Alerts ----
st.subheader("⚠ Pollution Alerts")

limit = 100

for i,row in data.iterrows():
    if row["PM2.5"] > limit:
        st.error(f"{row['City']} has dangerous PM2.5 level: {row['PM2.5']}")

# ---- AI Prediction (simple demo) ----
st.subheader("🤖 AI Pollution Risk Predictor")

city = st.selectbox("Select City", data["City"])

city_data = data[data["City"] == city]

pm = int(city_data["PM2.5"].values[0])

prediction = pm * 1.1

st.write(f"Current PM2.5: {pm}")

st.success(f"Predicted PM2.5 in next 24 hours: {round(prediction)}")

if prediction > 120:
    st.warning("High pollution risk predicted.")
