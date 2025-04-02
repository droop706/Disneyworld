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

        print(f"begin_dag: Type = {type(self.begin_dag)}, Value = {self.begin_dag}")
        print(f"eind_dag: Type = {type(self.eind_dag)}, Value = {self.eind_dag}")
        print(f"dagtype: Type = {type(self.dagtype)}, Value = {self.dagtype}")
        print(f"voorkeurweer: Type = {type(self.voorkeurweer)}, Value = {self.voorkeurweer}")
        print(f"attracties: Type = {type(self.attractions)}, Value = {self.attractions}")
        print(f"ML_model: Type = {type(self.ML_model)}, Value = {self.ML_model}")

    def plan(self):
        attraction_times = {}
        print(self.filter_dagen())
        print(type(self.filter_dagen()[0]))
        print(get_weather_forecast())
        print(apply_intensity_on_dates(self.filter_dagen()))
        random_day = random.choice(self.filter_dagen())
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

    def score_day(self):
        pass
