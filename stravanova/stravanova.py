# -*- coding: utf-8 -*-
''' stravanova
taking GPX files and storing some of their attributes as JSON
the JSON format compresses the info at the expense of being non-standard:

    routes = {
        'cow-watchin': [
            [123.456, 789.012, '2012-05-28T03:36:04']
            , [123.467, 789.023, '2012-05-28T03:36:09']
        ]
        , 'quadruple-century': [
            [345.456, 78.012, '2112-05-28T03:36:04']
            , [345.467, 78.023, '2112-05-28T03:36:09']
        ]
    }

'''
import json
from math import radians, cos, sin, asin, sqrt, atan2, pi
import os

import gpxpy


class Condenser():
    ''' saving gpx files as json
    strips out all but latitude, longitude and time
    '''
    def __init__(self, gpx_paths):
        self.file_paths = gpx_paths
        self.default_lat_lon_precision = 5
        self.default_time_binning = False

    def parse(self, **kwargs):
        lat_lon_precision = kwargs.pop('lat_lon_precision', 
                self.default_lat_lon_precision)
        time_binning = kwargs.pop('time_binning',
                self.default_time_binning)

        self.filenames = [os.path.basename(f).split('.')[0] 
                for f in self.file_paths]

        parsed_data = {}
        for path in self.file_paths:
            gpx = gpxpy.parse(open(path, 'r'))

            filename = os.path.basename(path).split('.')[0]

            for track in gpx.tracks:
                for segment in track.segments:
                    parsed_data[filename] = [
                        [round(p.latitude, lat_lon_precision), 
                        round(p.longitude, lat_lon_precision)] 
                        for p in segment.points]

        return parsed_data

    def _bearing(self, point_a, point_b):
        ''' calculate bearing between two points
        points are packed (lat, lon)
        via http://www.movable-type.co.uk/scripts/latlong.html
        '''
        point_a = map(radians, point_a)
        point_b = map(radians, point_b)
        y = sin(point_b[1] - point_a[1]) * cos(point_b[0])
        x = (cos(point_a[0]) * sin(point_b[0]) - sin(point_a[0]) *
                cos(point_b[0]) * cos(point_b[1] - point_a[1]))
        bearing = atan2(y, x) * 180 / pi
        # normalize to a compass bearing
        return (bearing + 360) % 360

    def _haversine_distance(self, point_a, point_b):
        ''' Haversine implementation to calcalculate the great circle distance
        between two coordinates (lat, lon)
        where lat and lon are in decimal degrees
        return distance in km
        via http://stackoverflow.com/questions/4913349
        should maybe consider law of cosines for small distances:
        http://gis.stackexchange.com/questions/4906
        '''
        R = 6371  # earth radius in km
        # unpack
        lat_a, lon_a = point_a
        lat_b, lon_b = point_b

        # convert decimal degrees to radians
        lat_a, lon_a, lat_b, lon_b = map(radians, [lat_a, lon_a, lat_b, lon_b])

        # haversine formula
        lat_delta = lat_b - lat_a
        lon_delta = lon_b - lon_a
        a = sin(lat_delta/2)**2 + cos(lat_a) * cos(lat_b) * sin(lon_delta/2)**2

        # return meters
        return 1000 * R * 2 * asin(sqrt(a))

    def destination_point(self, origin, bearing, distance):
        '''
        origin is [lat, lon] in decimal degrees
        bearing in degrees
        distance given in meters
        returns point that's a distance from an origin point at a bearing
        '''
        # convert
        distance = distance/1000.
        bearing = radians(bearing)
        origin = map(radians, origin)
        R = 6371  # earth radius in km

        # calculate
        lat_dest = (asin(sin(origin[0])*cos(distance/R)
            + cos(origin[0])*sin(distance/R)*cos(bearing)))
        lon_dest = (origin[1]
                + atan2(sin(bearing) * sin(distance/R) * cos(origin[0]),
                cos(distance/R) - sin(origin[0]) * sin(lat_dest)))

        # convert back to decimal degrees
        return [180/pi * lat_dest, 180/pi * lon_dest]

