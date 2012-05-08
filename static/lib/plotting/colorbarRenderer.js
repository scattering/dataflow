(function($) {
    // inherit from LineRenderer
    $.jqplot.colorbarRenderer = function(){
        $.jqplot.LineRenderer.call(this);
    };
    
    $.jqplot.colorbarRenderer.prototype = new $.jqplot.LineRenderer();
    $.jqplot.colorbarRenderer.prototype.constructor = $.jqplot.colorbarRenderer;
    
    // called with scope of a series
    $.jqplot.colorbarRenderer.prototype.init = function(options) {
        // Group: Properties
        //
        // put series options in options.series (dims, etc.)
        
        // this has to be defined: a 2d plot series 
        // with renderer: heatmapRenderer.
        this.parent_plot = null;
       
        $.extend(true, this, options);
        this.transform = this.parent_plot.transform;
        this.dims = this.parent_plot.dims;
        this.palette_array = this.parent_plot.palette_array;
        
        // need to create a canvas to draw on...
        this.canvas = new $.jqplot.GenericCanvas();
        this.canvas._plotDimensions = this._plotDimensions;
        this._type = 'colorbar';
        
        var display_dims = options.display_dims || this.dims; // plot_dims = data_dims if not specified
        this._xaxis.min = display_dims.xmin;
        this._xaxis.max = display_dims.xmax;
        this._yaxis.min = display_dims.zmin;
        this._yaxis.max = display_dims.zmax;
       
                    
        // group: Methods 
        //
        
        this.matchPlotToColorbar = matchPlotToColorbar;
        //this.update_plotdata = update_plotdata;
        this.set_transform = set_transform;
        this.set_dims = set_dims;
        //this.set_data = set_data;
        this.zoom_to = zoom_to;
        this.set_transform(this.transform);
        this.parent_plot._colorbar = this;
        
    };
    
        
    // called with scope of series
    // place rectangle of zoom-appropriate size for elements in source data.  
    $.jqplot.colorbarRenderer.prototype.draw_rect = function (ctx, gd, options) {
        // do stuff
        var width = ctx.canvas.width;
        var height = ctx.canvas.height;
        var rh = height/256.0;
        ctx.clearRect(0,0, width, height);
        for (var i=0; i<256; i++) {
            var y0 = Math.floor(i*rh);
            var rgba = this.palette_array[255-i];
		    ctx.fillStyle = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+", 1.0)";
            //ctx.fillStyle = this.palette_str[255-i];
            ctx.fillRect(0, y0, width, Math.ceil(rh));
        };
        
        this.matchPlotToColorbar();
    };
    
    $.jqplot.colorbarRenderer.prototype.draw = $.jqplot.colorbarRenderer.prototype.draw_rect;
    
    function matchPlotToColorbar() {
        var new_dims = {};
        var cb = this;
        new_dims.zmax = cb.tinv(cb._yaxis.max);
        new_dims.zmin = cb.tinv(cb._yaxis.min);
        $.extend(this.parent_plot.dims, new_dims, true);
        this.parent_plot.update_plotdata();
        this.parent_plot.draw();
    };
    
    function set_data(new_data, new_dims) {
        this.dims = new_dims;
        this.data = new_data;
        if (!this.dims.dx){ this.dims.dx = (this.dims.xmax - this.dims.xmin)/(this.dims.xdim -1); }
        if (!this.dims.dy){ this.dims.dy = (this.dims.ymax - this.dims.ymin)/(this.dims.ydim -1); }
        this.source_data = [];
        for (var i=0; i<this.dims.xdim; i++) {
            this.source_data.push(new_data[i].slice());
        }
        this.update_plotdata();
    };
    
    function get_minimum(array, transform, existing_min) {
        var new_min;
        for (var i in array) {
            var subarr = array[i];
            if (subarr.length == undefined) {
                var t_el = transform(subarr);
                if (isFinite(t_el)) new_min = t_el;
            } else {
                new_min = get_minimum(subarr, transform, existing_min);
            }
            if (existing_min == undefined || new_min < existing_min) {
                var existing_min = new_min;
            }
        }
        return existing_min
    };
    
    function set_dims(dims) {
        $.extend(true, this.dims, dims);
        this.set_transform();
    }
    
    function set_transform(tform) {
        // only knows log and lin for now
        //if (tform != this.transform) {
            var tform = tform || this.transform;
            this.transform = tform;
            this._yaxis.transform = tform;
            
            if (tform=='log'){
                this.t = function(datum) {
                    if (datum >=0) { return Math.log(datum)/Math.LN10 }
                    else { return NaN }
                }
                this.tinv = function(datum) {
                    return Math.pow(10, datum);
                }
            } else { // transform defaults to 'lin' if unrecognized
                this.t = function(datum) { return datum }
                this.tinv = this.t;
            }
            
            var tmin = this.t(this.dims.zmin);
            if (!isFinite(tmin)) tmin = get_minimum(this.parent_plot.source_data, this.t);
            this.dims.zmin = this.tinv(tmin);
            var tmax = this.t(this.dims.zmax);
            this._yaxis.min = tmin;
            this._yaxis.max = tmax;
            this._yaxis._dataBounds = {min: tmin, max: tmax};
            this.data = [[this.dims.xmin, tmin],
                    [this.dims.xmax, tmin],
                    [this.dims.xmax, tmax],
                    [this.dims.xmin, tmax]];
            this._plotData = [[this.dims.xmin, tmin],
                    [this.dims.xmax, tmin],
                    [this.dims.xmax, tmax],
                    [this.dims.xmin, tmax]];
            
        //}
        
        //if (this.source_data && this.dims) this.update_plotdata();
    };
    
    function zoom_to(limits) {
        // sets limits of plot to specified limits
        // defaults to data limits!
        var limits = limits || this.dims;
        if ('xmin' in limits) { console.log('xmin: ', limits.xmin, this._xaxis.min); this._xaxis.min = limits.xmin; }
        if ('xmax' in limits) this._xaxis.max = limits.xmax;
        if ('zmin' in limits) this._yaxis.min = limits.zmin;
        if ('zmax' in limits) this._yaxis.max = limits.zmax;
    };
       
})(jQuery);
