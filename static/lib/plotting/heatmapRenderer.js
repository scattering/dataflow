(function($) {
    // inherit from LineRenderer
    $.jqplot.heatmapRenderer = function(){
        $.jqplot.LineRenderer.call(this);
    };
    
    $.jqplot.heatmapRenderer.prototype = new $.jqplot.LineRenderer();
    $.jqplot.heatmapRenderer.prototype.constructor = $.jqplot.heatmapRenderer;
    
    // called with scope of a series
    $.jqplot.heatmapRenderer.prototype.init = function(options) {
        // Group: Properties
        //
        
        // prop: palette
        // palette to convert values to colors
        this.palette = null;
        this.transform = 'lin';
        
        
        $.extend(true, this, options);

        this.canvas = new $.jqplot.DivCanvas();
        this.canvas._plotDimensions = this._plotDimensions;
        this._type = 'heatmap';
        
        // group: Methods 
        //
        this.get_sxdx = function(){
            var xp = this.axes.xaxis.u2p;
            var yp = this.axes.yaxis.u2p;
            var dims = this.source_data.dims
            if (!dims.dx){ dims.dx = (dims.xmax - dims.xmin)/(dims.xdim-1); }
            if (!dims.dy){ dims.dy = (dims.ymax - dims.ymin)/(dims.ydim-1); }
            
            var xmin = Math.max(this.axes.xaxis.min, dims.xmin), xmax = Math.min(this.axes.xaxis.max, dims.xmax);
            var ymin = Math.max(this.axes.yaxis.min, dims.ymin), ymax = Math.min(this.axes.yaxis.max, dims.ymax);
            if (debug) {
                console.log('x', xmin,xmax, 'y', ymin,ymax, 'w', (xmax-xmin), 'h', (ymax-ymin));
                console.log('dims', dims);
            }
            
            var sx  = (xmin - dims.xmin)/dims.dx, sy  = (dims.ymax - ymax)/dims.dy,
                sx2 = (xmax - dims.xmin)/dims.dx, sy2 = (dims.ymax - ymin)/dims.dy,
                sw = sx2 - sx, sh = sy2 - sy;
            if (debug)
                console.log('sx', sx, 'sy', sy, 'sw', sw, 'sh', sh, '   sx2 ', sx2, 'sy2 ', sy2);
            
            var dx = xp.call(this.axes.xaxis, xmin), 
                dy = yp.call(this.axes.yaxis, ymax),
                dw = xp.call(this.axes.xaxis, xmax) - xp.call(this.axes.xaxis, xmin), 
                dh = yp.call(this.axes.yaxis, ymin) - yp.call(this.axes.yaxis, ymax);
            if (debug)
                console.log('dx', dx, 'dy', dy, 'dw', dw, 'dh', dh);
            return {sx:sx, sy:sy, sw:sw, sh:sh, dx:dx, dy:dy, dw:dw, dh:dh}
        }
    };
    
    // called with scope of series
    $.jqplot.heatmapRenderer.prototype.draw = function (ctx, gd, options) {
        // do stuff
        function t(datum) {
            if (options.transform=='log'){
                if (datum >=0) { return Math.log(datum)/Math.LN10 }
                else { return NaN }
            }
            else if (options.transform=='lin'){ return datum }
        }
    
        var dims = data.dims;
        var display_dims = data.display_dims || dims; // plot_dims = data_dims if not specified
        this.axes.xaxis.min = display_dims.xmin;
        this.axes.xaxis.max = display_dims.xmax;
        // don't ask me why we can't use xaxis.label directly. Is it a bug in jqPlot?
        this.axes.xaxis.labelOptions.label = data.xlabel;
        this.axes.yaxis.min = display_dims.ymin;
        this.axes.yaxis.max = display_dims.ymax;
        this.axes.yaxis.labelOptions.label = data.ylabel;
    };
    
    $.jqplot.DivCanvas = function() {
        $.jqplot.ElemContainer.call(this);
        this._ctx;  
    };
    
    $.jqplot.DivCanvas.prototype = new $.jqplot.ElemContainer();
    $.jqplot.DivCanvas.prototype.constructor = $.jqplot.DivCanvas;
    
    $.jqplot.DivCanvas.prototype.createElement = function(offsets, clss, plotDimensions) {
        this._offsets = offsets;
        var klass = 'jqplot-DivCanvas';
        if (clss != undefined) {
            klass = clss;
        }
        var elem;
        // if this canvas already has a dom element, don't make a new one.
        if (this._elem) {
            elem = this._elem.get(0);
        }
        else {
            elem = document.createElement('div');
        }
        // if new plotDimensions supplied, use them.
        if (plotDimensions != undefined) {
            this._plotDimensions = plotDimensions;
        }
        
        var w = this._plotDimensions.width - this._offsets.left - this._offsets.right + 'px';
        var h = this._plotDimensions.height - this._offsets.top - this._offsets.bottom + 'px';
        this._elem = $(elem);
        this._elem.css({ position: 'absolute', width:w, height:h, left: this._offsets.left, top: this._offsets.top });
        
        this._elem.addClass(klass);
        return this._elem;
    };
    
    $.jqplot.DivCanvas.prototype.setContext = function() {
        this._ctx = {
            canvas:{
                width:0,
                height:0
            },
            clearRect:function(){return null;}
        };
        return this._ctx;
    };
    
    $.jqplot.heatmapAxisRenderer = function() {
        $.jqplot.LinearAxisRenderer.call(this);
    };
    
    $.jqplot.heatmapAxisRenderer.prototype = new $.jqplot.LinearAxisRenderer();
    $.jqplot.heatmapAxisRenderer.prototype.constructor = $.jqplot.heatmapAxisRenderer;
        
    // called with scope of axis object.
    $.jqplot.heatmapAxisRenderer.prototype.init = function(options){
        $.extend(true, this, options);
        var db = this._dataBounds;
        
//        db.max = this.dims.
//        for (var i=0; i<this._series.length; i++) {
//            var s = this._series[i];
//            var d = s._plotData;
//        db.max += maxfact;
//        db.min -= minfact;
    };
    
})(jQuery);
