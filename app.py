import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PrithviNet", layout="wide")

data = pd.read_csv("pollution_data.csv")

# ----------------------------
# Pollution Causes Database
# ----------------------------

city_pollution_causes = {
"Delhi":["Vehicular emissions","Crop burning","Construction dust","Industrial pollution"],
"Mumbai":["Heavy traffic","Construction dust","Coastal humidity trapping pollutants"],
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
# TITLE
# ----------------------------

st.markdown("<h1 style='text-align:center;'>🌍 PrithviNet</h1>",unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center;font-size:18px;'>Smart Environmental Monitoring Platform for Air, Water and Noise Pollution</p>",
unsafe_allow_html=True
)

st.divider()

# ----------------------------
# GRAPH + MAP
# ----------------------------

col1,col2=st.columns([2,1])

with col1:

    st.subheader("Pollution Levels Across Cities")

    fig=px.bar(data,x="City",y="PM2.5",color="PM2.5")

    st.plotly_chart(fig,use_container_width=True)

with col2:

    st.subheader("India Pollution Map")

    map_data=data.rename(columns={"Latitude":"lat","Longitude":"lon"})

    st.map(map_data,zoom=4)

st.divider()

# ----------------------------
# Highest & Lowest City
# ----------------------------

highest=data.loc[data["PM2.5"].idxmax()]
lowest=data.loc[data["PM2.5"].idxmin()]

col3,col4=st.columns(2)

with col3:
    st.error(f"⚠ Highest Pollution: {highest['City']} ({highest['PM2.5']})")

with col4:
    st.success(f"✅ Lowest Pollution: {lowest['City']} ({lowest['PM2.5']})")

st.divider()

# ----------------------------
# City Analysis
# ----------------------------

st.subheader("City Pollution Analysis")

city=st.selectbox("Select City",data["City"])

city_data=data[data["City"]==city]

current=int(city_data["PM2.5"].values[0])

before=int(current*0.92)
after=int(current*1.08)

trend=pd.DataFrame({
"Time":["24h Before","Current","24h After"],
"PM2.5":[before,current,after]
})

fig2=px.line(trend,x="Time",y="PM2.5",markers=True,title=f"Pollution Trend for {city}")

st.plotly_chart(fig2,use_container_width=True)

# ----------------------------
# Floating AI Assistant
# ----------------------------

st.divider()

if "chat_open" not in st.session_state:
    st.session_state.chat_open=False

if st.button("🤖 AI Pollution Assistant"):
    st.session_state.chat_open=not st.session_state.chat_open

if st.session_state.chat_open:

    st.markdown("### 🤖 PrithviNet AI Assistant")

    city_ai=st.selectbox("Choose City",data["City"],key="chat")

    base=int(data[data["City"]==city_ai]["PM2.5"].values[0])

    prediction=int(base*1.08)

    st.markdown("### Possible Causes")

    for r in city_pollution_causes.get(city_ai,["Traffic congestion","Industrial emissions","Construction dust"]):
        st.write("•",r)

    st.markdown("### AI Prediction")

    st.warning(f"Estimated PM2.5 in next few days: {prediction}")
