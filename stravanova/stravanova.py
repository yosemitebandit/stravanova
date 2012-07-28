# -*- coding: utf-8 -*-
''' stravanova
taking GPX files and storing some of their attributes as JSON
the JSON format compresses the info at the expense of being non-standard:
[lat, lon, timestamp (epoch, UTC), speed (m/s)]

    routes = {
        'cow-watchin': [
            [123.456, 789.012, 1343461324, 4.523]
            , [123.467, 789.023, 1343461324, 2.160]
        ]
        , 'quadruple-century': [
            [345.456, 78.012, 1343464324, 4.523]
            , [345.467, 78.023, 1343463324, 2.160]
        ]
    }

'''
from math import radians, cos, sin, asin, sqrt, atan2, pi
import os
import time

import gpxpy
import numpy


class Condenser():
    ''' saving gpx files as json
    strips out all but latitude, longitude and time
    '''
    def __init__(self, gpx_paths, binning=False):
        self.file_paths = gpx_paths
        self.default_lat_lon_precision = 5
        self.default_time_binning = binning

    def parse(self, **kwargs):
        lat_lon_precision = kwargs.pop('lat_lon_precision', 
                self.default_lat_lon_precision)
        time_binning = kwargs.pop('time_binning',
                self.default_time_binning)

        self.filenames = [os.path.basename(f).split('.')[0] 
                for f in self.file_paths]

        point_data = {}
        for path in self.file_paths:
            gpx = gpxpy.parse(open(path, 'r'))

            filename = os.path.basename(path).split('.')[0]

            # extract the points
            for track in gpx.tracks:
                for segment in track.segments:
                    point_data[filename] = [p for p in segment.points]

        parsed_data = {}
        for filename in point_data:
            path = []
            for p in point_data[filename]:
                lat = p.latitude
                lon = p.longitude
                timestamp = time.mktime(p.time.timetuple())

                # calculate speeds
                if not path:
                    # append the first point
                    path.append([round(lat, lat_lon_precision),
                        round(lon, lat_lon_precision),
                        timestamp,
                        None])
                    continue
                # grab the previous point
                previous = path[-1]
                speed = self._speed(previous, [lat, lon, timestamp])
                if not speed:
                    continue

                # inject the calculated speed
                path.append([round(lat, lat_lon_precision),
                    round(lon, lat_lon_precision),
                    timestamp,
                    speed])

            if time_binning:
                # create a point for every N seconds
                N = 4
                # initialize the path with the first point
                binned_path = [[path[0][0], path[0][1]]]
                # array of all timestamps
                timestamps = [p[2] for p in path]

                # start the clock with the first timestamp
                tick = timestamps[0]
                while tick <= timestamps[-1]:
                    tick += N
                    index = numpy.searchsorted(timestamps, tick)

                    if index >= len(path):
                        break

                    # get previous and next points around this tick value
                    pp = path[index - 1]
                    np = path[index]

                    # find the bearing and distance
                    bearing = self._bearing([pp[0], pp[1]], [np[0], np[1]])
                    speed = self._speed(pp, np)
                    distance = speed * float(N)

                    # generate a point based on the average bearing and speed
                    # 'origin' set to the previously calculated point
                    # traveling N seconds from that point
                    binned_path.append(self.destination_point(
                        [binned_path[-1][0], binned_path[-1][1]], bearing,
                        distance))

                # strip all but lat/lon info
                parsed_data[filename] = [[p[0], p[1]] for p in binned_path]

            else:
                # not time-binning
                parsed_data[filename] = [[p[0], p[1]] for p in path]

        return parsed_data

    def _speed(self, a, b):
        ''' calculates speed between two points
        '''
        # find the distance
        distance = self._haversine_distance([a[0], a[1]], [b[0], b[1]])
        # calculate the time difference
        time_delta = b[2] - a[2]
        if time_delta <= 1:
            # haven't moved
            return None
        return round(float(distance) / time_delta, 2)
    
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

