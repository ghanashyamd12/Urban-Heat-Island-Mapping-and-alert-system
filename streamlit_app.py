
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import requests
import os

st.title("🌆 Urban Heat Island Mapping & Intervention Simulator")

city_choice = st.selectbox("Select a city", ["Bangalore", "Mysore", "Live Temperature - Your City"])

API_KEY = st.secrets["OPENWEATHER_API"] if "OPENWEATHER_API" in st.secrets else os.getenv("OPENWEATHER_API")

if city_choice == "Live Temperature - Your City":
    city_input = st.text_input("Enter your city name:")
    if city_input and API_KEY:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_input}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if "main" in response:
            temp = response["main"]["temp"]
            lat = response["coord"]["lat"]
            lon = response["coord"]["lon"]
            st.success(f"{city_input} - Current Temp: {temp}°C")
            df = pd.DataFrame([[lat, lon, temp]], columns=["lat", "lon", "temp"])
        else:
            st.error("City not found or API error")
            df = pd.DataFrame(columns=["lat", "lon", "temp"])
    else:
        df = pd.DataFrame(columns=["lat", "lon", "temp"])
else:
    file = "bangalore_data.csv" if city_choice == "Bangalore" else "mysore_data.csv"
    df = pd.read_csv(file)

if not df.empty:
    st.subheader("🌡️ Temperature Summary")
    avg = df["temp"].mean()
    max_temp = df["temp"].max()
    hot_zones = df[df["temp"] >= 40]
    st.markdown(f"- **Average Temp:** {avg:.2f}°C")
    st.markdown(f"- **Max Temp:** {max_temp:.2f}°C")
    st.markdown(f"- **Hot Zones (≥40°C):** {len(hot_zones)}")

    st.subheader("🌳 Green Intervention Simulator")
    trees = st.slider("🌳 Trees to Plant per Hot Zone", 0, 100, 20)
    roofs = st.slider("🏠 Cool Roof Area per Hot Zone (sqm)", 0, 1000, 200)
    drop = trees * 0.015 + roofs * 0.002
    cost = (trees * 100 + roofs * 30) * len(hot_zones)
    roi = len(hot_zones) * drop * 500

    st.markdown(f"- 🔻 **Temp Reduction/Zone:** {drop:.2f}°C")
    st.markdown(f"- 💰 **Total Cost:** ₹{cost}")
    st.markdown(f"- 📈 **Estimated ROI/year:** ₹{roi:.0f}")

    df["adjusted_temp"] = df.apply(lambda x: x["temp"] - drop if x["temp"] >= 40 else x["temp"], axis=1)

    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=12)
    heat = [[row["lat"], row["lon"], row["adjusted_temp"]] for _, row in df.iterrows()]
    HeatMap(heat, radius=25, blur=15).add_to(m)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            popup=f"{row['temp']}°C → {row['adjusted_temp']:.2f}°C",
            color='red' if row['adjusted_temp'] >= 40 else 'orange' if row['adjusted_temp'] >= 38 else 'green',
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    st.subheader("🗺️ Heatmap")
    folium_static(m)
