import random
from datetime import datetime, timedelta
from heatmapbackend import *

class OptimalDayFinder:
    def __init__(self, begin_dag, eind_dag, dagtype, voorkeurweer, attracties, ML_model):
        self.begin_dag = datetime.strptime(begin_dag, '%Y-%m-%d')
        self.eind_dag = datetime.strptime(eind_dag, '%Y-%m-%d')
        self.dagtype = dagtype
        self.voorkeurweer = voorkeurweer
        self.attractions = attracties
        self.ML_model = ML_model
        self.gefilterde_dage = self.filter_dagen()
        self.dage_gescored_weer = self.score_weer()

        print(f"begin_dag: Type = {type(self.begin_dag)}, Value = {self.begin_dag}")
        print(f"eind_dag: Type = {type(self.eind_dag)}, Value = {self.eind_dag}")
        print(f"dagtype: Type = {type(self.dagtype)}, Value = {self.dagtype}")
        print(f"voorkeurweer: Type = {type(self.voorkeurweer)}, Value = {self.voorkeurweer}")
        print(f"attracties: Type = {type(self.attractions)}, Value = {self.attractions}")
        print(f"ML_model: Type = {type(self.ML_model)}, Value = {self.ML_model}")
        print(self.dage_gescored_weer)

    def plan(self):
        attraction_times = {}
        random_day = random.choice(self.gefilterde_dage)
        self.score_weer()
        for attraction in self.attractions:
            random_hour = random.randint(9, 17)
            attraction_times[attraction] = f"{random_hour}:00"
        return self.attractions, attraction_times, random_day.strftime('%Y-%m-%d')

    def filter_dagen(self):
        filtered_days = []
        current_day = self.begin_dag
        while current_day <= self.eind_dag:
            if self.dagtype == 'Geen voorkeur':
                filtered_days.append(current_day)
            elif self.dagtype == 'Weekdag' and current_day.weekday() < 5:
                filtered_days.append(current_day)
            elif self.dagtype == 'Weekend' and current_day.weekday() >= 5:
                filtered_days.append(current_day)
            current_day += timedelta(days=1)
        return filtered_days

    def score_weer(self):
        weather_data = get_weather_forecast()
        forecasted_filtered_days = []
        for date in self.gefilterde_dage:
            date = date.date()
            for i, day in enumerate(weather_data['daily']['time']):
                day = datetime.strptime(day, "%Y-%m-%d").date()
                if day == date:
                    day_data = {
                        'date': date,
                        'temperature_2m_max': weather_data['daily']['temperature_2m_max'][i],
                        'sunshine_duration': weather_data['daily']['sunshine_duration'][i],
                        'precipitation_sum': weather_data['daily']['precipitation_sum'][i]
                    }
                    forecasted_filtered_days.append(day_data)
        max_temp = max(
            day['temperature_2m_max'] for day in forecasted_filtered_days if day['temperature_2m_max'] is not None)
        max_sunshine = max(
            day['sunshine_duration'] for day in forecasted_filtered_days if day['sunshine_duration'] is not None)
        max_precipitation = max(
            day['precipitation_sum'] for day in forecasted_filtered_days if day['precipitation_sum'] is not None)
        weather_scored_days = []
        for day_data in forecasted_filtered_days:
            temp_max = day_data['temperature_2m_max'] / max_temp
            sunshine = day_data['sunshine_duration'] / max_sunshine if day_data['sunshine_duration'] is not None else 0
            if max_precipitation != 0:
                precipitation = 1 - (day_data['precipitation_sum'] / max_precipitation) if day_data[
                                    'precipitation_sum'] is not None else 1
            else:
                precipitation = 1
            score = (temp_max * 0.4) + (sunshine * 0.5) + (precipitation * 0.1)
            weather_scored_days.append({'date': day_data['date'], 'score': score})
        return weather_scored_days

    def score_day(self):
        pass
