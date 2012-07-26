var map;

$(function() {
    map = new GMaps({
        div: '#map'
        , lat: 37.90625
        , lng: -122.45464
        , zoom: 11
    });

    $.getJSON('ride-files/test-rides.json', function(data) {
        _.map(data, function(route) {

            var player = new Route_Player(route, map);
            player.play();

        });
    });

});
