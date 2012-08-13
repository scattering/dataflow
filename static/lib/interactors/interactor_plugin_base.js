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
    
    var touchToMouse = function(event) {
        //if (event.touches.length > 1) return; //allow default multi-touch gestures to work
        var touch = event.changedTouches[0];
        touch.data = event.data;
        var type = "";
        
        switch (event.type) {
        case "touchstart": 
            type = "mousedown"; break;
        case "touchmove":  
            type="mousemove";   break;
        case "touchend":   
            type="mouseup";     break;
        default: 
            return;
        }
        
        // https://developer.mozilla.org/en/DOM/event.initMouseEvent for API
        var simulatedEvent = document.createEvent("MouseEvent");
        simulatedEvent.initMouseEvent(type, true, true, window, 1, 
                touch.screenX, touch.screenY, 
                touch.clientX, touch.clientY, false, 
                false, false, false, 0, null);
        
        touch.target.dispatchEvent(simulatedEvent);
        event.preventDefault();
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
            this.notMaster = true;

            this.grobs = [];
            this.mousedown = false;
            this.curgrob = null;
            
            this.color1 = '#6699ff';
            this.color2 = '#ff6699';
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
        
        reset: function() {
            for (var i=0; i<this.grobs.length; i++) {
                var g = this.grobs[i];
                if (g.reset) g.reset();
            }
        },
        
        redraw: function() {
            // unlike the non-plugin interactors, each plugin interactor has
            // its own context and canvas, so clear them at each redraw:
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            if (this.show) {
                for (var i = 0; i < this.grobs.length; i ++) {
                    var grob = this.grobs[i];
                    grob.render(this.context);
                }
            }
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
            
            this.color1 = '#6699ff';
            this.color2 = '#ff6699';
            this.color = this.color1;
            
            this.rc = 1;//Math.random();
            this.scrollZoom = true;
            this.dragPan = true;
            $.extend(true, this, options);
            this.notMaster = false;
            this.interactors = []; // number of interactors
            this.generate_ticks = generate_ticks;
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
            var coords = { x: this.plot.series[0]._xaxis.p2u(xpixel),
                           y: this.plot.series[0]._yaxis.p2u(ypixel) }
            return coords
        },
        
        putCoords: function(coords) {
            var pos = {};
            if ('x' in coords) {
                pos.x = this.plot.series[0]._xaxis.u2p(coords.x);
                pos.x -= this.canvas.offsetLeft;
            }
            if ('y' in coords) {
                pos.y = this.plot.series[0]._yaxis.u2p(coords.y);
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
        
        handleMouseDown: function(ev, gridpos, datapos, neighbor, plot) {
            console.log(this);
            this.mousedown = true;
            var pos = gridpos;
            var coords = datapos;
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
        },
        
        onDoubleClick: function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            var pos = this.getMouse(e);
            var sel_grob = null;
	    var sel_grob_num = null;
	    //console.log(pos);
            for (var i = 0; i < this.grobs.length; i ++) {
                var g = this.grobs[i];
                var inside = g.isInside(pos);
                
                if (inside) {
                    //this.prevpos = pos;
                    sel_grob_num = i;
		    sel_grob = g;
                }
            }
            //console.log("double-clicked:", sel_grob.parent);
            if (sel_grob_num == null) {
                // then we're double-clicking outside all the interactors
                this.zoomMax();
            } else {
	    	sel_grob.parent.onDoubleClick(sel_grob, pos);
                //this.redraw();
                //this.redraw();
            }
                
            return false;
        },
        
        reset: function() {
            for (var i=0; i<this.grobs.length; i++) {
                var g = this.grobs[i];
                if (g.reset) g.reset();
            }
        },
        
        redraw: function() {
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
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
            if (this.scrollZoom) {
                if (e.preventDefault) e.preventDefault();
                if (e.stopPropagation) e.stopPropagation();
                var pos = this.getMouse(e);
                var dzoom;
                if (e.wheelDelta) { dzoom = e.wheelDelta; }
                else if (e.detail) { dzoom = e.detail * -40; }
                else { dzoom = 0 } 
                this.zoomPlot(dzoom, pos);
            }
        },
        
        onMouseMove: function(e) {
            //console.log('mousemove');
            var pos = this.getMouse(e);
            //console.log('move', this.grobs, pos.x, pos.y, this.mousedown);
            var i = 0, inside = false;
            if (this.mousedown) {
                if (this.curgrob != null) {
                    var cg = this.grobs[this.curgrob];
                    cg.onDrag(e, pos);
                    //cg.parent.redraw();
                    this.redraw();
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
                        this.redraw();
                    } else {
                        if (g.inside) {
                            g.onMouseOut(e);
                            g.parent.onMouseOut(e);
                            this.redraw();
                        }
                    }
                    i++;
                }
            }
            //this.redraw();    
        },
        
        onEmptyDrag: function(pos) {
            if (this.dragPan == true) this.panPlot(pos);
        },
        
        zoomMax: function() {
	    var xdb = this.plot.series[0]._xaxis._dataBounds;
	    var ydb = this.plot.series[0]._yaxis._dataBounds;
	    if ((xdb.min != null) && (xdb.max != null) && (ydb.min != null) && (ydb.max != null)) {
                // zoom to the limits of the data, with good tick locations
                var xmin = xdb.min;
                var xmax = xdb.max;
                var ymin = ydb.min;
                var ymax = ydb.max;
                var xtransf = this.plot.series[0]._xaxis.transform || 'lin';
                var ytransf = this.plot.series[0]._yaxis.transform || 'lin';
                this.plot.series[0]._xaxis.ticks = generate_ticks({min:xmin, max:xmax}, xtransf);
                this.plot.series[0]._yaxis.ticks = generate_ticks({min:ymin, max:ymax}, ytransf);
                this.plot.replot();
            }
        },
        
        zoomPlot: function(dzoom, centerpos) {
            var center = this.getCoords(centerpos);
            // make a zoom of 120 = 10% change in axis limits
            var conv = dzoom * 0.2/120;
            
            var xtransf = this.plot.series[0]._xaxis.transform || 'lin';
            var ytransf = this.plot.series[0]._yaxis.transform || 'lin';
            var xmin = this.plot.series[0]._xaxis.min;
            var xmax = this.plot.series[0]._xaxis.max;
            if (!this.fix_x) {
                xmin += (center.x - xmin) * conv;
                xmax += (center.x - xmax) * conv;
            }
            if (!this.fix_y) {
                var ymin = this.plot.series[0]._yaxis.min;
                var ymax = this.plot.series[0]._yaxis.max;
            }
            ymin += (center.y - ymin) * conv;
            ymax += (center.y - ymax) * conv;
            this.plot.series[0]._xaxis.ticks = generate_ticks({min:xmin, max:xmax}, xtransf);
            this.plot.series[0]._yaxis.ticks = generate_ticks({min:ymin, max:ymax}, ytransf);
            this.plot.redraw();
        },
        
        panPlot: function(pos) {
            var newcoords = this.getCoords(pos);
            var prevcoords = this.getCoords(this.prevpos);
            this.prevpos = pos;
            var xtransf = this.plot.series[0]._xaxis.transform || 'lin';
            var ytransf = this.plot.series[0]._yaxis.transform || 'lin';
            var dx = newcoords.x - prevcoords.x;
            var dy = newcoords.y - prevcoords.y;
            var xmin = this.plot.series[0]._xaxis.min - dx;
            var xmax = this.plot.series[0]._xaxis.max - dx;
            var ymin = this.plot.series[0]._yaxis.min - dy;
            var ymax = this.plot.series[0]._yaxis.max - dy;
            this.plot.series[0]._xaxis.ticks = generate_ticks({min:xmin, max:xmax}, xtransf);
            this.plot.series[0]._yaxis.ticks = generate_ticks({min:ymin, max:ymax}, ytransf);
            this.plot.redraw();
        }
    });
    
    // called with context of plot
    $.jqplot.InteractorPlugin.postDraw = function() {
        
        var ec = this.eventCanvas._ctx.canvas;
        var master = this.plugins._interactor;
        if (master && master.interactors && master.interactors.length > 0) {
            master.Canvas = new $.jqplot.GenericCanvas();
            this.eventCanvas._elem.before(master.Canvas.createElement(this._gridPadding, 'jqplot-interactor-canvas', this._plotDimensions, this));
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
            ec.onselectstart = function() { return false; };
            
            ec.ontouchstart = touchToMouse;
            ec.ontouchmove = touchToMouse;
            ec.ontouchend = touchToMouse;
            
            /*
            
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
            
            */
            
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
                this.eventCanvas._elem.before(I.Canvas.createElement(this._gridPadding, 'jqplot-interactor-'+I.name+'-canvas', this._plotDimensions, this));
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
    $.jqplot.InteractorPluginSubtypes.standard = $.jqplot.InteractorPlugin;
    
    $.jqplot.InteractorPlugin.pluginit = function (target, data, opts) {
        // add an interactor attribute to the plot
        var options = opts || {};
        if (options.interactors) {
            if (!this.plugins.interactors) this.plugins.interactors = {};
            this.plugins._interactor = new $.jqplot.MasterInteractorPlugin();
            var master_opts = {}
            for (var i in options.interactors) {
                var iopts = options.interactors[i];
                var itype = iopts.type;
                if (itype == 'master') {
                    master_opts = iopts;
                    break
                }
            }
            this.plugins._interactor.init(master_opts);
            this.plugins._interactor.plot = this;
            this.plugins._interactor.name = "master";
            //var master = this.plugins._interactor;
            //this.eventListenerHooks.addOnce('jqplotMouseDown', bind(master, master.handleMouseDown));
            
            
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
            this._x0 = xcoord;
            this._y0 = ycoord;
            this.coords = {x: xcoord, y: ycoord};
        },
        
        reset: function() {
            this.coords = {x: this._x0, y: this._y0};
            this.updateListeners();
        },
        
        getCoords: function(pos) {
            var pos = pos || this.pos;
            this.coords = this.parent.getCoords(pos);
            return this.coords;
        },
        
        update: function(coords, updated_already) {
            if (updated_already && updated_already.indexOf && updated_already.indexOf(this) == -1) {
                var coords = coords || this.coords;
                var newpos = this.putCoords(coords);
                if ('x' in newpos) this.pos.x = newpos.x;
                if ('y' in newpos) this.pos.y = newpos.y;
                this.coords = coords;
                updated_already.push(this);
                this.updateListeners(updated_already);
//            var mypos = this.pos;
//            var dpos = {x: newpos.x-mypos.x, y: newpos.y-mypos.y};

//            if (fix_x) { dpos.x = 0; };
//            if (fix_y) { dpos.y = 0; };
//            this.translateBy(dpos);
                this.parent.redraw();
            }
        },
        
        translateBy: function(dpos) {
            if (dpos.x) 
                this.pos.x += dpos.x;
            if (dpos.y)
                this.pos.y += dpos.y;
            this.coords = this.getCoords();
            this.updateListeners();
        },
        
        updateListeners: function(updated_already) {
            var updated_already = updated_already || [this];
            for (var i in this.listeners) {
                this.listeners[i].update(this.coords, updated_already);
            }
        },
        
        putCoords: function(coords, setPos) {
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
	    if (setPos) { this.pos = pos; } 
            return pos     
        },
        
        render: function(ctx) {
	        ctx.fillStyle = this.color;
	        ctx.strokeStyle = 'transparent';
            ctx.beginPath();
	        //var coords = this.getCoords();
	        this.pos = this.putCoords();
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
	        this.pos = this.putCoords();
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

    function bestLinearInterval(range) {
        var expv = Math.floor(Math.log(range)/Math.LN10);
        var magnitude = Math.pow(10, expv);
        var f = range / magnitude;

        if (f<=1.6) {return 0.2*magnitude;}
        if (f<=4.0) {return 0.5*magnitude;}
        if (f<=8.0) {return magnitude;}
        return 2*magnitude; 
    };
    
    function generateLinearTicks(min, max) {
        var ticks = [];
        var tickInterval = bestLinearInterval(max-min);
        var expv = Math.floor(Math.log(tickInterval)/Math.LN10);
        var magnitude = Math.pow(10, expv);

        ticks.push([min, ' ']);
        var tick = min - mod(min, tickInterval) + tickInterval;
        while (tick < max) {
            if (Math.abs(tick) < 1e-13) tick = 0;
            var sigdigits = Math.ceil(Math.log(Math.abs(tick)/magnitude)/Math.LN10) - 1;
            var numdigits = Math.floor(Math.log(Math.abs(tick))/Math.LN10) + 1;
            if (sigdigits > 20) sigdigits = 20;
            if (sigdigits < 0) sigdigits = 0;
            if (numdigits < 4 && numdigits >= -2) {
                var fixeddigits;
                if (sigdigits < numdigits) { fixeddigits = 0; }
                else { fixeddigits = sigdigits - numdigits + 1; }
                ticks.push([tick, tick.toFixed(fixeddigits)]);
            } else {
                ticks.push([tick, tick.toExponential(sigdigits)]);
            }
            tick += tickInterval;
        }
        ticks.push([max,' ']);
        return ticks
    };
    
    function nextLogTick(val, round) {
        // finds the next log tick above the current value,
        // using 1, 2, 5, 10, 20, ... scaling
        var expv = Math.floor(Math.log(val)/Math.LN10);
        //var expv = Math.floor(val);
        var magnitude = Math.pow(10, expv);
        var f = val / magnitude;
        if (round) f = Math.round(f);
        
        var newf;
        if      (f<1.0) { newf = 1 }
        else if (f<2.0) { newf = 2 }
        else if (f<5.0) { newf = 5 }
        else if (f<10.0) { newf = 10 }
        else { newf = 20 };
        return {value: newf * magnitude, label: newf.toFixed() + 'e' + expv.toFixed()}
        
//        if (f<2.0) {return 2.0*magnitude;}
//        if (f<5.0) {return 5.0*magnitude;}
//        if (f<10.) {return 10.0*magnitude;}
//        return 20*magnitude; 
    };
    
    function prevLogTick(val) {
        // finds the next log tick above the current value,
        // using 1, 2, 5, 10, 20, ... scaling
        var expv = Math.floor(Math.log(val)/Math.LN10);
        //var expv = Math.floor(val);
        var magnitude = Math.pow(10, expv);
        var f = val / magnitude;

        if (f>10.0) {return 10.0*magnitude;}
        if (f>5.0) {return 5.0*magnitude;}
        if (f>2.0) {return 2.0*magnitude;}
        if (f>1.0) {return 1.0*magnitude;}
        return 0.5*magnitude;
    };
    
    function mod(a,b) {
        return a % b < 0 ? b + a % b : a % b
    };
    
    function generate12510ticks(min, max) {
        var ticks = [];
        ticks.push([min, ' ']); // ticks are positioned with log
        var tick = nextLogTick(Math.pow(10, min), false);
        //console.log(tick);
        //var tickpos = tick.value;
        var tickpos = Math.log(tick.value)/Math.LN10;
        var i = 0;
        while( tickpos < max && i < 100 ) {
            
            ticks.push([tickpos, tick.label]);
            tick = nextLogTick(tick.value, true);
            tickpos = Math.log(tick.value)/Math.LN10;
            i++;
        }
        ticks.push([max, ' ']);
        if (ticks.length < 4) {
            var newticks = generateLinearTicks(Math.pow(10, min), Math.pow(10, max));
            newticks[0] = [min, ' '];
            for (var i=1; i<(newticks.length-1); i++) {
                newticks[i][0] = Math.log(newticks[i][0])/Math.LN10;
            }
            newticks[newticks.length-1] = [max, ' '];
            ticks = newticks;
        }
        return ticks
    };
    
    
    function generateMagTicks(min, max, magdiff) {
        var ticks = [];
        ticks.push([min, ' ']); // ticks are positioned with log
        var tick = Math.pow(10, Math.ceil(min/magdiff) * magdiff);
        var tickpos = Math.round(Math.log(tick)/Math.LN10);
        var i = 0;
        while( tickpos < max && i < 100 ) {
            ticks.push([tickpos, '1e'+tickpos.toFixed()]);
            //tick *= Math.pow(10, magdiff);
            tickpos = Math.round(tickpos + magdiff);
            i++;
        }
        ticks.push([max, ' ']);
        return ticks
    };
    
    
    function generate_ticks(ticklimits, transform) {
        var transform = transform || 'lin';
        var min = ticklimits.min,
            max = ticklimits.max;
        var ticks = [];
        if (transform == 'lin') {
            ticks = generateLinearTicks(min, max);
        } 
        else if (transform == 'log') {
            var scalespan = max - min;
            if (scalespan >= 3) { 
                var magdiff = Math.ceil((scalespan / 5)); // more than five, divide by two.
                ticks = generateMagTicks(min, max, magdiff); 
            } else { ticks = generate12510ticks(min, max); }
        } 
        else {
            // unknown transform - return max and min
            ticks.push(min);
            ticks.push(max);
        }
        return ticks; 
    };
    
    function handleMouseDown(ev, gridpos, datapos, neighbor, plot) {
//            if (neighbor) {
//                var si = neighbor.seriesIndex;
//                var pi = neighbor.pointIndex;
//                var ins = [si, pi, neighbor.data, plot.series[si].gridData[pi][2]];
//                if (plot.series[ins[0]].highlightMouseDown && !(ins[0] == plot.plugins.bubbleRenderer.highlightedSeriesIndex && ins[1] == plot.series[ins[0]]._highlightedPoint)) {
//                    var evt = jQuery.Event('jqplotDataHighlight');
//                    evt.pageX = ev.pageX;
//                    evt.pageY = ev.pageY;
//                    plot.target.trigger(evt, ins);
//                    highlight (plot, ins[0], ins[1]);
//                }
//            }
//            else if (neighbor == null) {
//                unhighlight (plot);
//            }
            console.log(ev, gridpos, datapos, plot);
        };
})(jQuery);
