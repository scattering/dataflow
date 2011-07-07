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
        console.log('down', this.grobs, pos.x, pos.y, this.mousedown);
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
        console.log('up  ', this.grobs, pos.x, pos.y, this.mousedown);
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
        var x = 0, y = 0, d;
        
        for (var i = 0; i < points.length; j = i ++) {
            d = (points[i].pos.x * points[j].pos.y) - (points[i].pos.y * points[j].pos.x);
            area += d;
            x += (points[i].pos.x + points[j].pos.x) * d;
            y += (points[i].pos.y + points[j].pos.y) * d;
        }
        
        area /= 2;
        d = area * 6;
        return { x: x / d, y: y / d };
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
    
    redraw: function($super) {
        $super();
    },
});
var QuadInteractor = new Class.create(PolygonInteractor, {
    initialize: function($super, canvasid) {
        $super('Quad', 'quad.png', 0, canvasid);
        
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
        
        var p1 = new Point(this, 100, 100);
        var p2 = new Point(this, 200, 100);
        var p3 = new Point(this, 200, 200);
        var p4 = new Point(this, 100, 200);
        var c = new Center(this, 150, 150);
        var l1 = new Segment(this, p1, p2, 4);
        var l2 = new Segment(this, p2, p3, 4);
        var l3 = new Segment(this, p3, p4, 4);
        var l4 = new Segment(this, p4, p1, 4);
        this.grobs.push(l1, l2, l3, l4, c, p1, p2, p3, p4);
        this.c = c;
        
        this.redraw();
    },
});
var CircleInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Circ', 'circ.png', 0, canvasid);
        
        var c = new Center(this, 150, 150);
        var p1 = new Point(this, 200, 150);
        var circ = new Circle(this, c, p1, 4);
        this.grobs.push(circ, c, p1);
        
        this.redraw();
    },
});
var AnnulusInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Circ', 'circ.png', 0, canvasid);
        
        this.c = new Center(this, 150, 150);
        this.p1 = new Point(this, 200, 150);
        this.p2 = new Point(this, 250, 100);
        var circ1 = new Circle(this, this.c, this.p1, 4);
        var circ2 = new Circle(this, this.c, this.p2, 4);
        this.grobs.push(circ1, circ2, this.c, this.p1, this.p2);
        
        this.redraw();
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
var GaussianInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Gaussian', 'gaussian.png', 0, canvasid);
        
        var pk = new Point(this, 200, 150);
        var pw = new Point(this, 150, 100);
        var gaussian = new Gaussian(this, pk, pw, 4);
        this.grobs.push(gaussian, pk, pw);
        
        this.redraw();
    },
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

var Grob = Class.create({
    initialize: function(parent, x, y) {
        this.parent = parent;
        this.pos = { x: x, y: y };

        this.inside = false;
        this.translatable = true;
        this.prevpos = null;
        this.dpos = null;

        this.color1 = '#2C8139';
        this.color2 = '#4CCC60';
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
    onDrag: function($super, e, pos) {
        $super(e, pos);
        
        console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', this.dpos.x, this.dpos.y);
        for (var p in this.points)
            this.points[p].translateBy(this.dpos);
    },
});
var Circle = Class.create(GrobConnector, {
    initialize: function($super, parent, c, p1, width) {
        $super(parent, width);
        
        this.name = 'circle';
        this.points = { p1: p1, c: c };
        this.p1 = p1;
        this.c = c;
    },
    
    render: function($super, ctx) {
        $super(ctx);
        
        ctx.beginPath();
        ctx.arc(this.c.pos.x, this.c.pos.y, dist(this.c.pos, this.p1.pos), 0, 2 * Math.PI, true);
        ctx.closePath();
        ctx.stroke();
        ctx.globalAlpha = 0.15;
        ctx.fill();
        ctx.globalAlpha = 0.6;
    },
    
    isInside: function(pos) {
        return /*Math.abs*/(dist(this.c.pos, pos) - dist(this.c.pos, this.p1.pos)) <= this.width + 1;
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
        /*
        p1.onDrag = function(e, pos) {
            this.parent.arc.angleToXaxis(this.parent.p2);
        };*/
        
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
var Gaussian = Class.create(GrobConnector, {
    initialize: function($super, parent, pk, pw, width) {
        $super(parent, width);
        /*
        p1.onDrag = function(e, pos) {
            this.parent.arc.angleToXaxis(this.parent.p2);
        };*/
        
        this.name = 'gaussian';
        this.points = { pk: pk, pw: pw };
        this.pk = pk;
        this.pw = pw;
    },
    render: function($super, ctx) {
        $super(ctx);
        
        //ctx.beginPath();
        //console.log(t_1, t_2);
        //ctx.moveTo(this.c.pos.x, this.c.pos.y);
        drawEq(ctx, this.gaussian.bind(this), 0, this.pw.pos.y, 0, 300);
        //ctx.closePath();
        //ctx.stroke();
        //ctx.globalAlpha = 0.15;
        //ctx.fill();
        //ctx.globalAlpha = 0.6;
    },
    
    gaussian: function(x) {
        var peakX = this.pk.pos.x,
            peakY = this.pw.pos.y - this.pk.pos.y,
            FWHM = Math.abs(this.pw.pos.x - peakX),
            bkgdY = 0;
        var stdDev = FWHM / 2 / Math.sqrt(2 * Math.log(2));
        return bkgdY + (peakY - bkgdY) * Math.exp(- Math.pow((x - peakX), 2) / 2 / Math.pow(stdDev, 2));
    },
    distanceTo: function(pos) {
        var d = this.gaussian(pos.x) - pos.y;
        
        return d;
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
function drawEq(ctx, eq, x0, y0, xmin, xmax) {
	ctx.beginPath();
	ctx.moveTo(x0, y0);
	for( i = xmin; i <= xmax; i++ ) {
		ctx.lineTo(i, y0 - eq(i));
	}
 
	ctx.stroke();
}
