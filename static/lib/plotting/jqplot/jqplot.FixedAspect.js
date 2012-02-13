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

/**
 * Class: jqplot.FixedAspect
 * Author: Brian Maranville
 * 02/2012
 * this program was created as part of the regular duties of a US government
 * employee, and is in the public domain
 */ 
 
(function($) {
    // Class: $.jqplot.FixedAspect
    // Constrains the plotting to a fixed aspect ratio of y to x (in pixels)
    $.jqplot.FixedAspect = function(options) {
        // prop: aspectRatio
        // parameter for plotting constraint, = (yaxis range) / (xaxis range) 
        this.aspectRatio = 1.0;
        // prop: fixAspect
        // turns the aspect constraint on and off.
        this.fixAspect = false;
        
        $.extend(true, this, options);
    };
    
    $.jqplot.FixedAspect.init = function(target, data, opts) {
        // add a cursor attribute to the plot
        var options = opts || {};
        this.plugins.fixedAspect = new $.jqplot.FixedAspect(options.fixedAspect);
    };
    
    $.jqplot.FixedAspect.preDraw = function() {
        var fa = this.plugins.fixedAspect;
        if (fa.fixAspect == true) {
            var yrange = (this.axes.yaxis.max - this.axes.yaxis.min);
            var ycenter = (this.axes.yaxis.max + this.axes.yaxis.min) / 2.0;
            var xrange = (this.axes.xaxis.max - this.axes.xaxis.min);
            var xcenter = (this.axes.xaxis.max + this.axes.xaxis.min) / 2.0;
            var grid_ratio = this.grid._width / this.grid._height;
            var ratio = yrange/xrange * grid_ratio;
            var target_ratio = fa.aspectRatio;
            //console.log('ratios:', ratio, target_ratio);
            if (isNaN(ratio) || ratio == target_ratio) { return };
            if (ratio < target_ratio) { // y-range is too small
                yrange = target_ratio * xrange / grid_ratio;
            }
            if (ratio > target_ratio) {
                xrange = yrange / target_ratio * grid_ratio;
            }
            
            //console.log('ranges:', yrange, xrange);
            this.axes.xaxis.min = xcenter - xrange/2.0;
            this.axes.xaxis.max = xcenter + xrange/2.0;
            this.axes.yaxis.min = ycenter - yrange/2.0;
            this.axes.yaxis.max = ycenter + yrange/2.0;
            
            return;
        }
    };
    
    $.jqplot.preInitHooks.push($.jqplot.FixedAspect.init);
    $.jqplot.preDrawHooks.push($.jqplot.FixedAspect.preDraw);
    
    
    
})(jQuery);    
