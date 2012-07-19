// #############################################
// # Interactors as jqplot plugins             #
// # Brian Maranville                          #
// # 10/14/2011                                #
// #############################################

// ## requires interactors_nonprototype.js 
// ## and interactor_plugin_base.js (and jQuery, of course)

(function($) {
    function toArray(obj) {
        return Array.prototype.slice.call(obj);
    };
    
    var dist = $.jqplot.dist;
    function bind(scope, fn) {
        return function () {
            return fn.apply(scope, toArray(arguments));
        };
    };
    
    
    $.jqplot.VerticalLineInteractor = function() { $.jqplot.InteractorPlugin.call(this); };
    $.jqplot.VerticalLineInteractor.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.VerticalLineInteractor.prototype.constructor = $.jqplot.VerticalLineInteractor;
    $.jqplot.InteractorPluginSubtypes.VerticalLine = $.jqplot.VerticalLineInteractor;
    
    $.jqplot.VerticalLineInteractor.prototype.init = function(options) {
        $.jqplot.InteractorPlugin.prototype.init.call(this, options);
        //this.points = [];
        this.width = 4;
        this.x0 = 0.0;
        $.extend(this, options);
        this.p = new $.jqplot.PluginPoint();
        this.p.initialize(this, this.x0, 0);
        this.vline = new $.jqplot.VerticalLine();
        this.vline.initialize(this, this.p, this.width);
        this.grobs.push(this.vline);
        this.grobs.push(this.p);
        this.p.render = function(ctx) {
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.fillStyle = this.color;
            ctx.strokeStyle = 'transparent';
            ctx.beginPath();
            this.putCoords(null, true);
            this.pos.y = height/2.0;
            this.getCoords();
            ctx.fillText(this.coords.x.toPrecision(4) , this.pos.x + 5, this.pos.y - 5);
            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            ctx.fill(); 
        }
        this.p.move = function(dpos) {
            this.dpos.y = 0;
            this.translateBy(dpos);
            this.parent.redraw();
            //this.parent.translateBy(dpos);
            //this.parent.update();
        }
        
    };
    
    $.jqplot.HorizontalLineInteractor = function() { $.jqplot.InteractorPlugin.call(this); };
    $.jqplot.HorizontalLineInteractor.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.HorizontalLineInteractor.prototype.constructor = $.jqplot.HorizontalLineInteractor;
    $.jqplot.InteractorPluginSubtypes.HorizontalLine = $.jqplot.HorizontalLineInteractor;
    
    $.jqplot.HorizontalLineInteractor.prototype.init = function(options) {
        $.jqplot.InteractorPlugin.prototype.init.call(this, options);
        //this.points = [];
        this.width = 4;
        this.y0 = 0.0;
        $.extend(this, options);
        this.p = new $.jqplot.PluginPoint();
        this.p.initialize(this, 0, this.y0);
        this.hline = new $.jqplot.HorizontalLine();
        this.hline.initialize(this, this.p, this.width);
        this.grobs.push(this.hline);
        this.grobs.push(this.p);
        this.p.render = function(ctx) {
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.fillStyle = this.color;
            ctx.strokeStyle = 'transparent';
            ctx.beginPath();
            this.putCoords(null, true);
            this.pos.x = width/2.0;
            this.getCoords();
            ctx.fillText(this.coords.y.toPrecision(4) , this.pos.x + 5, this.pos.y - 5);
            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            ctx.fill(); 
        }
        this.p.move = function(dpos) {
            this.dpos.x = 0;
            this.translateBy(dpos);
            this.parent.redraw();
            //this.parent.translateBy(dpos);
            //this.parent.update();
        }
        
    };
    
    
    $.jqplot.RightAngleSegmentInteractor = function() { $.jqplot.PolygonInteractorPlugin.call(this); };
    $.jqplot.RightAngleSegmentInteractor.prototype = new $.jqplot.PolygonInteractorPlugin();
    $.jqplot.RightAngleSegmentInteractor.prototype.constructor = $.jqplot.RightAngleSegmentInteractor;
    $.jqplot.InteractorPluginSubtypes.RightAngleSegment = $.jqplot.RightAngleSegmentInteractor;
    
    $.jqplot.RightAngleSegmentInteractor.prototype.init = function(options) {
        $.jqplot.PolygonInteractorPlugin.prototype.init.call(this, options);
        // points are specified by left point x and x_width
        this.points = [];
        this.leftpoints = [];
        this.x_offset = 0;
        this.width = 4;
        $.extend(this, options);
        this.build_segments();
    };
    
    $.jqplot.RightAngleSegmentInteractor.prototype.build_segments = function() {
        //console.log(this);
        this.grobs = [];
        this.lp = [];
        this.rp = [];
        this.hseg = [];
        this.vseg = [];
        var pl, pr, hseg, vseg;
        var x0 = this.x_offset;
        var leftpoints = this.leftpoints;
        for (var i in leftpoints) {
            pl = new $.jqplot.PluginPoint();
            pl.initialize(this, x0, leftpoints[i].y);
            pl.n = i;
            this.lp.push(pl);
            pr = new $.jqplot.PluginPoint();
            pr.initialize(this, x0 + leftpoints[i].segwidth, leftpoints[i].y);
            pr.n = i;
            this.rp.push(pr);
            hseg = new $.jqplot.Segment();
            hseg.initialize(this, pl, pr, this.width);
            hseg.n = i;
            this.hseg.push(hseg);
            
            if (i > 0) {
                vseg = new $.jqplot.Segment();
                vseg.initialize(this, pl, this.rp[i-1], this.width);
                this.vseg.push(vseg);
            }
            x0 += leftpoints[i].segwidth;   
        }
        
        for (var i in this.hseg) {
            this.hseg[i].connectortranslatable = false;
            this.hseg[i].onDrag = function(e, pos) {
                $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
                this.dpos.x = 0;
                this.translateBy(this.dpos);
                this.parent.update();
            }
            this.grobs.push(this.hseg[i]); 
        };
        for (var i in this.vseg) { 
            this.vseg[i].connectortranslatable = false;
            this.vseg[i].onDrag = function(e, pos) {
                $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
                this.dpos.y = 0;
                this.translateBy(this.dpos);
                this.parent.update();
            }
            this.grobs.push(this.vseg[i]);
        };
        for (var i in this.lp)  {
            this.lp[i].render = function(ctx) {
	            ctx.fillStyle = this.color;
	            ctx.strokeStyle = 'transparent';
                ctx.beginPath();
	            //var coords = this.getCoords();
		    this.pos = this.putCoords();
	            ctx.fillText('(' + this.coords.x.toFixed() + ', ' + this.coords.y.toPrecision(4) + ')', this.pos.x, this.pos.y - 5);
	            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
	            ctx.closePath();
	            ctx.stroke();
	            ctx.fill();
            };
            
            this.lp[i].move = function(dpos) {
                this.translateBy(dpos);
                this.parent.rp[this.n].translateBy( {x: 0, y: dpos.y} );
                if (this.n > 0) { 
                    this.parent.rp[parseInt(this.n) - 1].translateBy( {x: dpos.x, y: 0} );
                }
                this.parent.update();
            }
            this.grobs.push(this.lp[i]); 
        };
        for (var i in this.rp)  {
            this.rp[i].render = function(ctx) {
	            ctx.fillStyle = this.color;
	            ctx.strokeStyle = 'transparent';
                ctx.beginPath();
	            //var coords = this.getCoords();
	            this.pos = this.putCoords();
		    //this.putCoords();
	            ctx.fillText('(' + this.coords.x.toFixed() + ', ' + this.coords.y.toPrecision(4) + ')', this.pos.x, this.pos.y - 5);
	            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
	            ctx.closePath();
	            ctx.stroke();
	            ctx.fill();
            };
            
            this.rp[i].move = function(dpos) {
                this.translateBy(dpos);
                this.parent.lp[this.n].translateBy( {x: 0, y: dpos.y} );
                if (this.n < (this.parent.lp.length-1)) { 
                    this.parent.lp[parseInt(this.n) + 1].translateBy( {x: dpos.x, y: 0} );
                }
                this.parent.update();
            }
            this.grobs.push(this.rp[i]); 
        };
        
        //this.redraw();
    };

})(jQuery);
