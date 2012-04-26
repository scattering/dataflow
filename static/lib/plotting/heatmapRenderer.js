// Renderer for 2-dimensional data.
// Ver. 1.0  Dec 15, 2011
//
// Developed by Brian Ben Maranville 
// at the National Institute of Standards and Technology,
// Gaithersburg, Maryland, USA
// This software is in the public domain and is not copyrighted
//
// data has the form
// data = [[z00,z01,z02,...z0n],
//    [z10,z11,z12,...z1n],
//    ...,
//    [zm0,zm1,zm2,...zmn]]
//
//    to specify axis values, include optional dims
//    dims = { xmin: xmin,  // x value of first data point on axis
//             xmax: xmax,  // x value of last data point on axis
//             xlabel: xlabel, 
//             xdim: xdim, // width of data array along x
//             
//             ymin: ymin,  // y value of first data point on axis
//             ymax: ymax,  // y value of last data point on axis
//             ylabel: ylabel, 
//             ydim: ydim, // width of data array along y
//           }
         

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
        // palette to convert values to colors: default is "jet" (defined below in this file)
        this.palette_array = jet_array;
        this.overflowColor = [0,0,0,0];
        this.palette_array.push(this.overflowColor);     
        this.transform = 'lin';
        // put series options in options.series (dims, etc.)
        var xdim = this.data.length;
        var ydim = this.data[0].length; // cheating, only looking at first column
        this.dims = {xmin:0, xmax:xdim, xdim: xdim,
                     ymin:0, ymax:ydim, ydim: ydim,
                     zmin: 0, zmax: 1};
        this.transform = 'lin';
        $.extend(true, this, options);
        this._colorbar = null; // colorbar will hook in when initialized;
        
        // need to create a canvas to draw on...
        this.canvas = new $.jqplot.GenericCanvas();
        this.canvas._plotDimensions = this._plotDimensions;
        this._type = 'heatmap';
        
        var display_dims = options.display_dims || this.dims; // plot_dims = data_dims if not specified
        this._xaxis.min = display_dims.xmin;
        this._xaxis.max = display_dims.xmax;
        this._yaxis.min = display_dims.ymin;
        this._yaxis.max = display_dims.ymax;
                      
        // group: Methods 
        //
        
        this.update_plotdata = update_plotdata;
        this.set_transform = set_transform;
        this.generate_histogram = generate_histogram;
        this.generate_cumsums = generate_cumsums;
        this.set_data = set_data;
        this.zoom_to = zoom_to;
        this.set_transform(this.transform);
        this.set_data(this.data, this.dims);
        this.update_plotdata();
    };
    
            
    // call with scope of series
    // this function courtesy of Ophir Lifshitz, 2011
    $.jqplot.heatmapRenderer.prototype.get_sxdx = function(){
        var xp = this._xaxis.u2p;
        var yp = this._yaxis.u2p;
        var dims = this.dims;
        if (!dims.dx){ dims.dx = (dims.xmax - dims.xmin)/(dims.xdim); }
        if (!dims.dy){ dims.dy = (dims.ymax - dims.ymin)/(dims.ydim); }
        
        var xmin = Math.max(this._xaxis.min, dims.xmin), xmax = Math.min(this._xaxis.max, dims.xmax);
        var ymin = Math.max(this._yaxis.min, dims.ymin), ymax = Math.min(this._yaxis.max, dims.ymax);
        if (debug) {
            console.log('x', xmin,xmax, 'y', ymin,ymax, 'w', (xmax-xmin), 'h', (ymax-ymin));
            console.log('dims', dims);
        }
        
        var sx  = (xmin - dims.xmin)/dims.dx, sy  = (dims.ymax - ymax)/dims.dy,
            sx2 = (xmax - dims.xmin)/dims.dx, sy2 = (dims.ymax - ymin)/dims.dy,
            sw = sx2 - sx, sh = sy2 - sy;
        if (debug)
            console.log('sx', sx, 'sy', sy, 'sw', sw, 'sh', sh, '   sx2 ', sx2, 'sy2 ', sy2);
        
        var dx = xp.call(this._xaxis, xmin) - this.canvas._offsets.left, 
            dy = yp.call(this._yaxis, ymax) - this.canvas._offsets.top,
            dw = xp.call(this._xaxis, xmax) - xp.call(this._xaxis, xmin), 
            dh = yp.call(this._yaxis, ymin) - yp.call(this._yaxis, ymax);
        if (debug)
            console.log('dx', dx, 'dy', dy, 'dw', dw, 'dh', dh);
        return {sx:sx, sy:sy, sw:sw, sh:sh, dx:dx, dy:dy, dw:dw, dh:dh}
    };
    
        
    // called with scope of series
    // place rectangle of zoom-appropriate size for elements in source data.  
    // steps are big enough to skip completely-overlapping rectangles (saving time);
    $.jqplot.heatmapRenderer.prototype.draw_rect = function (ctx, gd, options) {
        // do stuff
        var sxdx = this.renderer.get_sxdx();
        var xzoom = sxdx.dw / sxdx.sw;
        var yzoom = sxdx.dh / sxdx.sh;
        var xstep = Math.max(1/xzoom, 1);
        var ystep = Math.max(1/yzoom, 1);
        var sx = parseInt(sxdx.sx), sy = parseInt(sxdx.sy);
        var x0, y0, oldx0, oldy0, plotz;
        var width = ctx.canvas.width;
        var height = ctx.canvas.height;
        var tzmax = this.t(this.dims.zmax);
        if (sxdx.sw > 0 && sxdx.sh > 0) {
            var zoom = 24;
            ctx.clearRect(0,0, width, height);
            var xmax = (sxdx.sw + sxdx.sx);
            var ymax = (sxdx.sh + sxdx.sy);
            var xw = Math.ceil(xzoom);
            var yw = Math.ceil(yzoom);
            for (var x=sx;x<xmax;x+=xstep){
                var xindex = parseInt(x);
                var scol = this.plotdata[xindex];
                x0 = Math.round(sxdx.dx + (x-sxdx.sx)*xzoom);
		        for (var y=sy;y<ymax;y+=ystep){
			        plotz = scol[parseInt(y)];
			        y0 = Math.round(sxdx.dy + (y-sxdx.sy)*yzoom);
		            //ctx.fillStyle = "rgba("+r+","+g+","+b+","+(a/255)+")";
		            var rgba = this.palette_array[plotz];
		            ctx.fillStyle = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+", 255)";
		            ctx.fillRect(x0,y0,xw,yw);
		        }
	        }
        }
    };
    
    // draw directly on pixel buffer, then blit to screen:
    // uses reverse-lookup to grab z-value in source data. (no interpolation or averaging).
    $.jqplot.heatmapRenderer.prototype.draw_blit = function (ctx, gd, options) {
        var width = ctx.canvas.width;
        var height = ctx.canvas.height;
        ctx.clearRect(0,0, width, height);
        var myImageData = ctx.createImageData(width, height);
        var sxu = this._xaxis.p2u(1) - this._xaxis.p2u(0);
        var syu = this._yaxis.p2u(1) - this._yaxis.p2u(0);
        var sxp = sxu / this.dims.dx;
        var syp = syu / this.dims.dy;
        
        var dx0p = (this._xaxis.p2u(0 + this.canvas._offsets.left) - this.dims.xmin)/ this.dims.dx;
        var dy0p = (this._yaxis.p2u(0 + this.canvas._offsets.top) - this.dims.ymin) / this.dims.dy;
        for (var y=0; y<height; y++) {
            var dyp = Math.floor(dy0p + y * syp);
            if (dyp >= 0 && dyp < this.dims.ydim) {
                for (var x=0; x<width; x++) {
                    var dxp = Math.floor(dx0p + x * sxp);
                    if (dxp >=0 && dxp < this.dims.xdim) {
                        var offset = (y*width + x)*4;
                        //console.log(offset, this.plotdata);
                        var fillstyle = this.palette_array[this.plotdata[dyp][dxp]];
                        myImageData.data[offset    ] = fillstyle[0];
                        myImageData.data[offset + 1] = fillstyle[1];
                        myImageData.data[offset + 2] = fillstyle[2];
                        myImageData.data[offset + 3] = (fillstyle[3] == undefined) ? 255 : fillstyle[3];
                    }
                }
            }
        }
        ctx.putImageData(myImageData, 0,0);
    };
    
    $.jqplot.heatmapRenderer.prototype.draw = $.jqplot.heatmapRenderer.prototype.draw_blit; //default
    
    var jet_array = [[0,0,127],[0,0,132],[0,0,136],[0,0,141],[0,0,145],[0,0,150],[0,0,154],[0,0,159],[0,0,163],
                     [0,0,168],[0,0,172],[0,0,177],[0,0,181],[0,0,186],[0,0,190],[0,0,195],[0,0,199],[0,0,204],
                     [0,0,208],[0,0,213],[0,0,218],[0,0,222],[0,0,227],[0,0,231],[0,0,236],[0,0,240],[0,0,245],
                     [0,0,249],[0,0,254],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,3,255],[0,7,255],[0,11,255],
                     [0,15,255],[0,19,255],[0,23,255],[0,27,255],[0,31,255],[0,35,255],[0,39,255],[0,43,255],
                     [0,47,255],[0,51,255],[0,55,255],[0,59,255],[0,63,255],[0,67,255],[0,71,255],[0,75,255],
                     [0,79,255],[0,83,255],[0,87,255],[0,91,255],[0,95,255],[0,99,255],[0,103,255],[0,107,255],
                     [0,111,255],[0,115,255],[0,119,255],[0,123,255],[0,127,255],[0,131,255],[0,135,255],[0,139,255],
                     [0,143,255],[0,147,255],[0,151,255],[0,155,255],[0,159,255],[0,163,255],[0,167,255],[0,171,255],
                     [0,175,255],[0,179,255],[0,183,255],[0,187,255],[0,191,255],[0,195,255],[0,199,255],[0,203,255],
                     [0,207,255],[0,211,255],[0,215,255],[0,219,255],[0,223,251],[0,227,248],[1,231,245],[4,235,242],
                     [7,239,239],[10,243,235],[14,247,232],[17,251,229],[20,255,226],[23,255,222],[26,255,219],
                     [30,255,216],[33,255,213],[36,255,210],[39,255,206],[43,255,203],[46,255,200],[49,255,197],
                     [52,255,194],[55,255,190],[59,255,187],[62,255,184],[65,255,181],[68,255,178],[71,255,174],
                     [75,255,171],[78,255,168],[81,255,165],[84,255,161],[88,255,158],[91,255,155],[94,255,152],
                     [97,255,149],[100,255,145],[104,255,142],[107,255,139],[110,255,136],[113,255,133],[116,255,129],
                     [120,255,126],[123,255,123],[126,255,120],[129,255,116],[133,255,113],[136,255,110],[139,255,107],
                     [142,255,104],[145,255,100],[149,255,97],[152,255,94],[155,255,91],[158,255,88],[161,255,84],
                     [165,255,81],[168,255,78],[171,255,75],[174,255,71],[178,255,68],[181,255,65],[184,255,62],
                     [187,255,59],[190,255,55],[194,255,52],[197,255,49],[200,255,46],[203,255,43],[206,255,39],
                     [210,255,36],[213,255,33],[216,255,30],[219,255,26],[222,255,23],[226,255,20],[229,255,17],
                     [232,255,14],[235,255,10],[239,254,7],[242,250,4],[245,247,1],[248,243,0],[251,239,0],[255,235,0],
                     [255,232,0],[255,228,0],[255,224,0],[255,221,0],[255,217,0],[255,213,0],[255,210,0],[255,206,0],
                     [255,202,0],[255,199,0],[255,195,0],[255,191,0],[255,188,0],[255,184,0],[255,180,0],[255,176,0],
                     [255,173,0],[255,169,0],[255,165,0],[255,162,0],[255,158,0],[255,154,0],[255,151,0],[255,147,0],
                     [255,143,0],[255,140,0],[255,136,0],[255,132,0],[255,128,0],[255,125,0],[255,121,0],[255,117,0],
                     [255,114,0],[255,110,0],[255,106,0],[255,103,0],[255,99,0],[255,95,0],[255,92,0],[255,88,0],
                     [255,84,0],[255,81,0],[255,77,0],[255,73,0],[255,69,0],[255,66,0],[255,62,0],[255,58,0],
                     [255,55,0],[255,51,0],[255,47,0],[255,44,0],[255,40,0],[255,36,0],[255,33,0],[255,29,0],
                     [255,25,0],[255,21,0],[254,18,0],[249,14,0],[245,10,0],[240,7,0],[236,3,0],[231,0,0],[227,0,0],
                     [222,0,0],[218,0,0],[213,0,0],[208,0,0],[204,0,0],[199,0,0],[195,0,0],[190,0,0],[186,0,0],
                     [181,0,0],[177,0,0],[172,0,0],[168,0,0],[163,0,0],[159,0,0],[154,0,0],[150,0,0],[145,0,0],
                     [141,0,0],[136,0,0],[132,0,0]];
    
    function add_image(data) {
        var canvas = document.createElement('canvas');
        canvas.hidden = true;
        var width = this.dims.xdim;
        var height = this.dims.ydim;
        var context = canvas.getContext('2d');
        var myImageData = context.createImageData(width, height);
        canvas.width = width;
        canvas.height = height;
        var tzmax = this.t(this.dims.zmax);
        var data = this.data;
        
          for (var r = 0; r < width; r++) {
            for (var c = 0; c < height; c++) {
                var offset = 4*((c*width) + r);
                var z = data[r][height-c-1];
                var plotz = Math.floor((this.t(z) / tzmax) * 255.0);

                plotz = ((plotz>255)? 255 : plotz);
                plotz = ((plotz<0)? 0 : plotz);
                if (isNaN(plotz)) {
                    var rgb = [0,0,0];
                    var alpha = 0;
                }
                else {
                    var rgb = this.palette_array[plotz];
                    var alpha = 255;
                }
                //console.log(plotz, rgb)
                myImageData.data[offset + 0] = rgb[0];
                myImageData.data[offset + 1] = rgb[1];
                myImageData.data[offset + 2] = rgb[2];
                myImageData.data[offset + 3] = alpha;
            }
          }
        context.putImageData(myImageData, 0, 0);
        this.imgData = myImageData;
        this.img = {width: width, height:height};
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
    
    function get_maximum(array, transform, existing_max) {
        var new_max;
        for (var i in array) {
            var subarr = array[i];
            if (subarr.length == undefined) {
                var t_el = transform(subarr);
                if (isFinite(t_el)) new_max = t_el;
            } else {
                new_max = get_maximum(subarr, transform, existing_max);
            }
            if (existing_max == undefined || new_max > existing_max) {
                var existing_max = new_max;
            }
        }
        return existing_max
    };
    
    function set_data(new_data, new_dims) {
        this.dims = new_dims;
        
        if (!('dx' in this.dims)){ this.dims.dx = (this.dims.xmax - this.dims.xmin)/(this.dims.xdim -1); }
        if (!('dy' in this.dims)){ this.dims.dy = (this.dims.ymax - this.dims.ymin)/(this.dims.ydim -1); }
        this.source_data = [];
        //for (var i=0; i<this.dims.ydim; i++) {
        for (var i=0; i<new_data.length; i++) { 
            this.source_data.push(new_data[i].slice());
        }
        
        this.data = [[this.dims.xmin, this.dims.ymin],
                        [this.dims.xmax, this.dims.ymin],
                        [this.dims.xmax, this.dims.ymax],
                        [this.dims.xmin, this.dims.ymax]];
        this._plotData = [[this.dims.xmin, this.dims.ymin],
                        [this.dims.xmax, this.dims.ymin],
                        [this.dims.xmax, this.dims.ymax],
                        [this.dims.xmin, this.dims.ymax]];
        this.update_plotdata();
        var hists = this.generate_histogram();
        this.hist = hists.hist;
        this.fullhist = hists.fullhist;
    };
    
    function set_transform(tform) {
        // only knows log and lin for now
        this.transform = tform;
        if (tform=='log'){
            this.t = function(datum) {
                if (datum >=0) { return Math.log(datum)/Math.LN10 }
                else { return NaN }
            }
            this.tinv = function(datum) {
                    return Math.pow(10, datum);
            }  
        } else { // transform defaults to 'lin' if unrecognized
            this.t = function(datum) { return datum };
            this.tinv = this.t;
        }
        
        if (this.source_data && this.dims) {
            if (!isFinite(this.t(this.dims.zmin))) {
                this.dims.zmin = get_minimum(this.source_data, this.t);
            }
            this.update_plotdata();
        }
        if (this._colorbar && this._colorbar.set_transform) { 
            this._colorbar.set_transform(tform);
            this._colorbar.draw();
        }
    };
    
    function zoom_to(limits) {
        // sets limits of plot to specified limits
        // defaults to data limits!
        var limits = limits || this.dims;
        if ('xmin' in limits) this._xaxis.min = limits.xmin;
        if ('xmax' in limits) this._xaxis.max = limits.xmax;
        if ('ymin' in limits) this._yaxis.min = limits.ymin;
        if ('ymax' in limits) this._yaxis.max = limits.ymax;
    };
    
    function generate_histogram() {
        // create a histogram of the data...
        var hist = [], fullhist={}, plotz;
        for (var i=0; i<256; i++) hist.push(0);    
        for (var c=0; c<this.plotdata.length; c++) {
            datacol = this.plotdata[c];
            for (var r=0; r<datacol.length; r++) {
                plotz = datacol[r];
                hist[plotz] += 1;
                if (plotz in fullhist) { fullhist[plotz] += 1; }
                else { fullhist[plotz] = 1; }
            }
        }
        return {hist: hist, fullhist: fullhist}
    };

    // call after setting transform
    function update_plotdata() {
        var maxColorIndex = 255;
        var overflowIndex = 256;
        var width = this.dims.xdim;
        var height = this.dims.ydim;
        var tzmax = this.t(this.dims.zmax);
        var tzmin = this.t(this.dims.zmin);
        //var tzmax = get_maximum(this.source_data, this.t);
        //var tzmin = get_minimum(this.source_data, this.t);
        //if (isNaN(tzmin)) tzmin = 0;
        
        if (isNaN(tzmin)) tzmin = get_minimum(this.source_data, this.t);
        this.dims.zmin = this.tinv(tzmin);
        var data = this.source_data; 
        var plotdata = [], datarow;
        
        // plotdata is stored in row-major order ("C"), where row is "y"
        for (var r = 0; r < height; r++) {
            datarow = [];
            for (var c = 0; c < width; c++) {
                var z = data[r][c];
                var plotz = Math.floor(((this.t(z) - tzmin) / (tzmax - tzmin)) * maxColorIndex);
                
                if (isNaN(plotz) || (z == null)) { plotz = overflowIndex }
                else if (plotz > maxColorIndex) { plotz = maxColorIndex }
                else if (plotz < 0) { plotz = 0 }
                datarow.push(plotz);
            }
            plotdata.push(datarow.slice());
        }
        this.plotdata = plotdata;
    };
    
    function generate_cumsums() {
        //console.log('generating cumsum');
        var width = this.dims.xdim;
        var height = this.dims.ydim;
        var data = this.source_data;
        var cumsum_x = [], cumsum_x_col;
        var cumsum_y = [], cumsum_y_col;
        var ysum = [];
        // initialize the y-sum:
        for (var r = 0; r<height; r++) ysum.push(0);
        cumsum_y.push(ysum.slice());
        
        
        for (var c = 0; c < width; c++) {
            cumsum_x_col = [0]; xsum = 0;
            cumsum_y_col = [];
            for (var r = 0; r < height; r++) {
                var offset = 4*((r*width) + c);
                //var z = data[c][height-r-1];
                var z = data[r][c];
                xsum += z;
                ysum[r] += z;
                cumsum_x_col.push(xsum);
                cumsum_y_col.push(ysum[r]);
                
            }
            cumsum_x.push(cumsum_x_col);
            cumsum_y.push(cumsum_y_col);
        }
        this.cumsum_x = cumsum_x;
        this.cumsum_y = cumsum_y;
    };
    
       
})(jQuery);
