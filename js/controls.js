$(function() {

    // shortcuts for play/pause
    Mousetrap.bind(['p', 'space'], function() {
        for (var i in route_players) {
            route_players[i].play_pause();
        }
    });

    // shortcuts for showing/hiding the help overlay
    Mousetrap.bind('h', function() {
        fade_toggle_help_overlay();
    });

});
