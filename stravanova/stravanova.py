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
        self.parsed_data = None

    def parse(self, lat_lon_precision=5, time_binning=False):

        self.filenames = [os.path.basename(f).split('.')[0] 
                for f in self.file_paths]

        parsed_data = {}
        for filename in self.filenames:
            parsed_data[filename] = []

        return parsed_data
