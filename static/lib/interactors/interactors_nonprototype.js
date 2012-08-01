// #####################
// # INTERACTORS       #
// # by Ophir Lifshitz #
// # Aug, 2011         #
// #####################
debug = false;

(function($) {
    function toArray(obj) {
        return Array.prototype.slice.call(obj);
    };
    
    function bind(scope, fn) {
        return function () {
            return fn.apply(scope, toArray(arguments));
        };
    };

    $.jqplot.Interactor = function(){
    };
    
    // called with scope of a series
    $.jqplot.Interactor.prototype = {
    init: function(name, icon, state, canvasid, notMaster) {
        //console.log("nInteractor init", this, name, icon, state, canvasid)
        this.name = name;
        this.icon = icon;
        this.state = state;
        this.translatable = true;
        this.notMaster = notMaster || false;
        
        this.canvas = document.getElementById(canvasid);
        this.context = this.getContext(canvasid);
        this.context.globalAlpha = 0.6;
        this.context.lineJoin = 'round'
        this.grobs = [];
        this.mousedown = false;
        this.curgrob = null;
        
        this.color1 = '#69f';
        this.color2 = '#f69';
        this.color = this.color1;
        
        this.rc = 1;//Math.random();
        
        //this.canvas.onmouseover = this.onMouseOver.bind(this);
        //this.canvas.onmousemove = this.onMouseMove.bind(this);
        if (!this.notMaster) {
            this.canvas.onmousemove = bind(this, this.onMouseMove);
            this.canvas.onmousedown = bind(this, this.onMouseDown);
            this.canvas.onmouseup   = bind(this, this.onMouseUp);
        }
    },

    getMouse: function(e) {
	    var t = e.target;
	    var x = e.clientX + (window.pageXOffset || 0);
	    var y = e.clientY + (window.pageYOffset || 0);
	    do
		    x -= t.offsetLeft + parseInt(t.style.borderLeftWidth || 0),
		    y -= t.offsetTop  + parseInt(t.style.borderTopWidth  || 0);
	    while (t = t.offsetParent);
	
	    return { x: x, y: y };
    },
    
    getContext: function(id) {
        var elem = document.getElementById(id);
        if (!elem || !elem.getContext) {
            if (debug) { console.log('no elem or elem.getContext', elem, id); }
            return;
        }

        // Get the canvas 2d context.
        var context = elem.getContext('2d');
        if (!context) {
            return;
        }
        return context;
    },

    redraw: function() {
        if (!this.notMaster) { this.context.clearRect(0, 0, this.canvas.width, this.canvas.height); }
        for (var i = 0; i < this.grobs.length; i ++) {
            var grob = this.grobs[i];
            grob.render(this.context);
        }
    },
    
    dupdate: function(maxmoves, movenum) {
        // take current state and update until self-consistent, 
        // up to a maximum number of moves = maxmoves.
        var maxmoves = maxmoves || 10;
        var movenum = movenum || 0;
        var moves = [];
        for (var i = 0; i < this.grobs.length; i++) {
            var dpos = this.grobs[i].calc_update();
            moves.push(Math.pow(dpos.x, 2) + Math.pow(dpos.y, 2));
        }
        movenum++;
        if ((Math.max(moves) == 0) || (movenum >= maxmoves)) {
            for (var i = 0; i < this.grobs.length; i++) {
                this.grobs[i].translateBy({});
            }
        }
        // recurse;
    },
    
    update: function() {
        for (var i = 0; i < this.grobs.length; i ++) {
            var grob = this.grobs[i];
            grob.update();
        }
    },
    
    points: function() {
        var points = [];
        for (var i = 0; i < this.grobs.length; i ++)
            if (this.grobs[i] instanceof $.jqplot.Point && !(this.grobs[i] instanceof $.jqplot.Center))
                points.push(this.grobs[i]);
        return points;
    },
    center: function() {
        if (this.c)
            return this.c.pos;
        return { x: null, y: null };
    },
    translateBy: function(dpos) {
        for (var i = 0; i < this.grobs.length; i ++) {
            if (this.grobs[i].translatable)
                this.grobs[i].translateBy(dpos);
        }
    },

    
    onMouseOver: function(e) {
        this.canvas.style.cursor = 'move';
        this.color = this.color2;
    },
    onMouseOut: function(e) {
        this.canvas.style.cursor = 'auto';
        this.color = this.color1;
    },
    onMouseMove: function(e) {
        //console.log('mousemove');
        var pos = this.getMouse(e);
        //console.log('move', this.grobs, pos.x, pos.y, this.mousedown);
        var i = 0, inside = false;
        while (i < this.grobs.length) {
            var g = this.grobs[i];
            inside = g.isInside(pos);
            //if (inside)
            //console.log(i, g, 'pos', pos, inside, g.inside);
            
            if (this.mousedown && i == this.curgrob) {
                g.onDrag(e, pos);
                this.onDrag(e, pos);
            } 
            else {
                if (inside) {
                    g.onMouseOver(e);
                    this.onMouseOver(e);
                    
                }
                else if (!inside && g.inside) {
                    g.onMouseOut(e);
                    this.onMouseOut(e);
                }
            }
            i ++;
        }
        if (this.mousedown && this.curgrob == null) {
            this.onEmptyDrag(pos);
        };
        this.redraw();
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
            }
        }
        //console.log('down', /*this.grobs,*/ pos.x, pos.y, 'mousedown=',this.mousedown);
    },
    onMouseUp:   function(e) {
        this.mousedown = false;
        var pos = this.getMouse(e);
        this.prevpos = null;
        if (this.curgrob != null) {
            this.grobs[this.curgrob].onDrop(e, pos);
            this.onDrop(e, pos);
        }
        this.curgrob = null;
        //console.log('up  ', /*this.grobs,*/ pos.x, pos.y, 'mousedown=',this.mousedown);
        this.redraw();
    },
    onDrag: function(pos) {
        if (this.c) {
            var new_c = this.center();
            var dpos = {x: new_c.x - this.c.pos.x, y: new_c.y - this.c.pos.y}
            this.c.translateBy(dpos);
        }
    },
    onEmptyDrag: function(pos) {},
    onDrop: function(e, pos) {},
    onDoubleClick: function(pos) {}
    
};


    $.jqplot.PolygonInteractor = function() {
        $.jqplot.Interactor.call(this);
    };
    
    $.jqplot.PolygonInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.PolygonInteractor.prototype.constructor = $.jqplot.PolygonInteractor;
        

    $.jqplot.PolygonInteractor.prototype.center = function() {
        var area = 0;
        var points = this.points();
        var j = points.length - 1;
        var x = 0, y = 0, d, xavg = 0, yavg = 0;
        
        for (var i = 0; i < points.length; j = i ++) {
            d = (points[i].pos.x * points[j].pos.y) - (points[i].pos.y * points[j].pos.x);
            area += d;
            x += (points[i].pos.x + points[j].pos.x) * d;
            y += (points[i].pos.y + points[j].pos.y) * d;
            xavg += points[i].pos.x;
            yavg += points[i].pos.y;
        }
        
        if (area != 0) {
            area /= 2;
            d = area * 6;
            return { x: x / d, y: y / d };
        }
        else {
            return { x: xavg / points.length, y: yavg / points.length };
        }
    }
    

    $.jqplot.SegmentInteractor = function() {
        $.jqplot.PolygonInteractor.call(this)
    };
    
    $.jqplot.SegmentInteractor.prototype = new $.jqplot.PolygonInteractor();
    $.jqplot.SegmentInteractor.prototype.constructor = $.jqplot.SegmentInteractor;
    
    $.jqplot.SegmentInteractor.prototype.init = function(canvasid) {
        $.jqplot.PolygonInteractor.prototype.init.call(this, 'Segment', 'segment.png', 0, canvasid);
               
        var p1 = new $.jqplot.Point(); p1.initialize(this, 100, 150);
        var p2 = new $.jqplot.Point(); p2.initialize(this, 200, 150);
        //var l = new Segment(this, p1, p2, 4);
        var l = new $.jqplot.Segment(); l.initialize(this, p1, p2, 4);
        this.grobs.push(l, p1, p2);
        
        this.redraw();
    };
    
    $.jqplot.QuadrangleInteractor = function() {
        $.jqplot.PolygonInteractor.call(this)
    };
    
    $.jqplot.QuadrangleInteractor.prototype = new $.jqplot.PolygonInteractor();
    $.jqplot.QuadrangleInteractor.prototype.constructor = $.jqplot.QuadrangleInteractor;
    
    $.jqplot.QuadrangleInteractor.prototype.init = function(canvasid) {
        $.jqplot.PolygonInteractor.prototype.init.call(this, 'Quadrangle', 'quad.png', 0, canvasid);
               
        var p1 = new $.jqplot.Point(); p1.initialize(this, 100, 100);
        var p2 = new $.jqplot.Point(); p2.initialize(this, 200, 150);
        var p3 = new $.jqplot.Point(); p3.initialize(this, 200, 200);
        var p4 = new $.jqplot.Point(); p4.initialize(this, 100, 200);
        var l1 = new $.jqplot.Segment(); l1.initialize(this, p1, p2, 4);
        var l2 = new $.jqplot.Segment(); l2.initialize(this, p2, p3, 4);
        var l3 = new $.jqplot.Segment(); l3.initialize(this, p3, p4, 4);
        var l4 = new $.jqplot.Segment(); l4.initialize(this, p4, p1, 4);
        this.grobs.push(l1, l2, l3, l4, p1, p2, p3, p4);
        var c = new $.jqplot.Center(); c.initialize(this, 144 + 4/9, 161 + 1/9);
        this.grobs.push(c);
        this.c = c;
        
        this.redraw();
    };
    
    $.jqplot.ParallelogramInteractor = function() {
        $.jqplot.PolygonInteractor.call(this)
    };
    
    $.jqplot.ParallelogramInteractor.prototype = new $.jqplot.PolygonInteractor();
    $.jqplot.ParallelogramInteractor.prototype.constructor = $.jqplot.ParallelogramInteractor;
    
    $.jqplot.ParallelogramInteractor.prototype.init = function(canvasid) {
        $.jqplot.PolygonInteractor.prototype.init.call(this, 'Parallelogram', 'pgram.png', 0, canvasid);
               
        this.p1 = new $.jqplot.Point(); this.p1.initialize(this, 120, 100);
        this.p2 = new $.jqplot.Point(); this.p2.initialize(this, 220, 100);
        this.p3 = new $.jqplot.Point(); this.p3.initialize(this, 200, 200);
        this.p4 = new $.jqplot.Point(); this.p4.initialize(this, 100, 200);
        this.c = new $.jqplot.Center(); this.c.initialize(this, 160, 150);
        this.l1 = new $.jqplot.Segment(); this.l1.initialize(this, this.p1, this.p2, 4);
        this.l2 = new $.jqplot.Segment(); this.l2.initialize(this, this.p2, this.p3, 4);
        this.l3 = new $.jqplot.Segment(); this.l3.initialize(this, this.p3, this.p4, 4);
        this.l4 = new $.jqplot.Segment(); this.l4.initialize(this, this.p4, this.p1, 4);
        this.grobs.push(this.l1, this.l2, this.l3, this.l4, this.c, this.p1, this.p2, this.p3, this.p4);
        
        this.p1.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);         
            this.parent.p3.pos.x -= this.dpos.x;
            this.parent.p3.pos.y -= this.dpos.y;
        };
        this.p2.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p4.pos.x -= this.dpos.x;
            this.parent.p4.pos.y -= this.dpos.y;
        };
        this.p3.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p1.pos.x -= this.dpos.x;
            this.parent.p1.pos.y -= this.dpos.y;
        };
        this.p4.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p2.pos.x -= this.dpos.x;
            this.parent.p2.pos.y -= this.dpos.y;
        };
        
        this.redraw();
    };

    $.jqplot.RectangleInteractor = function() {
        $.jqplot.PolygonInteractor.call(this)
    };
    
    $.jqplot.RectangleInteractor.prototype = new $.jqplot.PolygonInteractor();
    $.jqplot.RectangleInteractor.prototype.constructor = $.jqplot.RectangleInteractor;
    
    $.jqplot.RectangleInteractor.prototype.init = function(canvasid) {
        $.jqplot.PolygonInteractor.prototype.init.call(this, 'Rectangle', 'rect.png', 0, canvasid);
        this.p1 = new $.jqplot.Point(); this.p1.initialize(this, 100, 100);
        this.p2 = new $.jqplot.Point(); this.p2.initialize(this, 200, 100);
        this.p3 = new $.jqplot.Point(); this.p3.initialize(this, 200, 200);
        this.p4 = new $.jqplot.Point(); this.p4.initialize(this, 100, 200);
        //this.c = new Center(this, 150, 150);
        this.c = new $.jqplot.Center(); this.c.initialize(this, 150, 150);
        this.l1 = new $.jqplot.Segment(); this.l1.initialize(this, this.p1, this.p2, 4);
        this.l2 = new $.jqplot.Segment(); this.l2.initialize(this, this.p2, this.p3, 4);
        this.l3 = new $.jqplot.Segment(); this.l3.initialize(this, this.p3, this.p4, 4);
        this.l4 = new $.jqplot.Segment(); this.l4.initialize(this, this.p4, this.p1, 4);
        this.grobs.push(this.l1, this.l2, this.l3, this.l4, this.c, this.p1, this.p2, this.p3, this.p4);
        
        this.p1.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p4.pos.x += this.dpos.x;
            this.parent.p2.pos.y += this.dpos.y;
            this.parent.c.pos.x += this.dpos.x / 2.0;
            this.parent.c.pos.y += this.dpos.y / 2.0;
        };
        this.p2.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p3.pos.x += this.dpos.x;
            this.parent.p1.pos.y += this.dpos.y;
        };
        this.p3.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p2.pos.x += this.dpos.x;
            this.parent.p4.pos.y += this.dpos.y;
        };
        this.p4.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            this.parent.p1.pos.x += this.dpos.x;
            this.parent.p3.pos.y += this.dpos.y;
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
        
        this.redraw();
    };
    
    $.jqplot.CircleInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.CircleInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.CircleInteractor.prototype.constructor = $.jqplot.CircleInteractor;
    
    $.jqplot.CircleInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Circle', 'circ.png', 0, canvasid);
        var c = new $.jqplot.Center(); c.initialize(this, 150, 150);
        var p1 = new $.jqplot.Point(); p1.initialize(this, 200, 150);
        var circ = new $.jqplot.Circle(); circ.initialize(this, c, p1, 4);
        this.grobs.push(circ, c, p1);
        
        this.redraw();
    };
    
    $.jqplot.AnnulusInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.AnnulusInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.AnnulusInteractor.prototype.constructor = $.jqplot.AnnulusInteractor;
    
    $.jqplot.AnnulusInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Annulus', 'annulus.png', 0, canvasid);
        this.showdata = false;
        this.c = new $.jqplot.Center(); this.c.initialize(this, 150, 150);
        this.p1 = new $.jqplot.Point(); this.p1.initialize(this, 200, 150);
        this.p2 = new $.jqplot.Point(); this.p2.initialize(this, 250, 150);
        this.circ1 = new $.jqplot.Circle(); this.circ1.initialize(this, this.c, this.p1, 4);
        this.circ2 = new $.jqplot.Circle(); this.circ2.initialize(this, this.c, this.p2, 4);
        this.grobs.push(this.circ1, this.circ2, this.c, this.p1, this.p2);
        
        this.p1.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            var r = dist(this.parent.p2.pos, this.parent.c.pos),
                t_ = this.parent.circ1.angleToXaxis(pos);
            this.parent.p2.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
            this.parent.p2.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
        };
        this.p2.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            var r = dist(this.parent.p1.pos, this.parent.c.pos),
                t_ = this.parent.circ1.angleToXaxis(pos);
            this.parent.p1.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
            this.parent.p1.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
        };
        this.circ1.filled = false;
        this.circ1.connectortranslatable = false;
        this.circ1.onDrag = function(e, pos) {
            $.jqplot.Circle.prototype.onDrag.call(this, e, pos);
            
            this.parent.translateBy(this.dpos);
            this.c.translateBy(this.dpos);
        };
        this.circ2.filled = false;
        this.circ2.connectortranslatable = false;
        this.circ2.onDrag = function(e, pos) {
            $.jqplot.Circle.prototype.onDrag.call(this, e, pos);
            
            this.parent.translateBy(this.dpos);
            this.c.translateBy(this.dpos);
        };
        
        this.redraw();
    };
    
    $.jqplot.AnnulusInteractor.prototype.redraw = function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        if (this.showdata) {
            this.context.globalAlpha = 1;
            this.context.drawImage(sansimg, 30, 30, 68, 68, 0, 0, this.canvas.width, this.canvas.height);
            this.context.globalAlpha = 0.6;
        }
        for (var i = 0; i < this.grobs.length; i ++) {
            var grob = this.grobs[i];
            grob.render(this.context);
        }
    };
    
    $.jqplot.ArcInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.ArcInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.ArcInteractor.prototype.constructor = $.jqplot.ArcInteractor;
    
    $.jqplot.ArcInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Arc', 'arc.png', 0, canvasid);
        var c = new $.jqplot.Center(); c.initialize(this, 150, 150);
        var p1 = new $.jqplot.Point(); p1.initialize(this, 200, 150);
        var p2 = new $.jqplot.Point(); p2.initialize(this, 150, 100);
        var arc = new $.jqplot.Arc(); arc.initialize(this, c, p1, p2, 4);
        this.grobs.push(arc, c, p1, p2);
        this.c = c;
        this.p1 = p1;
        this.p2 = p2;
        this.arc = arc;
        
        this.redraw();
    };
    
    $.jqplot.LinearInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.LinearInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.LinearInteractor.prototype.constructor = $.jqplot.LinearInteractor;
    
    $.jqplot.LinearInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Linear', 'linear.png', 0, canvasid);        
        var p1 = new $.jqplot.Point(); p1.initialize(this, 200, 150);
        var p2 = new $.jqplot.Point(); p2.initialize(this, 100, 100);
        this.linear = new $.jqplot.Linear(); this.linear.initialize(this, p1, p2, 4);
        this.grobs.push(this.linear, p1, p2);
        
        this.redraw();
    };
    
    $.jqplot.QuadraticInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.QuadraticInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.QuadraticInteractor.prototype.constructor = $.jqplot.QuadraticInteractor;    
    $.jqplot.QuadraticInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Quadratic', 'quadratic.png', 0, canvasid);
        var p1 = new $.jqplot.Point(); p1.initialize(this, 200, 150);
        var p2 = new $.jqplot.Point(); p2.initialize(this, 150, 100);
        var p3 = new $.jqplot.Point(); p3.initialize(this, 100, 150);
        this.quadratic = new $.jqplot.Quadratic(); this.quadratic.initialize(this, p1, p2, p3, 4);
        this.grobs.push(this.quadratic, p1, p2, p3);
        
        this.redraw();
    };
    
    $.jqplot.GaussianInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.GaussianInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.GaussianInteractor.prototype.constructor = $.jqplot.GaussianInteractor;    
    $.extend($.jqplot.GaussianInteractor.prototype, {
        init: function(canvasid) {
            $.jqplot.Interactor.prototype.init.call(this, 'Gaussian', 'gaussian.png', 0, canvasid);
            var pw = new $.jqplot.Point(); pw.initialize(this, 200, 200);
            var pk = new $.jqplot.Point(); pk.initialize(this, 150, 100);
            var gaussian = new $.jqplot.Gaussian(); gaussian.initialize(this, pk, pw, 4);
            this.grobs.push(gaussian, pk, pw);
            this.gaussian = gaussian;
            
            this.redraw();
        }
    });

    $.jqplot.Grob = function() {};
    $.jqplot.Grob.prototype = {
        initialize: function(parent, x, y, color1, color2) {
            this.parent = parent;
            this.pos = { x: x, y: y };

            this.inside = false;
            this.translatable = true;
            this.prevpos = null;
            this.dpos = null;
            
            var h = this.parent.rc * 360;
            this.color1 = color1 || this.parent.color1 || '#000';'hsl('+h+',100%,40%)'; //'#2C8139';
            this.color2 = color2 || this.parent.color2 || '#444';'hsl('+h+',100%,60%)'; //'#4CCC60';
            this.color = this.color1;
            this.listeners = [];
        },
        
        calc_update: function() {
            // make self-consistent with other grobs
            // overload in children, returning the calculated
            // dpos.
            this.dpos = {x:0, y:0};
            return {x:0, y:0}
        },
           
        move: function(dpos) {
            this.translateBy(dpos);
        },
        
        update: function(pos, fix_x, fix_y) {
            var newpos = this.putCoords ? this.putCoords(pos) : pos;
            var mypos = this.pos;
            var dpos = {x: newpos.x-mypos.x, y: newpos.y-mypos.y};

            if (fix_x) { dpos.x = 0; };
            if (fix_y) { dpos.y = 0; };
            this.translateBy(dpos);
            this.parent.redraw();
        },
        
        isInside: function(pos) {},
        distanceTo: function(pos) {
            return dist(this.pos, pos);
        },
        translateBy: function(dpos) {
            if (dpos.x) 
                this.pos.x += dpos.x;
            if (dpos.y)
                this.pos.y += dpos.y;
            this.updateListeners();
        },
        
        updateListeners: function() {
            for (var i in this.listeners) {
                var pos = this.getCoords? this.getCoords() : this.pos;
                this.listeners[i].update(pos);
            }
        },
        
        render: function(ctx) {},
        
        onDrag: function(e, pos) {
            if (!this.prevpos)
                this.prevpos = this.parent.prevpos;
            var dx = pos.x - this.prevpos.x,
                dy = pos.y - this.prevpos.y;
            this.dpos = { x: dx, y: dy };
            if (this.translatable) {
                this.move(this.dpos);
                this.parent.onDrag(this.dpos);
//                var alreadyUpdated = [this];
//                this.translateBy(this.dpos);
//                var update_pos = this.getCoords ? this.getCoords() : this.pos;
//                console.log('update_pos:', update_pos);
//                this.updateListeners(alreadyUpdated, false, false);
                this.parent.redraw()
            }    
            this.prevpos = pos;
        },
        onDrop: function(e, pos) {
            this.prevpos = null;
            this.dpos = null;
        },
        onMouseOver: function(e) { this.inside = true;  this.color = this.color2; },
        onMouseOut: function(e)  { this.inside = false; this.color = this.color1; }
    };
    
    $.jqplot.GrobConnector = function() {};
    $.jqplot.GrobConnector.prototype = new $.jqplot.Grob();
    $.jqplot.GrobConnector.prototype.constructor = $.jqplot.GrobConnector; 
    $.extend($.jqplot.GrobConnector.prototype, {
        initialize: function(parent, width) {
            $.jqplot.Grob.prototype.initialize.call(this, parent, null, null);
            this.name = 'grobconnector';
            this.translatable = false;
            this.connectortranslatable = true;
            this.points = {};
            this.width = width;
        },
        render: function(ctx) {
            ctx.strokeStyle = this.color;
            ctx.fillStyle = this.color;
            ctx.lineWidth = this.width;
        },
        
        isInside: function(pos) {
            return this.distanceTo(pos) <= this.width + 1;
        },
        translateBy: function(dpos) {
            for (var p in this.points)
                this.points[p].translateBy(dpos);
        },
        onDrag: function(e, pos) {
            $.jqplot.Grob.prototype.onDrag.call(this, e, pos);
            
            //console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ') dpos (', this.dpos.x, this.dpos.y, ')');
            if (this.connectortranslatable)
                this.translateBy(this.dpos);
            this.parent.onDrag(this.dpos);
            this.parent.redraw();
        }
    });
    
    $.jqplot.Segment = function() {};
    $.jqplot.Segment.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Segment.prototype.constructor = $.jqplot.Segment;    
    $.extend($.jqplot.Segment.prototype, {        
        initialize: function (parent, p1, p2, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            
            this.name = 'segment';
            this.points = { p1: p1, p2: p2 };
            this.p1 = p1;
            this.p2 = p2;
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);

            ctx.beginPath();
            ctx.moveTo(this.p1.pos.x, this.p1.pos.y);
            ctx.lineTo(this.p2.pos.x, this.p2.pos.y);
            ctx.closePath();
            ctx.stroke();
        },
        
        cross: function(c) {
            return (this.p2.pos.x - this.p1.pos.x) * (c.y - this.p1.pos.y) - (this.p2.pos.y - this.p1.pos.y) * (c.x - this.p1.pos.x);
        },
        dot: function(c) {
            return (this.p2.pos.x - this.p1.pos.x) * (c.x - this.p1.pos.x) + (this.p2.pos.y - this.p1.pos.y) * (c.y - this.p1.pos.y);
        },
        distanceTo: function(c) {
            var d = 0,
                v1 = this.dot(c),
                v2 = this.dot(this.p2.pos);
                
            if (v1 < 0)
                d = dist(this.p1.pos, c);
            else if (v1 > v2)
                d = dist(this.p2.pos, c);
            else
                d = Math.abs(this.cross(c) / dist(this.p1.pos, this.p2.pos));
            
            return d;
        },
        
        onMouseOver: function(e) {
            $.jqplot.GrobConnector.prototype.onMouseOver.call(this, e);
        },
        onMouseOut: function(e) {
            $.jqplot.GrobConnector.prototype.onMouseOut.call(this, e);
        }
    });
    
    $.jqplot.VerticalLine = function() {};
    $.jqplot.VerticalLine.prototype = new $.jqplot.GrobConnector();
    $.jqplot.VerticalLine.prototype.constructor = $.jqplot.VerticalLine;    
    $.extend($.jqplot.VerticalLine.prototype, {        
        initialize: function (parent, p1, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            
            this.name = 'vertline';
            this.points = { p1: p1 };
            this.p1 = p1;
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            var height = ctx.canvas.height;
            ctx.beginPath();
            ctx.moveTo(this.p1.pos.x, 0);
            ctx.lineTo(this.p1.pos.x, height);
            ctx.closePath();
            ctx.stroke();
        },
        
        distanceTo: function(c) {
            return (Math.abs(this.pos.x - c.x));
        },
        
        onMouseOver: function(e) {
            $.jqplot.GrobConnector.prototype.onMouseOver.call(this, e);
        },
        onMouseOut: function(e) {
            $.jqplot.GrobConnector.prototype.onMouseOut.call(this, e);
        }
    });
    
    $.jqplot.HorizontalLine = function() {};
    $.jqplot.HorizontalLine.prototype = new $.jqplot.GrobConnector();
    $.jqplot.HorizontalLine.prototype.constructor = $.jqplot.HorizontalLine;    
    $.extend($.jqplot.HorizontalLine.prototype, {        
        initialize: function (parent, p1, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            
            this.name = 'horizline';
            this.points = { p1: p1 };
            this.p1 = p1;
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.beginPath();
            ctx.moveTo(0, this.p1.pos.y);
            ctx.lineTo(width, this.p1.pos.y);
            ctx.closePath();
            ctx.stroke();
        },
        
        distanceTo: function(c) {
            return (Math.abs(this.pos.y - c.y));
        },
        
        onMouseOver: function(e) {
            $.jqplot.GrobConnector.prototype.onMouseOver.call(this, e);
        },
        onMouseOut: function(e) {
            $.jqplot.GrobConnector.prototype.onMouseOut.call(this, e);
        }
    });
    
    $.jqplot.Point = function() {};
    $.jqplot.Point.prototype = new $.jqplot.Grob();
    $.jqplot.Point.prototype.constructor = $.jqplot.Point;    
    $.extend($.jqplot.Point.prototype, {        
        initialize: function (parent, x, y, r) {
            $.jqplot.Grob.prototype.initialize.call(this, parent, x, y);          
            this.name = 'point';
            this.r = r || 6;
            this.show_pos = true;
        },
        
        render: function(ctx) {
	        ctx.fillStyle = this.color;
	        ctx.strokeStyle = 'transparent';
            ctx.beginPath();
	        //ctx.moveTo(this.x, this.y);
	        if (this.show_pos) {
                ctx.fillText('(' + this.pos.x.toFixed(0) + ', ' + this.pos.y.toFixed(0) + ')', this.pos.x, this.pos.y - 5);
	        }
	        ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
	        ctx.closePath();
	        ctx.stroke();
	        ctx.fill();
        },

        isInside: function(pos) {
            return this.distanceTo(pos) <= this.r;
        },
        
        onMouseOver: function(e) {
            $.jqplot.Grob.prototype.onMouseOver.call(this, e);
        },
        onMouseOut: function(e) {
            $.jqplot.Grob.prototype.onMouseOut.call(this, e);
        },
        onDrag: function(e, pos) {
            $.jqplot.Grob.prototype.onDrag.call(this, e, pos);
            //if (this.translatable)
            //    this.translateBy(this.dpos);
        }
    });
    
    $.jqplot.Circle = function() {};
    $.jqplot.Circle.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Circle.prototype.constructor = $.jqplot.Circle;    
    $.extend($.jqplot.Circle.prototype, {        
        initialize: function(parent, c, p1, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'circle';
            this.points = { p1: p1, c: c };
            this.p1 = p1;
            this.c = c;
            //this.c.parent = this;
            this.filled = true;
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            
            ctx.beginPath();
            ctx.arc(this.c.pos.x, this.c.pos.y, dist(this.c.pos, this.p1.pos), 0, 2 * Math.PI, true);
            ctx.closePath();
            ctx.stroke();
            if (this.filled) {
                ctx.globalAlpha = 0.15;
                ctx.fill();
                ctx.globalAlpha = 0.6;
            }
            
        },
        
        angleToXaxis: function(p) {
            return Math.atan2(p.y - this.c.pos.y, p.x - this.c.pos.x);
        },
        isInside: function(pos) {
            var dd = dist(this.c.pos, pos) - dist(this.c.pos, this.p1.pos);
            if (!this.filled)
                dd = Math.abs(dd);
            return dd <= this.width + 1;
        }
    });
    
    $.jqplot.Rectangle = function() {};
    $.jqplot.Rectangle.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Rectangle.prototype.constructor = $.jqplot.Rectangle;    
    $.extend($.jqplot.Rectangle.prototype, {        
        initialize: function(parent, p1, p2, p3, p4, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'rectangle';
            this.points = { p1: p1, p2: p2, p3: p3, p4: p4 };
            // this assumes that p1 and p3 are opposite corners! 
            this.p1 = p1;
            this.p3 = p3;
            //this.c.parent = this;
            this.filled = true;
        },
        
        findOppositeCorner: function(point) {
            var d = 0;
            var opp = point;
            for (var i in this.points) {
                var newd = dist(this.points[i], point);
                if (newd > d) {
                    d = newd;
                    opp = this.points[i];
                }
            }
            return opp
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            
            ctx.beginPath();
            ctx.moveTo(this.p1.pos.x, this.p1.pos.y);
            ctx.lineTo(this.p3.pos.x, this.p1.pos.y);
            ctx.lineTo(this.p3.pos.x, this.p3.pos.y);
            ctx.lineTo(this.p1.pos.x, this.p3.pos.y);
            ctx.lineTo(this.p1.pos.x, this.p1.pos.y);
            ctx.closePath();
            ctx.stroke();
            if (this.filled) {
                ctx.globalAlpha = 0.15;
                ctx.fill();
                ctx.globalAlpha = 0.6;
            }
            
        },
        
        isInside: function(pos) {
            var sizex = this.p1.pos.x - this.p3.pos.x;
            var sizey = this.p1.pos.y - this.p3.pos.y;
            var dx = this.p1.pos.x - pos.x;
            var dy = this.p1.pos.y - pos.y;
            var betweenx = (dx == 0) || (sizex / dx > 1.0);
            var betweeny = (dy == 0) || (sizey / dy > 1.0);
            if (this.filled && betweenx && betweeny)
                return true;
            if (betweenx) {
                if (Math.abs(pos.y - this.p1.pos.y) <= this.width + 1) return true;
                if (Math.abs(pos.y - this.p3.pos.y) <= this.width + 1) return true;
            }
            if (betweeny) {
                if (Math.abs(pos.x - this.p1.pos.x) <= this.width + 1) return true;
                if (Math.abs(pos.x - this.p3.pos.x) <= this.width + 1) return true;
            }
            return false;
        }
    });
    
    $.jqplot.Center = function() {};
    $.jqplot.Center.prototype = new $.jqplot.Point();
    $.jqplot.Center.prototype.constructor = $.jqplot.Center;    
    $.extend($.jqplot.Center.prototype, {        
        initialize: function(parent, x, y, r) {
            $.jqplot.Point.prototype.initialize.call(this, parent, x, y, r || 6);
            this.name = 'center';
            this.translatable = false;
        },
        
        render: function(ctx) {
	        ctx.fillStyle = this.color;
	        ctx.strokeStyle = 'transparent';
            ctx.beginPath();
	        //ctx.moveTo(this.x, this.y);
            ctx.fillText('(' + this.pos.x.toFixed(0) + ', ' + this.pos.y.toFixed(0) + ')', this.pos.x, this.pos.y - 5);
	        ctx.moveTo(this.pos.x + this.r, this.pos.y);
	        ctx.lineTo(this.pos.x, this.pos.y + this.r);
	        ctx.lineTo(this.pos.x - this.r, this.pos.y);
	        ctx.lineTo(this.pos.x, this.pos.y - this.r);
	        ctx.closePath();
	        ctx.stroke();
	        ctx.fill();
        },

        onDrag: function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            
            //console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', this.dpos.dx, this.dpos.dy, dist(this.parent.p1.pos, this.pos), dist(this.parent.p2.pos, this.pos));
            if (this.parent.translatable) {
                this.parent.translateBy(this.dpos);
                this.translateBy(this.dpos);
            };
        }
        
    });
    
    $.jqplot.Arc = function() {};
    $.jqplot.Arc.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Arc.prototype.constructor = $.jqplot.Arc;    
    $.extend($.jqplot.Arc.prototype, {        
        initialize: function(parent, c, p1, p2, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            
            p1.onDrag = function(e, pos) {
                $.jqplot.Point.prototype.onDrag.call(this, e, pos);
                
                var r = dist(this.pos, this.parent.c.pos),
                    t_ = this.parent.arc.angleToXaxis(this.parent.p2.pos);
                this.parent.p2.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
                this.parent.p2.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
            };
            p2.onDrag = function(e, pos) {
                $.jqplot.Point.prototype.onDrag.call(this, e, pos);
                
                var r = dist(this.pos, this.parent.c.pos),
                    t_ = this.parent.arc.angleToXaxis(this.parent.p1.pos);
                this.parent.p1.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
                this.parent.p1.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
            };
            
            this.name = 'arc';
            this.points = { c: c, p1: p1, p2: p2 };
            this.p1 = p1;
            this.p2 = p2;
            this.c = c;
        },
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            
            ctx.beginPath();
            var t_1 = this.angleToXaxis(this.p1.pos),
                t_2 = this.angleToXaxis(this.p2.pos);
            //console.log(t_1, t_2);
            //ctx.moveTo(this.c.pos.x, this.c.pos.y);
            ctx.arc(this.c.pos.x, this.c.pos.y, dist(this.c.pos, this.p1.pos), t_1, t_2, true);
            //ctx.closePath();
            ctx.stroke();
            //ctx.globalAlpha = 0.15;
            //ctx.fill();
            //ctx.globalAlpha = 0.6;
        },
        
        angleToXaxis: function(p) {
            return Math.atan2(p.y - this.c.pos.y, p.x - this.c.pos.x);
        },
        angleBetweenAngles: function(n, a, b) {
            n = (360 + (n % 360)) % 360;
            a = (3600000 + a) % 360;
            b = (3600000 + b) % 360;

            if (a < b)
                return a <= n && n <= b;
            return 0 <= n && n <= b || a <= n && n < 360;
        },
        distanceTo: function(pos) {
            var d = 0,
                t_1 = this.angleToXaxis(this.p1.pos),
                t_2 = this.angleToXaxis(this.p2.pos),
                t_  = this.angleToXaxis(pos);
            var between = this.angleBetweenAngles(t_, t_2, t_1);
            //console.log(t_, t_1, t_2, between);
                
            if (between)
                d = Math.abs(dist(this.c.pos, pos) - dist(this.c.pos, this.p1.pos));
            else
                d = Math.min(dist(this.p1.pos, pos), dist(this.p2.pos, pos));
            
            return d;
        }
    });
    
    $.jqplot.FunctionConnector = function() {};
    $.jqplot.FunctionConnector.prototype = new $.jqplot.GrobConnector();
    $.jqplot.FunctionConnector.prototype.constructor = $.jqplot.FunctionConnector;    
    $.extend($.jqplot.FunctionConnector.prototype, {        
        initialize: function(parent, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);            
            this.f = null;
        },
        distanceTo: function(pos) {
            
            var f = bind(this, (function(x) { return dist(pos, { x: x, y: this.c.pos.y - this.f(x) }); }));
            var df = nDeriv(f),
                d2f = nDeriv(df),
                x0 = pos.x,
                prevxs = [],
                min = [],
                minx = null;
            
            for (x0 = 0; x0 < this.parent.canvas.width; x0 += 1)
              if (minx == null || f(x0) < f(minx))
                minx = x0;
            min = root_bisect(df, minx - 4, minx + 4, 0.1);
            
            /*
            //console.log(min[0], f(min[0]));
            min = root_bisect(df, 0, this.parent.canvas.width);
            min = root_newtons(df, d2f, min[0]);*/
            var x = min[0], prevxs = min[1];
            
            var fpos = { x: x, y: this.c.pos.y - this.f(x) };
            var d = dist(pos, fpos);
            //console.log('pos (',pos.x, pos.y,') fpos (',fpos.x.toFixed(2), fpos.y.toFixed(2), ') x =',x ,'d =', d);
            return d;
        },
        drawEq: function (ctx, eq, x0, y0, xmin, xmax, pm) {
            var tmp = ctx.strokeStyle;
            var prevcolor = newcolor = null;
            ctx.beginPath();
            for (var i = xmin - 1; i <= xmax + 1; i ++) {
                var y = eq(i);
                if (pm) {
                    prevcolor = newcolor;
                    newcolor = (y >= 0) ? 'red' : 'blue';
                    if (prevcolor != null && prevcolor != newcolor) {
                        var h = i - 1 + y / (eq(i - 1) - y);
                        //ctx.lineTo(h, y0);
                        ctx.lineTo(i, y0 - 1);
                        ctx.strokeStyle = prevcolor;
                        ctx.stroke();
                        ctx.beginPath();
                        //ctx.moveTo(h, y0);
                        ctx.moveTo(i - 1, y0 - eq(i - 1));
                        ctx.lineTo(i, y0 - y);
                    }
                    else
                        ctx.lineTo(i, y0 - y);
                }
                else
                    ctx.lineTo(i, y0 - y);
            }
            if (pm)
                ctx.strokeStyle = prevcolor;
            ctx.stroke();
            //ctx.lineWidth = 1; ctx.moveTo(0,y0); ctx.lineTo(ctx.canvas.width,y0); ctx.stroke();
            ctx.strokeStyle = tmp;
        }      
    });
    
    $.jqplot.Linear = function() {};
    $.jqplot.Linear.prototype = new $.jqplot.FunctionConnector();
    $.jqplot.Linear.prototype.constructor = $.jqplot.Linear;    
    $.extend($.jqplot.Linear.prototype, {        
        initialize: function(parent, p1, p2, width) {
            $.jqplot.FunctionConnector.prototype.initialize.call(this, parent, width);

            this.name = 'Linear';
            this.f = this.linear;
            this.points = { p1: p1, p2: p2 };
            this.p1 = p1;
            this.p2 = p2;
            this.c = p1;
        },
        render: function(ctx) {
            $.jqplot.FunctionConnector.prototype.render.call(this, ctx);
            
            // Vertical lines
            if (this.p1.pos.x == this.p2.pos.x) {
                ctx.beginPath();
                ctx.moveTo(this.p1.pos.x, 0);
                ctx.lineTo(this.p2.pos.x, this.parent.canvas.height);
                ctx.closePath();
                ctx.stroke();
            }
            else
                this.drawEq(ctx, bind(this, this.f), 0, this.c.pos.y, 0, this.parent.canvas.width);
        },
        
        linear: function(x) {
            var X1 = this.p1.pos.x, X2 = this.p2.pos.x,
                Y1 = this.c.pos.y - this.p1.pos.y, Y2 = this.c.pos.y - this.p2.pos.y;
            var a = (Y2-Y1) / (X2-X1),
                b = Y1 - a*X1;
                
            return a*x+b;
        },
        // Overriding super because the computation here is much simpler
        distanceTo: function(pos) {
            var X1 = this.p1.pos.x, X2 = this.p2.pos.x,
                Y1 = this.c.pos.y - this.p1.pos.y, Y2 = this.c.pos.y - this.p2.pos.y;
            
            var d = 0;
            // Vertical lines
            if (X1 == X2)
                d = Math.abs(pos.x - X1);
            else {
                var a = (Y2-Y1) / (X2-X1),
                    b = Y1 - a*X1;
                
                d = Math.abs(-a * pos.x + this.c.pos.y - pos.y - b) / Math.sqrt(a * a);
            }
            return d;
        }
    });
    
    $.jqplot.Quadratic = function() {};
    $.jqplot.Quadratic.prototype = new $.jqplot.FunctionConnector();
    $.jqplot.Quadratic.prototype.constructor = $.jqplot.Quadratic;    
    $.extend($.jqplot.Quadratic.prototype, {        
        initialize: function(parent, p1, p2, p3, width) {
            $.jqplot.FunctionConnector.prototype.initialize.call(this, parent, width);
            this.name = 'quadratic';
            this.f = this.quadratic;
            this.points = { p1: p1, p2: p2, p3: p3 };
            this.p1 = p1;
            this.p2 = p2;
            this.p3 = p3;
            this.c = p1;
        },
        render: function(ctx) {
            $.jqplot.FunctionConnector.prototype.render.call(this, ctx);
            
            this.drawEq(ctx, bind(this, this.f), 0, this.c.pos.y, 0, this.parent.canvas.width);
        },
        
        quadratic: function(x) {
            var X1 = this.p1.pos.x, X2 = this.p2.pos.x, X3 = this.p3.pos.x,
                Y1 = this.c.pos.y - this.p1.pos.y, Y2 = this.c.pos.y - this.p2.pos.y, Y3 = this.c.pos.y - this.p3.pos.y;
            var a = ((Y2-Y1)*(X1-X3) + (Y3-Y1)*(X2-X1))/((X1-X3)*(X2*X2-X1*X1) + (X2-X1)*(X3*X3-X1*X1)),
                b = ((Y2-Y1) - a*(X2*X2-X1*X1)) / (X2-X1),
                c = Y1 - a*X1*X1 - b*X1;
                
            return a*x*x+b*x+c;
        }
    });
    
    $.jqplot.Gaussian = function() {};
    $.jqplot.Gaussian.prototype = new $.jqplot.FunctionConnector();
    $.jqplot.Gaussian.prototype.constructor = $.jqplot.Gaussian;    
    $.extend($.jqplot.Gaussian.prototype, {        
        initialize: function(parent, pk, pw, width) {
            $.jqplot.FunctionConnector.prototype.initialize.call(this, parent, width);
            
            this.name = 'gaussian';
            this.f = this.gaussian;
            this.points = { pk: pk, pw: pw };
            this.pk = pk;
            this.pw = pw;
            this.c = pw;
        },
        render: function(ctx) {
            $.jqplot.FunctionConnector.prototype.render.call(this, ctx);
            this.drawEq(ctx, bind(this, this.f), 0, this.c.pos.y, 0, this.parent.canvas.width);
        },
        
        gaussian: function(x) {
            var peakX = this.pk.pos.x,
                peakY = this.c.pos.y - this.pk.pos.y,
                FWHM = Math.abs(this.c.pos.x - peakX),
                bkgdY = 0;
            var stdDev = FWHM / 2 / Math.sqrt(2 * Math.log(2));
            //return - peakY + Math.pow(x - 150, 2) / 100;
            return bkgdY + (peakY - bkgdY) * Math.exp(- Math.pow((x - peakX), 2) / 2 / Math.pow(stdDev, 2));
        }
    });
    
    $.jqplot.dist = function(a, b) {
        return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
    };
    
    var dist = $.jqplot.dist;
    
})(jQuery);



function d_dist_f(pos, x, f) {
    var y = f(x);
    return ((nDeriv(f))(x) * (y - pos.y) + (x - pos.x)) / dist(pos, { x: x, y: y });
}

function nDeriv(f) {
    var h = 1e-3;
    var df = function(x) { return (f(x + h) - f(x - h)) / 2 / h; };
    df.f = f;
    return df;
}
function root_bisect(f, a, b, tol) {
    var maxiters = 20, tol = tol || 0.5, x, prevxs = [];
    var iter = 0;
    while (Math.abs(b - a) > tol && iter < maxiters) {
      x = (a + b) / 2;
      prevxs.push(x);
      if (f(x) == 0)
        break;
      else if ((f(a) * f(x)) < 0)
        b = x;
      else
        a = x;
      iter ++;
    }
    //console.log(iter, x, f(x));
    return [x, prevxs];
}
function root_newtons(f, df, x0) {
    var maxiters = 40, tol = 1, v;
    var x = x0, prevx = null, prevxs = [];
    var g = function(x) { newx = x - f(x) / df(x); /*f1=f;df1=df;console.log('x=',x, 'f(x)=',f(x), 'f\'(x)=',df(x), 'newx=',newx);*/ return newx; };
    
    //console.log('start minimize');
    var iter = 0;
    while (prevx == null || Math.abs(x - prevx) > tol && iter < maxiters) {
        prevx = x;
        prevxs.push(prevx);
        x = g(x);
        iter ++;
    }
    //console.log(prevxs);
    //console.log('end minimize');
    return [x, prevxs];
}
