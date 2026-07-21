from weather_api import get_weather

city = input("Enter City: ")

data = get_weather(city)

if data:
    print(data)
else:
    print("Weather data not found.")