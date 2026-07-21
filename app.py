import streamlit as st
from weather_api import get_weather, get_forecast
from charts import create_weather_chart
from database import create_table, save_weather, get_history
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Weather Data Dashboard",
    page_icon="🌦️",
    layout="wide"
)
create_table()

# -----------------------------
# Title
# -----------------------------
st.title("🌦️ Weather Data Dashboard")
st.write("Search any city to get live weather information.")

# -----------------------------
# City Input
# -----------------------------
city = st.text_input("Enter City Name")

# -----------------------------
# Search Button
# -----------------------------
if st.button("Search Weather"):

    if city == "":
        st.warning("Please enter a city name.")
    else:

        data = get_weather(city)
        forecast = get_forecast(city)

        if data:

            st.success("Weather Data Found!")
            save_weather(
    data["name"],
    data["main"]["temp"],
    data["main"]["humidity"],
    data["weather"][0]["description"]
)

            st.subheader(f"📍 {data['name']}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
                st.metric("💧 Humidity", f"{data['main']['humidity']} %")
                st.metric("🌬 Wind Speed", f"{data['wind']['speed']} m/s")

            with col2:
                st.metric("🌡 Feels Like", f"{data['main']['feels_like']} °C")
                st.metric("🔵 Pressure", f"{data['main']['pressure']} hPa")
                st.metric("☁ Weather", data['weather'][0]['description'].title())
if data:

    st.success("Weather Data Found!")

    # Weather Icon
    icon = data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    # City Name
    st.header(f"📍 {data['name']}")

    # Display Icon
    st.image(icon_url, width=100)

    # Two Columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
        st.metric("🌡 Feels Like", f"{data['main']['feels_like']} °C")
        st.metric("💧 Humidity", f"{data['main']['humidity']} %")
        st.metric("🌬 Wind Speed", f"{data['wind']['speed']} m/s")

    with col2:
        st.metric("🔵 Pressure", f"{data['main']['pressure']} hPa")
        st.metric("☁ Weather", data['weather'][0]['description'].title())
        st.metric("👁 Visibility", f"{data['visibility']/1000} km")

        sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(data['sys']['sunset'])

        st.metric("🌅 Sunrise", sunrise.strftime("%I:%M %p"))
        st.metric("🌇 Sunset", sunset.strftime("%I:%M %p"))

    st.divider()

    st.subheader("📍 Location Information")

    col3, col4 = st.columns(2)

    with col3:
        st.write(f"**Latitude:** {data['coord']['lat']}")

    with col4:
        st.write(f"**Longitude:** {data['coord']['lon']}")
        st.divider()

st.subheader("📊 Weather Statistics")

fig = create_weather_chart(data)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("📅 5-Day Weather Forecast")

if forecast:

    shown_dates = []

    cols = st.columns(5)

    index = 0

    for item in forecast["list"]:

        date = item["dt_txt"].split()[0]

        if date not in shown_dates and "12:00:00" in item["dt_txt"]:

            shown_dates.append(date)

            icon = item["weather"][0]["icon"]

            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

            with cols[index]:

                st.write(f"**{date}**")

                st.image(icon_url, width=70)

                st.write(f"🌡 {item['main']['temp']} °C")

                st.write(item["weather"][0]["description"].title())

            index += 1

            if index == 5:
                break
            st.divider()

st.subheader("🕒 Recent Search History")

history = get_history()

if history:

    for row in history:

        st.write(
            f"📍 {row[0]} | 🌡 {row[1]}°C | 💧 {row[2]}% | ☁ {row[3]} | 🕒 {row[4]}"
        )

else:
    st.info("No search history available.")