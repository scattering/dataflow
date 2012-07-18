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
    
    $.jqplot.LinearInteractorPlugin = function() {};
    $.jqplot.LinearInteractorPlugin.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.LinearInteractorPlugin.prototype.constructor = $.jqplot.LinearInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.Line = $.jqplot.LinearInteractorPlugin;
    
    $.jqplot.LinearInteractorPlugin.prototype.init = function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.xmin = 0.0;
            this.ymin = 0.0;
            this.xmax = 1.0;
            this.ymax = 1.0;
            this.slope = 1.0;
            $.extend(this, options);
            this.slope = (this.ymax - this.ymin) / (this.xmax - this.xmin);
            this.intercept = (this.ymax - this.ymin) - (this.slope * (this.xmax - this.xmin));
        
            this.p1 = new $.jqplot.PluginPoint(); this.p1.initialize(this, this.xmin, this.ymin);
            this.p2 = new $.jqplot.PluginPoint(); this.p2.initialize(this, this.xmax, this.ymax);
        
            this.linear = new $.jqplot.Linear(); this.linear.initialize(this, this.p1, this.p2, 4);
        
            this.grobs.push(this.linear, this.p1, this.p2);
        
            //this.redraw();              
    }
    
})(jQuery);
