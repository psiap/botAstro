from kerykeion import CompositeAspects, KrInstance
first = KrInstance("Maria", 1979, 11, 15, 5, 15, lng=48.023, lat=37.8022)
second = KrInstance(lng=48.023, lat=37.8022, year=2023, month=2, day=14, hour=1, minute=24)

name = CompositeAspects(first, second)
aspect_list = name.get_relevant_aspects()
for planets_i in aspect_list:
    print(planets_i['p1_name'],planets_i['p2_name'],planets_i['aspect_degrees'])