// ###############
// # INTERACTORS #
// ###############

var Interactor = Class.create({
    initialize: function(name, icon, state, canvasid) {
        this.name = name;
        this.icon = icon;
        this.state = state;
        
        this.canvas = document.getElementById(canvasid);
        this.context = getContext(canvasid);
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
        this.canvas.onmousemove = this.onMouseMove.bind(this);
        this.canvas.onmousedown = this.onMouseDown.bind(this);
        this.canvas.onmouseup   = this.onMouseUp.bind(this);
    },
    redraw: function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        for (var i = 0; i < this.grobs.length; i ++) {
            var grob = this.grobs[i];
            grob.render(this.context);
        }
    },
    
    points: function() {
        var points = [];
        for (var i = 0; i < this.grobs.length; i ++)
            if (this.grobs[i] instanceof Point && !(this.grobs[i] instanceof Center))
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
        var pos = getMouse(e);
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
        this.redraw();
    },
    onMouseDown: function(e) {
        this.mousedown = true;
        var pos = getMouse(e);
        for (var i = 0; i < this.grobs.length; i ++) {
            var g = this.grobs[i];
            var inside = g.isInside(pos);
            
            if (inside) {
                this.prevpos = pos;
                this.curgrob = i;
            }
        }
        //console.log('down', /*this.grobs,*/ pos.x, pos.y, 'mousedown=',this.mousedown);
    },
    onMouseUp:   function(e) {
        this.mousedown = false;
        var pos = getMouse(e);
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
        if (this.c)
            this.c.pos = this.center();
    },
    onDrop: function(e, pos) {
    
    },
});
var PolygonInteractor = new Class.create(Interactor, {
    initialize: function($super, name, icon, state, canvasid) {
        $super(name, icon, state, canvasid);
    },
    center: function() {
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
    },
});
var SegmentInteractor = new Class.create(PolygonInteractor, {
    initialize: function($super, canvasid) {
        $super('Segment', 'segment.png', 0, canvasid);
        
        var p1 = new Point(this, 100, 150);
        var p2 = new Point(this, 200, 150);
        var l = new Segment(this, p1, p2, 4);
        this.grobs.push(l, p1, p2);
        
        this.redraw();
    },
});
var QuadrangleInteractor = new Class.create(PolygonInteractor, {
    initialize: function($super, canvasid) {
        $super('Quadrangle', 'quad.png', 0, canvasid);
        
        var p1 = new Point(this, 100, 100);
        var p2 = new Point(this, 200, 150);
        var p3 = new Point(this, 200, 200);
        var p4 = new Point(this, 100, 200);
        var l1 = new Segment(this, p1, p2, 4);
        var l2 = new Segment(this, p2, p3, 4);
        var l3 = new Segment(this, p3, p4, 4);
        var l4 = new Segment(this, p4, p1, 4);
        this.grobs.push(l1, l2, l3, l4, p1, p2, p3, p4);
        var c = new Center(this, 144 + 4/9, 161 + 1/9);
        this.grobs.push(c);
        this.c = c;
        
        this.redraw();
    },
});
var ParallelogramInteractor = new Class.create(PolygonInteractor, {
    initialize: function($super, canvasid) {
        $super('Parallelogram', 'pgram.png', 0, canvasid);
        
        this.p1 = new Point(this, 120, 100);
        this.p2 = new Point(this, 220, 100);
        this.p3 = new Point(this, 200, 200);
        this.p4 = new Point(this, 100, 200);
        this.c = new Center(this, 160, 150);
        this.l1 = new Segment(this, this.p1, this.p2, 4);
        this.l2 = new Segment(this, this.p2, this.p3, 4);
        this.l3 = new Segment(this, this.p3, this.p4, 4);
        this.l4 = new Segment(this, this.p4, this.p1, 4);
        this.grobs.push(this.l1, this.l2, this.l3, this.l4, this.c, this.p1, this.p2, this.p3, this.p4);
        
        this.p1.onDrag = this.p1.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p3.pos.x -= this.dpos.x;
            this.parent.p3.pos.y -= this.dpos.y;
        });
        this.p2.onDrag = this.p2.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p4.pos.x -= this.dpos.x;
            this.parent.p4.pos.y -= this.dpos.y;
        });
        this.p3.onDrag = this.p3.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p1.pos.x -= this.dpos.x;
            this.parent.p1.pos.y -= this.dpos.y;
        });
        this.p4.onDrag = this.p4.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p2.pos.x -= this.dpos.x;
            this.parent.p2.pos.y -= this.dpos.y;
        });
        
        this.redraw();
    },
});
var RectangleInteractor = new Class.create(PolygonInteractor, {
    initialize: function($super, canvasid) {
        $super('Rectangle', 'rect.png', 0, canvasid);
        
        this.p1 = new Point(this, 100, 100);
        this.p2 = new Point(this, 200, 100);
        this.p3 = new Point(this, 200, 200);
        this.p4 = new Point(this, 100, 200);
        this.c = new Center(this, 150, 150);
        this.l1 = new Segment(this, this.p1, this.p2, 4);
        this.l2 = new Segment(this, this.p2, this.p3, 4);
        this.l3 = new Segment(this, this.p3, this.p4, 4);
        this.l4 = new Segment(this, this.p4, this.p1, 4);
        this.grobs.push(this.l1, this.l2, this.l3, this.l4, this.c, this.p1, this.p2, this.p3, this.p4);
        
        this.p1.onDrag = this.p1.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p4.pos.x += this.dpos.x;
            this.parent.p2.pos.y += this.dpos.y;
        });
        this.p2.onDrag = this.p2.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p3.pos.x += this.dpos.x;
            this.parent.p1.pos.y += this.dpos.y;
        });
        this.p3.onDrag = this.p3.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p2.pos.x += this.dpos.x;
            this.parent.p4.pos.y += this.dpos.y;
        });
        this.p4.onDrag = this.p4.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.p1.pos.x += this.dpos.x;
            this.parent.p3.pos.y += this.dpos.y;
        });
        this.l1.connectortranslatable = false;
        this.l1.onDrag = this.l1.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.dpos.x = 0;
            this.translateBy(this.dpos);
        });
        this.l2.connectortranslatable = false;
        this.l2.onDrag = this.l2.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.dpos.y = 0;
            this.translateBy(this.dpos);
        });
        this.l3.connectortranslatable = false;
        this.l3.onDrag = this.l3.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.dpos.x = 0;
            this.translateBy(this.dpos);
        });
        this.l4.connectortranslatable = false;
        this.l4.onDrag = this.l4.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.dpos.y = 0;
            this.translateBy(this.dpos);
        });
        
        this.redraw();
    },
});
var CircleInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Circle', 'circ.png', 0, canvasid);
        
        var c = new Center(this, 150, 150);
        var p1 = new Point(this, 200, 150);
        var circ = new Circle(this, c, p1, 4);
        this.grobs.push(circ, c, p1);
        
        this.redraw();
    },
});
var AnnulusInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Annulus', 'annulus.png', 0, canvasid);
        
        this.showdata = false;
        this.c = new Center(this, 150, 150);
        this.p1 = new Point(this, 200, 150);
        this.p2 = new Point(this, 250, 150);
        this.circ1 = new Circle(this, this.c, this.p1, 4);
        this.circ2 = new Circle(this, this.c, this.p2, 4);
        this.grobs.push(this.circ1, this.circ2, this.c, this.p1, this.p2);
        
        this.p1.onDrag = this.p1.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            var r = dist(this.parent.p2.pos, this.parent.c.pos),
                t_ = this.parent.circ1.angleToXaxis(pos);
            this.parent.p2.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
            this.parent.p2.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
        });
        this.p2.onDrag = this.p2.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            var r = dist(this.parent.p1.pos, this.parent.c.pos),
                t_ = this.parent.circ1.angleToXaxis(pos);
            this.parent.p1.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
            this.parent.p1.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
        });
        this.circ1.filled = false;
        this.circ1.connectortranslatable = false;
        this.circ1.onDrag = this.circ1.onDrag.wrap(function (callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.translateBy(this.dpos);
            this.c.translateBy(this.dpos);
        });
        this.circ2.filled = false;
        this.circ2.connectortranslatable = false;
        this.circ2.onDrag = this.circ2.onDrag.wrap(function (callOriginal, e, pos) {
            callOriginal(e, pos);
            
            this.parent.translateBy(this.dpos);
            this.c.translateBy(this.dpos);
        });
        
        this.redraw();
    },
    
    redraw: function($super) {
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
    },
});
var ArcInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Arc', 'arc.png', 0, canvasid);
        
        var c = new Center(this, 150, 150);
        var p1 = new Point(this, 200, 150);
        var p2 = new Point(this, 150, 100);
        var arc = new Arc(this, c, p1, p2, 4);
        this.grobs.push(arc, c, p1, p2);
        this.c = c;
        this.p1 = p1;
        this.p2 = p2;
        this.arc = arc;
        
        this.redraw();
    },
});
var LinearInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Linear', 'linear.png', 0, canvasid);
        
        var p1 = new Point(this, 200, 150);
        var p2 = new Point(this, 100, 100);
        this.linear = new Linear(this, p1, p2, 4);
        this.grobs.push(this.linear, p1, p2);
        
        this.redraw();
    },
});
var QuadraticInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Quadratic', 'quadratic.png', 0, canvasid);
        
        var p1 = new Point(this, 200, 150);
        var p2 = new Point(this, 150, 100);
        var p3 = new Point(this, 100, 150);
        this.quadratic = new Quadratic(this, p1, p2, p3, 4);
        this.grobs.push(this.quadratic, p1, p2, p3);
        
        this.redraw();
    },
});
var GaussianInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Gaussian', 'gaussian.png', 0, canvasid);
        
        var pw = new Point(this, 200, 200);
        var pk = new Point(this, 150, 100);
        var gaussian = new Gaussian(this, pk, pw, 4);
        this.grobs.push(gaussian, pk, pw);
        this.gaussian = gaussian;
        
        this.redraw();
    },
    /*
    onMouseMove: function($super, e) {
        $super(e);
        pos = getMouse(e);
        this.gaussian.distanceTo(pos);
    },*/
});


function getMouse(e) {
	var t = e.target;
	var x = e.clientX + (window.pageXOffset || 0);
	var y = e.clientY + (window.pageYOffset || 0);
	do
		x -= t.offsetLeft + parseInt(t.style.borderLeftWidth || 0),
		y -= t.offsetTop  + parseInt(t.style.borderTopWidth  || 0);
	while (t = t.offsetParent);
	
	return { x: x, y: y };
}

// #########
// # GROBS #
// #########

var Grob = Class.create({
    initialize: function(parent, x, y) {
        this.parent = parent;
        this.pos = { x: x, y: y };

        this.inside = false;
        this.translatable = true;
        this.prevpos = null;
        this.dpos = null;
        
        var h = this.parent.rc * 360;
        this.color1 = '#000';'hsl('+h+',100%,40%)'; //'#2C8139';
        this.color2 = '#444';'hsl('+h+',100%,60%)'; //'#4CCC60';
        this.color = this.color1;
    },
    
    isInside: function(pos) {},
    distanceTo: function(pos) {
        return dist(this.pos, pos);
    },
    translateBy: function(dpos) {
        this.pos.x += dpos.x;
        this.pos.y += dpos.y;
    },
    render: function(ctx) {},
    
    onDrag: function(e, pos) {
        if (!this.prevpos)
            this.prevpos = this.parent.prevpos;
        var dx = pos.x - this.prevpos.x,
            dy = pos.y - this.prevpos.y;
        this.dpos = { x: dx, y: dy };
        if (this.translatable)
            this.translateBy(this.dpos);
            
        this.prevpos = pos;
    },
    onDrop: function(e, pos) {
        this.prevpos = null;
        this.dpos = null;
    },
    onMouseOver: function(e) { this.inside = true;  this.color = this.color2; },
    onMouseOut: function(e)  { this.inside = false; this.color = this.color1; },
});

var Point = Class.create(Grob, {
    initialize: function($super, parent, x, y, r) {
        $super(parent, x, y);
        
        this.name = 'point';
        this.r = r || 6;
    },
    
    render: function(ctx) {
	    ctx.fillStyle = this.color;
	    ctx.strokeStyle = 'transparent';
        ctx.beginPath();
	    //ctx.moveTo(this.x, this.y);
        ctx.fillText('(' + this.pos.x.toFixed(0) + ', ' + this.pos.y.toFixed(0) + ')', this.pos.x, this.pos.y - 5);
	    ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
	    ctx.closePath();
	    ctx.stroke();
	    ctx.fill();
    },

    isInside: function(pos) {
        return this.distanceTo(pos) <= this.r;
    },
    
    onMouseOver: function($super, e) {
        $super(e);
    },
    onMouseOut: function($super, e) {
        $super(e);
    },
    onDrag: function($super, e, pos) {
        $super(e, pos);
    },
});
var GrobConnector = Class.create(Grob, {
    initialize: function($super, parent, width) {
        $super(parent, null, null);
        
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
    onDrag: function($super, e, pos) {
        $super(e, pos);
        
        //console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ') dpos (', this.dpos.x, this.dpos.y, ')');
        if (this.connectortranslatable)
            this.translateBy(this.dpos);
    },
});
var Circle = Class.create(GrobConnector, {
    initialize: function($super, parent, c, p1, width) {
        $super(parent, width);
        
        this.name = 'circle';
        this.points = { p1: p1, c: c };
        this.p1 = p1;
        this.c = c;
        this.filled = true;
    },
    
    render: function($super, ctx) {
        $super(ctx);
        
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
    },
});
var Center = Class.create(Point, {
    initialize: function($super, parent, x, y, r) {
        $super(parent, x, y, r || 6);
        
        this.name = 'center';
        this.translatable = false;
    },
    
    render: function($super, ctx) {
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

    onDrag: function($super, e, pos) {
        $super(e, pos);
        
        //console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', this.dpos.dx, this.dpos.dy, dist(this.parent.p1.pos, this.pos), dist(this.parent.p2.pos, this.pos));
        this.parent.translateBy(this.dpos);
        this.translateBy(this.dpos);
    },
});
var Arc = Class.create(GrobConnector, {
    initialize: function($super, parent, c, p1, p2, width) {
        $super(parent, width);
        
        p1.onDrag = p1.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            var r = dist(this.pos, this.parent.c.pos),
                t_ = this.parent.arc.angleToXaxis(this.parent.p2.pos);
            this.parent.p2.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
            this.parent.p2.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
        });
        p2.onDrag = p2.onDrag.wrap(function(callOriginal, e, pos) {
            callOriginal(e, pos);
            
            var r = dist(this.pos, this.parent.c.pos),
                t_ = this.parent.arc.angleToXaxis(this.parent.p1.pos);
            this.parent.p1.pos.x = this.parent.c.pos.x + Math.cos(t_) * r;
            this.parent.p1.pos.y = this.parent.c.pos.y + Math.sin(t_) * r;
        });
        
        this.name = 'arc';
        this.points = { c: c, p1: p1, p2: p2 };
        this.p1 = p1;
        this.p2 = p2;
        this.c = c;
    },
    render: function($super, ctx) {
        $super(ctx);
        
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
    },
});
var FunctionConnector = Class.create(GrobConnector, {
    initialize: function($super, parent, width) {
        $super(parent, width);
        
        this.f = null;
    },
    
    distanceTo: function(pos) {
        var f = (function(x) { return dist(pos, { x: x, y: this.c.pos.y - this.f(x) }); }).bind(this),
            df = nDeriv(f),
            d2f = nDeriv(df),
            x0 = pos.x,
            prevxs = [],
            min = [],
            minx = null;
        
        /*
        for (x0 = 0; x0 < this.parent.canvas.width; x0 += 1) {
          if (!min.length || f(x0) < f(min[0]))
            min[0] = x0;
        }
        x = min[0];
        */
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
        /*
        var tmp = this.parent.context.strokeStyle;
        this.parent.context.strokeStyle = '#999';
        this.parent.context.lineWidth = 2;
        this.parent.context.moveTo(pos.x,this.c.pos.y+300);
        this.parent.context.lineTo(pos.x, pos.y);
        this.parent.context.lineTo(fpos.x, fpos.y);
        this.parent.context.lineTo(x,this.c.pos.y+300);
        this.parent.context.stroke();
        this.parent.context.moveTo(0,this.c.pos.y+200);
        this.parent.context.lineTo(this.parent.canvas.width,this.c.pos.y+200);
        this.parent.context.moveTo(0,this.c.pos.y+300);
        this.parent.context.lineTo(this.parent.canvas.width,this.c.pos.y+300);
        this.parent.context.fillText('y=0', 2, this.c.pos.y+198);
        this.parent.context.fillText('y=0', 2, this.c.pos.y+298);
        this.parent.context.fillText(x.toPrecision(4), x, this.c.pos.y+311);
        this.parent.context.fillText(f(x).toPrecision(4), x, this.c.pos.y-f(x)/10+298);
        this.parent.context.strokeText('d \' ( x )', 2, this.c.pos.y+213);
        this.parent.context.strokeText('d ( x )', 2, this.c.pos.y+313);
        this.parent.context.stroke();
        if (prevxs.length) {
          this.parent.context.strokeStyle = '#ccc';
          this.parent.context.beginPath();
          this.parent.context.moveTo(x0, this.c.pos.y+200);
          for (var i = 0; i < prevxs.length - 1; i ++) {
            this.parent.context.lineTo(prevxs[i], this.c.pos.y-df(prevxs[i])*20+200);
            this.parent.context.lineTo(prevxs[i+1], this.c.pos.y+200);
            this.parent.context.fillText(i, prevxs[i] + 2, this.c.pos.y+194-3*i);
          }
          this.parent.context.stroke();
        }
        
        drawEq(this.parent.context, function(x){ return df(x) * 20; }, this.c.pos.x, this.c.pos.y + 200, 0, this.parent.canvas.width, true);
        drawEq(this.parent.context, function(x){ return f(x) / 10; }, this.c.pos.x, this.c.pos.y + 300, 0, this.parent.canvas.width);
        this.parent.context.strokeStyle = tmp;
        this.parent.context.lineWidth = this.width;*/
        var d = dist(pos, fpos);
        //console.log('pos (',pos.x, pos.y,') fpos (',fpos.x.toFixed(2), fpos.y.toFixed(2), ') x =',x ,'d =', d);
        return d;
    },
    
});

var Linear = Class.create(FunctionConnector, {
    initialize: function($super, parent, p1, p2, width) {
        $super(parent, width);

        this.name = 'Linear';
        this.f = this.linear;
        this.points = { p1: p1, p2: p2 };
        this.p1 = p1;
        this.p2 = p2;
        this.c = p1;
    },
    render: function($super, ctx) {
        $super(ctx);
        
        // Vertical lines
        if (this.p1.pos.x == this.p2.pos.x) {
            ctx.beginPath();
            ctx.moveTo(this.p1.pos.x, 0);
            ctx.lineTo(this.p2.pos.x, this.parent.canvas.height);
            ctx.closePath();
            ctx.stroke();
        }
        else
            drawEq(ctx, this.f.bind(this), 0, this.c.pos.y, 0, this.parent.canvas.width);
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
    },
});
var Quadratic = Class.create(FunctionConnector, {
    initialize: function($super, parent, p1, p2, p3, width) {
        $super(parent, width);

        this.name = 'quadratic';
        this.f = this.quadratic;
        this.points = { p1: p1, p2: p2, p3: p3 };
        this.p1 = p1;
        this.p2 = p2;
        this.p3 = p3;
        this.c = p1;
    },
    render: function($super, ctx) {
        $super(ctx);
        
        drawEq(ctx, this.f.bind(this), 0, this.c.pos.y, 0, this.parent.canvas.width);
    },
    
    quadratic: function(x) {
        var X1 = this.p1.pos.x, X2 = this.p2.pos.x, X3 = this.p3.pos.x,
            Y1 = this.c.pos.y - this.p1.pos.y, Y2 = this.c.pos.y - this.p2.pos.y, Y3 = this.c.pos.y - this.p3.pos.y;
        var a = ((Y2-Y1)*(X1-X3) + (Y3-Y1)*(X2-X1))/((X1-X3)*(X2*X2-X1*X1) + (X2-X1)*(X3*X3-X1*X1)),
            b = ((Y2-Y1) - a*(X2*X2-X1*X1)) / (X2-X1),
            c = Y1 - a*X1*X1 - b*X1;
            
        return a*x*x+b*x+c;
    },
});
    
var Gaussian = Class.create(FunctionConnector, {
    initialize: function($super, parent, pk, pw, width) {
        $super(parent, width);
        
        this.name = 'gaussian';
        this.f = this.gaussian;
        this.points = { pk: pk, pw: pw };
        this.pk = pk;
        this.pw = pw;
        this.c = pw;
    },
    render: function($super, ctx) {
        $super(ctx);
        
        drawEq(ctx, this.f.bind(this), 0, this.c.pos.y, 0, this.parent.canvas.width);
    },
    
    gaussian: function(x) {
        var peakX = this.pk.pos.x,
            peakY = this.c.pos.y - this.pk.pos.y,
            FWHM = Math.abs(this.c.pos.x - peakX),
            bkgdY = 0;
        var stdDev = FWHM / 2 / Math.sqrt(2 * Math.log(2));
        //return - peakY + Math.pow(x - 150, 2) / 100;
        return bkgdY + (peakY - bkgdY) * Math.exp(- Math.pow((x - peakX), 2) / 2 / Math.pow(stdDev, 2));
    },
});
var Segment = Class.create(GrobConnector, {
    initialize: function($super, parent, p1, p2, width) {
        $super(parent, width);
        
        this.name = 'segment';
        this.points = { p1: p1, p2: p2 };
        this.p1 = p1;
        this.p2 = p2;
    },
    
    render: function($super, ctx) {
        $super(ctx);

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
    
    onMouseOver: function($super, e) {
        $super(e);
    },
    onMouseOut: function($super, e) {
        $super(e);
    },
});


// ########
// # MISC #
// ########

function getContext(id) {
  var elem = document.getElementById(id);
  if (!elem || !elem.getContext) {
    return;
  }

  // Get the canvas 2d context.
  var context = elem.getContext('2d');
  if (!context) {
    return;
  }
  return context;
}
function dist(a, b) {
    return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
}
function d_dist_f(pos, x, f) {
    var y = f(x);
    return ((nDeriv(f))(x) * (y - pos.y) + (x - pos.x)) / dist(pos, { x: x, y: y });
}
function drawEq(ctx, eq, x0, y0, xmin, xmax, pm) {
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
