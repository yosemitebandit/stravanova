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
