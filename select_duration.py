__author__ = 'Jesse Moy'

import random
from datetime import date

input_dir = 'E:/FIRE_MODELING/fire_model_python/_m_test/inputs/farsite'

# Rain in mm needed to extinguish a fire
extinguish_threshold = 100

# Number of days used to condition fuel before the start of fire
conditioning_length = 15


def select_duration(year):
    # Define Window for ignition start date
    fire_season_start = date(day=1, month=3, year=year).toordinal()
    fire_season_end = date(day=31, month=5, year=year).toordinal()

    # Weather lines holds the climate records for a given year
    weather_lines = []

    # Select a start date without rain
    def get_clear_day():

        rain = True
        while rain is True:
            random_date = date.fromordinal(random.randint(fire_season_start, fire_season_end))
            for i in weather_lines[1:]:
                if int(i[0]) == random_date.month and int(i[1]) == random_date.day:
                    if int(i[2]) == 0:
                        rain = False

        return random_date
    with open(input_dir + '/weather.wtr') as weather:
        for line in weather:
            record = line.split()
            weather_lines.append(record)
        start_date = get_clear_day()

    # Calculate conditioning date
    conditioning_date = date.fromordinal(start_date.toordinal() - conditioning_length)

    con_month = conditioning_date.month
    con_day = conditioning_date.day
    start_month = start_date.month
    start_day = start_date.day
    end_month = 0
    end_day = 0

    # Find the next day with sufficient rain to end the fire
    for i in weather_lines[1:]:
        if int(i[0]) == start_month and int(i[1]) == start_day:
            start_index = weather_lines.index(i)
            for e in weather_lines[start_index:]:
                if int(e[2]) > extinguish_threshold:
                    end_month = int(e[0])
                    end_day = int(e[1])
                    break

    return con_month, con_day, start_month, start_day, end_month, end_day

