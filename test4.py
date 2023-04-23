import time
from kerykeion import CompositeAspects, KrInstance

def get_moon_in_days():
    first = KrInstance("Михаил", 1985, 7, 5, 12, 0, lng=55.086036, lat=30.301586)
    all_moon_array = []
    target_values = [0, 60, 120, 90, 180]

    for i in range(0,24):
        second = KrInstance(lng=55.357977, lat=27.528732, year=2023, month=4, day=14,hour=i)

        name = CompositeAspects(first, second)

        numbers = []
        aspect_list = name.get_relevant_aspects()
        for planets_i in aspect_list:
            if 'Moon' in planets_i['p2_name']:
                numbers.append([planets_i['p2_name'],planets_i['p1_name'],planets_i['diff'],i, planets_i['aspect_degrees']])
        closest_number = min(numbers, key=lambda x: min(abs(x[2] - target) for target in target_values))

        try:
            if all_moon_array[-1][1] == closest_number[1]:
                continue
        except:
            pass
        all_moon_array.append(closest_number)
    return all_moon_array

def get_all_planet_in_days():
    first = KrInstance("Михаил", 1985, 7, 5, 12, 0, lng=55.086036, lat=30.301586)
    target_values = [0, 60, 120, 90, 180]
    second = KrInstance(lng=55.357977, lat=27.528732, year=2023, month=4, day=14)
    name = CompositeAspects(first, second)
    aspect_list = name.get_relevant_aspects()
    numbers = []
    for planets_i in aspect_list:
        if 'Moon' != planets_i['p2_name'] and planets_i['p2_name'] in ['Sun','Mercury', 'Venus','Mars']:
            for n in target_values:
                #print(f"{planets_i['diff']} < {n + 2} | {planets_i['diff']} > {n - 2} ")
                if planets_i['diff'] < n + 2 and planets_i['diff'] > n - 2:
                    numbers.append(
                        [planets_i['p2_name'], planets_i['p1_name'], planets_i['diff'], planets_i['aspect_degrees']])

                    break



    #closest_number = min(numbers, key=lambda x: min(abs(x[2] - target) for target in target_values))
    #print(closest_number)
    return numbers

all_moon_array = get_moon_in_days()
all_planet_array = get_all_planet_in_days()
print(all_moon_array)
print(all_planet_array)

