#! /usr/bin/env python
# -*- coding: utf-8 -*-
''' testing parsing
metadata capture
lat/lon precision limits
time binning
point limitation
'''

import decimal
import os
import unittest

import gpxpy
import stravanova

class ParsingTest(unittest.TestCase):
    ''' basic parsing of GPX files into one JSON file
    '''
    def setUp(self):
        self.gpx_paths = ['fixtures/richmond-jaunt.gpx',
                'fixtures/caltrain-expedition.gpx']
        self.c = stravanova.Condenser(self.gpx_paths)

    def test_parsing_result_type(self):
        result = self.c.parse()
        assert type(result) is dict

    def test_parsing_result_keys(self):
        result = self.c.parse()
        assert (set(['richmond-jaunt', 'caltrain-expedition']) == 
                set(result.keys()))

    def test_basic_parsing_result(self):
        result = self.c.parse()

        # use gpxpy to calculate the result
        gpxpy_result = {}
        for path in self.gpx_paths:
            gpx = gpxpy.parse(open(path, 'r'))

            filename = os.path.basename(path).split('.')[0]

            for track in gpx.tracks:
                for segment in track.segments:
                    gpxpy_result[filename] = [
                        [round(p.latitude, self.c.default_lat_lon_precision), 
                        round(p.longitude, self.c.default_lat_lon_precision)] 
                        for p in segment.points]

        assert result == gpxpy_result


class LatLonPrecisionTest(unittest.TestCase):
    ''' limit the number of decimal places stored for each point
    '''
    def setUp(self):
        self.gpx_paths = ['fixtures/richmond-jaunt.gpx',
                'fixtures/caltrain-expedition.gpx']
        self.c = stravanova.Condenser(self.gpx_paths)

    def test_default_latlon_precision(self):
        result = self.c.parse()
        for route in result:
            for point in result[route]:
                for number in point:
                    ''' this is a trick to get the number of places
                    after the decimal point
                    '''
                    d = decimal.Decimal(str(number))
                    assert (abs(d.as_tuple().exponent) 
                            <= self.c.default_lat_lon_precision)

    def test_specified_latlon_precision(self):
        precision_limit = 6 
        result = self.c.parse(lat_lon_precision=precision_limit)
        for route in result:
            for point in result[route]:
                for number in point:
                    d = decimal.Decimal(str(number))
                    assert abs(d.as_tuple().exponent) <= precision_limit


class TimeBinningTest(unittest.TestCase):
    ''' bin the data such that recordings occur every N seconds
    interpolate when neccessary to create that point
    '''
    def setUp(self):
        self.gpx_paths = ['fixtures/richmond-jaunt.gpx',
                'fixtures/caltrain-expedition.gpx']
        self.c = stravanova.Condenser(self.gpx_paths)

    def test_bearing_calculation(self):
        ''' bearing in degrees from two points
        'true' values from: http://www.movable-type.co.uk/scripts/latlong.html
        multiple asserts is kinda silly for one test, alas
        '''
        p1 = [11.11, -77.77]
        p2 = [22.22, 33.33]
        p3 = [-22.22, 33.33]
        p4 = [-11.11, -77.77]
        assert 63.2520 == round(self.c._bearing(p1, p2), 3)
        assert 109.560 == round(self.c._bearing(p1, p3), 3)
        assert 180.000 == round(self.c._bearing(p1, p4), 3)
        assert 180.000 == round(self.c._bearing(p2, p3), 3)
        assert 267.199 == round(self.c._bearing(p2, p4), 3)
        assert 251.182 == round(self.c._bearing(p3, p4), 3)

    def test_haversine_distance_calculation(self):
        ''' calculates great circle distance
        'true' values from: http://www.movable-type.co.uk/scripts/latlong.html
        should maybe consider law of cosines for small distances:
        http://gis.stackexchange.com/questions/4906
        '''
        p1 = [11.11, -77.77]
        p2 = [22.22, 33.33]
        p3 = [37.820726071974306, -122.47897624969482]
        p4 = [37.82064132128241, -122.47896552085876]
        assert 11644680 == round(self.c._haversine_distance(p1, p2), -1)
        assert 9.47 == round(self.c._haversine_distance(p3, p4), 2)
