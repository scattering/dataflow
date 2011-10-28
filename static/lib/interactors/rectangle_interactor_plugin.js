// #############################################
// # Interactors as jqplot plugins             #
// # Brian Maranville                          #
// # 10/14/2011                                #
// #############################################

// ## requires interactors_nonprototype.js 

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
    
    //console.log($.jqplot.PolygonInteractor);
    $.jqplot.InteractorPlugin = function() {
        //$.jqplot.Interactor.call(this);
    };
    $.jqplot.InteractorPlugin.prototype = new $.jqplot.Interactor();
    $.jqplot.InteractorPlugin.prototype.constructor = $.jqplot.InteractorPlugin;
    $.extend($.jqplot.InteractorPlugin.prototype, {
        // options: name, icon, state, plot
        init: function(options) {
            //name, icon, state, plot) {
            console.log("nInteractor init", this, options);
            this.name = null;
            this.icon = null;
            this.state = null;
            this.plot = null;
            this.translatable = true;

            this.grobs = [];
            this.mousedown = false;
            this.curgrob = null;
            
            this.color1 = '#69f';
            this.color2 = '#f69';
            this.color = this.color1;
            
            this.rc = 1;//Math.random();
            $.extend(true, this, options);
        },
        
        points: function() {
            var points = [];
            for (var i = 0; i < this.grobs.length; i ++)
                if (this.grobs[i] instanceof $.jqplot.PluginPoint && !(this.grobs[i] instanceof $.jqplot.PluginCenter))
                    points.push(this.grobs[i]);
            return points;
        },
        
        transformCalc: function(me) {
            // use the p2u and u2p functions in jqplot to calculate the 
            // transform function to use with HTML5 canvas!
            var me = me || this;
            var a, b, c, d, e, f, tmp;
            function putCoords(coords) {
                var pos = {};
                if ('x' in coords) {
                    pos.x = me.plot.axes.xaxis.u2p(coords.x);
                    pos.x -= me.canvas.offsetLeft;
                }
                if ('y' in coords) {
                    pos.y = me.plot.axes.yaxis.u2p(coords.y);
                    pos.y -= me.canvas.offsetTop;
                }
                return pos
            }  
            tmp = putCoords({x: 0, y:0});
            e = tmp.x; f = tmp.y;
            tmp = putCoords({x:1, y:0});
            a = tmp.x - e; b = tmp.y - f;
            tmp = putCoords({x:0, y:1});
            c = tmp.x - e; d = tmp.y - f;
            me.context.setTransform(a, b, c, d, e, f);
            console.log(a,b,c,d,e,f);
            return {a:a, b:b, c:c, d:d, e:e, f:f}
        },
        
        getCoords: function(pos) {
            // have to correct for the fact that jqplot p2u calculates
            // in terms of pixels with respect to outer (containing) canvas
            // not the actual graph canvas...
            var xpixel = pos.x + this.canvas.offsetLeft;
            var ypixel = pos.y + this.canvas.offsetTop;
            var coords = { x: this.plot.axes.xaxis.p2u(xpixel),
                           y: this.plot.axes.yaxis.p2u(ypixel) }
            return coords
        },
        
        putCoords: function(coords) {
            var pos = {};
            if ('x' in coords) {
                pos.x = this.plot.axes.xaxis.u2p(coords.x);
                pos.x -= this.canvas.offsetLeft;
            }
            if ('y' in coords) {
                pos.y = this.plot.axes.yaxis.u2p(coords.y);
                pos.y -= this.canvas.offsetTop;
            }
            return pos     
        },
        
        onMouseOver: function(e) {
            this.plot.eventCanvas._ctx.canvas.style.cursor = 'move';
            this.color = this.color2;
        },
        onMouseOut: function(e) {
            this.plot.eventCanvas._ctx.canvas.style.cursor = 'auto';
            this.color = this.color1;
        },
        onMouseWheel: function(e) {
            if (e.preventDefault) e.preventDefault();
            if (e.stopPropagation) e.stopPropagation();
            var pos = this.getMouse(e);
            var dzoom;
            if (e.wheelDelta) { dzoom = e.wheelDelta; }
            else if (e.detail) { dzoom = e.detail * -40; }
            else { dzoom = 0 } 
            this.zoomPlot(dzoom, pos);
        },
        
        onEmptyDrag: function(pos) {
            this.panPlot(pos);
        },
        
        zoomPlot: function(dzoom, centerpos) {
            var center = this.getCoords(centerpos);
            // make a zoom of 120 = 10% change in axis limits
            var conv = dzoom * 0.1/120;
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }

            // x zoom
            var xticks = [];
            var xtickInterval = this.plot.axes.xaxis.tickInterval;
            var numxticks = this.plot.axes.xaxis.numberTicks;
            var xmin = this.plot.axes.xaxis.min;
            var xmax = this.plot.axes.xaxis.max;
            xmin += (center.x - xmin) * conv;
            xmax += (center.x - xmax) * conv;
            if (Math.abs(xmax-xmin)/xtickInterval < 5) {
                xtickInterval *= 0.5;
            }
            if (Math.abs(xmax-xmin)/xtickInterval > 10) {
                xtickInterval *= 2.0;
            }
            xticks.push(xmin);
            var tickx = xticks[0] - mod(xticks[0], xtickInterval) + xtickInterval;
            while (tickx < xmax) {
                if (Math.abs(tickx) < 1e-13) tickx = 0;            
                xticks.push(tickx);
                tickx += xtickInterval;
            }
            xticks.push(xmax);
            
            // y zoom
            var yticks = [];
            var ytickInterval = this.plot.axes.yaxis.tickInterval;
            var numyticks = this.plot.axes.yaxis.numberTicks;
            var ymin = this.plot.axes.yaxis.min;
            var ymax = this.plot.axes.yaxis.max;
            ymin += (center.y - ymin) * conv;
            ymax += (center.y - ymax) * conv;
            if (Math.abs(ymax-ymin)/ytickInterval < 5) {
                ytickInterval *= 0.5;
            }
            if (Math.abs(ymax-ymin)/ytickInterval > 10) {
                ytickInterval *= 2.0;
            }
            yticks.push(ymin);
            var ticky = yticks[0] - mod(yticks[0], ytickInterval) + ytickInterval;
            while (ticky < ymax) {
                if (Math.abs(ticky) < 1e-13) ticky = 0;
                yticks.push(ticky);
                ticky += ytickInterval;
            }
            yticks.push(ymax);
            
            //this.plot.axes.yaxis.min += (center.y - this.plot.axes.yaxis.min) * conv;
            //this.plot.axes.yaxis.max += (center.y - this.plot.axes.yaxis.max) * conv;
            this.plot.axes.xaxis.ticks = xticks;
            this.plot.axes.yaxis.ticks = yticks;
            this.plot.replot();
            this.plot.axes.xaxis.tickInterval = xtickInterval;
            this.plot.axes.yaxis.tickInterval = ytickInterval;
            
        },
        
        panPlot: function(pos) {
            var newcoords = this.getCoords(pos);
            var prevcoords = this.getCoords(this.prevpos);
            this.prevpos = pos;
            var dx = newcoords.x - prevcoords.x;
            var dy = newcoords.y - prevcoords.y;
            this.plot.axes.xaxis.min -= dx;
            this.plot.axes.xaxis.max -= dx;
            this.plot.axes.yaxis.min -= dy;
            this.plot.axes.yaxis.max -= dy;
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }
            
            var xticks = [];
            var xtickInterval = this.plot.axes.xaxis.tickInterval;
            xticks.push(this.plot.axes.xaxis.min);
            var tickx = xticks[0] - mod(xticks[0], xtickInterval) + xtickInterval;
            while (tickx < this.plot.axes.xaxis.max) {
                if (Math.abs(tickx) < 1e-13) tickx = 0;
                xticks.push(tickx);
                tickx += this.plot.axes.xaxis.tickInterval;                
            }
            xticks.push(this.plot.axes.xaxis.max);
            var yticks = [];
            var ytickInterval = this.plot.axes.yaxis.tickInterval;
            yticks.push(this.plot.axes.yaxis.min);
            var ticky = yticks[0] - mod(yticks[0], ytickInterval) + ytickInterval;
            while (ticky < this.plot.axes.yaxis.max) {
                if (Math.abs(ticky) < 1e-13) ticky = 0;
                yticks.push(ticky);
                ticky += this.plot.axes.yaxis.tickInterval;               
            }
            yticks.push(this.plot.axes.yaxis.max);
            
            this.plot.axes.xaxis.ticks = xticks;
            this.plot.axes.yaxis.ticks = yticks;
            this.plot.replot();
            this.plot.axes.xaxis.tickInterval = xtickInterval;
            this.plot.axes.yaxis.tickInterval = ytickInterval;
        }
    });
    
    // called with context of plot
    $.jqplot.InteractorPlugin.postDraw = function() {
        for (var i in this.plugins.interactors) {
            var I = this.plugins.interactors[i];
            I.Canvas = new $.jqplot.GenericCanvas();
            this.eventCanvas._elem.before(I.Canvas.createElement(this._gridPadding, 'jqplot-interactor-canvas', this._plotDimensions));
            I.Canvas.setContext();
            I.context = I.Canvas._ctx;
            I.canvas = I.context.canvas;
            I.context.globalAlpha = 0.6;
            I.context.lineJoin = 'round';
            var ec = this.eventCanvas._ctx.canvas
            //ec.onmouseover = bind(I, I.onMouseOver);
            ec.onmousemove = bind(I, I.onMouseMove);
            ec.onmousedown = bind(I, I.onMouseDown);
            ec.onmouseup = bind(I, I.onMouseUp);
            ec.onmousewheel = bind(I, I.onMouseWheel);
            if (!ec._touchstartregistered) {
                ec.addEventListener('touchstart', function(event) {
                    ec.onmousedown(event.touches[0]);
                }, false);
                ec._touchstartregistered = true;
            }
            if (!ec._touchmoveregistered) {
                ec.addEventListener('touchmove', function(event) {
                    event.preventDefault();
                    ec.onmousemove(event.touches[0]);
                }, false);
                ec._touchmoveregistered = true;
            }
            if (!ec._touchendregistered) {
                ec.addEventListener('touchend', function(event) {
                    event.preventDefault();
                    ec.onmouseup(event.touches[0]);
                }, false);
                ec._touchendregistered = true;
            }
            
            if (!ec._scrollregistered) {
                ec.addEventListener('DOMMouseScroll', function(event) {
                    ec.onmousewheel(event);
                });
                ec._scrollregistered = true;
            }
            this.eventCanvas._elem.before(I.Canvas.createElement(this._gridPadding, 'jqplot-interactor-canvas', this._plotDimensions));
            I.redraw(); // first one updates the pos (in pixel units) of everything;
            I.redraw(); // second one finishes the draw.
        }
    };
    
//    $.jqplot.InteractorPlugin.postDrawSeries = function() {
//        for (var i in this.plugins.interactors) {
//            var I = this.plugins.interactors[i];
//            I.transformCalc();
//            I.redraw();
//        }
//    };
    
    $.jqplot.InteractorPluginSubtypes = {}; // fill as child classes are declared.
    
    $.jqplot.InteractorPlugin.pluginit = function (target, data, opts) {
        // add an interactor attribute to the plot
        var options = opts || {};
        if (!this.plugins.interactors) this.plugins.interactors = {};
        for (var i in options.interactors) {
            var iopts = options.interactors[i];
            var itype = iopts.type;
            var name = iopts.name || String(this.plugins.interactors.length);
            var newi = new $.jqplot.InteractorPluginSubtypes[itype]();
            this.plugins.interactors[name] = newi;
            newi.init(iopts);
            newi.plot = this;
        }
    };
    
    $.jqplot.preInitHooks.push($.jqplot.InteractorPlugin.pluginit);
    $.jqplot.postDrawHooks.push($.jqplot.InteractorPlugin.postDraw);
//    $.jqplot.postDrawSeriesHooks.push($.jqplot.InteractorPlugin.postDrawSeries);

    // here we go
//    $.jqplot.Grob.prototype.update = function(context, coords, fix_x, fix_y) {
//    };
    
    $.jqplot.PluginPoint = function() {};
    $.jqplot.PluginPoint.prototype = new $.jqplot.Point();
    $.jqplot.PluginPoint.prototype.constructor = $.jqplot.PluginPoint;    
    $.extend($.jqplot.PluginPoint.prototype, { 
        initialize: function (parent, xcoord, ycoord, r) {
            $.jqplot.Point.prototype.initialize.call(this, parent, 0, 0, r);
            this.coords = {x: xcoord, y: ycoord};
        },
        
        getCoords: function(pos) {
            var pos = pos || this.pos;
            this.coords = this.parent.getCoords(pos);
            return this.coords;
        },
        
        update: function(coords, fix_x, fix_y) {
            var coords = coords || this.coords;
            var newpos = this.putCoords(coords);
            this.coords = coords;
            this.updateListeners();
//            var mypos = this.pos;
//            var dpos = {x: newpos.x-mypos.x, y: newpos.y-mypos.y};

//            if (fix_x) { dpos.x = 0; };
//            if (fix_y) { dpos.y = 0; };
//            this.translateBy(dpos);
            this.parent.redraw();
        },
        
        translateBy: function(dpos) {
            if (dpos.x) 
                this.pos.x += dpos.x;
            if (dpos.y)
                this.pos.y += dpos.y;
            this.getCoords();
            this.updateListeners();
        },
        
        updateListeners: function() {
            for (var i in this.listeners) {
                this.listeners[i].update(this.coords);
            }
        },
        
        putCoords: function(coords) {
            var coords = coords || this.coords;
            var pos = {};
            if ('x' in coords) {
                pos.x = this.parent.plot.axes.xaxis.u2p(coords.x);
                pos.x -= this.parent.canvas.offsetLeft;
            }
            if ('y' in coords) {
                pos.y = this.parent.plot.axes.yaxis.u2p(coords.y);
                pos.y -= this.parent.canvas.offsetTop;
            }
            this.pos = pos;
            return pos     
        },
        
        render: function(ctx) {
	        ctx.fillStyle = this.color;
	        ctx.strokeStyle = 'transparent';
            ctx.beginPath();
	        //var coords = this.getCoords();
	        this.putCoords();
	        ctx.fillText('(' + this.coords.x.toFixed(3) + ', ' + this.coords.y.toFixed(3) + ')', this.pos.x, this.pos.y - 5);
	        ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
	        ctx.closePath();
	        ctx.stroke();
	        ctx.fill();
        }
    });
    
    $.jqplot.PluginCenter = function() {};
    $.jqplot.PluginCenter.prototype = new $.jqplot.PluginPoint();
    $.jqplot.PluginCenter.prototype.constructor = $.jqplot.PluginCenter;    
    $.extend($.jqplot.PluginCenter.prototype, {        
        initialize: function(parent, x, y, r) {
            $.jqplot.PluginPoint.prototype.initialize.call(this, parent, x, y, r || 6);
            this.name = 'center';
            this.translatable = false;
        },
        
        render: function(ctx) {
	        ctx.fillStyle = this.color;
	        ctx.strokeStyle = 'transparent';
            ctx.beginPath();
	        //ctx.moveTo(this.x, this.y);
	        var coords = this.coords;
	        this.putCoords();
	        ctx.fillText('(' + coords.x.toFixed(3) + ', ' + coords.y.toFixed(3) + ')', this.pos.x, this.pos.y - 5);
            //ctx.fillText('(' + this.pos.x.toFixed(0) + ', ' + this.pos.y.toFixed(0) + ')', this.pos.x, this.pos.y - 5);
	        ctx.moveTo(this.pos.x + this.r, this.pos.y);
	        ctx.lineTo(this.pos.x, this.pos.y + this.r);
	        ctx.lineTo(this.pos.x - this.r, this.pos.y);
	        ctx.lineTo(this.pos.x, this.pos.y - this.r);
	        ctx.closePath();
	        ctx.stroke();
	        ctx.fill();
        },

        onDrag: function(e, pos) {
            $.jqplot.PluginPoint.prototype.onDrag.call(this, e, pos);
            if (this.parent.translatable) {
                this.parent.translateBy(this.dpos);
                this.translateBy(this.dpos);
            };
        }
        
    });
    
    $.jqplot.PolygonInteractorPlugin = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.PolygonInteractorPlugin.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.PolygonInteractorPlugin.prototype.constructor = $.jqplot.PolygonInteractorPlugin;        
    $.jqplot.PolygonInteractorPlugin.prototype.center = $.jqplot.PolygonInteractor.prototype.center;

    
    $.jqplot.RectangleInteractorPlugin = function() { $.jqplot.PolygonInteractorPlugin.call(this); };
    $.jqplot.RectangleInteractorPlugin.prototype = new $.jqplot.PolygonInteractorPlugin();
    $.jqplot.RectangleInteractorPlugin.prototype.constructor = $.jqplot.RectangleInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.Rectangle = $.jqplot.RectangleInteractorPlugin;
    
    $.jqplot.RectangleInteractorPlugin.prototype.init = function(options) {
        $.jqplot.PolygonInteractorPlugin.prototype.init.call(this, options);
        this.p1 = new $.jqplot.PluginPoint(); this.p1.initialize(this, 0, 4.0);
        this.p2 = new $.jqplot.PluginPoint(); this.p2.initialize(this, 6, 4.0);
        this.p3 = new $.jqplot.PluginPoint(); this.p3.initialize(this, 6, -4.0);
        this.p4 = new $.jqplot.PluginPoint(); this.p4.initialize(this, 0, -4.0);
        //this.c = new Center(this, 150, 150);
        
        //this.rect = new $.jqplot.Rectangle(); this.rect.initialize(this, this.p1, this.p3);
        this.l1 = new $.jqplot.Segment(); this.l1.initialize(this, this.p1, this.p2, 4);
        this.l2 = new $.jqplot.Segment(); this.l2.initialize(this, this.p2, this.p3, 4);
        this.l3 = new $.jqplot.Segment(); this.l3.initialize(this, this.p3, this.p4, 4);
        this.l4 = new $.jqplot.Segment(); this.l4.initialize(this, this.p4, this.p1, 4);
        
        if (options.showrect) {
            this.rect = new $.jqplot.Rectangle(); this.rect.initialize(this, this.p1, this.p2, this.p3, this.p4);
            this.grobs.push(this.rect);
        }
        
        this.grobs.push(this.l1, this.l2, this.l3, this.l4, this.p1, this.p2, this.p3, this.p4);
        
        if (options.showcenter) {
            this.c = new $.jqplot.PluginCenter(); this.c.initialize(this, 3, 0);
            this.grobs.push(this.c);
        }
        
        
        var me = this;
        

        this.p1.move = function(dpos) {
            this.translateBy(dpos);
            this.parent.p4.translateBy( {x: dpos.x, y:0} );
            this.parent.p2.translateBy( {x: 0, y: dpos.y} );
        };
        
        this.p2.move = function(dpos) {
            this.translateBy(dpos);
            this.parent.p3.translateBy( {x: dpos.x, y:0} );
            this.parent.p1.translateBy( {x: 0, y: dpos.y} );
        }; 
        
        this.p3.move = function(dpos) {
            this.translateBy(dpos);
            this.parent.p2.translateBy( {x: dpos.x, y:0} );
            this.parent.p4.translateBy( {x: 0, y: dpos.y} );
        }; 
        
        this.p4.move = function(dpos) {
            this.translateBy(dpos);
            this.parent.p1.translateBy( {x: dpos.x, y:0} );
            this.parent.p3.translateBy( {x: 0, y: dpos.y} );
        }; 

        this.l1.connectortranslatable = false;
        this.l1.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.x = 0;
            this.translateBy(this.dpos);
        };
        this.l2.connectortranslatable = false;
        this.l2.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.y = 0;
            this.translateBy(this.dpos);
        };
        this.l3.connectortranslatable = false;
        this.l3.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.x = 0;
            this.translateBy(this.dpos);
        };
        this.l4.connectortranslatable = false;
        this.l4.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.y = 0;
            this.translateBy(this.dpos);
        };
        
        //this.redraw();
    };
    
    $.jqplot.QFromThetaTwotheta = function() {};
    $.jqplot.QFromThetaTwotheta.prototype = new $.jqplot.GrobConnector();
    $.jqplot.QFromThetaTwotheta.prototype.constructor = $.jqplot.QFromThetaTwotheta;
    $.extend($.jqplot.QFromThetaTwotheta.prototype, {
        getQxQz: function(A3, A4, wavelength) { 
            var qLength = 2.0 * Math.PI / wavelength;
            var tilt = A3 - ( A4 / 2.0 );
            var dq = 2.0 * qLength * Math.sin( ( Math.PI / 180.0 ) * ( A4 / 2.0 ) );
            var qxOut = dq * Math.sin( Math.PI * tilt / 180.0 );
            var qzOut = dq * Math.cos( Math.PI * tilt / 180.0 );
            return {x: qxOut, y: qzOut};
        },
        
        initialize: function (parent, p1, p2, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            // convert all the values of theta and twotheta between points 1 and 2
            // (assumed to be corners of a bounding box)
            this.xdim = parent.xdim || 201;
            this.ydim = parent.ydim || 201;
            this.q_points = [];
            this.p1 = p1;
            this.p2 = p2;
            this.updateQPoints();
            this.wavelength = 5.0;
            this.filled = true;
        }, 
        
        updateQPoints: function() {
            this.q_points = [];
            p1coords = this.p1.getCoords();
            p2coords = this.p2.getCoords();
            var xmin = Math.min(p1coords.x, p2coords.x);
            var xmax = Math.max(p1coords.x, p2coords.x);
            var ymin = Math.min(p1coords.y, p2coords.y);
            var ymax = Math.max(p1coords.y, p2coords.y);
            
            var dx = (xmax - xmin) / (this.xdim - 1);
            var dy = (ymax - ymin) / (this.ydim - 1);
            var j = 0;
            for (var i = 0; i<this.xdim-1; i++) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
            for (var j = 0; j<this.ydim-1; j++) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
            for (var i = this.xdim-1; i>0; i--) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
            for (var j = this.ydim-1; j>0; j--) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
//            ctx.save();
//            this.parent.transformCalc();
            
            ctx.beginPath();
            var newpos = this.parent.putCoords(this.q_points[0]);
            //var newpos = this.q_points[0];
            ctx.moveTo(newpos.x, newpos.y);
            for (var i in this.q_points) {
                newpos = this.parent.putCoords(this.q_points[i]);
                //newpos = this.q_points[i];
                ctx.lineTo(newpos.x, newpos.y);
            }
            ctx.closePath();
            ctx.stroke();
            if (this.filled) {
                ctx.globalAlpha = 0.15;
                ctx.fill();
                ctx.globalAlpha = 0.6;
            }
            
            //ctx.restore();
            
        }
    
    });
    
    $.jqplot.QFromThetaTwothetaInteractorPlugin = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.QFromThetaTwothetaInteractorPlugin.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.QFromThetaTwothetaInteractorPlugin.prototype.constructor = $.jqplot.QFromThetaTwothetaInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.QSpace = $.jqplot.QFromThetaTwothetaInteractorPlugin;
    $.extend($.jqplot.QFromThetaTwothetaInteractorPlugin.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.qspace_patch = new $.jqplot.QFromThetaTwotheta();
            this.p1 = options.p1;
            this.p2 = options.p2;
            this.qspace_patch.initialize(this, this.p1, this.p2, 4);
            this.filled = true;
            this.grobs.push(this.qspace_patch);
            //this.redraw();
        },
        
        
        
        update: function() {
            this.qspace_patch.updateQPoints();
            this.redraw();
        }
        
    });
    
    $.jqplot.QGrating = function() {};
    $.jqplot.QGrating.prototype = new $.jqplot.GrobConnector();
    $.jqplot.QGrating.prototype.constructor = $.jqplot.QGrating;
    $.extend($.jqplot.QGrating.prototype, {
        initialize: function (parent, width, autoColor) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'Grating';
            this.colors = $.jqplot.config.defaultColors;
            this.autoColor = autoColor || false;
            this.show_pos = true;
            this.translatable = false;
            this.connectortranslatable = false;
            //this.points = { p1: p1 };
            //this.q_spacing = q_spacing;

            //this.y_center = this.parent.canvas.height / 2;
            //this.x_center = this.parent.canvas.width / 2;
            //this.p1.pos.y = this.y_center;
            
        },
        
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }
            var height = this.parent.canvas.height;
            var width = this.parent.canvas.width;
            var xpos = this.parent.putCoords({x:0, y:0}).x;
            this.x_spacing = Math.abs(this.parent.putCoords({x:this.parent.q_spacing, y:0}).x - xpos);
            var i = 0;
            while (xpos >= 0) {
                ctx.beginPath();
                if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                ctx.moveTo(xpos, 0);
                ctx.lineTo(xpos, height);
                ctx.stroke();
                if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height - 5);   
                xpos -= this.x_spacing;
                i -= 1;
            }
            xpos = this.parent.putCoords({x:0, y:0}).x + this.x_spacing;
            i = 1;
            while (xpos <= width) {
                ctx.beginPath();
                if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                ctx.moveTo(xpos, 0);
                ctx.lineTo(xpos, height);
                ctx.stroke();
                if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height - 5); 
                xpos += this.x_spacing;
                i += 1;
            }
        },
        
        distanceTo: function(c) {
            //return Math.abs(this.parent.putCoords({x:c.x, y:0}).x % this.x_spacing);
        }
    });
    
    $.jqplot.QGratingInteractor = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.QGratingInteractor.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.QGratingInteractor.prototype.constructor = $.jqplot.QGratingInteractor;
    $.jqplot.InteractorPluginSubtypes.QGrating = $.jqplot.QGratingInteractor;
    $.extend($.jqplot.QGratingInteractor.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.q_spacing = 0.001;
            $.extend(this, options);
            this.grating = new $.jqplot.QGrating();
            this.grating.initialize(this, 4, true);
            this.grobs.push(this.grating);
        },
        update: function(pos) {
            this.q_spacing = (pos.x > 0) ? Math.abs(2 * Math.PI / pos.x) : 1e-6; // avoid divide by zero errors
            this.redraw();
        }
    });
    
    $.jqplot.Th2ThFromQGrating = function() {};
    $.jqplot.Th2ThFromQGrating.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Th2ThFromQGrating.prototype.constructor = $.jqplot.Th2ThFromQGrating;
    $.extend($.jqplot.Th2ThFromQGrating.prototype, {
        initialize: function (parent, width, autoColor) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'Grating';
            this.colors = $.jqplot.config.defaultColors;
            this.autoColor = autoColor || false;
            this.show_pos = false;
            this.translatable = false;
            this.connectortranslatable = false;
            //this.points = { p1: p1 };
            //this.q_spacing = q_spacing;

            //this.y_center = this.parent.canvas.height / 2;
            //this.x_center = this.parent.canvas.width / 2;
            //this.p1.pos.y = this.y_center;
            
        },
        
        get_theta_array: function(twotheta, mx, qx_feature, wl) {
            var Q = 4.0 * Math.PI / wl * Math.sin( twotheta_array / 2.0 * (pi / 180.0) )
            qx_target = mx * qx_feature
            mask_2th = (abs(Q) > qx_target)
            Q_masked = Q[mask_2th]
            th = twotheta_array[mask_2th] / 2.0 + arcsin( qx_target / Q[mask_2th] ) * 180.0 / pi
            return twotheta_array[mask_2th], th
        },
        get_wl_twoth: function(qz, mx, qx_feature, theta) {
            var qx = qx_feature * mx;
            var tilt = Math.arctan2(qx, qz);
            var tth = 2.0*(theta*Math.PI/180.0 - tilt);
            var Q = Math.sqrt(Math.pow(qx,2) + Math.pow(qz,2));
            var wl_out = 4*pi/Q * sin(tth/2.0)
            return {x: wl_out, y:tth * 180.0/Math.PI}
        },
        
        get_th_twoth: function (qcoords, wl) {
            //var qx = qx_feature * mx;
            var qx = qcoords.x;
            var qz = qcoords.y;
            var tilt = Math.atan2(qx, Math.abs(qz));
            var Q = Math.sqrt(Math.pow(qx,2) + Math.pow(qz,2));
            var tth = Math.asin(wl * Q / (4 * Math.PI)) * 2.0;
            if (qz < 0) {
                tth *= -1;
                tilt *= -1;
            }
            var th = tth / 2.0 + tilt;
            //2.0*(theta*Math.PI/180.0 - tilt);
            return {x: tth*180.0/Math.PI, y:th * 180.0/Math.PI}
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }
            // have to be careful: this is initialized before the qspace!
            // remember to come back to link qspace to this before rendering page.
            if (this.parent.qspace) {
                //console.log('drawing curvy th-tth lines');
                var height = this.parent.qspace.canvas.height;
                var width = this.parent.qspace.canvas.width;
                var xpos = this.parent.qspace.putCoords({x:0, y:0}).x;
                this.x_spacing = Math.abs(this.parent.qspace.putCoords({x:this.parent.qspace.q_spacing, y:0}).x - xpos);
                var i = 0, pos, prevcoords, coords;
                while (xpos >= 0) {
                    ctx.beginPath();
                    if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                    coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:0}), this.parent.wavelength);
                    pos = this.parent.putCoords(coords);
                    prevcoords = coords;
                    ctx.moveTo(pos.x, pos.y);
                    for (var j = 0; j < this.parent.subsegments; j++) {
                        var y = j/this.parent.subsegments * this.parent.qspace.canvas.height;
                        coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:y}), this.parent.wavelength);
                        pos = this.parent.putCoords(coords);
                        if (coords.x != 0 && (prevcoords.x / coords.x > 0)) ctx.lineTo(pos.x, pos.y);
                        else { ctx.stroke(); ctx.beginPath(); ctx.moveTo(pos.x, pos.y); } 
                        prevcoords = coords;
                    }
                    ctx.stroke();
                    //if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height);   
                    xpos -= this.x_spacing;
                    i -= 1;
                }
                xpos = this.parent.qspace.putCoords({x:0, y:0}).x + this.x_spacing;
                i = 1;
                while (xpos <= width) {
                    ctx.beginPath();
                    if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                    coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:0}), this.parent.wavelength);
                    pos = this.parent.putCoords(coords);
                    prevcoords = coords;
                    ctx.moveTo(pos.x, pos.y);
                    for (var j = 0; j < this.parent.subsegments; j++) {
                        var y = j/this.parent.subsegments * this.parent.qspace.canvas.height;
                        coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:y}), this.parent.wavelength);
                        pos = this.parent.putCoords(coords);
                        if (coords.x != 0 && (prevcoords.x / coords.x > 0)) ctx.lineTo(pos.x, pos.y);
                        else { ctx.stroke(); ctx.beginPath(); ctx.moveTo(pos.x, pos.y); } 
                        prevcoords = coords;
                    }
                    ctx.stroke();
                    //if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height); 
                    xpos += this.x_spacing;
                    i += 1;
                }
            }
        },
        
        distanceTo: function(c) {
            //return Math.abs(this.parent.putCoords({x:c.x, y:0}).x % this.x_spacing);
        }
    });
    
    $.jqplot.Th2ThFromQGratingInteractor = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.Th2ThFromQGratingInteractor.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.Th2ThFromQGratingInteractor.prototype.constructor = $.jqplot.Th2ThFromQGratingInteractor;
    $.jqplot.InteractorPluginSubtypes.Th2ThFromQGrating = $.jqplot.Th2ThFromQGratingInteractor;
    $.extend($.jqplot.Th2ThFromQGratingInteractor.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            //this.q_spacing = 0.001;
            this.qspace = options.qspace || null;
            this.subsegments = 201;
            this.wavelength = 5.0;
            $.extend(this, options);
            this.grating = new $.jqplot.Th2ThFromQGrating();
            this.grating.initialize(this, 4, true);
            this.grobs.push(this.grating);
        },
        update: function(pos) {
            this.redraw();
        }
    });
})(jQuery);
