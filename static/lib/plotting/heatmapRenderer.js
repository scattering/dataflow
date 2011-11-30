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
        // put series options in options.series (dims, etc.)
        this.dims = {xmin:0, xmax:1, ymin:0, ymax:1};
        this.xlabel = 'x';
        this.ylabel = 'y';
        $.extend(true, this, options);

        this.canvas = new $.jqplot.GenericCanvas();
        this.canvas._plotDimensions = this._plotDimensions;
        this._type = 'heatmap';
        
        var display_dims = options.display_dims || this.dims; // plot_dims = data_dims if not specified
        this._xaxis.min = display_dims.xmin;
        this._xaxis.max = display_dims.xmax;
        // don't ask me why we can't use xaxis.label directly. Is it a bug in jqPlot?
        this._xaxis.label = this.xlabel;
        this._yaxis.min = display_dims.ymin;
        this._yaxis.max = display_dims.ymax;
        this._yaxis.label = this.ylabel;
        
        // group: Methods 
        //
        this.get_sxdx = function(){
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
        
        this.getOrigin = function() {
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
            
            var sx  = 0, sy  = 0,
                sx2 = (dims.xmax - dims.xmin)/dims.dx, sy2 = (dims.ymax - dims.ymin)/dims.dy,
                sw = sx2 - sx, sh = sy2 - sy;
            if (debug)
                console.log('sx', sx, 'sy', sy, 'sw', sw, 'sh', sh, '   sx2 ', sx2, 'sy2 ', sy2);
            
            var dx = xp.call(this._xaxis, dims.xmin) - this.canvas._offsets.left, 
                dy = yp.call(this._yaxis, dims.ymax) - this.canvas._offsets.top,
                dw = xp.call(this._xaxis, dims.xmax) - xp.call(this._xaxis, dims.xmin), 
                dh = yp.call(this._yaxis, dims.ymin) - yp.call(this._yaxis, dims.ymax);
            if (debug)
                console.log('dx', dx, 'dy', dy, 'dw', dw, 'dh', dh);
            return {sx:sx, sy:sy, sw:sw, sh:sh, dx:dx, dy:dy, dw:dw, dh:dh}
        };
        
        var transform = options.transform || 'lin';
        this.t = function(tform) {
            if (tform=='log'){
                return function(datum) {
                    if (datum >=0) { return Math.log(datum)/Math.LN10 }
                    else { return NaN }
                }   
            } 
            else { // transform defaults to 'lin' if unrecognized
                return function(datum) { return datum }
            }
        }(transform);
        
        //this.add_image(this.data[0]);
        this.img = null;
        
        var jet = palettes.jet;
        var palette_array = jet(256).array;
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
                    var rgb = palette_array[plotz];
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
        var img = new Image();
        //img.style.setProperty("image-rendering", "-webkit-optimize-contrast", "important");
        img.src = canvas.toDataURL('image/png');
       
        var that = this;
        
        img.onload = function(){
            that.img = img;
            //that.postDrawHooks.add(that.draw_image);
            that.draw(that._ctx);         
        } 
    };
    
    // called with scope of series
//    $.jqplot.heatmapRenderer.prototype.get_sxdx = function(){
//            var xp = this._xaxis.u2p;
//            var yp = this._yaxis.u2p;
//            var dims = this.dims;
//            if (!dims.dx){ dims.dx = (dims.xmax - dims.xmin)/(dims.xdim-1); }
//            if (!dims.dy){ dims.dy = (dims.ymax - dims.ymin)/(dims.ydim-1); }
//            
//            var xmin = Math.max(this._xaxis.min, dims.xmin), xmax = Math.min(this._xaxis.max, dims.xmax);
//            var ymin = Math.max(this._yaxis.min, dims.ymin), ymax = Math.min(this._yaxis.max, dims.ymax);
//            if (debug) {
//                console.log('x', xmin,xmax, 'y', ymin,ymax, 'w', (xmax-xmin), 'h', (ymax-ymin));
//                console.log('dims', dims);
//            }
//            
//            var sx  = (xmin - dims.xmin)/dims.dx, sy  = (dims.ymax - ymax)/dims.dy,
//                sx2 = (xmax - dims.xmin)/dims.dx, sy2 = (dims.ymax - ymin)/dims.dy,
//                sw = sx2 - sx, sh = sy2 - sy;
//            if (debug)
//                console.log('sx', sx, 'sy', sy, 'sw', sw, 'sh', sh, '   sx2 ', sx2, 'sy2 ', sy2);
//            
//            var dx = xp.call(this._xaxis, xmin), 
//                dy = yp.call(this._yaxis, ymax),
//                dw = xp.call(this._xaxis, xmax) - xp.call(this._xaxis, xmin), 
//                dh = yp.call(this._yaxis, ymin) - yp.call(this._yaxis, ymax);
//            if (debug)
//                console.log('dx', dx, 'dy', dy, 'dw', dw, 'dh', dh);
//            return {sx:sx, sy:sy, sw:sw, sh:sh, dx:dx, dy:dy, dw:dw, dh:dh}
//    };
    
    // called with scope of series
    $.jqplot.heatmapRenderer.prototype.draw = function (ctx, gd, options) {
        // do stuff
        var img = this.img;
        if (img) {
            var sxdx = this.getOrigin();
            var xzoom = sxdx.dw / sxdx.sw;
            var yzoom = sxdx.dh / sxdx.sh;
            var x0, y0, oldx0, oldy0;
            //console.log(img, sxdx);
            if (sxdx.sw > 0 && sxdx.sh > 0) {
                //ctx.mozImageSmoothingEnabled = false;
                //ctx.drawImage(img, sxdx.sx, sxdx.sy, sxdx.sw, sxdx.sh, sxdx.dx, sxdx.dy, sxdx.dw, sxdx.dh);
                var zoom = 24;
                ctx.clearRect(0,0,ctx.canvas.width, ctx.canvas.height);
                for (var x=0;x<img.width;++x){
			        for (var y=0;y<img.height;++y){
				        var i = (y*img.width + x)*4;
				        var r = this.imgData.data[i  ];
				        var g = this.imgData.data[i+1];
				        var b = this.imgData.data[i+2];
				        var a = this.imgData.data[i+3];
				        x0 = parseInt(sxdx.dx + x*xzoom);
				        y0 = parseInt(sxdx.dy + y*yzoom);
				        if (x0 != oldx0 || y0 != oldy0) {
				            ctx.fillStyle = "rgba("+r+","+g+","+b+","+(a/255)+")";
				            ctx.fillRect(x0,y0,Math.ceil(xzoom),Math.ceil(yzoom));
				        }
				        oldx0 = x0;
				        oldy0 = y0;
			        }
		        }
                //console.log('draw_image')
            }
        }
    };
    
    function add_image(data) {
        this.img = null;
        
        var jet = palettes.jet;
        var palette_array = jet(256).array;
        var canvas = document.createElement('canvas');
        canvas.hidden = true;
        var width = this.dims.xdim;
        var height = this.dims.ydim;
        var context = canvas.getContext('2d');
        var myImageData = context.createImageData(width, height);
        canvas.width = width;
        canvas.height = height;
        var tzmax = this.t(this.dims.zmax);
      
          for (var r = 0; r < width; r++) {
            for (var c = 0; c < height; c++) {
                var offset = 4*((c*width) + r);
                var z = data[r][height-c];
                var plotz = Math.floor((this.t(z) / tzmax) * 255.0);

                plotz = ((plotz>255)? 255 : plotz);
                plotz = ((plotz<0)? 0 : plotz);
                if (isNaN(plotz)) {
                    var rgb = [0,0,0];
                    var alpha = 0;
                }
                else {
                    var rgb = palette_array[plotz];
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
        var img = new Image();
        //img.style.setProperty("image-rendering", "-webkit-optimize-contrast", "important");
        img.src = canvas.toDataURL('image/png');
       
        var that = this;
        
        img.onload = function(){
            that.img = img;
            //that.postDrawHooks.add(that.draw_image);
            that.draw(that._ctx);         
        } 
    }
    
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
