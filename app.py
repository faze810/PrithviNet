import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PrithviNet", layout="wide")

# ----------------------------
# Load Data
# ----------------------------

data = pd.read_csv("pollution_data.csv")

# ----------------------------
# Pollution causes database
# ----------------------------

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
"Jaipur":["Dust storms","Vehicle emissions"]
}

# ----------------------------
# Title
# ----------------------------

st.markdown("<h1 style='text-align:center;'>🌍 PrithviNet</h1>", unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center;font-size:18px;'>AI Environmental Monitoring Platform for Air, Water and Noise Pollution</p>",
unsafe_allow_html=True
)

st.divider()

# ----------------------------
# City Pollution Bar Graph
# ----------------------------

col1, col2 = st.columns([2,1])

with col1:

    st.subheader("Pollution Levels Across Cities")

    fig = px.bar(
        data,
        x="City",
        y="PM2.5",
        color="PM2.5",
        height=420,
        color_continuous_scale="reds"
    )

    fig.update_traces(width=0.35)

    fig.update_layout(xaxis_tickangle=-60)

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# India Map
# ----------------------------

with col2:

    st.subheader("India Pollution Map")

    map_data = data.rename(columns={
        "Latitude":"lat",
        "Longitude":"lon"
    })

    st.map(map_data[["lat","lon"]])

st.divider()

# ----------------------------
# Highest & Lowest Pollution
# ----------------------------

highest = data.loc[data["PM2.5"].idxmax()]
lowest = data.loc[data["PM2.5"].idxmin()]

col3,col4 = st.columns(2)

with col3:
    st.error(f"⚠ Highest Pollution: {highest['City']} ({highest['PM2.5']})")

with col4:
    st.success(f"✅ Lowest Pollution: {lowest['City']} ({lowest['PM2.5']})")

st.divider()

# ----------------------------
# City Selection
# ----------------------------

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

# ----------------------------
# Source Breakdown + Intervention Simulator
# ----------------------------

st.subheader(f"Pollution Analysis for {city}")

colA, colB = st.columns(2)

# Source breakdown

with colA:

    st.markdown(f"### Source Breakdown in {city}")

    sources = pd.DataFrame({
        "Source":["Vehicles","Industries","Construction","Waste Burning"],
        "Contribution":[45,30,15,10]
    })

    fig3 = px.pie(
        sources,
        names="Source",
        values="Contribution",
        height=350
    )

    st.plotly_chart(fig3,use_container_width=True)

# Intervention simulator

with colB:

    st.markdown(f"### Pollution Intervention Simulator ({city})")

    vehicle_reduction = st.slider(
        "Reduce vehicle emissions (%)",
        0,50,10
    )

    industry_reduction = st.slider(
        "Reduce industrial emissions (%)",
        0,50,10
    )

    impact = vehicle_reduction*0.5 + industry_reduction*0.5

    new_pm = int(current * (1-impact/100))

    st.success(f"Predicted PM2.5 after intervention: {new_pm}")

st.divider()

# ----------------------------
# AI Early Warning System
# ----------------------------

st.subheader("AI Early Warning System")

if current > 120:
    st.error(f"⚠ {city} pollution may reach hazardous levels soon")

elif current > 80:
    st.warning(f"{city} pollution likely to increase in next 24 hours")

else:
    st.success(f"{city} pollution levels expected to remain stable")

st.divider()

# ----------------------------
# AI Environmental Copilot
# ----------------------------

st.subheader("🤖 AI Environmental Copilot")

question = st.selectbox(
"Ask AI about pollution",
[
"Why is pollution high in this city?",
"Which cities are most polluted?",
"What actions can reduce pollution?"
]
)

if question == "Why is pollution high in this city?":

    causes = city_pollution_causes.get(
        city,
        ["Traffic congestion","Industrial emissions","Construction dust"]
    )

    st.write(f"Possible causes in **{city}**:")

    for c in causes:
        st.write("•",c)

elif question == "Which cities are most polluted?":

    top = data.sort_values("PM2.5",ascending=False).head(5)

    st.write("Top polluted cities:")

    st.dataframe(top[["City","PM2.5"]])

elif question == "What actions can reduce pollution?":

    st.write("""
• Reduce vehicle traffic  
• Control industrial emissions  
• Increase green cover  
• Improve public transport  
• Implement stricter pollution regulations
""")
