/**
 * jqPlot
 * Pure JavaScript plotting plugin using jQuery
 *
 * Version: 1.0.0b1_r746
 *
 * Copyright (c) 2009-2011 Chris Leonello
 * jqPlot is currently available for use in all personal or commercial projects 
 * under both the MIT (http://www.opensource.org/licenses/mit-license.php) and GPL 
 * version 2.0 (http://www.gnu.org/licenses/gpl-2.0.html) licenses. This means that you can 
 * choose the license that best suits your project and use it accordingly. 
 *
 * Although not required, the author would appreciate an email letting him 
 * know of any substantial use of jqPlot.  You can reach the author at: 
 * chris at jqplot dot com or see http://www.jqplot.com/info.php .
 *
 * If you are feeling kind and generous, consider supporting the project by
 * making a donation at: http://www.jqplot.com/donate.php .
 *
 * sprintf functions contained in jqplot.sprintf.js by Ash Searle:
 *
 *     version 2007.04.27
 *     author Ash Searle
 *     http://hexmen.com/blog/2007/03/printf-sprintf/
 *     http://hexmen.com/js/sprintf.js
 *     The author (Ash Searle) has placed this code in the public domain:
 *     "This code is unrestricted: you are free to use it however you like."
 * 
 */
(function($) {

    var isNumeric = function(n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
    }

    /**
     * Class: $.jqplot.errorbarRenderer
     * jqPlot Plugin to draw error bars.
     * 
     * To use this plugin, include the renderer js file in 
     * your source:
     * 
     * > <script type="text/javascript" src="plugins/jqplot.errorbarRenderer.js"></script>
     * 
     * Then you set the renderer in the series options on your plot:
     * 
     * > series: [{renderer:$.jqplot.errorbarRenderer}]
     * 
     * For errorbar and candlestick charts, data should be specified
     * like so:
     * 
     * Data must be supplied in one of these forms:
     * 
     * > data = [[x1, y1, { xerr: xerr1,            yerr: yerr1            }, mask ], ...]
     * > data = [[x1, y1, { xerr: [xerr1l, xerr1h], yerr: [yerr1l, yerr1h] } ], ...]
     * 
     */
    $.jqplot.errorbarRenderer = function(){
        // subclass line renderer to make use of some of it's methods.
        $.jqplot.LineRenderer.call(this);
        // prop: candleStick
        // true to render chart as candleStick.
        // Must have an open price, cannot be a hlc chart.
        this.candleStick = false;
        // prop: tickLength
        // length of the line in pixels indicating open and close price.
        // Default will auto calculate based on plot width and 
        // number of points displayed.
        this.tickLength = 'auto';
        // prop: bodyWidth
        // width of the candlestick body in pixels.  Default will auto calculate
        // based on plot width and number of candlesticks displayed.
        this.bodyWidth = 'auto';
        // prop: openColor
        // color of the open price tick mark.  Default is series color.
        this.openColor = null;
        // prop: closeColor
        // color of the close price tick mark.  Default is series color.
        this.closeColor = null;
        // prop: wickColor
        // color of the hi-lo line thorugh the candlestick body.
        // Default is the series color.
        this.wickColor = null;
        // prop: hlc
        // true if is a hi-low-close chart (no open price).
        // This is determined automatically from the series data.
        this.hlc = false;
        // prop: errorBar
        // true to render error bars
        // Must be specified manually.
        this.errorBar = false;
        // prop: lineWidth
        // Width of the hi-low line and open/close ticks.
        // Must be set in the rendererOptions for the series.
        this.lineWidth = 1.5;
        this._tickLength;
        this._bodyWidth;
    };
    
    $.jqplot.errorbarRenderer.prototype = new $.jqplot.LineRenderer();
    $.jqplot.errorbarRenderer.prototype.constructor = $.jqplot.errorbarRenderer;
    
    // called with scope of series.
    $.jqplot.errorbarRenderer.prototype.init = function(options) {
        options = options || {};
        // lineWidth has to be set on the series, changes in renderer
        // constructor have no effect.  set the default here
        // if no renderer option for lineWidth is specified.
        this.lineWidth = options.lineWidth || 1.5;
        $.jqplot.LineRenderer.prototype.init.call(this, options);
        this._type = 'errorbar';
        // set the yaxis data bounds here to account for hi and low values
        var dbx = this._xaxis._dataBounds;
        var dby = this._yaxis._dataBounds;
        var d = this._plotData;
        if (this.renderer.errorBar) {
          // Loop through all points
          for (var j=0; j<d.length; j++) {
            // First set xupper, xlower, yupper, ylower
            // Then adjust axis ranges if necessary
          
            var eb = d[j][2];
            if (eb.xerr) {
              // If symmetric
              if (isNumeric(eb.xerr)) {
                eb.xerr = [eb.xerr, eb.xerr];
              }
              if (jQuery.isArray(eb.xerr)) {
                eb.xlower = d[j][0] - eb.xerr[0];
                eb.xupper = d[j][0] + eb.xerr[1];
              }
            }
            if (eb.yerr) {
              // If symmetric
              if (isNumeric(eb.yerr)) {
                eb.yerr = [eb.yerr, eb.yerr];
              }
              if (jQuery.isArray(eb.yerr)) {
                eb.ylower = d[j][1] - eb.yerr[0];
                eb.yupper = d[j][1] + eb.yerr[1];
              }
            }
            
            if (eb.xlower < dbx.min || dbx.min == null) {
                dbx.min = eb.xlower;
            }
            if (eb.xupper > dbx.max || dbx.max == null) {
                dbx.max = eb.xupper;
            }
            if (eb.ylower < dby.min || dby.min == null) {
                dby.min = eb.ylower;
            }
            if (eb.yupper > dby.max || dby.max == null) {
                dby.max = eb.yupper;
            }
          }
        }
        
    };
    
    // called within scope of series.
    $.jqplot.errorbarRenderer.prototype.draw = function(ctx, gd, options) {
        var d = this.data;
        var xmin = this._xaxis.min;
        var xmax = this._xaxis.max;
        // index of last value below range of plot.
        var xminidx = 0;
        // index of first value above range of plot.
        var xmaxidx = d.length;
        var xp = this._xaxis.series_u2p;
        var yp = this._yaxis.series_u2p;
        var i, prevColor, ops, b, h, w, a, points;
        var o;
        var r = this.renderer;
        var opts = (options != undefined) ? options : {};
        var shadow = (opts.shadow != undefined) ? opts.shadow : this.shadow;
        var fill = (opts.fill != undefined) ? opts.fill : this.fill;
        var fillAndStroke = (opts.fillAndStroke != undefined) ? opts.fillAndStroke : this.fillAndStroke;
        r.bodyWidth = (opts.bodyWidth != undefined) ? opts.bodyWidth : r.bodyWidth;
        r.tickLength = (opts.tickLength != undefined) ? opts.tickLength : r.tickLength;
        ctx.save();
        if (this.show) {
            var x, y, xu, xl, yu, yl;
            // need to get widths based on number of points shown,
            // not on total number of points.  Use the results 
            // to speed up drawing in next step.
            for (var i=0; i<d.length; i++) {
                if (d[i][0] < xmin) {
                    xminidx = i;
                }
                else if (d[i][0] < xmax) {
                    xmaxidx = i+1;
                }
            }

            var dwidth = this.gridData[xmaxidx-1][0] - this.gridData[xminidx][0];
            var nvisiblePoints = xmaxidx - xminidx;
            try {
                var dinterval = Math.abs(this._xaxis.series_u2p(parseInt(this._xaxis._intervalStats[0].sortedIntervals[0].interval)) - this._xaxis.series_u2p(0)); 
            }

            catch (e) {
                var dinterval = dwidth / nvisiblePoints;
            }
            
            if (r.candleStick) {
                if (typeof(r.bodyWidth) == 'number') {
                    r._bodyWidth = r.bodyWidth;
                }
                else {
                    r._bodyWidth = Math.min(20, dinterval/1.75);
                }
            }
            else {
                if (typeof(r.tickLength) == 'number') {
                    r._tickLength = r.tickLength;
                }
                else {
                    r._tickLength = Math.min(10, dinterval/3.5);
                }
            }
            
            for (var i=xminidx; i<xmaxidx; i++) {
                x = xp(d[i][0]);
                y = yp(d[i][1]);

                xu = xp(d[i][2].xupper);
                xl = xp(d[i][2].xlower);
                yu = yp(d[i][2].yupper);
                yl = yp(d[i][2].ylower);
                close = yp(d[i][1]);
                //console.log('[',i,']: (x:',d[i][2].xlower,',',d[i][0],',',d[i][2].xupper,'; y:',d[i][2].ylower,',',d[i][1],',',d[i][2].yupper,')');

                o = {};
                
                prevColor = opts.color;
                if (r.openColor) {
                    opts.color = r.openColor;
                }
                // draw open tick
                opts.color = prevColor;
                // draw wick
                if (r.wickColor) {
                    opts.color = r.wickColor;
                }
                // draw horizontal line of upper and lower bound
                r.shapeRenderer.draw(ctx, [[x, yu], [x, yl]], opts);
                // draw vertical line of upper and lower bound
                r.shapeRenderer.draw(ctx, [[xu, y], [xl, y]], opts);

                opts.color  = prevColor;
                if (r.openColor) {
                    opts.color = r.openColor;
                }
                if (d[i][2].yerr[1])
                  // draw upper bound horizontal line
                  r.shapeRenderer.draw(ctx, [[x+r._tickLength/2, yu], [x-r._tickLength/2, yu]], opts);
                if (d[i][2].xerr[1])
                  // draw upper bound vertical line
                  r.shapeRenderer.draw(ctx, [[xu, y+r._tickLength/2], [xu, y-r._tickLength/2]], opts);
                
                opts.color  = prevColor;
                if (r.closeColor) {
                    opts.color = r.closeColor;
                }
                if (d[i][2].yerr[0])
                  // draw lower bound horizontal line
                  r.shapeRenderer.draw(ctx, [[x+r._tickLength/2, yl], [x-r._tickLength/2, yl]], opts);
                if (d[i][2].xerr[0])
                  // draw lower bound vertical line
                  r.shapeRenderer.draw(ctx, [[xl, y+r._tickLength/2], [xl, y-r._tickLength/2]], opts);
                
                
                opts.color  = prevColor;
                
                // draw the mean
                opts.fillRect = true;
                r.shapeRenderer.draw(ctx, [Math.round(x-(r._tickLength/4)), Math.round(y-(r._tickLength/4)), r._tickLength/2, r._tickLength/2], opts);

                opts.color = prevColor;
                opts.fillRect = false;
            }
        }
        
        ctx.restore();
    };  
    
    $.jqplot.errorbarRenderer.prototype.drawShadow = function(ctx, gd, options) {
        // This is a no-op, shadows drawn with lines.
    };
    
    // called with scope of plot.
    $.jqplot.errorbarRenderer.checkOptions = function(target, data, options) {
        // provide some sensible highlighter options by default
        // These aren't good for hlc, only for errorbar or candlestick
        if (!options.highlighter) {
            options.highlighter = {
                showMarker:false,
                tooltipAxes: 'y',
                yvalues: 4,
                formatString:'<table class="jqplot-highlighter"><tr><td>date:</td><td>%s</td></tr><tr><td>open:</td><td>%s</td></tr><tr><td>hi:</td><td>%s</td></tr><tr><td>low:</td><td>%s</td></tr><tr><td>close:</td><td>%s</td></tr></table>'
            };
        }
    };
    
    //$.jqplot.preInitHooks.push($.jqplot.errorbarRenderer.checkOptions);
    
})(jQuery);    
