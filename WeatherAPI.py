import json 
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def header():
    print("\n")
    print("=" * 50)
    print("\t\tWEATHER APP")
    print("=" * 50)

def weather_fn(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data_py = response.json()
    except requests.exceptions.RequestException:
        print("Unable to connect to the weather service.")
        return None

    if data_py.get("cod") != 200:
        print("City not found. Please try again.")
        return None
    
    temp = data_py.get("main", {}).get("temp", "N/A")
    feel_like = data_py.get("main", {}).get("feels_like", "N/A")
    humidity = data_py.get("main", {}).get("humidity", "N/A")
    condition = data_py.get("weather", [{}])[0].get("description", "N/A")
    wind_speed = data_py.get("wind", {}).get("speed", "N/A")

    lon = data_py['coord']['lon']
    lat = data_py['coord']['lat']


    url2 = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        response2 = requests.get(url2)
        data_aqi = response2.json()
    except requests.exceptions.RequestException:
        print("Unable to connect to the weather service.")
        return None

    aqi = data_aqi['list'][0]['main']['aqi']

    aqi_advisory ={
        1:("Good", "Air quality is satisfactory."),
        2:("Fair","Air quality is acceptable."),
        3:("Moderate","Sensitive individuals should reduce outdoor activity."),
        4:("Poor","Reduse prolonged outdoor exertion."),
        5:("Very Poor","Avoid outdoor activities if possible.")
    }
    status,advisory = aqi_advisory[aqi]

    api_data = {
        "city": city,
        "temp": temp,
        "humidity": humidity,
        "wind_speed" : wind_speed,
        "condition" : condition,
        "aqi" : aqi
    }
    try:
        with open("history.json","r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    history.append(api_data)
    history = history[-5:]

    with open("history.json","w") as file:
        json.dump(history,file,indent =4)

    return temp,feel_like,humidity,condition,wind_speed,aqi,status,advisory,api_data
          
def print_weather_fn(city,temp,feel_like,humidity,condition,wind_speed,aqi,status,advisory):

    print(f"Weather in {city}")
    print(f"Temp : {temp}*C (Feels like {feel_like}*C)")
    print(f"Humidity : {humidity}%")
    print(f"Condition : {condition}")
    print(f"Wind Speed : {wind_speed} km/h")
    print(f"Air Quality Index: {aqi} — {status}")
    print(f"Advisory: {advisory}")

def history_fn():

    with open ("history.json","r") as file:
        data = json.load(file)

    print("\n"+"="*57)
    print(f"{'City':<10}{'Temp(°C)':<10}{'Humidity(%)':<13}{'Wind Speed(km/h)':<20}{'AQI':<7}")
    print("="*57)
    for items in data:
        print(f"{items['city']:<11}"
              f"{items['temp']:<13}"
              f"{items['humidity']:<14}"
              f"{items['wind_speed']:<16}"
              f"{items['aqi']:<7}")
    print("="*57)

def last_search():
    try:
        with open("history.json", "r") as file:
            history = json.load(file)

        if history:   
            last = history[-1]

            print("Last Search:")
            print(
                f"{last['city']} | "
                f"{last['temp']}°C | "
                f"{last['humidity']}% | "
                f"{last['wind_speed']} km/h | "
                f"AQI {last['aqi']} | "
                f"{last['condition']}"
            )

    except (FileNotFoundError, json.JSONDecodeError):
         pass
    
def main():
    while True:

        header()
        last_search()
        print()

        city = input("Enter city name (or 'history'): ")

        if city.lower() == "history":
            history_fn()

        else:
            result = weather_fn(city)

            if result is not None:
                temp, feel_like, humidity, condition, wind_speed, aqi, status, advisory, api_data = result
                print_weather_fn(
                    city,
                    temp,
                    feel_like,
                    humidity,
                    condition,
                    wind_speed,
                    aqi,
                    status,
                    advisory
                )
        
main()
