from kerykeion import KrInstance, MakeSvgInstance
from pathlib import Path


def main():
    first = KrInstance("Maria", 1979, 11, 15, 5, 15,city='Donetsk', lng=48.023, lat=37.8022)
    second = KrInstance(city='Donetsk',lng=48.023, lat=37.8022, year=2023, month=2, day=14, hour=1, minute=24)

    # Set the type, it can be Natal, Composite or Transit
    name = MakeSvgInstance(first, chart_type="Composite", second_obj=second)
    name.makeSVG()
    print(len(name.aspects_list))


if __name__ == "__main__":
    main()