import math

def floor_to_nearest(offset: float, value: float, step: int) -> int:
    return range(int(offset), math.floor(value), step)[-1]


def limit_degrees(degrees):
    while degrees >= 360:
        degrees -= 360
    while degrees <= 0:
        degrees += 360
    return degrees