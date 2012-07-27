#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
                    gpxpy_result[filename] = [[p.latitude, p.longitude] 
                            for p in segment.points]

        assert result == gpxpy_result
