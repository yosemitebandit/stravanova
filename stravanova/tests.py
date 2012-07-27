#! /usr/bin/env python
# -*- coding: utf-8 -*-
import decimal
import os
import unittest

import gpxpy
import stravanova

class ParsingTest(unittest.TestCase):
    def setUp(self):
        self.gpx_paths = ['fixtures/richmond-jaunt.gpx',
                'fixtures/caltrain-expedition.gpx']
        self.c = stravanova.Condenser(self.gpx_paths)

    def tearDown(self):
        pass

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

    def test_default_latlon_precision(self):
        result = self.c.parse()
        for route in result:
            for point in result[route]:
                for number in point:
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
