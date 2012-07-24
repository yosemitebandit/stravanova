#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' stravanova
command line utility that takes GPX files and stores some of their attributes 
in a JSON format:

    $ ./stravanova.py --files mountains.gpx valleys.gpx --output rides.json
    $ ./stravanova.py --directory /secret/climb/routes/ --output climbs.json


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

import argparse
import json
import os

import gpxpy

parser = argparse.ArgumentParser(description='GPX -> JSON')
parser.add_argument('-f', '--files', dest='files', nargs='+', help=('paths to'
        ' your GPX files'))
parser.add_argument('-d', '--directory', dest='directory', help=('paths to'
        ' your GPX files'))
parser.add_argument('-o', '--output', dest='output', help=('path to save your'
        ' json file'), required=True)
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

routes = {}
for gpx_file in files:
    try:
        gpx = gpxpy.parse(open(gpx_file, 'r'))
    except TypeError:
        # not parseable as a gpx file
        continue

    filename = os.path.basename(gpx_file).split('.')[0]

    for track in gpx.tracks:
        for segment in track.segments:
            routes[filename] = [[round(p.latitude, 5), round(p.longitude, 5), 
                p.time.isoformat()] for p in segment.points]


output = open(arguments.output, 'w')
output.write(json.dumps(routes))
