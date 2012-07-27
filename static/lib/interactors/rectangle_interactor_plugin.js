// #############################################
// # Interactors as jqplot plugins             #
// # Brian Maranville                          #
// # 10/14/2011                                #
// #############################################

// ## requires interactors_nonprototype.js
// ## and interactor_plugin_base.js

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
   
    $.jqplot.RectangleInteractorPlugin = function() { $.jqplot.PolygonInteractorPlugin.call(this); };
    $.jqplot.RectangleInteractorPlugin.prototype = new $.jqplot.PolygonInteractorPlugin();
    $.jqplot.RectangleInteractorPlugin.prototype.constructor = $.jqplot.RectangleInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.Rectangle = $.jqplot.RectangleInteractorPlugin;
    
    $.jqplot.RectangleInteractorPlugin.prototype.init = function(options) {
        $.jqplot.PolygonInteractorPlugin.prototype.init.call(this, options);
        this.showcenter = true;
        this.showrect = true;
        this.xmin = 0;
        this.xmax = 6.0;
        this.ymin = -4.0;
        this.ymax = 4.0;
        //this.p1pos = {x: 0, y: 4.0};
        //this.p2pos = {x: 6, y: 4.0};
        //this.p3pos = {x: 6, y: -4.0};
        //this.p4pos = {x: 0, y: -4.0};
        $.extend(this, options);
        this.p1 = new $.jqplot.PluginPoint(); this.p1.initialize(this, this.xmin, this.ymax);
        this.p2 = new $.jqplot.PluginPoint(); this.p2.initialize(this, this.xmax, this.ymax);
        this.p3 = new $.jqplot.PluginPoint(); this.p3.initialize(this, this.xmax, this.ymin);
        this.p4 = new $.jqplot.PluginPoint(); this.p4.initialize(this, this.xmin, this.ymin);
        //this.c = new Center(this, 150, 150);
        
        //this.rect = new $.jqplot.Rectangle(); this.rect.initialize(this, this.p1, this.p3);
        this.l1 = new $.jqplot.Segment(); this.l1.initialize(this, this.p1, this.p2, 4);
        this.l2 = new $.jqplot.Segment(); this.l2.initialize(this, this.p2, this.p3, 4);
        this.l3 = new $.jqplot.Segment(); this.l3.initialize(this, this.p3, this.p4, 4);
        this.l4 = new $.jqplot.Segment(); this.l4.initialize(this, this.p4, this.p1, 4);
        
        if (this.showrect) {
            this.rect = new $.jqplot.Rectangle(); this.rect.initialize(this, this.p1, this.p2, this.p3, this.p4);
            this.rect.connectortranslatable = true;
            this.grobs.push(this.rect);
        }
        
        this.grobs.push(this.l1, this.l2, this.l3, this.l4, this.p1, this.p2, this.p3, this.p4);
        
        if (this.showcenter) {
            var center = {x: (this.xmin + this.xmax) / 2.0, 
                         y: (this.ymin + this.ymax) / 2.0 }
            this.c = new $.jqplot.PluginCenter(); this.c.initialize(this, center.x, center.y);
            this.grobs.push(this.c);
        }
        
        
        var me = this;
        

        this.p1.move = function(dp) {
            var dpos = {x: dp.x || 0, y: dp.y || 0 };
            this.translateBy(dpos);
            this.parent.p4.translateBy( {x: dpos.x, y:0} );
            this.parent.p2.translateBy( {x: 0, y: dpos.y} );
        };
        
        this.p2.move = function(dp) {
            var dpos = {x: dp.x || 0, y: dp.y || 0 };
            this.translateBy(dpos);
            this.parent.p3.translateBy( {x: dpos.x, y:0} );
            this.parent.p1.translateBy( {x: 0, y: dpos.y} );
        }; 
        
        this.p3.move = function(dp) {
            var dpos = {x: dp.x || 0, y: dp.y || 0 };
            this.translateBy(dpos);
            this.parent.p2.translateBy( {x: dpos.x, y:0} );
            this.parent.p4.translateBy( {x: 0, y: dpos.y} );
        }; 
        
        this.p4.move = function(dp) {
            var dpos = {x: dp.x || 0, y: dp.y || 0 };
            this.translateBy(dpos);
            this.parent.p1.translateBy( {x: dpos.x, y:0} );
            this.parent.p3.translateBy( {x: 0, y: dpos.y} );
        }; 

        this.l1.connectortranslatable = false;
        this.l1.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.x = 0;
            this.translateBy(this.dpos);
            this.parent.onDrag(this.dpos);
        };
        this.l2.connectortranslatable = false;
        this.l2.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.y = 0;
            this.translateBy(this.dpos);
            this.parent.onDrag(this.dpos);
        };
        this.l3.connectortranslatable = false;
        this.l3.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.x = 0;
            this.translateBy(this.dpos);
            this.parent.onDrag(this.dpos);
        };
        this.l4.connectortranslatable = false;
        this.l4.onDrag = function(e, pos) {
            $.jqplot.Segment.prototype.onDrag.call(this, e, pos);
            
            this.dpos.y = 0;
            this.translateBy(this.dpos);
            this.parent.onDrag(this.dpos);
        };
        
        //this.redraw();
    };
    
    $.jqplot.QFromThetaTwotheta = function() {};
    $.jqplot.QFromThetaTwotheta.prototype = new $.jqplot.GrobConnector();
    $.jqplot.QFromThetaTwotheta.prototype.constructor = $.jqplot.QFromThetaTwotheta;
    $.extend($.jqplot.QFromThetaTwotheta.prototype, {
        getQxQz: function(A3, A4, wavelength) { 
            var qLength = 2.0 * Math.PI / wavelength;
            var tilt = A3 - ( A4 / 2.0 );
            var dq = 2.0 * qLength * Math.sin( ( Math.PI / 180.0 ) * ( A4 / 2.0 ) );
            var qxOut = dq * Math.sin( Math.PI * tilt / 180.0 );
            var qzOut = dq * Math.cos( Math.PI * tilt / 180.0 );
            return {x: qxOut, y: qzOut};
        },
        
        initialize: function (parent, p1, p2, width) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            // convert all the values of theta and twotheta between points 1 and 2
            // (assumed to be corners of a bounding box)
            this.xdim = parent.xdim || 201;
            this.ydim = parent.ydim || 201;
            this.q_points = [];
            this.p1 = p1;
            this.p2 = p2;
            this.updateQPoints();
            this.wavelength = 5.0;
            this.filled = true;
        }, 
        
        updateQPoints: function() {
            this.q_points = [];
            p1coords = this.p1.getCoords();
            p2coords = this.p2.getCoords();
            var xmin = Math.min(p1coords.x, p2coords.x);
            var xmax = Math.max(p1coords.x, p2coords.x);
            var ymin = Math.min(p1coords.y, p2coords.y);
            var ymax = Math.max(p1coords.y, p2coords.y);
            
            var dx = (xmax - xmin) / (this.xdim - 1);
            var dy = (ymax - ymin) / (this.ydim - 1);
            var j = 0;
            for (var i = 0; i<this.xdim-1; i++) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
            for (var j = 0; j<this.ydim-1; j++) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
            for (var i = this.xdim-1; i>0; i--) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
            for (var j = this.ydim-1; j>0; j--) {
                this.q_points.push(this.getQxQz(ymin + j * dy, xmin + i * dx, this.wavelength));
            }
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
//            ctx.save();
//            this.parent.transformCalc();
            
            ctx.beginPath();
            var newpos = this.parent.putCoords(this.q_points[0]);
            //var newpos = this.q_points[0];
            ctx.moveTo(newpos.x, newpos.y);
            for (var i in this.q_points) {
                newpos = this.parent.putCoords(this.q_points[i]);
                //newpos = this.q_points[i];
                ctx.lineTo(newpos.x, newpos.y);
            }
            ctx.closePath();
            ctx.stroke();
            if (this.filled) {
                ctx.globalAlpha = 0.15;
                ctx.fill();
                ctx.globalAlpha = 0.6;
            }
            
            //ctx.restore();
            
        }
    
    });
    
    $.jqplot.QFromThetaTwothetaInteractorPlugin = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.QFromThetaTwothetaInteractorPlugin.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.QFromThetaTwothetaInteractorPlugin.prototype.constructor = $.jqplot.QFromThetaTwothetaInteractorPlugin;
    $.jqplot.InteractorPluginSubtypes.QSpace = $.jqplot.QFromThetaTwothetaInteractorPlugin;
    $.extend($.jqplot.QFromThetaTwothetaInteractorPlugin.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.qspace_patch = new $.jqplot.QFromThetaTwotheta();
            this.p1 = options.p1;
            this.p2 = options.p2;
            this.qspace_patch.initialize(this, this.p1, this.p2, 4);
            this.filled = true;
            this.grobs.push(this.qspace_patch);
            //this.redraw();
        },
        
        
        
        update: function() {
            this.qspace_patch.updateQPoints();
            this.redraw();
        }
        
    });
    
    $.jqplot.QGrating = function() {};
    $.jqplot.QGrating.prototype = new $.jqplot.GrobConnector();
    $.jqplot.QGrating.prototype.constructor = $.jqplot.QGrating;
    $.extend($.jqplot.QGrating.prototype, {
        initialize: function (parent, width, autoColor) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'Grating';
            this.colors = $.jqplot.config.defaultColors;
            this.autoColor = autoColor || false;
            this.show_pos = true;
            this.translatable = false;
            this.connectortranslatable = false;
            //this.points = { p1: p1 };
            //this.q_spacing = q_spacing;

            //this.y_center = this.parent.canvas.height / 2;
            //this.x_center = this.parent.canvas.width / 2;
            //this.p1.pos.y = this.y_center;
            
        },
        
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }
            var height = this.parent.canvas.height;
            var width = this.parent.canvas.width;
            var xpos = this.parent.putCoords({x:0, y:0}).x;
            this.x_spacing = Math.abs(this.parent.putCoords({x:this.parent.q_spacing, y:0}).x - xpos);
            var i = 0;
            while (xpos >= 0) {
                ctx.beginPath();
                if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                ctx.moveTo(xpos, 0);
                ctx.lineTo(xpos, height);
                ctx.stroke();
                if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height - 5);   
                xpos -= this.x_spacing;
                i -= 1;
            }
            xpos = this.parent.putCoords({x:0, y:0}).x + this.x_spacing;
            i = 1;
            while (xpos <= width) {
                ctx.beginPath();
                if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                ctx.moveTo(xpos, 0);
                ctx.lineTo(xpos, height);
                ctx.stroke();
                if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height - 5); 
                xpos += this.x_spacing;
                i += 1;
            }
        },
        
        distanceTo: function(c) {
            //return Math.abs(this.parent.putCoords({x:c.x, y:0}).x % this.x_spacing);
        }
    });
    
    $.jqplot.QGratingInteractor = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.QGratingInteractor.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.QGratingInteractor.prototype.constructor = $.jqplot.QGratingInteractor;
    $.jqplot.InteractorPluginSubtypes.QGrating = $.jqplot.QGratingInteractor;
    $.extend($.jqplot.QGratingInteractor.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.q_spacing = 0.001;
            $.extend(this, options);
            this.grating = new $.jqplot.QGrating();
            this.grating.initialize(this, 4, true);
            this.grobs.push(this.grating);
        },
        update: function(pos) {
            this.q_spacing = (pos.x > 0) ? Math.abs(2 * Math.PI / pos.x) : 1e-6; // avoid divide by zero errors
            this.redraw();
        }
    });
    
    $.jqplot.Th2ThFromQGrating = function() {};
    $.jqplot.Th2ThFromQGrating.prototype = new $.jqplot.GrobConnector();
    $.jqplot.Th2ThFromQGrating.prototype.constructor = $.jqplot.Th2ThFromQGrating;
    $.extend($.jqplot.Th2ThFromQGrating.prototype, {
        initialize: function (parent, width, autoColor) {
            $.jqplot.GrobConnector.prototype.initialize.call(this, parent, width);
            this.name = 'Grating';
            this.colors = $.jqplot.config.defaultColors;
            this.autoColor = autoColor || false;
            this.show_pos = false;
            this.translatable = false;
            this.connectortranslatable = false;
            //this.points = { p1: p1 };
            //this.q_spacing = q_spacing;

            //this.y_center = this.parent.canvas.height / 2;
            //this.x_center = this.parent.canvas.width / 2;
            //this.p1.pos.y = this.y_center;
            
        },
        
        get_theta_array: function(twotheta, mx, qx_feature, wl) {
            var Q = 4.0 * Math.PI / wl * Math.sin( twotheta_array / 2.0 * (pi / 180.0) )
            qx_target = mx * qx_feature
            mask_2th = (abs(Q) > qx_target)
            Q_masked = Q[mask_2th]
            th = twotheta_array[mask_2th] / 2.0 + arcsin( qx_target / Q[mask_2th] ) * 180.0 / pi
            return twotheta_array[mask_2th], th
        },
        get_wl_twoth: function(qz, mx, qx_feature, theta) {
            var qx = qx_feature * mx;
            var tilt = Math.arctan2(qx, qz);
            var tth = 2.0*(theta*Math.PI/180.0 - tilt);
            var Q = Math.sqrt(Math.pow(qx,2) + Math.pow(qz,2));
            var wl_out = 4*pi/Q * sin(tth/2.0)
            return {x: wl_out, y:tth * 180.0/Math.PI}
        },
        
        get_th_twoth: function (qcoords, wl) {
            //var qx = qx_feature * mx;
            var qx = qcoords.x;
            var qz = qcoords.y;
            var tilt = Math.atan2(qx, Math.abs(qz));
            var Q = Math.sqrt(Math.pow(qx,2) + Math.pow(qz,2));
            var tth = Math.asin(wl * Q / (4 * Math.PI)) * 2.0;
            if (qz < 0) {
                tth *= -1;
                tilt *= -1;
            }
            var th = tth / 2.0 + tilt;
            //2.0*(theta*Math.PI/180.0 - tilt);
            return {x: tth*180.0/Math.PI, y:th * 180.0/Math.PI}
        },
        
        render: function(ctx) {
            $.jqplot.GrobConnector.prototype.render.call(this, ctx);
            function mod(a,b) {
                return a % b < 0 ? b + a % b : a % b
            }
            // have to be careful: this is initialized before the qspace!
            // remember to come back to link qspace to this before rendering page.
            if (this.parent.qspace) {
                //console.log('drawing curvy th-tth lines');
                var height = this.parent.qspace.canvas.height;
                var width = this.parent.qspace.canvas.width;
                var xpos = this.parent.qspace.putCoords({x:0, y:0}).x;
                this.x_spacing = Math.abs(this.parent.qspace.putCoords({x:this.parent.qspace.q_spacing, y:0}).x - xpos);
                var i = 0, pos, prevcoords, coords;
                while (xpos >= 0) {
                    ctx.beginPath();
                    if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                    coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:0}), this.parent.wavelength);
                    pos = this.parent.putCoords(coords);
                    prevcoords = coords;
                    ctx.moveTo(pos.x, pos.y);
                    for (var j = 0; j < this.parent.subsegments; j++) {
                        var y = j/this.parent.subsegments * this.parent.qspace.canvas.height;
                        coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:y}), this.parent.wavelength);
                        pos = this.parent.putCoords(coords);
                        if (coords.x != 0 && (prevcoords.x / coords.x > 0)) ctx.lineTo(pos.x, pos.y);
                        else { ctx.stroke(); ctx.beginPath(); ctx.moveTo(pos.x, pos.y); } 
                        prevcoords = coords;
                    }
                    ctx.stroke();
                    //if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height);   
                    xpos -= this.x_spacing;
                    i -= 1;
                }
                xpos = this.parent.qspace.putCoords({x:0, y:0}).x + this.x_spacing;
                i = 1;
                while (xpos <= width) {
                    ctx.beginPath();
                    if (this.autoColor) ctx.strokeStyle = this.colors[mod(i, this.colors.length)];
                    coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:0}), this.parent.wavelength);
                    pos = this.parent.putCoords(coords);
                    prevcoords = coords;
                    ctx.moveTo(pos.x, pos.y);
                    for (var j = 0; j < this.parent.subsegments; j++) {
                        var y = j/this.parent.subsegments * this.parent.qspace.canvas.height;
                        coords = this.get_th_twoth(this.parent.qspace.getCoords({x:xpos, y:y}), this.parent.wavelength);
                        pos = this.parent.putCoords(coords);
                        if (coords.x != 0 && (prevcoords.x / coords.x > 0)) ctx.lineTo(pos.x, pos.y);
                        else { ctx.stroke(); ctx.beginPath(); ctx.moveTo(pos.x, pos.y); } 
                        prevcoords = coords;
                    }
                    ctx.stroke();
                    //if (this.show_pos) if (this.show_pos) ctx.fillText( (i > 0 ? '+' : '') + i, xpos + 5, height); 
                    xpos += this.x_spacing;
                    i += 1;
                }
            }
        },
        
        distanceTo: function(c) {
            //return Math.abs(this.parent.putCoords({x:c.x, y:0}).x % this.x_spacing);
        }
    });
    
    $.jqplot.Th2ThFromQGratingInteractor = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.Th2ThFromQGratingInteractor.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.Th2ThFromQGratingInteractor.prototype.constructor = $.jqplot.Th2ThFromQGratingInteractor;
    $.jqplot.InteractorPluginSubtypes.Th2ThFromQGrating = $.jqplot.Th2ThFromQGratingInteractor;
    $.extend($.jqplot.Th2ThFromQGratingInteractor.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            //this.q_spacing = 0.001;
            this.qspace = options.qspace || null;
            this.subsegments = 201;
            this.wavelength = 5.0;
            $.extend(this, options);
            this.grating = new $.jqplot.Th2ThFromQGrating();
            this.grating.initialize(this, 4, true);
            this.grobs.push(this.grating);
        },
        update: function(pos) {
            this.redraw();
        }
    });
    
    $.jqplot.CursorInteractor = function() {
        $.jqplot.InteractorPlugin.call(this);
    };
    $.jqplot.CursorInteractor.prototype = new $.jqplot.InteractorPlugin;
    $.jqplot.CursorInteractor.prototype.constructor = $.jqplot.CursorInteractor;
    $.jqplot.InteractorPluginSubtypes.Cursor = $.jqplot.CursorInteractor;
    $.extend($.jqplot.CursorInteractor.prototype, {
        init: function(options) {
            $.jqplot.InteractorPlugin.prototype.init.call(this, options);
            this.x = 0.0;
            this.y = 0.0;
            this.r = 10.0;
            this.color = "yellow";
            $.extend(this, options);
            this.p1 = new $.jqplot.PluginPoint(); this.p1.initialize(this, this.x, this.y, this.r);
            this.p1.color = this.color;
            this.grobs.push(this.p1);
        },
        update: function(pos) {
            this.redraw();
        }
    });
    
})(jQuery);
