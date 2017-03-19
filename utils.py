#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import radians, cos, sin, asin, sqrt

def distance((lat1, lng1), lat2, lng2):
    return (lat2 - lat1)**2 + (lng2 - lng1)**2


def haversine((lat1, lng1), lat2, lng2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # haversine formula 
    dlon = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
