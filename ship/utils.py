from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    # haversine formula
    d_lat = lat2 - lat1
    d_lng = lng2 - lng1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lng/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def get_orders_nearest(lat, lng, items):
    return [item for item in items
            if haversine(lat, lng,
                         item.from_address.latitude,
                         item.from_address.longitude) < 1]
