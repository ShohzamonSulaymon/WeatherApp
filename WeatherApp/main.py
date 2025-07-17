import sys
import requests
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, 
                              QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 250, 400, 350)
        self.weather_app = QLabel("Weather ⛅")
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("∞°",self)
        self.emoji_label = QLabel("☀️",self)
        self.description_label = QLabel("Sky’s mood update",self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weather")
        vbox = QVBoxLayout()

        vbox.setContentsMargins(30,30,30,30)

        vbox.addWidget(self.weather_app)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.temperature_label)
        hbox.addWidget(self.emoji_label)
        vbox.addLayout(hbox)

        vbox.addWidget(self.description_label)
        self.setLayout(vbox)


        self.weather_app.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignLeft)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        

        self.setObjectName("main")
        self.weather_app.setObjectName("weather_app")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
                           #main { background-color: white;
                           }
                           
                           QLabel {
                           font-family: calibri;
                           font-size: 120px;
                           font-weight: 550;
                           background-color: white;
                           color: black;
                           border-radius: 18px;

                           }
                           #city_input {
                           border-radius: 18px;
                           border: 1px solid black;
                           padding: 10px;
                           padding-left: 20px;
                           font-size: 25px;
                           font-weight: 600;
                           background-color: white;
                           color: black;
                           
                           }
                           #get_weather_button {
                           padding: 10px;
                           background-color: #2563EB;
                           color: #FFFFFF;
                           font-family: calibri;
                           font-size: 25px;
                           font-weight: 600;
                           border-radius: 18px;
                           margin-top: 10px;
                           }
                           #get_weather_button:hover{
                           background-color: #1D4ED8;
                           }
                           #get_weather_button:pressed{
                           background-color: #1E40AF;
                           }
                           #description_label {
                           font-size: 40px;
                           font-weight: 550;
                           border-radius: 18px;
                           }
                           #weather_app {
                           font-size: 50px;
                           margin-bottom: 20px;}
                           """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)
        
         
    
    
    def get_weather(self):
        api_key = "50f3a213243ada7975bba87c17183cef"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
         
         
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
            

        
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 401:
                    self.display_error("Unauhorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAcces denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavialabel\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error("HTTP error occured\n{http_error}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")
            



    def display_error(self, message):
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setText(message)
        self.description_label.setStyleSheet("font-size: 20px;")
        self.temperature_label.setText("∞°")



    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_description = data["weather"][0]["description"]
        code = data["weather"][0]["id"]
        icon = data["weather"][0]["icon"]
        self.description_label.setText(weather_description.capitalize())
        self.description_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.description_label.setStyleSheet("font-size: 40px;")
        self.temperature_label.setText(f"{temperature_c:.0f}°")
        self.emoji_label.setText(self.get_weather_emoji(code, icon))
    
    @staticmethod
    def get_weather_emoji(code, icon):
        
        is_night = icon.endswith("n")

        if 200 <= code < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= code < 400:
            return "🌦️"  # Drizzle
        elif 500 <= code < 600:
            return "🌧️"  # Rain
        elif 600 <= code < 700:
            return "❄️"  # Snow
        elif 700 <= code < 800:
            return "🌫️"  # Fog, mist, etc.
        elif code == 800:
            return "🌙" if is_night else "☀️"  # Clear night/day
        elif code == 801:
            return "🌤️" if is_night else "🌤️"  # Few clouds
        elif code == 802:
            return "☁️" if is_night else "⛅"   # Scattered clouds
        elif code in [803, 804]:
            return "☁️"  # Broken/overcast clouds
        else:
            return "🌈"  # Fallback / unknown









if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())

