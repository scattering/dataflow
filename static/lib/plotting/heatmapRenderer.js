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
        // palette to convert values to colors: default is "jet"
        this.palette_array = [[0,0,127],[0,0,132],[0,0,136],[0,0,141],[0,0,145],[0,0,150],[0,0,154],[0,0,159],[0,0,163],[0,0,168],[0,0,172],[0,0,177],[0,0,181],[0,0,186],[0,0,190],[0,0,195],[0,0,199],[0,0,204],[0,0,208],[0,0,213],[0,0,218],[0,0,222],[0,0,227],[0,0,231],[0,0,236],[0,0,240],[0,0,245],[0,0,249],[0,0,254],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,3,255],[0,7,255],[0,11,255],[0,15,255],[0,19,255],[0,23,255],[0,27,255],[0,31,255],[0,35,255],[0,39,255],[0,43,255],[0,47,255],[0,51,255],[0,55,255],[0,59,255],[0,63,255],[0,67,255],[0,71,255],[0,75,255],[0,79,255],[0,83,255],[0,87,255],[0,91,255],[0,95,255],[0,99,255],[0,103,255],[0,107,255],[0,111,255],[0,115,255],[0,119,255],[0,123,255],[0,127,255],[0,131,255],[0,135,255],[0,139,255],[0,143,255],[0,147,255],[0,151,255],[0,155,255],[0,159,255],[0,163,255],[0,167,255],[0,171,255],[0,175,255],[0,179,255],[0,183,255],[0,187,255],[0,191,255],[0,195,255],[0,199,255],[0,203,255],[0,207,255],[0,211,255],[0,215,255],[0,219,255],[0,223,251],[0,227,248],[1,231,245],[4,235,242],[7,239,239],[10,243,235],[14,247,232],[17,251,229],[20,255,226],[23,255,222],[26,255,219],[30,255,216],[33,255,213],[36,255,210],[39,255,206],[43,255,203],[46,255,200],[49,255,197],[52,255,194],[55,255,190],[59,255,187],[62,255,184],[65,255,181],[68,255,178],[71,255,174],[75,255,171],[78,255,168],[81,255,165],[84,255,161],[88,255,158],[91,255,155],[94,255,152],[97,255,149],[100,255,145],[104,255,142],[107,255,139],[110,255,136],[113,255,133],[116,255,129],[120,255,126],[123,255,123],[126,255,120],[129,255,116],[133,255,113],[136,255,110],[139,255,107],[142,255,104],[145,255,100],[149,255,97],[152,255,94],[155,255,91],[158,255,88],[161,255,84],[165,255,81],[168,255,78],[171,255,75],[174,255,71],[178,255,68],[181,255,65],[184,255,62],[187,255,59],[190,255,55],[194,255,52],[197,255,49],[200,255,46],[203,255,43],[206,255,39],[210,255,36],[213,255,33],[216,255,30],[219,255,26],[222,255,23],[226,255,20],[229,255,17],[232,255,14],[235,255,10],[239,254,7],[242,250,4],[245,247,1],[248,243,0],[251,239,0],[255,235,0],[255,232,0],[255,228,0],[255,224,0],[255,221,0],[255,217,0],[255,213,0],[255,210,0],[255,206,0],[255,202,0],[255,199,0],[255,195,0],[255,191,0],[255,188,0],[255,184,0],[255,180,0],[255,176,0],[255,173,0],[255,169,0],[255,165,0],[255,162,0],[255,158,0],[255,154,0],[255,151,0],[255,147,0],[255,143,0],[255,140,0],[255,136,0],[255,132,0],[255,128,0],[255,125,0],[255,121,0],[255,117,0],[255,114,0],[255,110,0],[255,106,0],[255,103,0],[255,99,0],[255,95,0],[255,92,0],[255,88,0],[255,84,0],[255,81,0],[255,77,0],[255,73,0],[255,69,0],[255,66,0],[255,62,0],[255,58,0],[255,55,0],[255,51,0],[255,47,0],[255,44,0],[255,40,0],[255,36,0],[255,33,0],[255,29,0],[255,25,0],[255,21,0],[254,18,0],[249,14,0],[245,10,0],[240,7,0],[236,3,0],[231,0,0],[227,0,0],[222,0,0],[218,0,0],[213,0,0],[208,0,0],[204,0,0],[199,0,0],[195,0,0],[190,0,0],[186,0,0],[181,0,0],[177,0,0],[172,0,0],[168,0,0],[163,0,0],[159,0,0],[154,0,0],[150,0,0],[145,0,0],[141,0,0],[136,0,0],[132,0,0]];
        this.palette_str = ["rgb(0,0,127)", "rgb(0,0,132)", "rgb(0,0,136)", "rgb(0,0,141)", "rgb(0,0,145)", "rgb(0,0,150)", "rgb(0,0,154)", "rgb(0,0,159)", "rgb(0,0,163)", "rgb(0,0,168)", "rgb(0,0,172)", "rgb(0,0,177)", "rgb(0,0,181)", "rgb(0,0,186)", "rgb(0,0,190)", "rgb(0,0,195)", "rgb(0,0,199)", "rgb(0,0,204)", "rgb(0,0,208)", "rgb(0,0,213)", "rgb(0,0,218)", "rgb(0,0,222)", "rgb(0,0,227)", "rgb(0,0,231)", "rgb(0,0,236)", "rgb(0,0,240)", "rgb(0,0,245)", "rgb(0,0,249)", "rgb(0,0,254)", "rgb(0,0,255)", "rgb(0,0,255)", "rgb(0,0,255)", "rgb(0,0,255)", "rgb(0,3,255)", "rgb(0,7,255)", "rgb(0,11,255)", "rgb(0,15,255)", "rgb(0,19,255)", "rgb(0,23,255)", "rgb(0,27,255)", "rgb(0,31,255)", "rgb(0,35,255)", "rgb(0,39,255)", "rgb(0,43,255)", "rgb(0,47,255)", "rgb(0,51,255)", "rgb(0,55,255)", "rgb(0,59,255)", "rgb(0,63,255)", "rgb(0,67,255)", "rgb(0,71,255)", "rgb(0,75,255)", "rgb(0,79,255)", "rgb(0,83,255)", "rgb(0,87,255)", "rgb(0,91,255)", "rgb(0,95,255)", "rgb(0,99,255)", "rgb(0,103,255)", "rgb(0,107,255)", "rgb(0,111,255)", "rgb(0,115,255)", "rgb(0,119,255)", "rgb(0,123,255)", "rgb(0,127,255)", "rgb(0,131,255)", "rgb(0,135,255)", "rgb(0,139,255)", "rgb(0,143,255)", "rgb(0,147,255)", "rgb(0,151,255)", "rgb(0,155,255)", "rgb(0,159,255)", "rgb(0,163,255)", "rgb(0,167,255)", "rgb(0,171,255)", "rgb(0,175,255)", "rgb(0,179,255)", "rgb(0,183,255)", "rgb(0,187,255)", "rgb(0,191,255)", "rgb(0,195,255)", "rgb(0,199,255)", "rgb(0,203,255)", "rgb(0,207,255)", "rgb(0,211,255)", "rgb(0,215,255)", "rgb(0,219,255)", "rgb(0,223,251)", "rgb(0,227,248)", "rgb(1,231,245)", "rgb(4,235,242)", "rgb(7,239,239)", "rgb(10,243,235)", "rgb(14,247,232)", "rgb(17,251,229)", "rgb(20,255,226)", "rgb(23,255,222)", "rgb(26,255,219)", "rgb(30,255,216)", "rgb(33,255,213)", "rgb(36,255,210)", "rgb(39,255,206)", "rgb(43,255,203)", "rgb(46,255,200)", "rgb(49,255,197)", "rgb(52,255,194)", "rgb(55,255,190)", "rgb(59,255,187)", "rgb(62,255,184)", "rgb(65,255,181)", "rgb(68,255,178)", "rgb(71,255,174)", "rgb(75,255,171)", "rgb(78,255,168)", "rgb(81,255,165)", "rgb(84,255,161)", "rgb(88,255,158)", "rgb(91,255,155)", "rgb(94,255,152)", "rgb(97,255,149)", "rgb(100,255,145)", "rgb(104,255,142)", "rgb(107,255,139)", "rgb(110,255,136)", "rgb(113,255,133)", "rgb(116,255,129)", "rgb(120,255,126)", "rgb(123,255,123)", "rgb(126,255,120)", "rgb(129,255,116)", "rgb(133,255,113)", "rgb(136,255,110)", "rgb(139,255,107)", "rgb(142,255,104)", "rgb(145,255,100)", "rgb(149,255,97)", "rgb(152,255,94)", "rgb(155,255,91)", "rgb(158,255,88)", "rgb(161,255,84)", "rgb(165,255,81)", "rgb(168,255,78)", "rgb(171,255,75)", "rgb(174,255,71)", "rgb(178,255,68)", "rgb(181,255,65)", "rgb(184,255,62)", "rgb(187,255,59)", "rgb(190,255,55)", "rgb(194,255,52)", "rgb(197,255,49)", "rgb(200,255,46)", "rgb(203,255,43)", "rgb(206,255,39)", "rgb(210,255,36)", "rgb(213,255,33)", "rgb(216,255,30)", "rgb(219,255,26)", "rgb(222,255,23)", "rgb(226,255,20)", "rgb(229,255,17)", "rgb(232,255,14)", "rgb(235,255,10)", "rgb(239,254,7)", "rgb(242,250,4)", "rgb(245,247,1)", "rgb(248,243,0)", "rgb(251,239,0)", "rgb(255,235,0)", "rgb(255,232,0)", "rgb(255,228,0)", "rgb(255,224,0)", "rgb(255,221,0)", "rgb(255,217,0)", "rgb(255,213,0)", "rgb(255,210,0)", "rgb(255,206,0)", "rgb(255,202,0)", "rgb(255,199,0)", "rgb(255,195,0)", "rgb(255,191,0)", "rgb(255,188,0)", "rgb(255,184,0)", "rgb(255,180,0)", "rgb(255,176,0)", "rgb(255,173,0)", "rgb(255,169,0)", "rgb(255,165,0)", "rgb(255,162,0)", "rgb(255,158,0)", "rgb(255,154,0)", "rgb(255,151,0)", "rgb(255,147,0)", "rgb(255,143,0)", "rgb(255,140,0)", "rgb(255,136,0)", "rgb(255,132,0)", "rgb(255,128,0)", "rgb(255,125,0)", "rgb(255,121,0)", "rgb(255,117,0)", "rgb(255,114,0)", "rgb(255,110,0)", "rgb(255,106,0)", "rgb(255,103,0)", "rgb(255,99,0)", "rgb(255,95,0)", "rgb(255,92,0)", "rgb(255,88,0)", "rgb(255,84,0)", "rgb(255,81,0)", "rgb(255,77,0)", "rgb(255,73,0)", "rgb(255,69,0)", "rgb(255,66,0)", "rgb(255,62,0)", "rgb(255,58,0)", "rgb(255,55,0)", "rgb(255,51,0)", "rgb(255,47,0)", "rgb(255,44,0)", "rgb(255,40,0)", "rgb(255,36,0)", "rgb(255,33,0)", "rgb(255,29,0)", "rgb(255,25,0)", "rgb(255,21,0)", "rgb(254,18,0)", "rgb(249,14,0)", "rgb(245,10,0)", "rgb(240,7,0)", "rgb(236,3,0)", "rgb(231,0,0)", "rgb(227,0,0)", "rgb(222,0,0)", "rgb(218,0,0)", "rgb(213,0,0)", "rgb(208,0,0)", "rgb(204,0,0)", "rgb(199,0,0)", "rgb(195,0,0)", "rgb(190,0,0)", "rgb(186,0,0)", "rgb(181,0,0)", "rgb(177,0,0)", "rgb(172,0,0)", "rgb(168,0,0)", "rgb(163,0,0)", "rgb(159,0,0)", "rgb(154,0,0)", "rgb(150,0,0)", "rgb(145,0,0)", "rgb(141,0,0)", "rgb(136,0,0)", "rgb(132,0,0)"];
        this.transform = 'lin';
        // put series options in options.series (dims, etc.)
        this.dims = {xmin:0, xmax:1, ymin:0, ymax:1};
        this.transform = 'lin';
        $.extend(true, this, options);
        
        if (!this.dims.dx){ this.dims.dx = (this.dims.xmax - this.dims.xmin)/(this.dims.xdim); }
        if (!this.dims.dy){ this.dims.dy = (this.dims.ymax - this.dims.ymin)/(this.dims.ydim); }
        
        // need to create a canvas to draw on...
        this.canvas = new $.jqplot.GenericCanvas();
        this.canvas._plotDimensions = this._plotDimensions;
        this._type = 'heatmap';
        
        var display_dims = options.display_dims || this.dims; // plot_dims = data_dims if not specified
        this._xaxis.min = display_dims.xmin;
        this._xaxis.max = display_dims.xmax;
        this._yaxis.min = display_dims.ymin;
        this._yaxis.max = display_dims.ymax;
        // kind of a hack, but prevents jqplot from messing with the data 
        // (if sortData=true were turned on, for instance);
        this.source_data = [];
        for (var i=0; i<this.dims.xdim; i++) {
            this.source_data.push(this.data[i].slice());
        }
        
        this.data = [[this.dims.xmin, this.dims.ymin],
                    [this.dims.xmax, this.dims.ymin],
                    [this.dims.xmax, this.dims.ymax],
                    [this.dims.xmin, this.dims.ymax]];
        
        this._plotData = [[this.dims.xmin, this.dims.ymin],
                    [this.dims.xmax, this.dims.ymin],
                    [this.dims.xmax, this.dims.ymax],
                    [this.dims.xmin, this.dims.ymax]];
                    
        // group: Methods 
        //
        
        this.update_plotdata = update_plotdata;
        this.set_transform = set_transform;
        this.set_data = set_data;
        this.zoom_to = zoom_to;
        this.set_transform(this.transform);
        this.update_plotdata();
    };
    
            
    // call with scope of series    
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
    
    // call with scope of series
    $.jqplot.heatmapRenderer.prototype.generate_cumsums = function () {
        var width = this.dims.xdim;
        var height = this.dims.ydim;
        var cumsum_x = [], cumsum_x_col;
        var cumsum_y = [], cumsum_y_col;
        for (var c = 0; c < width; c++) {
            cumsum_x_col = []; xsum = 0;
            cumsum_y_col = [];
            for (var r = 0; r < height; r++) {
                var offset = 4*((r*width) + c);
                var z = data[c][height-r-1];
                xsum += z;
                cumsum_x_col.push(xsum);
                
            }
            cumsum_x.push(cumsum_x_col);
        }
        this.cumsum_x = cumsum_x;
        
    };
        
    // called with scope of series
    // place rectangle of zoom-appropriate size for elements in source data.  
    // steps are big enough to skip completely-overlapping rectangles (saving time);
    $.jqplot.heatmapRenderer.prototype.draw_rect = function (ctx, gd, options) {
        // do stuff
        var sxdx = this.get_sxdx();
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
		            ctx.fillStyle = this.palette_str[plotz];
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
        var dxu = this._xaxis.p2u(1) - this._xaxis.p2u(0);
        var dyu = this._yaxis.p2u(1) - this._yaxis.p2u(0);
        
        var sx0 = this._xaxis.p2u(0 + this.canvas._offsets.left);
        var sy0 = this._yaxis.p2u(0 + this.canvas._offsets.top);
        for (var y=0; y<height; y++) {
            var syu = sy0 + y * dyu;
            for (var x=0; x<width; x++) {
                var sxu = sx0 + x * dxu;
                var offset = (y*width + x)*4; 
                if (sxu < this.dims.xmax && sxu >= this.dims.xmin && syu < this.dims.ymax && syu >= this.dims.ymin) {
                    var sx = Math.floor((sxu - this.dims.xmin) / this.dims.dx);
                    var sy = Math.floor((syu - this.dims.ymin) / this.dims.dy);
                    var fillstyle = this.palette_array[this.plotdata[sx][sy]];
                    myImageData.data[offset    ] = fillstyle[0];
                    myImageData.data[offset + 1] = fillstyle[1];
                    myImageData.data[offset + 2] = fillstyle[2];
                    myImageData.data[offset + 3] = 255;
                }
            }
        }
        ctx.putImageData(myImageData, 0,0);
    }
    
    $.jqplot.heatmapRenderer.prototype.draw = $.jqplot.heatmapRenderer.prototype.draw_blit;
    
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
    
    function set_data(new_data, new_dims) {
        this.dims = new_dims;
        this.data = new_data;
        this.source_data = [];
        for (var i=0; i<this.dims.xdim; i++) {
            this.source_data.push(this.new_data[i].slice());
        }
        this.update_plotdata();
    };
    
    function set_transform(tform) {
        // only knows log and lin for now
        this.transform = tform;
        if (tform=='log'){
            this.t = function(datum) {
                if (datum >=0) { return Math.log(datum)/Math.LN10 }
                else { return NaN }
            }   
        } else { // transform defaults to 'lin' if unrecognized
            this.t = function(datum) { return datum }
        }
        
        if (this.source_data && this.dims) this.update_plotdata();
    };
    
    function zoom_to(limits) {
        // sets limits of plot to specified limits
        // defaults to data limits!
        var limits = limits || this.dims;
        if ('xmin' in limits) { console.log('xmin: ', limits.xmin, this._xaxis.min); this._xaxis.min = limits.xmin; }
        if ('xmax' in limits) this._xaxis.max = limits.xmax;
        if ('ymin' in limits) this._yaxis.min = limits.ymin;
        if ('ymax' in limits) this._yaxis.max = limits.ymax;
    };
    
    // call after setting transform
    function update_plotdata() {
        var width = this.dims.xdim;
        var height = this.dims.ydim;
        var tzmax = this.t(this.dims.zmax);
        var data = this.source_data; 
        var plotdata = [], datacol;      
        
        for (var c = 0; c < width; c++) {
            datacol = [];
            for (var r = 0; r < height; r++) {
                var offset = 4*((r*width) + c);
                //var z = data[c][height-r-1];
                var z = data[c][r];
                var plotz = Math.floor((this.t(z) / tzmax) * 255.0);

                plotz = ((plotz>255)? 255 : plotz);
                plotz = ((plotz<0)? 0 : plotz);
                datacol.push(plotz);
            }
            plotdata.push(datacol.slice());
        }
        this.plotdata = plotdata;
    };
       
})(jQuery);
