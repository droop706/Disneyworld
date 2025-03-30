
#--------- HARDCODED VALUES ---------
DISNEY_WORLD_coords = {
    'latitude': 28.4237,
    'longitude': -81.5812
}
HTTP_RESPONSE_SUCCESS = 200
US_NY_tz = 'America/New_York'
HISTORICAL_START_DATE = "2015-01-01"
HISTORICAL_END_DATE = "2021-12-28"


#--------- COMMON PARAMETERS ---------
COMMON_PARAMETERS = {
    'daily': (
        'precipitation_sum,'
        'sunshine_duration,'
        'temperature_2m_max,'
        'temperature_2m_min,'
        'uv_index_max,'
        'weather_code,'
        'wind_speed_10m_max,'
    ),
    'latitude': DISNEY_WORLD_coords['latitude'],
    'longitude': DISNEY_WORLD_coords['longitude'],
    'timezone': US_NY_tz
}

#--------- HISTORICAL SPECIFIC PARAMETERS---------
HISTORICAL_PARAMETERS = {
    "start_date": HISTORICAL_START_DATE,
    "end_date": HISTORICAL_END_DATE
}
