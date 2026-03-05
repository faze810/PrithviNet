import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PrithviNet", layout="wide")

# Load data
data = pd.read_csv("pollution_data.csv")

st.title("🌍 PrithviNet Environmental Monitoring Platform")
st.write("AI-powered monitoring system for **Air, Water and Noise pollution**.")

# ==============================
# Sidebar Navigation
# ==============================

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Pollution Map",
        "Pollution Heatmap",
        "Alerts",
        "AI Prediction",
        "Industry Monitor",
        "Citizen Portal"
    ]
)

# ==============================
# Dashboard
# ==============================

if page == "Dashboard":

    st.header("📊 Pollution Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Highest PM2.5", data["PM2.5"].max())
    col2.metric("Average Noise", round(data["Noise"].mean(),2))
    col3.metric("Average Water pH", round(data["Water_pH"].mean(),2))

    st.divider()

    st.subheader("Air Pollution Levels")

    fig = px.bar(
        data,
        x="City",
        y="PM2.5",
        color="PM2.5",
        title="PM2.5 Levels Across Cities"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# Pollution Map
# ==============================

elif page == "Pollution Map":

    st.header("🗺 Pollution Map")

    map_data = data.rename(columns={
        "Latitude": "lat",
        "Longitude": "lon"
    })

    st.map(map_data)


# ==============================
# Pollution Heatmap
# ==============================

elif page == "Pollution Heatmap":

    st.header("🔥 Pollution Heatmap")

    fig_map = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        size="PM2.5",
        color="PM2.5",
        hover_name="City",
        zoom=4
    )

    fig_map.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig_map, use_container_width=True)


# ==============================
# Alerts
# ==============================

elif page == "Alerts":

    st.header("⚠ Pollution Alerts")

    limit = 100

    for i,row in data.iterrows():
        if row["PM2.5"] > limit:
            st.error(f"{row['City']} has dangerous PM2.5 level: {row['PM2.5']}")
        else:
            st.success(f"{row['City']} pollution level is safe")


# ==============================
# AI Prediction
# ==============================

elif page == "AI Prediction":

    st.header("🤖 AI Pollution Risk Predictor")

    city = st.selectbox("Select City", data["City"])

    city_data = data[data["City"] == city]

    pm = int(city_data["PM2.5"].values[0])

    prediction = pm * 1.1

    st.write(f"Current PM2.5 level: {pm}")

    st.success(f"Predicted PM2.5 in next 24 hours: {round(prediction)}")

    if prediction > 120:
        st.warning("High pollution risk predicted.")
    else:
        st.success("Pollution expected to remain moderate.")


# ==============================
# Industry Monitor
# ==============================

elif page == "Industry Monitor":

    st.header("🏭 Industry Emission Monitor")

    industry = st.text_input("Industry Name")

    emission = st.slider("SO2 Emission Level",0,200,80)

    if emission > 120:
        st.error("⚠ Industry exceeds pollution limits. Inspection required.")
    else:
        st.success("Emission within safe limit.")


# ==============================
# Citizen Portal
# ==============================

elif page == "Citizen Portal":

    st.header("👥 Citizen Pollution Checker")

    city_check = st.selectbox("Check pollution in your city", data["City"])

    city_info = data[data["City"] == city_check]

    pm = city_info["PM2.5"].values[0]

    st.write(f"Current PM2.5 level: {pm}")

    if pm < 80:
        st.success("Air quality is safe")
    elif pm < 120:
        st.warning("Moderate pollution level")
    else:
        st.error("Dangerous pollution level")
