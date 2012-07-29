/* palette.js
*/

// color-generator
// init the palette with a saturation and value
// then call Palette.generate_hex_color() to get a color of random hue with those S and V settings

var Palette = function(saturation, value) {
    // init with a saturation and value
    this.saturation = saturation;
    this.value = value;
};

Palette.prototype.generate_hex_color = function(hue) {
    // via http://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
    
    var hue_integer = Math.floor(hue*6);
    var f = hue*6 - hue_integer;
    var p = this.value * (1 - this.saturation);
    var q = this.value * (1 - f*this.saturation);
    var t = this.value * (1 - (1 - f) * this.saturation);

    var r, g, b;

    if (hue_integer == 0) {
        r = this.value;
        g = t;
        b = p;

    } else if (hue_integer == 1) {
        r = q;
        g = this.value;
        b = p;

    } else if (hue_integer == 2) {
        r = p;
        g = this.value;
        b = t;
    
    } else if (hue_integer == 3) {
        r = p;
        g = q;
        b = this.value;

    } else if (hue_integer == 4) {
        r = t;
        g = p;
        b = this.value;

    } else if (hue_integer == 5) {
        r = this.value;
        g = p;
        b = q;
    }

    // convert to [0, 255]
    r = Math.floor(r*255);
    g = Math.floor(g*255);
    b = Math.floor(b*255);

    return this.rgb_to_hex(r, g, b);
};


Palette.prototype.rgb_to_hex = function(r, g, b) {
    // via http://www.javascripter.net/faq/rgbtohex.htm

    // enforce [0, 255]
    r = Math.max(0, Math.min(r, 255));
    g = Math.max(0, Math.min(g, 255));
    b = Math.max(0, Math.min(b, 255));

    // concatenate the hex values
    return this.to_hex(r) + this.to_hex(g) + this.to_hex(b)
};


Palette.prototype.to_hex = function(n) {
    // integers to their hex values
    // via http://www.javascripter.net/faq/rgbtohex.htm
    n = parseInt(n, 10);
    if (isNaN(n)) return "00";

    return "0123456789ABCDEF".charAt((n - n%16) / 16)
        + "0123456789ABCDEF".charAt(n%16);
};
