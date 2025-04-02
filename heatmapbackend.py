import matplotlib.pyplot as plt
import numpy as np
import calendar
import requests

# Fetch weather data
def get_weather_forecast():
    url = 'https://api.open-meteo.com/v1/forecast'
    parameters = {
        'latitude': 28.4237,
        'longitude': -81.5812,
        'daily': ('precipitation_sum,'
                  'temperature_2m_max,'
                  'temperature_2m_min,'
                  'sunshine_duration'),
        'timezone': 'America/New_York',
        'forecast_days': 16
    }
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching weather forecast")
        return None

# Calculate intensity score based on weather features
def calculate_intensity(day_data):
    # Normalize each feature to a scale of 0-1
    temp_max = day_data['temperature_2m_max'] / 50  # Assuming max temperature is 50°C
    sunshine = day_data['sunshine_duration'] / 1440  # Max sunshine duration (minutes/day)
    precipitation = 1 - (day_data['precipitation_sum'] / 50)  # Assuming max precipitation is 50mm

    # Weighted scoring (adjust weights as needed)
    return (temp_max * 0.4) + (sunshine * 0.5) + (precipitation * 0.1)

# Weather forecast data
def generate_monthly_data(year, month, weather_data):
    num_days = calendar.monthrange(year, month)[1]
    intensity_values = np.zeros(num_days)

    for day_idx in range(1, num_days + 1):
        try:
            day_data = {
                'temperature_2m_max': weather_data['temperature_2m_max'][day_idx - 1],
                'sunshine_duration': weather_data['sunshine_duration'][day_idx - 1],
                'precipitation_sum': weather_data['precipitation_sum'][day_idx - 1]
            }
            intensity_values[day_idx - 1] = calculate_intensity(day_data)
        except IndexError:
            # Handle missing data for certain days
            intensity_values[day_idx - 1] = 0
    return intensity_values

# Visualize heatmap
def create_calendar_heatmap(year, month, data, cmap='plasma'):
    num_days = calendar.monthrange(year, month)[1]
    weeks, days = calendar.monthcalendar(year, month), 7
    heatmap_data = np.zeros((len(weeks), days))

    for week_idx, week in enumerate(weeks):
        for day_idx, day in enumerate(week):
            if day != 0:  # Ignore zeros as they denote days from adjacent months
                heatmap_data[week_idx, day_idx] = data[day - 1]

    fig, ax = plt.subplots()

    im = ax.imshow(heatmap_data, cmap=cmap)

    ax.set_xticks(np.arange(days))
    ax.set_yticks(np.arange(len(weeks)))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.set_yticklabels([f'Week {i+1}' for i in range(len(weeks))])

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    ax.set_title(f"Heatmap of {calendar.month_name[month]} {year}")
    fig.tight_layout()

    cbar = plt.colorbar(im)
    cbar.set_label('Intensity')

    plt.show()

# Update heatmap dynamically based on year, month, and weather data
def update_heatmap(year, month):
    weather_forecast_data = get_weather_forecast()
    if weather_forecast_data:
        weather_data = weather_forecast_data['daily']
        data = generate_monthly_data(year, month, weather_data)
        create_calendar_heatmap(year, month, data)
