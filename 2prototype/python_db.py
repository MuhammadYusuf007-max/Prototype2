import requests
import psycopg2
from flask import Flask, render_template


db_config = {
    'dbname': 'data',
    'user': 'postgres',
    'password': '1234567890',
    'host': 'localhost'
}

api_key = '617827a88878fb36cb2c3c1650e82180'
city = 'New York'  


url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

delete_query = """
    DELETE FROM weather_data
    WHERE city = 'New York';"""

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(delete_query)
    conn.commit()

    print("Data deleted successfully.")

except psycopg2.Error as e:
    print("Error deleting data:", e)

finally:
    cursor.close()
    conn.close()
try:
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()

        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO weather_data (city, temperature, humidity) VALUES (%s, %s, %s)"
        data = (city,  temperature, humidity, )
        
        print(data)

        cursor.execute(insert_query, data)
        conn.commit()

        print("Weather data inserted successfully")

        cursor.close()
        conn.close()
    else:
        print("Failed to fetch data from OpenWeatherMap API")
except Exception as e:
    print("An error occurred:", e)
    

app = Flask(__name__)

@app.route('/')
def index():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            print(weather_data)
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']

            return render_template('index.html', city=city,  temperature=temperature, humidity=humidity)
        else:
            return "Failed to fetch data from OpenWeatherMap API"
    except Exception as e:
        return "An error occurred: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
    