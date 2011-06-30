var Interactor = Class.create({
    initialize: function(name, icon, state, canvasid) {
        this.name = name;
        this.icon = icon;
        this.state = state;
        console.log(canvasid);
        this.canvas = document.getElementById(canvasid);
        this.context = getContext(canvasid);
        this.grobs = [];
        
        this.canvas.onmouseover = function(e) {
            console.log('mouseover');
            var pos = getMouse(e);
            for (i in this.grobs) {
                var grob = this.grobs[i];
                var inside = grob.isInside(pos);
                if (inside) grob.onMouseOver(e);
                else if (!inside && grob.inside) grob.onMouseOut(e);
            }
        };
    },
    redraw: function() {
        for (var i = 0; i < this.grobs.length; i ++) {
            var grob = this.grobs[i];
            grob.render(this.context);
        }
        this.context.stroke();
    },
});
var RulerInteractor = new Class.create(Interactor, {
    initialize: function($super, canvasid) {
        $super('Ruler', 'ruler.png', 0, canvasid);
        var c1 = new ControlPoint(50, 50);
        this.grobs.push(c1);
    },
});

function getMouse(e) {
  return { x: null, y: null };
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
    onMouseOver: function(e) {},
    onMouseOut: function(e) {},
});

var ControlPoint = Class.create(Grob, {
    initialize: function($super, x, y) {
        $super(x, y);
        this.w = 6;
        this.h = 6;
        this.r = 3;

        this.color = '#69f';
    },
    
    render: function(ctx) {
        ctx.fillText('34',this.x,this.y);
        ctx.beginPath();
	    ctx.fillStyle = this.color;
	    ctx.moveTo(this.x, this.y);
	    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2, true);
	    ctx.fill();
    },

    isInside: function(pos) {
      return this.distanceTo(pos) <= this.r;
    },
});
ControlPoint.prototype = new Grob;
ControlPoint.prototype.constructor = ControlPoint;

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
