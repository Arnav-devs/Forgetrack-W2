import json 
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print(API_KEY)

def header():
    print("\n")
    print("=" * 30)
    print("\tWEATHER APP")
    print("=" * 30)

def weather_fn(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data_py = response.json()

    temp = data_py['main']['temp']
    feel_like = data_py['main']['feels_like']
    
    humidity = data_py['main']['humidity']
    
    condition = data_py['weather'][0]['description']
    
    wind_speed = data_py['wind']['speed']
    

    lon = data_py['coord']['lon']
    lat = data_py['coord']['lat']


    url2 = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response2 = requests.get(url2)
    data_aqi = response2.json()

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

def history_fn(api_data):
    

def main():

    while True:
        temp,feel_like,humidity,condition,wind_speed,aqi,status,advisory,api_data =weather_fn(city)
        header()
        last_search()
        city = input("enter city name or history : ")
        if city == 'history':
            history_fn(api_data)
        else :
            print_weather_fn(city,temp,feel_like,humidity,condition,wind_speed,aqi,status,advisory)
        
        

