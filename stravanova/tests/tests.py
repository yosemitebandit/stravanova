#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import gpxpy
import stravanova

class ParsingTest(unittest.TestCase):
    def setUp(self):
        gpx_paths = ['fixtures/richmond-jaunt.gpx', 'caltrain-expedition.gpx']
        self.c = stravanova.Condenser(gpx_paths)

    def tearDown(self):
        pass

    def test_parsing_result_type(self):
        result = self.c.parse()
        assert type(result) is dict

    def test_parsing_result_keys(self):
        result = self.c.parse()
        assert (set(['richmond-jaunt', 'caltrain-expedition']) == 
                set(result.keys()))
