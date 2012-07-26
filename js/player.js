/* player.js
*/
var Route_Player = function(route, map) {
    this.route = route;
    this.map = map
    this.current_frame = 0;

    // draw the first marker
    this.current_marker = this.map.addMarker({
        lat: this.route[0][0]
        , lng: this.route[0][1]
    });
};

Route_Player.prototype.play = function() {
    var self = this;
    this.timeout_id = window.setInterval( function() {
        self.animate_frame();
    }, 100);
};

Route_Player.prototype.pause = function() {
    window.clearTimeout(this.timeout_id);
};

Route_Player.prototype.stop = function() {
    window.clearTimeout(this.timeout_id);
    this.current_frame = 0;
}

Route_Player.prototype.animate_frame = function() {
    this.current_frame++;

    // update position
    this.current_marker.setPosition(
        new google.maps.LatLng(
            this.route[this.current_frame][0]
            , this.route[this.current_frame][1]
        )
    );
};
