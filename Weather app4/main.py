"""
Advanced Weather App - GUI with current weather and forecasts
"""

import tkinter as tk
from tkinter import ttk, messagebox
from weather_core import WeatherCore, WeatherIcons
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weather App")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.weather_core = WeatherCore()
        self.recent_cities = []
        
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'text': '#ffffff',
            'accent': '#0f3460',
            'highlight': '#e94560'
        }
        
        self.setup_ui()
        self.load_saved_data()
    
    def setup_ui(self):
        self.root.configure(bg=self.colors['bg'])
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.setup_header(main_frame)
        self.setup_search(main_frame)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        self.current_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.forecast_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        
        self.notebook.add(self.current_tab, text="🌤️ Current")
        self.notebook.add(self.forecast_tab, text="📅 Forecast")
        
        self.setup_current_tab()
        self.setup_forecast_tab()
    
    def setup_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg'])
        header.pack(fill='x', pady=(0, 15))
        
        tk.Label(header, text="🌤️ Weather App", 
                font=('Arial', 24, 'bold'),
                fg=self.colors['text'], bg=self.colors['bg']).pack(side='left')
        
        self.time_label = tk.Label(header, text="", 
                                  font=('Arial', 12),
                                  fg='#aaaaaa', bg=self.colors['bg'])
        self.time_label.pack(side='right')
        self.update_time()
    
    def setup_search(self, parent):
        search_frame = tk.Frame(parent, bg=self.colors['bg'])
        search_frame.pack(fill='x', pady=(0, 15))
        
        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(search_frame, textvariable=self.city_var,
                                  font=('Arial', 14),
                                  bg=self.colors['card'],
                                  fg=self.colors['text'],
                                  insertbackground='white',
                                  relief='flat',
                                  width=30)
        self.city_entry.pack(side='left', padx=(0, 10))
        self.city_entry.bind('<Return>', lambda e: self.search_weather())
        
        tk.Button(search_frame, text="🔍 Search",
                 command=self.search_weather,
                 bg=self.colors['highlight'],
                 fg='white',
                 font=('Arial', 12, 'bold'),
                 relief='flat',
                 padx=20).pack(side='left')
        
        self.recent_var = tk.StringVar()
        self.recent_combo = ttk.Combobox(search_frame, textvariable=self.recent_var,
                                        font=('Arial', 12), width=20,
                                        state='readonly')
        self.recent_combo.pack(side='left', padx=(10, 0))
        self.recent_combo.bind('<<ComboboxSelected>>', 
                              lambda e: self.load_recent_city())
    
    def setup_current_tab(self):
        card = tk.Frame(self.current_tab, bg=self.colors['card'], relief='raised', bd=0)
        card.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.location_label = tk.Label(card, text="Search for a city",
                                      font=('Arial', 20, 'bold'),
                                      fg=self.colors['text'], bg=self.colors['card'])
        self.location_label.pack(pady=(20, 5))
        
        temp_frame = tk.Frame(card, bg=self.colors['card'])
        temp_frame.pack(pady=10)
        
        self.icon_label = tk.Label(temp_frame, text="🌤️",
                                  font=('Arial', 60),
                                  bg=self.colors['card'])
        self.icon_label.pack(side='left', padx=(0, 20))
        
        self.temp_label = tk.Label(temp_frame, text="--°C",
                                  font=('Arial', 48, 'bold'),
                                  fg=self.colors['text'], bg=self.colors['card'])
        self.temp_label.pack(side='left')
        
        self.desc_label = tk.Label(card, text="Enter a city to get started",
                                  font=('Arial', 16),
                                  fg='#aaaaaa', bg=self.colors['card'])
        self.desc_label.pack(pady=5)
        
        details_frame = tk.Frame(card, bg=self.colors['card'])
        details_frame.pack(pady=20, fill='x')
        
        details = [
            ('💧 Humidity', '--%'),
            ('🌬️ Wind', '-- m/s'),
            ('📊 Pressure', '-- hPa'),
            ('🤔 Feels Like', '--°C')
        ]
        
        self.detail_labels = {}
        for i, (label, value) in enumerate(details):
            frame = tk.Frame(details_frame, bg=self.colors['card'])
            frame.grid(row=i//2, column=i%2, padx=20, pady=10, sticky='nsew')
            
            tk.Label(frame, text=label, font=('Arial', 12),
                    fg='#aaaaaa', bg=self.colors['card']).pack()
            
            self.detail_labels[label] = tk.Label(frame, text=value,
                                                font=('Arial', 16, 'bold'),
                                                fg=self.colors['text'],
                                                bg=self.colors['card'])
            self.detail_labels[label].pack()
        
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)
    
    def setup_forecast_tab(self):
        self.forecast_container = tk.Frame(self.forecast_tab, bg=self.colors['bg'])
        self.forecast_container.pack(fill='both', expand=True)
        
        tk.Label(self.forecast_container, text="5-Day Forecast",
                font=('Arial', 18, 'bold'),
                fg=self.colors['text'], bg=self.colors['bg']).pack(pady=10)
        
        self.forecast_cards_frame = tk.Frame(self.forecast_container, bg=self.colors['bg'])
        self.forecast_cards_frame.pack(fill='both', expand=True)
    
    def search_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        self.update_weather(city)
    
    def load_recent_city(self):
        city = self.recent_var.get()
        if city:
            self.city_var.set(city)
            self.update_weather(city)
    
    def update_weather(self, city):
        # Show loading state
        self.location_label.config(text="Loading...")
        self.temp_label.config(text="--°C")
        self.root.update()
        
        # Get current weather
        current_data = self.weather_core.get_current_weather(city)
        
        if 'error' in current_data:
            messagebox.showerror("Error", f"Failed to get weather: {current_data['error']}")
            self.location_label.config(text="Search for a city")
            return
        
        if current_data.get('cod') != 200:
            error_msg = current_data.get('message', 'City not found')
            messagebox.showerror("Error", f"City not found: {error_msg}")
            self.location_label.config(text="Search for a city")
            return
        
        self.display_current_weather(current_data)
        
        # Get forecast
        forecast_data = self.weather_core.get_forecast(city)
        if 'error' not in forecast_data:
            self.display_forecast(forecast_data)
        else:
            messagebox.showwarning("Warning", f"Could not get forecast: {forecast_data['error']}")
        
        self.add_recent_city(city)
    
    def display_current_weather(self, data):
        try:
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            description = data['weather'][0]['description'].capitalize()
            icon = data['weather'][0]['icon']
            wind_speed = data['wind']['speed']
            
            self.location_label.config(text=f"{city}, {country}")
            self.icon_label.config(text=WeatherIcons.get_icon(icon))
            self.temp_label.config(text=f"{temp:.1f}°C")
            self.desc_label.config(text=description)
            
            self.detail_labels['💧 Humidity'].config(text=f"{humidity}%")
            self.detail_labels['🌬️ Wind'].config(text=f"{wind_speed} m/s")
            self.detail_labels['📊 Pressure'].config(text=f"{pressure} hPa")
            self.detail_labels['🤔 Feels Like'].config(text=f"{feels_like:.1f}°C")
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid data received: {str(e)}")
    
    def display_forecast(self, data):
        for widget in self.forecast_cards_frame.winfo_children():
            widget.destroy()
        
        if 'error' in data:
            tk.Label(self.forecast_cards_frame, text="Forecast data not available",
                    font=('Arial', 14), fg='#aaaaaa', bg=self.colors['bg']).pack(pady=20)
            return
        
        forecast_cards = tk.Frame(self.forecast_cards_frame, bg=self.colors['bg'])
        forecast_cards.pack(fill='both', expand=True)
        
        for i, day in enumerate(data['forecast']):
            card = tk.Frame(forecast_cards, bg=self.colors['card'], relief='raised', bd=0)
            card.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            forecast_cards.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=day['day'], 
                    font=('Arial', 14, 'bold'),
                    fg=self.colors['text'], bg=self.colors['card']).pack(pady=(10, 5))
            
            tk.Label(card, text=WeatherIcons.get_icon(day['icon']),
                    font=('Arial', 30),
                    bg=self.colors['card']).pack(pady=5)
            
            tk.Label(card, text=f"{day['temp_avg']:.1f}°C",
                    font=('Arial', 16, 'bold'),
                    fg=self.colors['text'], bg=self.colors['card']).pack()
            
            tk.Label(card, text=f"↑{day['temp_max']:.0f}° ↓{day['temp_min']:.0f}°",
                    font=('Arial', 10),
                    fg='#aaaaaa', bg=self.colors['card']).pack()
            
            tk.Label(card, text=day['description'],
                    font=('Arial', 10),
                    fg='#aaaaaa', bg=self.colors['card'],
                    wraplength=120).pack(pady=(5, 10))
    
    def add_recent_city(self, city):
        if city not in self.recent_cities:
            self.recent_cities.insert(0, city)
            if len(self.recent_cities) > 5:
                self.recent_cities.pop()
            self.update_recent_cities()
    
    def update_recent_cities(self):
        self.recent_combo['values'] = self.recent_cities
        if self.recent_cities:
            self.recent_combo.set(self.recent_cities[0])
    
    def load_saved_data(self):
        
        pass
    
    def update_time(self):
        self.time_label.config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.root.after(1000, self.update_time)

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()