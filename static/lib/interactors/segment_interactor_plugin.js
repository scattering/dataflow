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
    
    $.jqplot.SegmentInteractorPlugin = function() {};
    $.jqplot.SegmentInteractorPlugin.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.SegmentInteractorPlugin.prototype.constructor = $.jqplot.SegmentInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.Segment = $.jqplot.SegmentInteractorPlugin;
    
    $.jqplot.SegmentInteractorPlugin.prototype.init = function(options) {
        $.jqplot.InteractorPlugin.prototype.init.call(this, options);
        this.xmin = options.xmin || 0.0;
        this.ymin = options.ymin || 0.0;
        this.xmax = options.xmax || 1.0;
        this.ymax = options.ymax || 1.0;
        //this.slope = 1.0;
        $.extend(this, options);
        this.slope = (this.ymax - this.ymin) / (this.xmax - this.xmin);
        this.intercept = (this.ymax - this.ymin) - (this.slope * (this.xmax - this.xmin));
        
        this.p1 = new $.jqplot.PluginPoint(); this.p1.initialize(this, this.xmin, this.ymin);
        this.p2 = new $.jqplot.PluginPoint(); this.p2.initialize(this, this.xmax, this.ymax);

        this.p1.move = function(dp) {
            var dpos = {x: dp.x || 0, y: dp.y || 0 };
            this.translateBy(dpos);
        };
        
        this.p2.move = function(dp) {
            var dpos = {x: dp.x || 0, y: dp.y || 0 };
            this.translateBy(dpos);
        }; 
        
        this.segment = new $.jqplot.Segment(); this.segment.initialize(this, this.p1, this.p2, 4);
        
        this.grobs.push(this.segment, this.p1, this.p2);
        
        //this.redraw();
    }
    
})(jQuery);
