import streamlit as st
from weather import city_weather
import pandas as pd
import plotly.express as px
import datetime

st.title("Real Time Weather Prediction App")

today = datetime.date.today()
selected_date = st.date_input(
    " Select any date (up to two days from now) to get the weather forecast:",
    value=today,
    min_value=today,
    max_value=today + datetime.timedelta(days=2))

forecast_date = selected_date.strftime("%Y-%m-%d")
city  = st.text_input("Enter the city name can also enter multiple cities for comaprision: ")

data,data1,data2 = None,None,None

if st.button("Get Weather"):
    with st.spinner("Gathering weather info..."):
        #st.subheader(f"The Weather in {data['location']['name']} on {forecast_date}")
        data,data1,data2 = city_weather(city,forecast_date)
        st.write("Processed")
    if data and 'location' in data:
        st.subheader(f"The Weather in {data['location']['name']}")
        st.write(f"Temperature: {data['current']['temp_c']} °C")
        st.write(f"Feels Like: {data['current']['feelslike_c']} °C")

    else:
        st.error("Failed to get current weather data.")

    if data1 and 'forecast' in data1:
        forecast_day_data = next((day for day in data1['forecast']['forecastday'] if day['date'] == forecast_date), None)

        if forecast_day_data:
            st.markdown("### Forecast")
            st.write(f"Date: {forecast_day_data['date']}")
            st.write(f"Sunrise: {forecast_day_data['astro']['sunrise']}")
            st.write(f"Humidity (Hour 0): {forecast_day_data['hour'][0]['humidity']}%")
            st.write(f"Chance of Rain (Hour 0): {forecast_day_data['hour'][0]['chance_of_rain']}%")

            hours = [hour['time'].split(' ')[1] for hour in forecast_day_data['hour']]
            temperature = [hour['temp_c'] for hour in forecast_day_data['hour']]

            df = pd.DataFrame({'Time': hours, 'Temperature': temperature})
            st.markdown("Temperature Forecast in next 24 hours")
            st.line_chart(df.set_index('Time'))
        else:
            st.warning("No forecast available for the selected date.")



#st.set_page_config("Multiple Cities Weather Comparision")
st.title("Multiple cities comparision")
multi_city = st.text_input("Enter multiple city names for comparision")
if st.button("Compare Cities"):
    with st.spinner("Gathering weather info..."):
        #st.subheader(f"The Weather in {data['location']['name']} on {forecast_date}")
        cities = [c.strip() for c in multi_city.split(",") if c.strip()]
    if len(cities) < 2 or len(cities) > 3:
        st.error(" Please enter 2 or 3 valid city names.")
    else:
        comparision_data = []
        forecast_chart_data = []
        cols = st.columns(len(cities))
        for i,city in enumerate(cities):
            data,data1,_ = city_weather(city,forecast_date)
            with cols[i]:
                if data:
                    st.subheader(f"The Weather in {data['location']['name']}")
                    st.metric("Temp", f"{data['current']['temp_c']}°C", f"Feels like {data['current']['feelslike_c']}°C")
                    st.metric("Humidity", f"{data['current']['humidity']}%")
                    st.caption(data['current']['condition']['text'])
                if data1 and 'forecast' in data1:
                    forecast_day_data = next(
                    (day for day in data1['forecast']['forecastday'] if day['date'] == forecast_date), None
                    )
                    if forecast_day_data:
                        for hour in forecast_day_data['hour']:
                            time = hour['time'].split(' ')[1][:2]
                            forecast_chart_data.append({
                            'City': city.title(),
                            'Time': time,
                            'Temperature': hour['temp_c']
                            })
        if forecast_chart_data:
            df = pd.DataFrame(forecast_chart_data)
            st.markdown("Temperature comparison for multiple cities for next 24 hours")
            fig = px.line(df,x = "Time",y = "Temperature", color = "City", markers = True)
            st.plotly_chart(fig,use_container_width=True)