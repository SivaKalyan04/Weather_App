import requests

def city_weather(city, date=None):
    API_KEY = "0ba9e5bd2ccc404e9b055920251607"
    #date_param = f"&dt={date}" if date else ""

    current_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
    marine_url = f"http://api.weatherapi.com/v1/marine.json?key={API_KEY}&q={city}"

    response = requests.get(current_url)
    response1 = requests.get(forecast_url)
    response2 = requests.get(marine_url)

    data = response.json() if response.status_code == 200 else None
    data1 = response1.json() if response1.status_code == 200 else None 
    data2 = response2.json() if response2.status_code == 200 else None  

    return data, data1, data2