#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' parse
command line utility that takes GPX files and stores some of their attributes 
in a JSON format:

    (venv) $ ./parse.py --files mountains.gpx valleys.gpx --output rides.json
    (venv) $ ./parse.py --directory /secret/climb/routes/ --output climbs.json
    (venv) $ ./parse.py -d ~/climbs/ -o climbs.json --binning
    (venv) $ ./parse.py -d ~/climbs/ -o climbs.json --precision 7


the JSON format compresses the info at the expense of being non-standard:

    routes = {
        'cow-watchin': [
            [123.456, 789.012]
            , [123.467, 789.023]
        ]
        , 'quadruple-century': [
            [345.456, 78.012]
            , [345.467, 78.023]
        ]
    }

'''
import argparse
import json
import os

from stravanova import stravanova

parser = argparse.ArgumentParser(description='GPX -> JSON')
parser.add_argument('-f', '--files', dest='files', nargs='+', help=('paths to'
        ' your GPX files'))
parser.add_argument('-d', '--directory', dest='directory', help=('paths to'
        ' your GPX files'))
parser.add_argument('-o', '--output', dest='output', help=('path to save your'
        ' json file'), required=True)
parser.add_argument('-p', '--precision', type=int, default=5, dest='precision',
        help=('truncate lat/lon values to N decimal places'))
parser.add_argument('-b', '--binning', action='store_true', default=False,
        dest='binning', help=('create point for every second'))
arguments = parser.parse_args()

# see what we've got
if not arguments.files and not arguments.directory:
    parser.error('specify a set of files or a directory with -f or -d')
if arguments.files and arguments.directory:
    parser.error('specify only files or a directory, not both')

# pull out the actual files
if arguments.files:
    files = [f for f in arguments.files if not os.path.isdir(f)]
elif arguments.directory:
    # not walking into sub-directories for now
    if os.path.isdir(arguments.directory):
        files = [os.path.join(arguments.directory, f) 
                for f in os.listdir(arguments.directory) 
                if not os.path.isdir(f)]
    else:
        parser.error('the dir you specified is not actually a directory..')

c = stravanova.Condenser(files)
data = c.parse(binning=arguments.binning,
        lat_lon_precision=arguments.precision)

output = open(arguments.output, 'w')
output.write(json.dumps(data))
