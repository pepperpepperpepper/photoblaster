(function($){

    $.okgradient = function(el, options){
        var base = this;       
        base.$el = $(el);
        base.el = el;        
        base.$el.data("okgradient", base);
        
        var width = $(window).width();
        var height = $(window).height();

        var browsers = " -webkit- -moz- -o- -ms-".split(" ");

        base.init = function(){            
            base.options = $.extend({}, $.okgradient.options, options);
            base.build();
        };

        base.build = function(){
            base.start();
            if (base.options.type in base.actions) {
                base.action = base.actions[ base.options.type ];
            }
        };
        
        base.start = function () {
            $(window).bind({
                mousemove: base.mousemove
            });
            base.mousemove({ pageX: $(window).width() / 2, pageY: $(window).height() / 2 });
            if (base.options.transparent) {
                base.el.style.color = "transparent";
            }
        };

        base.parsecolor = function (rgb) {
            var x = rgb.replace('rgb(','').replace(')','').split(',');
            return [parseInt(x[0]), parseInt(x[1]), parseInt(x[2])];
        };

        base.scale = function (x, xbasis, newbasis) {
            return (x - xbasis[0]) / (xbasis[1] - xbasis[0]) * (newbasis[1] - newbasis[0]) + newbasis[0];
        };
        base.clamp = function (x, min, max) {
            return Math.max(min, Math.min(max, x));
        };
        base.parse_range = function (x, range) {
            if (typeof range === "number") return range;
            return base.scale(x, [0,1], range);
        };

        base.average_rgb = function (a, b, distance) {
          var x = [];
          for (var i = 0; i < 3; i++)
            x[i] = Math.floor( a[i] * distance + b[i] * (1-distance) )
          return x;
        };

        base.setoption = function (key, value) {
            if (typeof key === "string") {
              base.options[key] = value;
            } else {
              base.options = $.extend(base.options, key);
            }
            base.mousemove(base);
        };

        base.mousemove = function (e){
            var offset = base.$el.offset(),
                x = e.pageX,
                y = e.pageY;
                cy = offset.top + base.$el.height() / 2,
                cx = offset.left + base.$el.width() / 2,
                dx = (cx - x),
                dy = (cy - y),
                distance = Math.sqrt(dx*dx + dy*dy),
                ratio = 1 - distance / $(window).height();
            base.pageX = x;
            base.pageY = y;
            base.action(ratio);
        };

        base.opacity = function (ratio) {
            base.el.style.opacity = ratio;
        };

        base.hsl = function (ratio, ranges) {
            var hue = base.parse_range(ratio, ranges.hue),
                sat = base.parse_range(ratio, ranges.saturation),
                lum = base.parse_range(ratio, ranges.luminance);
            if ("alpha" in ranges) {
                var alpha = base.parse_range(ratio, ranges.alpha);
                return "hsla(" + hue + "," + sat + "%," + lum + "%," + alpha + ")";
            } else {
                return "hsl(" + hue + "," + sat + "%," + lum + "%)";
            }
        };

        base.background = function (ratio) { 
            var color = base.hsl(ratio, base.options);
            base.el.style.background = color;
        };

        base.backgroundRadialGradient = function (ratio) {
            var start = base.hsl(ratio, base.options.start),
                end = base.hsl(ratio, base.options.end);
            var gradient = 'radial-gradient(bottom, ' + start + ' 0%, ' + end + ' 100%);';
            var gradients = "";
            for (var i = 0, len = browsers.length; i < len; i++)
                gradients += "background: " + browsers[i] + gradient + ";";
            base.el.style.cssText = gradients;
        };

        base.backgroundLinearGradient = function (ratio) {
            var start = base.hsl(ratio, base.options.start),
                end = base.hsl(ratio, base.options.end);
            var gradient = 'linear-gradient(bottom, ' + start + ' 0%, ' + end + ' 100%);';
            var gradients = "";
            for (var i = 0, len = browsers.length; i < len; i++)
                gradients += "background: " + browsers[i] + gradient + ";";
            base.el.style.cssText = gradients;
        };

        // initialize action to no-op
        base.action = function(){};
        base.actions = {
            "opacity": base.opacity,
            "background": base.background,
            "background linear-gradient": base.backgroundLinearGradient,
            "background radial-gradient": base.backgroundRadialGradient,
        };

        base.init();
    };

    $.okgradient.options = { 
        hue: [0,360],
        saturation: [50,50],
        luminance: [50,50],
        opacity: [1,1],
    };
    
    $.fn.okgradient = function(options){
        return this.each(function(){
            (new $.okgradient(this, options));            
        });
    };
    
})(jQuery);
