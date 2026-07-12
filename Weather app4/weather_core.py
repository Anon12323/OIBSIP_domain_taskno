"""
Weather App Core Logic - API calls and data processing
"""

import requests
import json
import os
from datetime import datetime, timedelta

class WeatherCore:
    def __init__(self, api_key=None):
        
        self.api_key =  ""
        self.current_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.cache_file = "weather_data.json"
        self.cache = self.load_cache()
    
    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass
    
    def get_current_weather(self, city):
        
        if self.api_key == "YOUR_API_KEY_HERE":
            return {'error': 'Please add your OpenWeatherMap API key to weather_core.py'}
        
        cache_key = f"{city.lower()}_current"
        
        # Check cache
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time < timedelta(minutes=10):
                return cached['data']
        
        params = {
            'q': city, 
            'appid': self.api_key, 
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.current_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save to cache
                self.cache[cache_key] = {
                    'timestamp': datetime.now().isoformat(),
                    'data': data
                }
                self.save_cache()
                return data
            elif response.status_code == 401:
                return {'error': 'Invalid API key. Please check your OpenWeatherMap API key.'}
            elif response.status_code == 404:
                return {'error': f'City "{city}" not found. Check spelling.'}
            else:
                return {'error': f'Error {response.status_code}: {response.text[:100]}'}
                
        except requests.exceptions.ConnectionError:
            return {'error': 'No internet connection. Check your network.'}
        except requests.exceptions.Timeout:
            return {'error': 'Connection timed out. Try again.'}
        except Exception as e:
            return {'error': f'Error: {str(e)}'}
    
    def get_forecast(self, city):
        
        if self.api_key == "YOUR_API_KEY_HERE":
            return {'error': 'Please add your OpenWeatherMap API key to weather_core.py'}
        
        cache_key = f"{city.lower()}_forecast"
        
        # Check cache
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time < timedelta(hours=1):
                return cached['data']
        
        params = {
            'q': city, 
            'appid': self.api_key, 
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.forecast_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                processed = self.process_forecast(data)
                
                # Save to cache
                self.cache[cache_key] = {
                    'timestamp': datetime.now().isoformat(),
                    'data': processed
                }
                self.save_cache()
                return processed
            else:
                return {'error': f'Forecast error: {response.status_code}'}
                
        except Exception as e:
            return {'error': f'Forecast error: {str(e)}'}
    
    def process_forecast(self, data):
        if data.get('cod') != '200':
            return {'error': data.get('message', 'Error fetching forecast')}
        
        forecast_list = []
        daily_forecasts = {}
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        count = 0
        for date in sorted(daily_forecasts.keys()):
            if count >= 5:
                break
            items = daily_forecasts[date]
            temps = [i['main']['temp'] for i in items]
            temps_min = [i['main']['temp_min'] for i in items]
            temps_max = [i['main']['temp_max'] for i in items]
            
            forecast_list.append({
                'date': date,
                'day': datetime.strptime(date, '%Y-%m-%d').strftime('%a'),
                'temp_avg': sum(temps) / len(temps),
                'temp_min': min(temps_min),
                'temp_max': max(temps_max),
                'description': items[0]['weather'][0]['description'].capitalize(),
                'icon': items[0]['weather'][0]['icon'],
                'humidity': items[0]['main']['humidity'],
                'wind_speed': items[0]['wind']['speed']
            })
            count += 1
        
        return {
            'city': data['city']['name'],
            'country': data['city']['country'],
            'forecast': forecast_list
        }

class WeatherIcons:
    ICONS = {
        '01d': '☀️', '01n': '🌙',
        '02d': '⛅', '02n': '☁️',
        '03d': '☁️', '03n': '☁️',
        '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️',
        '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️',
        '13d': '❄️', '13n': '❄️',
        '50d': '🌫️', '50n': '🌫️'
    }
    
    @staticmethod
    def get_icon(icon_code):
        return WeatherIcons.ICONS.get(icon_code, '🌤️')