
// Requires interactors_nonprototype.js
// Requires interactors_plugin_base.js

(function($){
    function toArray(obj){
        return Array.prototype.slice.call(obj);
        };
    
    var dist = $.jqplot.dist;
    function bind(scope, fn){
        return function(){
            return fn.apply(scope, toArray(arguments));
        };
    };
    
    $.jqplot.LinearInteractorPlugin = function() {}; // defines LinearInteractorPlugin
    $.jqplot.LinearInteractorPlugin.prototype = new $.jqplot.InteractorPlugin(); // LinearInteractorPlugin inherits from InteractorPlugin
    $.jqplot.LinearInteractorPlugin.prototype.constructor = $.jqplot.LinearInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.Line = $.jqplot.LinearInteractorPlugin; // adds LinearInteractorPlugin to InteractorPluginSubtypes list as 'Line'
    $.extend($.jqplot.LinearInteractorPlugin.prototype, {
        init: function(options) {
    //$.jqplot.LinearInteractorPlugin.prototype.init = function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.xmin = 0.0;  // keeps track of slope, intercept, and the coordinates of the two defining points of the line
            this.ymin = 0.0;
            this.xmax = 1.0;
            this.ymax = 1.0;
            this.slope = 1.0;
            $.extend(this, options);
            this.slope = (this.ymax - this.ymin) / (this.xmax - this.xmin); // calculates initial slope of line 
            this.intercept = (this.ymax - this.ymin) - (this.slope * (this.xmax - this.xmin)); // calculates initial y-intercept of line
            
            this.p1 = new $.jqplot.PluginPoint(); this.p1.initialize(this, this.xmin, this.ymin); // creates two plugin points for the line
            this.p2 = new $.jqplot.PluginPoint(); this.p2.initialize(this, this.xmax, this.ymax);
            
            this.linear = new $.jqplot.Linear(); this.linear.initialize(this, this.p1, this.p2, 4); // creates a line using both plugin points
            
            this.grobs.push(this.linear, this.p1, this.p2); // adds line interactor (PluginPoints, line) to list of interactors on graph
            
            //this.redraw();              
        },
        /*getSlope: function() {
            this.slope = (this.p2.coords.y - this.p1.coords.y) / (this.p2.coords.x - this.p1.coords.x);
            return this.slope;
        },
        getIntercept: function() {
            var slope = this.getSlope();
            this.intercept = (this.p2.coords.y - this.p1.coords.y) - (slope *  (this.p2.coords.x - this.p1.coords.x));
            return this.intercept;
        }*/
        
/*
        this.grobs.push(this.linear, this.p1, this.p2);
        
        //this.redraw();
    }
*/
    });
    
    $.jqplot.LinearInteractorPlugin.prototype.init

    
})(jQuery);
