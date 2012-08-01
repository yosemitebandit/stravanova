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
        if (playback_speed >= 128) {
            playback_speed = 128;
        }
        $('.playback-speed').html(playback_speed);

        for (var i in route_players) {
            route_players[i].playback_speed = playback_speed
        }

    });

    // speed controls
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

    // add the top-right button
    map.addControl({
        position: 'top_right',
        text: 'stravanova',
        style: {
            margin: '5px',
            padding: '1px 6px',
            border: 'solid 1px #717B87',
            background: '#fff'
        },
        events: {
            click: function(){
                fade_toggle_help_overlay();
            }
        }
    });

    // hide the overlay when clicking the x
    $('.close-overlay').click(function() {
        fade_toggle_help_overlay();
    });

    // onload, fade out the overlay after a while
    overlay_hide_timeout = window.setTimeout( function() {
        $('#help-overlay').fadeOut(800);
    }, 10000);

});

function fade_toggle_help_overlay() {
    // clear the auto-hide timer if it hasn't fired
    window.clearTimeout(overlay_hide_timeout);

    // show/hide the div
    $('#help-overlay').fadeToggle(100);
}
