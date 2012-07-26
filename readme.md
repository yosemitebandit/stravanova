### ie

1. take gpx data from Strava riders
    - anonymize it
2. animate their path on a map
3. repeat for a set of riders that share an origin
    - or select riders with a common destination
    - or select riders with a common (ships passing in the night)
    - normalize their start times
4. anthropomorphize the markers
    - 'oof' when they're headed up hills

### consisting of

1. GPX -> JSON parser
    - API like `$ ./stravanova.py alpine-dam.gpx mt-tam.gpx mt-ham.gpx fun-rides.json`
    - or `$ ./stravanova.py local-climbs-dir/ local-climbs.json`
    - maybe [geojson](http://www.geojson.org/geojson-spec.html)..
    - bin times so that each route has a point every N seconds
        - that way the js player will play things at the correct speed
2. js lib for animating markers along a route
3. custom js for connecting the json and the animator class
4. play/pause/speedup??

### eg

[Econym](http://econym.org.uk/gmap/example_cartrip.htm)

[Flushtracker](http://www.flushtracker.com/) (hah)

[js+GPX](https://github.com/tkafka/Javascript-GPX-track-viewer)
