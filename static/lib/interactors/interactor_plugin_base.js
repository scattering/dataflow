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
    
    $.jqplot.InteractorPlugin = function() {
        //$.jqplot.Interactor.call(this);
    };
    $.jqplot.InteractorPlugin.prototype = new $.jqplot.Interactor();
    $.jqplot.InteractorPlugin.prototype.constructor = $.jqplot.InteractorPlugin;
    $.extend($.jqplot.InteractorPlugin.prototype, {
        // options: name, icon, state, plot
        init: function(options) {
            //name, icon, state, plot) {
            //console.log("nInteractor init", this, options);
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
            this.show = true;
            $.extend(true, this, options);
        },
        
        points: function() {
            var points = [];
            for (var i = 0; i < this.grobs.length; i ++)
                if (this.grobs[i] instanceof $.jqplot.PluginPoint && !(this.grobs[i] instanceof $.jqplot.PluginCenter))
                    points.push(this.grobs[i]);
            return points;
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
        }  
    });

/// begin master interactor plugin

    $.jqplot.MasterInteractorPlugin = function() {
        //$.jqplot.Interactor.call(this);
    };
    $.jqplot.MasterInteractorPlugin.prototype = new $.jqplot.Interactor();
    $.jqplot.MasterInteractorPlugin.prototype.constructor = $.jqplot.MasterInteractorPlugin;
    $.extend($.jqplot.MasterInteractorPlugin.prototype, {
        // options: name, icon, state, plot
        init: function(options) {
            //name, icon, state, plot) {
            //console.log("nInteractor init", this, options);
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
            this.interactors = []; // number of interactors
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
        
        onMouseDown: function(e) {
            this.mousedown = true;
            var pos = this.getMouse(e);
            this.prevpos = pos;
            for (var i = 0; i < this.grobs.length; i ++) {
                var g = this.grobs[i];
                var inside = g.isInside(pos);
                
                if (inside) {
                    //this.prevpos = pos;
                    this.curgrob = i;
                    g.prevpos = pos;
                }
            }
            //console.log('down', /*this.grobs,*/ pos.x, pos.y, 'mousedown=',this.mousedown);
        },
        
        onDoubleClick: function(e) {
            var pos = this.getMouse(e);
            var sel_grob;
            for (var i = 0; i < this.grobs.length; i ++) {
                var g = this.grobs[i];
                var inside = g.isInside(pos);
                
                if (inside) {
                    //this.prevpos = pos;
                    sel_grob = i;
                }
            }
            //console.log("double-clicked:", sel_grob);
        },
        
        redraw: function() {
            this.grobs = [];
            for (var i in this.interactors) {
                var I = this.interactors[i];
                if (I.show) {
                    this.grobs = this.grobs.concat(I.grobs);
                    I.redraw();
                }
            }
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
        
        onMouseMove: function(e) {
            //console.log('mousemove');
            var pos = this.getMouse(e);
            //console.log('move', this.grobs, pos.x, pos.y, this.mousedown);
            var i = 0, inside = false;
            if (this.mousedown) {
                if (this.curgrob) {
                    var cg = this.grobs[this.curgrob];
                    cg.onDrag(e, pos);
                    cg.parent.redraw();
                } else {
                    this.onEmptyDrag(pos);
                }
            } else {
                while (i < this.grobs.length) {
                    var g = this.grobs[i];
                    inside = g.isInside(pos);
                    if (inside) {
                        g.onMouseOver(e);
                        g.parent.onMouseOver(e);
                    } else {
                        if (g.inside) {
                            g.onMouseOut(e);
                            g.parent.onMouseOut(e);
                        }
                    }
                    i++;
                }
            }
            this.redraw();    
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
        var ec = this.eventCanvas._ctx.canvas;
        var master = this.plugins._interactor;
        if (master.interactors.length > 0) {
            master.Canvas = new $.jqplot.GenericCanvas();
            this.eventCanvas._elem.before(master.Canvas.createElement(this._gridPadding, 'jqplot-interactor-canvas', this._plotDimensions));
            master.Canvas.setContext();
            master.context = master.Canvas._ctx;
            master.canvas = master.context.canvas;
            //master.context.globalAlpha = 0.6;
            //master.context.lineJoin = 'round';
            
            ec.onmousemove = bind(master, master.onMouseMove);
            ec.onmousedown = bind(master, master.onMouseDown);
            ec.onmouseup = bind(master, master.onMouseUp);
            ec.onmousewheel = bind(master, master.onMouseWheel);
            ec.ondblclick = bind(master, master.onDoubleClick);
            
            if (!ec._touchstartregistered && ec.addEventListener) {
                ec.addEventListener('touchstart', function(event) {
                    ec.onmousedown(event.touches[0]);
                }, false);
                ec._touchstartregistered = true;
            }
            if (!ec._touchmoveregistered && ec.addEventListener) {
                ec.addEventListener('touchmove', function(event) {
                    event.preventDefault();
                    ec.onmousemove(event.touches[0]);
                }, false);
                ec._touchmoveregistered = true;
            }
            if (!ec._touchendregistered && ec.addEventListener) {
                ec.addEventListener('touchend', function(event) {
                    event.preventDefault();
                    ec.onmouseup(event.touches[0]);
                }, false);
                ec._touchendregistered = true;
            }
            
            if (!ec._scrollregistered && ec.addEventListener) {
                ec.addEventListener('DOMMouseScroll', function(event) {
                    ec.onmousewheel(event);
                });
                ec._scrollregistered = true;
            }
            
            for (var i in this.plugins.interactors) {
                var I = this.plugins.interactors[i];
                //I.Canvas = master.Canvas;
                I.Canvas = new $.jqplot.GenericCanvas();
                this.eventCanvas._elem.before(I.Canvas.createElement(this._gridPadding, 'jqplot-interactor-'+I.name+'-canvas', this._plotDimensions));
                I.Canvas.setContext();
                I.context = I.Canvas._ctx;
                I.canvas = I.context.canvas;
                I.context.globalAlpha = 0.6;
                I.context.lineJoin = 'round';
                //var ec = this.eventCanvas._ctx.canvas;
                
                //this.eventCanvas._elem.before(I.Canvas.createElement(this._gridPadding, 'jqplot-interactor-canvas', this._plotDimensions));
                //I.redraw(); // first one updates the pos (in pixel units) of everything;
                //I.redraw(); // second one finishes the draw.
            }
            master.redraw();
            master.redraw();
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
        if (options.interactors) {
            if (!this.plugins.interactors) this.plugins.interactors = {};
            this.plugins._interactor = new $.jqplot.MasterInteractorPlugin();
            this.plugins._interactor.init();
            this.plugins._interactor.plot = this;
            this.plugins._interactor.name = "master";
            
            
            for (var i in options.interactors) {
                var iopts = options.interactors[i];
                var itype = iopts.type;
                var name = iopts.name || String(this.plugins.interactors.length);
                var newi = new $.jqplot.InteractorPluginSubtypes[itype]();
                this.plugins.interactors[name] = newi;
                newi.init(iopts);
                newi.plot = this;
                //for (var j in newi.grobs) {
                //    this.plugins._interactor.grobs.push(newi.grobs[j]);
                //}
                this.plugins._interactor.interactors.push(newi);
            }
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
                this.parent.redraw();
            };
        }
        
    });
    
    $.jqplot.PolygonInteractorPlugin = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.PolygonInteractorPlugin.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.PolygonInteractorPlugin.prototype.constructor = $.jqplot.PolygonInteractorPlugin;        
    $.jqplot.PolygonInteractorPlugin.prototype.center = $.jqplot.PolygonInteractor.prototype.center;

    
    
    
})(jQuery);
