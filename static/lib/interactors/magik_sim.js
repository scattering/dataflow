

// #############################################
// # Interactive Offspecular Reflectometry Lib #
// # Brian Maranville                          #
// # 10/13/2011                                #
// #############################################

// ## requires interactors_nonprototype.js 

(function($) {
    var dist = $.jqplot.dist;
    // here we go
   
    $.jqplot.RotationAxis = function() {};
    $.jqplot.RotationAxis.prototype = new $.jqplot.Center();
    $.jqplot.RotationAxis.prototype.constructor = $.jqplot.RotationAxis;
    $.extend($.jqplot.RotationAxis.prototype, {
        render: function(ctx) {
	            ctx.fillStyle = this.color;
	            ctx.strokeStyle = 'transparent';
                ctx.beginPath();
	            //ctx.moveTo(this.x, this.y);
                ctx.fillText('(' + (this.angle/Math.PI * 180.0).toFixed(1) + ')', this.pos.x, this.pos.y - 5);
	            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
	            ctx.closePath();
	            ctx.stroke();
	            ctx.fill() 
	    }
    });
    
    
    
    $.jqplot.Spinor = function() {};
    $.jqplot.Spinor.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Spinor.prototype.constructor = $.jqplot.Spinor;    
    $.extend($.jqplot.Spinor.prototype, {        
        initialize: function(parent, c, angle, len, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'spinor';
            this.translatable = false;
            this.rotatable = true;
            this.connectortranslatable = false;
            this.points = { c: c };
            this.c = c;
            this.angle = angle;
            this.len = len;
        },

        getEndPoints: function() {
            var p1 = {pos: {x: (this.c.pos.x - Math.cos(this.angle) * this.len/2),
                        y: (this.c.pos.y - Math.sin(this.angle) * this.len/2)} }
            var p2 = {pos: {x: (2*this.c.pos.x - p1.pos.x) ,
                        y: (2*this.c.pos.y - p1.pos.y)} }
            return {p1: p1, p2: p2}
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            
            var endPoints = this.getEndPoints();
                 
            ctx.beginPath();
            ctx.moveTo(endPoints.p1.pos.x, endPoints.p1.pos.y);
            ctx.lineTo(endPoints.p2.pos.x, endPoints.p2.pos.y);
            ctx.closePath();
            ctx.stroke();   
        },
        
        distanceToLine: function(c, p1_pos, p2_pos) {
            // taken from mathworld
            var d = (p2_pos.x - p1_pos.x) * (p1_pos.y - c.y) - (p1_pos.x - c.x) * (p2_pos.y - p1_pos.y);
            d = Math.abs(d)/Math.sqrt(Math.pow((p2_pos.x - p1_pos.x), 2) + Math.pow((p2_pos.y - p1_pos.y), 2));
            return d
        },
        
        distanceTo: function(c) {
            var new_angle = Math.atan2(c.y - this.c.pos.y, c.x - this.c.pos.x);
            var endPoints = this.getEndPoints();
            var r_proj = Math.abs(dist(c, this.c.pos) * Math.cos(new_angle - this.angle));
            // if the point is farther away from the center than the endpoints, then 
            // the distanceTo is the distance to the nearest endpoint:
            var d;
            if (r_proj > this.len/2) {
                var dp1 = dist(c, endPoints.p1.pos);
                var dp2 = dist(c, endPoints.p2.pos);
                d = Math.min(dp1, dp2);
            } else {
                d = this.distanceToLine(c, endPoints.p1.pos, endPoints.p2.pos);
            }
            return d
        },
        
        onDrag: function(e, pos) {
            //$.jqplot.GrobConnector.prototype.onDrag.call(this, e, pos);
            var new_angle = Math.atan2(pos.y - this.c.pos.y, pos.x - this.c.pos.x);
            if (this.rotatable) {
                this.angle = new_angle;
                this.c.angle = new_angle;
            };
        },
        
        translateBy: function(dpos) {}
        
    });
    
    $.jqplot.SpinorInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.SpinorInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.SpinorInteractor.prototype.constructor = $.jqplot.SpinorInteractor;
    
    $.jqplot.SpinorInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Spinor', 'spinor.png', 0, canvasid);        
        var c = new $.jqplot.RotationAxis(); c.initialize(this, 200, 150);
        c.translatable = false;
        var spinor = new $.jqplot.Spinor(); spinor.initialize(this, c, 30.0*Math.PI/180, 200, 4);
        this.grobs.push(spinor, c);
        // the order matters!!  if you push(c, spinor) the spinor is the last to get checked for isInside
        // so it becomes the selected object (put items in order of increasing z-value!)
        this.spinor = spinor;
        
        this.redraw();
    };
    
    $.jqplot.SpinArrow = function() {};
    $.jqplot.SpinArrow.prototype = new $.jqplot.Spinor();
    $.jqplot.SpinArrow.prototype.constructor = $.jqplot.SpinArrow;
    $.extend($.jqplot.SpinArrow.prototype, {
        initialize: function (parent, c, p1, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'spinarrow';
            this.translatable = false;
            this.rotatable = true;
            this.connectortranslatable = false;
            this.points = { c: c, p1: p1 };
            this.c = c;
            this.p1 = p1;
            this.arrow_width = width * 5;
            
            this.angle = Math.atan2(p1.pos.y - c.pos.y, p1.pos.x - c.pos.x);
            this.c.angle = this.angle;
            this.len = 2*Math.sqrt(Math.pow(p1.pos.y - c.pos.y, 2) + Math.pow(p1.pos.x - c.pos.x, 2));
        },
        
        getEndPoints: function() {
            var p1 = this.p1;
            var p2 = {pos: {x: (2*this.c.pos.x - p1.pos.x) ,
                        y: (2*this.c.pos.y - p1.pos.y)} }
            return {p1: p1, p2: p2}
        },
        
        render: function(ctx) {
            $.jqplot.Spinor.prototype.render.call(this, ctx);
            arrow_p1 = { x: ( this.p1.pos.x + Math.cos(this.angle + Math.PI*0.85) * this.arrow_width ),
                         y: ( this.p1.pos.y + Math.sin(this.angle + Math.PI*0.85) * this.arrow_width ) }
            arrow_p2 = { x: ( this.p1.pos.x + Math.cos(this.angle - Math.PI*0.85) * this.arrow_width ),
                         y: ( this.p1.pos.y + Math.sin(this.angle - Math.PI*0.85) * this.arrow_width ) }
            ctx.beginPath();
            ctx.moveTo(arrow_p1.x, arrow_p1.y);
            ctx.lineTo(this.p1.pos.x, this.p1.pos.y);
            ctx.lineTo(arrow_p2.x, arrow_p2.y);
            ctx.stroke();   
        },
        
        onDrag: function(e, pos) {
            $.jqplot.Spinor.prototype.onDrag.call(this, e, pos);
            this.p1.pos.x = this.c.pos.x + Math.cos(this.angle) * this.len/2;
            this.p1.pos.y = this.c.pos.y + Math.sin(this.angle) * this.len/2;
        }
        
    });
    
    
    $.jqplot.SpinArrowInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.SpinArrowInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.SpinArrowInteractor.prototype.constructor = $.jqplot.SpinArrowInteractor;
    
    $.jqplot.SpinArrowInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'SpinArrow', 'Arrow.png', 0, canvasid);        
        this.c = new $.jqplot.RotationAxis(); this.c.initialize(this, 200, 150);
        this.c.translatable = false;
        this.p1 = new $.jqplot.Point(); this.p1.initialize(this, 150, 100);
        
        var Arrow = new $.jqplot.SpinArrow(); Arrow.initialize(this, this.c, this.p1, 4);
        this.grobs.push(Arrow, this.c,  this.p1);
        // the order matters!!  if you push(c, Arrow) the Arrow is the last to get checked for isInside
        // so it becomes the selected object (put items in order of increasing z-value!)
        this.SpinArrow = Arrow;
        this.p1.onDrag = function(e, pos) {
                $.jqplot.Point.prototype.onDrag.call(this, e, pos);
                
                var new_angle = Math.atan2(this.pos.y - this.parent.c.pos.y, this.pos.x - this.parent.c.pos.x);
                var new_len = 2*Math.sqrt(Math.pow(this.pos.y - this.parent.c.pos.y, 2) + Math.pow(this.pos.x - this.parent.c.pos.x, 2));
                this.parent.SpinArrow.angle = new_angle;
                this.parent.SpinArrow.len = new_len;
                this.parent.c.angle = new_angle;
            };
        
        this.redraw();
    };
    
    $.jqplot.Arrow = function() {};
    $.jqplot.Arrow.prototype = new $.jqplot.Segment();
    $.jqplot.Arrow.prototype.constructor = $.jqplot.Arrow;
    $.extend($.jqplot.Arrow.prototype, {
        initialize: function (parent, p2, p1, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'arrow';
            this.translatable = false;
            this.connectortranslatable = false;
            this.arrow_width = width * 5;
            
            this.angle = Math.atan2(this.p2.pos.y - this.p1.pos.y, this.p2.pos.x - this.p1.pos.x);
            this.len = Math.sqrt(Math.pow(p2.pos.y - p1.pos.y, 2) + Math.pow(p2.pos.x - p1.pos.x, 2));
        },
        
        update_angle: function() {
            this.angle = Math.atan2(this.p2.pos.y - this.p1.pos.y, this.p2.pos.x - this.p1.pos.x);
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            this.update_angle();
            arrow_p1 = { x: ( this.p2.pos.x + Math.cos(this.angle + Math.PI*0.85) * this.arrow_width ),
                         y: ( this.p2.pos.y + Math.sin(this.angle + Math.PI*0.85) * this.arrow_width ) }
            arrow_p2 = { x: ( this.p2.pos.x + Math.cos(this.angle - Math.PI*0.85) * this.arrow_width ),
                         y: ( this.p2.pos.y + Math.sin(this.angle - Math.PI*0.85) * this.arrow_width ) }
            ctx.beginPath();
            ctx.moveTo(arrow_p1.x, arrow_p1.y);
            ctx.lineTo(this.p2.pos.x, this.p2.pos.y);
            ctx.lineTo(arrow_p2.x, arrow_p2.y);
            ctx.stroke();   
        }
        
    });
    
    $.jqplot.ArrowInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.ArrowInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.ArrowInteractor.prototype.constructor = $.jqplot.ArrowInteractor;
    
    $.jqplot.ArrowInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Arrow', 'Arrow.png', 0, canvasid);        
        this.p1 = new $.jqplot.Point(); this.p1.initialize(this, 50, 50);
        this.p2 = new $.jqplot.Point(); this.p1.initialize(this, 150, 100);
        var Arrow = new $.jqplot.Arrow(); Arrow.initialize(this, this.p1, this.p2, 4);
        this.grobs.push(Arrow, this.p1,  this.p2);
        // the order matters!!  if you push(c, Arrow) the Arrow is the last to get checked for isInside
        // so it becomes the selected object (put items in order of increasing z-value!)
        this.Arrow = Arrow;
        this.p1.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
            //var new_len = 2*Math.sqrt(Math.pow(this.pos.y - this.parent.c.pos.y, 2) + Math.pow(this.pos.x - this.parent.c.pos.x, 2));
            //this.parent.SpinArrow.angle = new_angle;
            //this.parent.SpinArrow.len = new_len;
            //this.parent.c.angle = new_angle;
        };
        this.p2.onDrag = function(e, pos) {
            $.jqplot.Point.prototype.onDrag.call(this, e, pos);
        };
        
        this.redraw();
    };
    
    $.jqplot.Grating = function() {};
    $.jqplot.Grating.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Grating.prototype.constructor = $.jqplot.Grating;
    $.extend($.jqplot.Grating.prototype, {
        initialize: function (parent, p1, width, autoColor) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'Grating';
            this.colors = $.jqplot.config.defaultColors;
            this.color = "#aaaaaa";
            this.autoColor = autoColor || false;
            this.show_pos = true;
            this.translatable = false;
            this.connectortranslatable = false;
            this.points = { p1: p1 };
            this.p1 = p1;
            this.p1.show_pos = false;
            this.y_center = this.parent.canvas.height / 2;
            this.x_center = this.parent.canvas.width / 2;
            this.p1.pos.y = this.y_center;
            this.p1.translatable = false;
            this.p1.onDrag = function(e, pos) {
                var pos = pos;
                $.jqplot.Point.prototype.onDrag.call(this, e, pos);
                var dpos = this.dpos;
                dpos.y = 0;
                var new_x = this.pos.x + dpos.x;
                if (new_x > (this.parent.x_center - 4)) { new_x = (this.parent.x_center - 4); }
                dpos.x = new_x - this.pos.x;
                //console.log(this.pos.x, new_x, dpos.x);
                this.move(dpos);
                this.parent.redraw();
            }
            
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }
            var height = this.parent.canvas.height;
            var width = this.parent.canvas.width;
            this.x_spacing = Math.abs(this.p1.pos.x - this.x_center);
            // draw center line (a little longer than the others);
            var xpos = this.x_center;
            var i = 0;
            ctx.beginPath();
            if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
            ctx.moveTo(xpos, 0);
            ctx.lineTo(xpos, height);
            ctx.stroke();
            //var xpos = Math.ceil(-this.x_center/this.x_spacing) * this.x_spacing + this.x_center;
            xpos -= this.x_spacing;
            i -= 1;
            
            while (xpos >= 0) {
                ctx.beginPath();
                if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                ctx.moveTo(xpos, 10);
                ctx.lineTo(xpos, height - 10);
                ctx.stroke();
                if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height);   
                xpos -= this.x_spacing;
                i -= 1;
            }
            xpos = this.x_center + this.x_spacing;
            i = 1;
            while (xpos <= width) {
                ctx.beginPath();
                if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                ctx.moveTo(xpos, 10);
                ctx.lineTo(xpos, height -10);
                ctx.stroke();
                if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height); 
                xpos += this.x_spacing;
                i += 1;
            }
        },
            
        distanceTo: function(c) {
            //return Math.abs((this.x_center - c.x) % this.x_spacing);
        },
        
        onMouseOver: function(e, pos) {}
    });
    
    $.jqplot.GratingInteractor = function() {
        $.jqplot.Interactor.call(this)
    };
    
    $.jqplot.GratingInteractor.prototype = new $.jqplot.Interactor();
    $.jqplot.GratingInteractor.prototype.constructor = $.jqplot.GratingInteractor;
    
    $.jqplot.GratingInteractor.prototype.init = function(canvasid) {
        $.jqplot.Interactor.prototype.init.call(this, 'Grating', 'Grating.png', 0, canvasid);
        var x_center = this.canvas.width / 2.0;
        this.x_center = x_center;
        this.y_center = this.canvas.height / 2.0;
        var width = this.canvas.width;  
        this.p1 = new $.jqplot.Point(); this.p1.initialize(this, x_center - 50, 100);
        this.max_spacing = 20000;
        this.p1.getCoords = function() { 
            return {x: (x_center - this.pos.x) * 2.0 / width * this.parent.max_spacing, y: this.pos.y}
        }
        this.p1.putCoords = function(pos) { return {x: x_center - pos.x * width / (2.0 * this.parent.max_spacing), y: pos.y} };
        this.grating = new $.jqplot.Grating(); this.grating.initialize(this, this.p1, 4);
        this.grobs.push(this.grating, this.p1);
        //this.redraw();
    };
    
})(jQuery);

