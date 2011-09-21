AutosizeImageContainer = function(opts, layer) {
    AutosizeImageContainer.superclass.constructor.call(this, opts, layer);
    var that = this;

    function auto_space(number, width) {
        // takes a number and places it in the width evenly
        var locs = [];
        if (number == 1) {
            locs.push(Math.round(width / 2));
        } else {
            var spacing = width / (number-1);
            for (var i=0; i<number; i++) {
                locs.push(Math.round(i*spacing));
            }
        }  
        return locs;
    }
    
    function distribute_terminals(terminals, width, height) {
        var locs = [];
        var directions = {
            'left': {'fit_axis':'top', 'range': width, 'test': function(el) { return el.direction[0] < 0 } },
            'right': {'fit_axis':'top', 'range': width, 'test': function(el) { return el.direction[0] > 0 } },
            'top': {'fit_axis':'left', 'range': height, 'test': function(el) { return el.direction[1] < 0 } },
            'bottom': {'fit_axis':'left', 'range': height, 'test': function(el) { return el.direction[1] > 0 } },
        }
        
        for (var d in directions) {
            var terms = terminals.filter( directions[d].test );
            var padding = 4;
            var term_size = 16;
            var range = (directions[d].range - term_size) - (2*padding);
            var locs = auto_space(terms.length, range);
            for (var i in terms) {
                var term = terms[i];
                term.el.style.setProperty(d, (-1 * term_size));
                term.offsetPosition = {d: (-1 * term_size)};
                term.el.style.setProperty(directions[d].fit_axis, (locs[i] - (term_size/2) + padding));
                term.offsetPosition[directions[d].fit_axis] = (locs[i] - (term_size/2) + padding);
            }
        }
    }
    
    this.image_obj = new Image();
    var that = this;
    this.image_obj.onload = function() {
        // set the element size, and distribute terminals.
        that.el.style.width = that.image_obj.width + "px";
        that.el.style.height = that.image_obj.height + "px";
        distribute_terminals(that.terminals, that.image_obj.width, that.image_obj.height);
    }
    this.image_obj.src = opts.image;
}

YAHOO.lang.extend(AutosizeImageContainer, WireIt.ImageContainer, {
    xtype: 'AutosizeImageContainer',
});
