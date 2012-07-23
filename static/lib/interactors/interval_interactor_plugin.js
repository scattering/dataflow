
// Requires reflectivity_sim.js

(function($) { 
    function toArray(obj) {
        return Array.prototype.slice.call(obj);
    };
    
    var dist = $.jqplot.dist;
    function bind(scope, fn) {
        return function() {
            return fn.apply(scope, toArray(arguments));
        };
    };
    
    
    $.jqplot.IntervalInteractorPlugin = function() {};
    $.jqplot.IntervalInteractorPlugin.prototype = new $.jqplot.InteractorPlugin();
    $.jqplot.IntervalInteractorPlugin.prototype.constructor = $.jqplot.IntervalInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.Interval = $.jqplot.IntervalInteractorPlugin;
    
    $.jqplot.IntervalInteractorPlugin.prototype.init = function(options) {
        $.jqplot.InteractorPlugin.prototype.init.call(this, options);
       
        this.width1 = 4;
        this.x01 = 0.0;
        this.width2 = 4;
        this.x02 = 0.0;
        this.y = 5;
        $.extend(this, options);
        
        // vertical line 1
        this.p1 = new $.jqplot.PluginPoint();
        this.p1.initialize(this, this.x01, 0);
        this.vline1 = new $.jqplot.VerticalLine();
        this.vline1.initialize(this, this.p1, this.width1);
        this.grobs.push(this.vline1);
        this.grobs.push(this.p1);
        this.p1.render = function(ctx) {
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.fillStyle = this.color;
            ctx.strokeStyle = 'transparent';
            ctx.beginPath();
            this.putCoords(null, true);
            this.pos.y = height/2.0;
            this.getCoords();
            ctx.fillText(this.coords.x.toPrecision(4) , this.pos.x + 5, this.pos.y - 5);
            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            ctx.fill(); 
        }
        this.p1.move = function(dpos) {
            //this.dpos.y = 0;
            this.translateBy(dpos);
            this.parent.redraw();
            //this.parent.translateBy(dpos);
            //this.parent.update();
        }
         
        // vertical line 2
        this.p2 = new $.jqplot.PluginPoint();
        this.p2.initialize(this, this.x02, 0);
        this.vline2 = new $.jqplot.VerticalLine();
        this.vline2.initialize(this, this.p2, this.width2);
        this.grobs.push(this.vline2);
        this.grobs.push(this.p2);
        this.p2.render = function(ctx) {
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.fillStyle = this.color;
            ctx.strokeStyle = 'transparent';
            ctx.beginPath();
            this.putCoords(null, true);
            this.pos.y = height/2.0;
            this.getCoords();
            ctx.fillText(this.coords.x.toPrecision(4) , this.pos.x + 5, this.pos.y - 5);
            ctx.arc(this.pos.x, this.pos.y, this.r, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            ctx.fill(); 
        }
        this.p2.move = function(dpos) {
            //this.dpos.y = 0;
            this.translateBy(dpos);
            this.parent.redraw();
            //this.parent.translateBy(dpos);
            //this.parent.update();
        }
        
        this.p3 = new $.jqplot.PluginPoint(); this.p3.initialize(this, this.x01, this.y);
        this.p4 = new $.jqplot.PluginPoint(); this.p4.initialize(this, this.x02, this.y);
        
        this.p3.render = function(ctx) {
	        ctx.fillStyle = "rgba(0, 0, 0, 0)";
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
        this.p4.render = function(ctx) {
	        ctx.fillStyle = "rgba(0, 0, 0, 0)";
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
        
        this.rect = new $.jqplot.Rectangle(); this.rect.initialize(this, this.p1, this.p3, this.p2, this.p4); // Rectangle assumes that the second and fourth
                                                                                                              // arguments are diagonal (in this case they aren't)
                                                                                                              // so we have to make them appear that they are.
        this.rect.connectortranslatable = false;
        
        this.rect.render = function(ctx) {
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
            ctx.beginPath();
            ctx.moveTo(this.p1.pos.x, 0);
            ctx.lineTo(this.p1.pos.x, height);
            ctx.lineTo(this.p3.pos.x, height);
            ctx.lineTo(this.p3.pos.x, 0);
            ctx.lineTo(this.p1.pos.x, 0);
            ctx.closePath();
            ctx.globalAlpha = 0.2;
            ctx.stroke();
            //ctx.globalAlpha = 0.6;
            ctx.fill();
            ctx.globalAlpha = 0.6;
        }
        
        this.grobs.push(this.p3, this.p4, this.rect);
        
        this.render = function(ctx) {                     
            var height = ctx.canvas.height;
            var width = ctx.canvas.width;
            ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
            ctx.beginPath();
            ctx.moveTo(this.p1.pos.x, 0);
            ctx.lineTo(this.p1.pos.x, height);
            ctx.lineTo(this.p3.pos.x, height);
            ctx.lineTo(this.p3.pos.x, 0);
            ctx.lineTo(this.p1.pos.x, 0);
            ctx.closePath();
            ctx.globalAlpha = 0.2;
            ctx.stroke();
            //ctx.globalAlpha = 0.6;
            ctx.fill();
            ctx.globalAlpha = 0.6;
        }
    }           
})(jQuery);






