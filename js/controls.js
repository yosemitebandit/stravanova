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

    // speed controls
    Mousetrap.bind('f', function() {
        playback_speed = playback_speed * 2;
        if (playback_speed >= 256) {
            playback_speed = 256;
        }
        $('.playback-speed').html(playback_speed);

        for (var i in route_players) {
            route_players[i].playback_speed = playback_speed
        }

    });

    Mousetrap.bind('s', function() {
        playback_speed = playback_speed / 2;
        if (playback_speed <= 1) {
            playback_speed = 1;
        }
        $('.playback-speed').html(playback_speed);

        for (var i in route_players) {
            route_players[i].playback_speed = playback_speed
        }
    });

    // init the playback speed display
    $('.playback-speed').html(playback_speed);

});
