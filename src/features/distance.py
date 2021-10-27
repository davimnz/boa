from math import sin, cos, sqrt, atan2, radians


def distance(latitude_1, longitude_1, latitude_2, longitude_2) -> float:
    """
    Evaluates the distance between two points on the Earth surface.
    """
    earth_radius = 6373.0  # unit : km

    latitude_1_rad = radians(latitude_1)
    longitude_1_rad = radians(longitude_1)
    latitude_2_rad = radians(latitude_2)
    longitude_2_rad = radians(longitude_2)

    distance_longitude = longitude_2_rad - longitude_1_rad
    distance_latitude = latitude_2_rad - latitude_1_rad

    a = sin(distance_latitude / 2)**2 + cos(latitude_1_rad) * \
        cos(latitude_2_rad) * sin(distance_longitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius*c
