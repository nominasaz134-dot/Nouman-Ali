from datetime import datetime
import streamlit as st

# Local module imports
from charts import create_weather_chart
from database import create_table, get_history, save_weather
from weather_api import get_forecast, get_weather

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Weather Data Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# Initialize database table
create_table()

# -----------------------------
# App Header
# -----------------------------
st.title("🌦️ Weather Data Dashboard")
st.write("Search any city to get live weather information.")

# -----------------------------
# City Input & Search
# -----------------------------
city = st.text_input("Enter City Name")

if st.button("Search Weather"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        data = get_weather(city)
        forecast = get_forecast(city)

        if data:
            st.success("Weather Data Found!")

            # 1. Save search history to Database
            save_weather(
                data["name"],
                data["main"]["temp"],
                data["main"]["humidity"],
                data["weather"][0]["description"]
            )

            # 2. Hero Section Header & Icon
            icon = data["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

            st.header(f"📍 {data['name']}")
            st.image(icon_url, width=100)

            # 3. Weather Metrics Grid
            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
                st.metric("🌡 Feels Like", f"{data['main']['feels_like']} °C")
                st.metric("💧 Humidity", f"{data['main']['humidity']} %")
                st.metric("🌬 Wind Speed", f"{data['wind']['speed']} m/s")

            with col2:
                st.metric("🔵 Pressure", f"{data['main']['pressure']} hPa")
                st.metric("☁ Weather", data["weather"][0]["description"].title())
                st.metric("👁 Visibility", f"{data['visibility'] / 1000} km")

                # Format UNIX timestamps to readable 12-hour time
                sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset = datetime.fromtimestamp(data["sys"]["sunset"])
                st.metric("🌅 Sunrise", sunrise.strftime("%I:%M %p"))
                st.metric("🌇 Sunset", sunset.strftime("%I:%M %p"))

            st.divider()

            # 4. Location Coordinates
            st.subheader("📍 Location Information")
            col3, col4 = st.columns(2)
            with col3:
                st.write(f"**Latitude:** {data['coord']['lat']}")
            with col4:
                st.write(f"**Longitude:** {data['coord']['lon']}")

            st.divider()

            # 5. Interactive Weather Chart
            st.subheader("📊 Weather Statistics")
            fig = create_weather_chart(data)
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # 6. 5-Day Forecast Display
            st.subheader("📅 5-Day Weather Forecast")
            if forecast and "list" in forecast:
                shown_dates = []
                cols = st.columns(5)
                index = 0

                for item in forecast["list"]:
                    date = item["dt_txt"].split()[0]

                    # Pick midday reading (12:00:00) for a consistent daily summary
                    if date not in shown_dates and "12:00:00" in item["dt_txt"]:
                        shown_dates.append(date)
                        f_icon = item["weather"][0]["icon"]
                        f_icon_url = f"https://openweathermap.org/img/wn/{f_icon}@2x.png"

                        with cols[index]:
                            st.write(f"**{date}**")
                            st.image(f_icon_url, width=70)
                            st.write(f"🌡 {item['main']['temp']} °C")
                            st.write(item["weather"][0]["description"].title())

                        index += 1
                        if index == 5:
                            break
            else:
                st.info("No forecast available for this location.")
        else:
            st.error("City not found or unable to fetch weather data. Please check the spelling.")

st.divider()

# -----------------------------
# Search History Section
# -----------------------------
st.subheader("🕒 Recent Search History")
history = get_history()

if history:
    for row in history:
        st.write(
            f"📍 {row[0]} | 🌡 {row[1]}°C | 💧 {row[2]}% | ☁ {row[3]} | 🕒 {row[4]}"
        )
else:
    st.info("No search history available yet.")