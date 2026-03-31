import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def fetch(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        return data
    else:
        raise Exception("Failed to fetch weather data. Check city name.")

def clothes(data):
    temp = data["main"]["temp"]

    if temp >= 30:
        return "Wear light cotton clothes"
    elif temp >= 20 and temp < 30:
        return "Normal clothes are fine"
    elif temp >= 10 and temp < 20:
        return "Wear jacket or hoodie"
    else:
        return "Wear heavy winter clothes"

def drive(data):
    visibility = data.get("visibility", 0)
    weather = data["weather"][0]["main"].lower()

    if visibility >= 5000:
        return "Excellent visibility: Safe to drive"
    elif visibility >= 2000:
        if weather in ["clear", "clouds", "drizzle"]:
            return "Good visibility: Safe to drive normally"
        else:
            return "Moderate visibility: Drive carefully"
    elif visibility >= 1000:
        return "Reduced visibility: Drive with caution"
    else:
        return "Poor visibility: Not safe to drive"

def aqi(data):
    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    aqi_response = requests.get(aqi_url).json()
    aqi_level = aqi_response["list"][0]["main"]["aqi"]

    aqi_messages = {
        1: "Air Quality: Good and Mask: Not needed",
        2: "Air Quality: Fair and Mask: Not needed",
        3: "Air Quality: Moderate and Mask: Surgical recommended",
        4: "Air Quality: Poor and Mask: N95 recommended",
        5: "Air Quality: Very Poor and Mask: N95 mandatory"
    }
    return aqi_messages.get(aqi_level, "Unknown AQI")

def uvi(data):
    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]
    url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        uv_index = requests.get(url).json()
        uvi = uv_index["value"]
    except Exception:
        return "UV index unavailable"

    if uvi >= 11:
        return "UV Index: Extreme - Stay indoors"
    elif uvi >= 8:
        return "UV Index: Very High - Avoid direct sun"
    elif uvi >= 6:
        return "UV Index: High - Sunglasses & sunscreen recommended"
    elif uvi >= 3:
        return "UV Index: Moderate - Protection may be needed"
    else:
        return "UV Index: Low - No protection needed"

def forecast(data):
    lon = data["coord"]["lon"]
    lat = data["coord"]["lat"]
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url).json()

    print("5-Day Forecast:")
    print("Date       | Temp   | Weather")
    print("-" * 35)
    for day in range(5):
        index = day * 8
        if index < len(response["list"]):
            temp = response["list"][index]["main"]["temp"]
            weather = response["list"][index]["weather"][0]["main"]
            date = response["list"][index]["dt_txt"].split(" ")[0]
            print(f"{date}   | {temp}°C  | {weather}")

def humid(data):
    humi = data["main"]["humidity"]
    if humi < 30:
        return "Low humidity, dry air, use moisturizer"
    elif humi >= 30 and humi <= 60:
        return "Comfortable humidity"
    else:
        return "High humidity, drink more water"

def alert(data):
    w = data["weather"][0]["main"]
    wind = data["wind"]["speed"]

    if w in ["Thunderstorm", "Tornado"]:
        return "Severe weather alert!"
    if wind > 25:
        return "High wind alert!"
    return "No extreme weather"

if __name__ == "__main__":
    city = input("Enter city: ")
    data = fetch(city)
    print(f"Weather in {city}: {data['weather'][0]['description']}")
    print(f"Temperature: {data['main']['temp']}°C")
