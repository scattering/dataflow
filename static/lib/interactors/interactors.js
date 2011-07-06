var Interactor = Class.create({
    initialize: function(name, icon, state, canvasid) {
        this.name = name;
        this.icon = icon;
        this.state = state;
        console.log(canvasid);
        this.canvas = document.getElementById(canvasid);
        this.context = getContext(canvasid);
        this.grobs = [];
        this.mousedown = false;
        this.curgrob = null;
        
        this.canvas.onmouseover = this.onMouseOver;
        this.canvas.onmousemove = this.onMouseMove.bind(this);
        this.canvas.onmousedown = this.onMouseDown;
        this.canvas.onmouseup   = this.onMouseUp;
    },
    redraw: function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        for (var i = 0; i < this.grobs.length; i ++) {
            var grob = this.grobs[i];
            grob.render(this.context);
        }
    },
    onMouseOver: function(e) {
        //console.log('mouseover');
    },
    onMouseOut:  function(e) {
    
    },
    onMouseMove: function(e) {
        //console.log('mousemove');
        var pos = getMouse(e);
        //console.log('move', this.grobs, pos.x, pos.y, this.mousedown);
        for (var i = 0; i < this.grobs.length; i ++) {
            var g = this.grobs[i];
            var inside = g.isInside(pos);
            console.log(i, g, 'pos', pos, inside, g.inside);
            if (inside) {
              g.onMouseOver(e);
              this.onMouseOver(e);
            }
            else if (!inside && g.inside) {
                g.onMouseOut(e);
                this.onMouseOut(e);
            }
        }
        this.redraw();
    },
    onMouseDown: function(e) {
        this.mousedown = true;
        var pos = getMouse(e);
        this.prevpos = pos;
        console.log('down', this.grobs, pos.x, pos.y, this.mousedown);
    },
    onMouseUp:   function(e) {
        this.mousedown = false;
        var pos = getMouse(e);
        this.prevpos = null;
        console.log('up  ', this.grobs, pos.x, pos.y, this.mousedown);
    },
});
var RulerInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Ruler', 'ruler.png', 0, canvasid);
        
        var c1 = new ControlPoint(50, 50);
        var c2 = new ControlPoint(100, 50);
        this.color1 = '#f96';
        this.color2 = '#96f';
        this.color = this.color1;
        this.grobs.push(c1, c2);
    },
    
    redraw: function($super) {
        $super();
        
        this.context.strokeStyle = this.color;
        this.context.beginPath();
        this.context.moveTo(this.grobs[0].x, this.grobs[0].y);
        this.context.lineTo(this.grobs[1].x, this.grobs[1].y);
        this.context.closePath();
        this.context.stroke();
    },
    
    onMouseOver: function($super, e) {
        $super(e);
        this.color = this.color2;
    },
    onMouseOut: function($super, e) {
        $super(e);
        this.color = this.color1;
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
    initialize: function(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;

        this.inside = false;
    },
    
    isInside: function(pos) {},
    distanceTo: function(pos) {
        return Math.sqrt(Math.pow(this.x - pos.x, 2) + Math.pow(this.y - pos.y, 2));
    },
    render: function(ctx) {},
    
    onDrag: function(e) {},
    onDrop: function(e) {},
    onMouseOver: function(e) { this.inside = true;  },
    onMouseOut: function(e)  { this.inside = false; },
});

var ControlPoint = Class.create(Grob, {
    initialize: function($super, x, y) {
        $super(x, y);
        this.w = 6;
        this.h = 6;
        this.r = 6;

        this.color1 = '#69f';
        this.color2 = '#f69';
        this.color = this.color1;
    },
    
    render: function(ctx) {
	    ctx.fillStyle = this.color;
	    ctx.strokeStyle = 'transparent';
        ctx.beginPath();
	    //ctx.moveTo(this.x, this.y);
        ctx.fillText(this.x + ', ' + this.y, this.x, this.y - 6);
	    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2, true);
	    ctx.closePath();
	    ctx.stroke();
	    ctx.fill();
    },

    isInside: function(pos) {
        return this.distanceTo(pos) <= this.r;
    },
    onMouseOver: function($super, e) {
        $super(e);
        this.color = this.color2;
    },
    onMouseOut: function($super, e) {
        $super(e);
        this.color = this.color1;
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
