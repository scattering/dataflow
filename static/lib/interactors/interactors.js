var Interactor = Class.create({
    initialize: function(name, icon, state, canvasid) {
        this.name = name;
        this.icon = icon;
        this.state = state;
        
        this.canvas = document.getElementById(canvasid);
        this.context = getContext(canvasid);
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
    
    translateBy: function(dpos) {
        for (var i = 0; i < this.grobs.length; i ++) {
            if (this.grobs[i].translatable)
                this.grobs[i].translateBy(dpos);
        }
    },

    
    onMouseOver: function(e) {
        this.color = this.color2;
    },
    onMouseOut: function(e) {
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
    onDrag: function(e, pos) {
    
    },
    onDrop: function(e, pos) {
    
    },
});
var RulerInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Ruler', 'ruler.png', 0, canvasid);
        
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
var QuadInteractor = new Class.create(Interactor, {
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
        
        this.redraw();
    },
});
var CircInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Circ', 'circ.png', 0, canvasid);
        
        var c = new Point(this, 150, 150);
        var p1 = new Point(this, 200, 150);
        var circ = new Circle(this, c, p1, 4);
        this.grobs.push(circ, c, p1);
        
        this.redraw();
    },
});
var AnnulusInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Circ', 'circ.png', 0, canvasid);
        
        this.c = new AnnulusCenter(this, 150, 150);
        this.p1 = new Point(this, 200, 150);
        this.p2 = new Point(this, 250, 100);
        var circ1 = new Circle(this, this.c, this.p1, 4);
        var circ2 = new Circle(this, this.c, this.p2, 4);
        this.grobs.push(circ1, circ2, this.c, this.p1, this.p2);
        
        this.redraw();
    },
});


function getMouse(e) {
	var t = e.srcElement;
	var x = e.clientX + (window.pageXOffset || 0);
	var y = e.clientY + (window.pageYOffset || 0);
	do
		x -= t.offsetLeft + parseInt(t.style.borderLeftWidth || 0),
		y -= t.offsetTop  + parseInt(t.style.borderTopWidth  || 0);
	while (t = t.offsetParent);
	
	return {x: x, y: y};
}

var Grob = Class.create({
    initialize: function(parent, x, y) {
        this.parent = parent;
        this.pos = { x: x, y: y };

        this.inside = false;
        this.translatable = true;

        this.color1 = '#559';
        this.color2 = '#88e';
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
    
    onDrag: function(e, pos) {},
    onDrop: function(e, pos) {},
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
        ctx.fillText('(' + this.pos.x + ', ' + this.pos.y + ')', this.pos.x, this.pos.y - 5);
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
        this.pos.x = pos.x;
        this.pos.y = pos.y;
    },
});
var Circle = Class.create(Grob, {
    initialize: function($super, parent, c, p1, width) {
        $super(parent);
        
        this.name = 'circle';
        this.translatable = false;
        this.p1 = p1;
        this.c = c;
        this.width = width;
        this.prevpos = null;
    },
    
    render: function(ctx) {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.width;
        ctx.beginPath();
        ctx.arc(this.c.pos.x, this.c.pos.y, dist(this.c.pos, this.p1.pos), 0, 2 * Math.PI, true);
        ctx.closePath();
        ctx.stroke();
    },
    
    isInside: function(pos) {
        return Math.abs(dist(this.c.pos, pos) - dist(this.c.pos, this.p1.pos)) <= this.width + 1;
    },
    onDrag: function($super, e, pos) {
        $super(e, pos);
        if (!this.prevpos)
            this.prevpos = this.parent.prevpos;
        var dx = pos.x - this.prevpos.x,
            dy = pos.y - this.prevpos.y;
        console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', dx, dy);
        this.p1.pos.x += dx;
        this.c.pos.x += dx;
        this.p1.pos.y += dy;
        this.c.pos.y += dy;
        this.prevpos = pos;
    },
    onDrop: function($super, e, pos) {
        $super(e, pos);
        this.prevpos = null;
    }
});
var AnnulusCenter = Class.create(Point, {
    initialize: function($super, parent, x, y, r) {
        $super(parent, x, y, r);
        
        this.name = 'annuluscenter';
        this.translatable = false;
        this.prevpos = null;
    },

    onDrag: function($super, e, pos) {
        $super(e, pos);
        if (!this.prevpos)
            this.prevpos = this.parent.prevpos;
        var dx = pos.x - this.prevpos.x,
            dy = pos.y - this.prevpos.y;
        console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', dx, dy, dist(this.parent.p1.pos, this.pos), dist(this.parent.p2.pos, this.pos));
        this.parent.translateBy({ x: dx, y: dy });
        this.prevpos = pos;
    },
    onDrop: function($super, e, pos) {
        $super(e, pos);
        this.prevpos = null;
    }
});
var Arc = Class.create(Grob, {
    initialize: function($super, parent, p1, p2, c, width) {
        $super(parent);
        
        this.name = 'arc';
        this.p1 = p1;
        this.p2 = p2;
        this.c = c;
        this.width = width;
        this.prevpos = null;
    },
    render: function(ctx) {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.width;
        ctx.beginPath();
        ctx.moveTo(this.p1.pos.x, this.p1.pos.y);
        ctx.arcTo(this.p2.pos.x, this.p2.pos.y, dist(c.pos, p1.pos));
        ctx.closePath();
        ctx.stroke();
    },
    onDrag: function($super, e, pos) {
        $super(e, pos);
        if (!this.prevpos)
            this.prevpos = this.parent.prevpos;
        var dx = pos.x - this.prevpos.x,
            dy = pos.y - this.prevpos.y;
        console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', dx, dy);
        this.p1.pos.x += dx;
        this.c.pos.x += dx;
        this.p1.pos.y += dy;
        this.c.pos.y += dy;
        this.prevpos = pos;
    },
    onDrop: function($super, e, pos) {
        $super(e, pos);
        this.prevpos = null;
    }
});
var Segment = Class.create(Grob, {
    initialize: function($super, parent, p1, p2, width) {
        $super(parent);
        
        this.name = 'segment';
        this.p1 = p1;
        this.p2 = p2;
        this.width = width;
        this.prevpos = null;
    },
    
    render: function(ctx) {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.width;
        ctx.beginPath();
        ctx.moveTo(this.p1.pos.x, this.p1.pos.y);
        ctx.lineTo(this.p2.pos.x, this.p2.pos.y);
        ctx.closePath();
        ctx.stroke();
    },
    
    isInside: function(pos) {
        return this.distanceTo(pos) <= this.width + 1;
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
    onDrag: function($super, e, pos) {
        $super(e, pos);
        if (!this.prevpos)
            this.prevpos = this.parent.prevpos;
        var dx = pos.x - this.prevpos.x,
            dy = pos.y - this.prevpos.y;
        console.log('pos (', pos.x, pos.y ,') prev (', this.prevpos.x, this.prevpos.y, ')', dx, dy);
        this.p1.pos.x += dx;
        this.p2.pos.x += dx;
        this.p1.pos.y += dy;
        this.p2.pos.y += dy;
        this.prevpos = pos;
    },
    onDrop: function($super, e, pos) {
        $super(e, pos);
        this.prevpos = null;
    }
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
