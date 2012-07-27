/* player.js
*/

// collection of all instantiated players
// useful for play/pause operations
var route_players = []

var Route_Player = function(route, map) {
    this.route = route;
    this.map = map
    this.current_frame = 0;

    // draw the first marker
    this.current_marker = this.map.addMarker({
        lat: this.route[0][0]
        , lng: this.route[0][1]
    });

    // start a polyline of 0 length
    this.polyline = this.map.drawPolyline({
        path: [[this.route[0][0], this.route[0][1]]
            , [this.route[0][0], this.route[0][1]]]
        , strokeColor: '1c86ff'
        , strokeOpacity: 0.6
    });

    // save in the global list of route_players
    route_players.push(this);

};

Route_Player.prototype.play = function() {
    this.is_playing = true;

    var self = this;
    // should change to timeout
    this.timeout_id = window.setInterval( function() {
        self.animate_frame();
    }, 100);
};

Route_Player.prototype.play_pause = function() {
    if (!this.is_playing) {
        // was paused, play it
        this.play();
    } else {
        // was playing, pause it
        this.is_playing = false;
        window.clearTimeout(this.timeout_id);
    }
};

Route_Player.prototype.stop = function() {
    window.clearTimeout(this.timeout_id);
    this.current_frame = 0;
}

Route_Player.prototype.animate_frame = function() {
    this.current_frame++;

    var latest_position = new google.maps.LatLng(
        this.route[this.current_frame][0]
        , this.route[this.current_frame][1]
    )

    // update position of marker
    this.current_marker.setPosition(latest_position);

    // extend polyline trace
    var path = this.polyline.getPath();
    path.push(latest_position);

};

// shortcuts for play/pause
Mousetrap.bind(['p', 'space'], function() {
    for (var i in route_players) {
        route_players[i].play_pause();
    }
});

