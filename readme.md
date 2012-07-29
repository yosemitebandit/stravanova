There are two pieces to this puzzle:
a Python module that parses `.gpx` files into a `JSON` format
and a javascript "route player" that plays back the `JSON` data.

### coordinate parsing and interpolation
`stravanova.py` contains a `Condenser` class that reduces `.gpx` files to lat/lon pairs.
These pairs get dumped in a list; the list is identified by the `.gpx` filename.  E.g.

    'cow-watching': [
        [123.456, 78.910]
        , [123.567, 78.101]
    ]

The js route player can handle this just fine, but the route player is kind of dumb.
It just blithely steps through these coordinates and animates the markers.
It does not really have any sense of *when* these coordinates are relevant.
The player's blind march assumes that each point was recorded N seconds apart.
In the raw `.gpx` file, this is obviously not necessarily the case.
Strava will try to record coordinates every four seconds but it might fail for lack of GPS reception or something else.

So the `stravanova` module has a way to "bin" these coordinates.
Essentially it's a way to interpolate points and create a dataset that *does* have measurements spaced exactly N seconds apart.
(Currently N is fixed at 1 because other larger values caused peculiar offsets -- maybe this will be parameterized one day.)
How does it do this binning?
It linearly interpolates coordinates by using the bearing and average speed between two known measurements.
So if we want to know where we were on the path between two points one second after leaving the origin point
we can first take that one second and multiply it by the speed.
This gives a circle from the origin -- our interpolated point lies somewhere on that circle.
If we know the bearing (an angle) we can find the exact point.

These calculations are made using formulae from [this excellent site](http://www.movable-type.co.uk/scripts/latlong.html).
Distances between coordinates are often quite small in these files
so non-spherical calculations would probably be more than sufficient.
But the "Great-Circle" calculations used in the module hold to about
[half a meter](http://www.movable-type.co.uk/scripts/latlong.html) and the results seem good enough.


### coordinate playback
The js player just merrily steps through the lat/lon pairs and updates the markers and traces.
It does not have any notion of when the coordinates were recorded.
So to get traces that are accurate relative to one another we need the measurements to each be exactly N seconds apart.
The parser above can create datasets like this.
(This ignores things like js timer accuracy which isn't stupendous, I think.
Not to mention that each route player has its own timer so there's no synching.)


### the site
`master` has a template `map.html` file and all of the associated js.
`gh-pages` has the info for http://yosemitebandit.github.com/stravanova -- each map is built from that template.
Each map's js is hotlinked to master.


### testing the parser

    (venv) $ cd stravanova
    (venv) $ nosetests


### idears
* repeat for a set of riders that share an origin
    - or select riders with a common destination
    - or select riders with a common (ships passing in the night)
    - normalize their start times
* anthropomorphize the markers
    - 'oof' when they're headed up hills
