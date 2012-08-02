/* player.js
*/

// collection of all instantiated players
// useful for play/pause operations
var route_players = []
var playback_speed = 16;

var Route_Player = function(route, map, color) {
    this.route = route;
    this.map = map;
    this.color = color;
    this.current_frame = 0;
    this.total_frames = route.length;
    this.playback_speed = playback_speed;

    // draw the first marker
    this.current_marker = this.map.addMarker({
        lat: this.route[0][0]
        , lng: this.route[0][1]
    });

    // start a polyline of 0 length
    this.polyline = this.map.drawPolyline({
        path: [[this.route[0][0], this.route[0][1]]
            , [this.route[0][0], this.route[0][1]]]
        , strokeColor: this.color
        , strokeOpacity: 0.6
    });

    // save in the global list of route_players
    route_players.push(this);

};

Route_Player.prototype.play = function() {
    this.is_playing = true;

    // reset the path if player was stopped at the last frame
    if (this.is_finished) {
        this.polyline.setMap(null);

        this.polyline = this.map.drawPolyline({
            path: [[this.route[0][0], this.route[0][1]]
                , [this.route[0][0], this.route[0][1]]]
            , strokeColor: this.color
            , strokeOpacity: 0.6
        });

        this.is_finished = false;
    }

    this.animate_frame();
};

Route_Player.prototype.animate_frame = function() {
    var self = this;

    this.timeout_id = window.setTimeout( function() {
        self.current_frame++;

        // check if we're at the end of the reel, as it were
        if (self.current_frame >= self.total_frames) {
            self.stop();

        } else {
            var latest_position = new google.maps.LatLng(
                self.route[self.current_frame][0]
                , self.route[self.current_frame][1]
            )

            // update position of marker
            self.current_marker.setPosition(latest_position);

            // extend polyline trace
            var path = self.polyline.getPath();
            path.push(latest_position);

            self.animate_frame();
        }

    }, Math.round(1000/this.playback_speed));
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
    this.is_finished = true;
};

Route_Player.prototype.set_path_color = function(color) {
    this.polyline.setOptions({strokeColor: color});
    console.log(color);
};
