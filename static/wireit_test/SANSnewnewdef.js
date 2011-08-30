var sans = {"propertiesFields": [{"typeInvite": "Enter a title", "type": "string", "name": "name", "label": "Title"}, {"type": "text", "name": "description", "cols": 30, "label": "Description"}], "modules": [{"fields": [{"type": "[file]", "name": "files", "value": [], "label": "Files"}, {"type": "string", "name": "intent", "value": "", "label": "Intent"}], "container": {"width": 120, "terminals": [{"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 1, "right": -16}}], "xtype": "WireIt.Container", "height": 16}, "name": "Load"}, {"fields": [{"type": "string", "name": "intent", "value": "", "label": "Intent"}, {"type": "[string]", "name": "ext", "value": "", "label": "Save extension"}], "container": {"width": 120, "terminals": [{"direction": [-1, 0], "multiple": false, "name": "input", "required": true, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 1, "left": -16}}], "xtype": "WireIt.Container", "height": 16}, "name": "Save"}, {"fields": [{"type": "float", "name": "deadtimeConstant", "value": 3.4e-06, "label": "Deadtime Constant (default=3.4e-6)"}], "container": {"terminals": [{"direction": [-1, 0], "multiple": false, "name": "sample_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 10, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "empty_cell_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 20, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "empty_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 30, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "blocked_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 40, "left": -16}}, {"direction": [1, 0], "multiple": true, "name": "sample_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 10, "left": 48}}, {"direction": [1, 0], "multiple": true, "name": "empty_cell_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 20, "left": 48}}, {"direction": [1, 0], "multiple": true, "name": "empty_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 30, "left": 48}}, {"direction": [1, 0], "multiple": true, "name": "blocked_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 40, "left": 48}}], "xtype": "AutosizeImageContainer", "image": "../../static/img/SANS/deadtime.png", "icon": "../../static/img/SANS/deadtime_image.png"}, "name": "Dead time Correction"}, {"fields": [{"type": "float", "name": "monitorNormalize", "value": 100000000.0, "label": "Monitor Normalization Count (default=1e8)"}, {"type": "dict", "name": "bottomLeftCoord", "value": {"Y": 0, "X": 0}, "label": "Bottom Left Coordinate"}, {"type": "dict", "name": "topRightCoord", "value": {"Y": 0, "X": 0}, "label": "Top Right Coordinate"}], "container": {"terminals": [{"direction": [-1, 0], "multiple": false, "name": "sample_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 5, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "empty_cell_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 15, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "empty_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 25, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "Tsam_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 35, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "Temp_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 45, "left": -16}}, {"direction": [1, 0], "multiple": true, "name": "sample_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 10, "left": 48}}, {"direction": [1, 0], "multiple": true, "name": "empty_cell_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 30, "left": 48}}], "xtype": "AutosizeImageContainer", "image": "../../static/img/SANS/gen_trans_image.png", "icon": "../../static/img/SANS/gen_trans.png"}, "name": "Generate Transmission"}, {"fields": [], "container": {"terminals": [{"direction": [-1, 0], "multiple": false, "name": "COR", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 10, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "DIV_in", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 30, "left": -16}}, {"direction": [1, 0], "multiple": true, "name": "DIV_out", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 10, "left": 48}}], "xtype": "AutosizeImageContainer", "image": "../../static/img/SANS/div_image.png", "icon": "../../static/img/SANS/div.png"}, "name": "Correct Detector Sensitivity"}, {"fields": [], "container": {"terminals": [{"direction": [-1, 0], "multiple": false, "name": "sample", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 8, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "empty_cell", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 28, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "blocked", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 48, "left": -16}}, {"direction": [1, 0], "multiple": true, "name": "COR", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 10, "left": 48}}], "xtype": "AutosizeImageContainer", "image": "../../static/img/SANS/initial_correction_image.png", "icon": "../../static/img/SANS/initial_image.png"}, "name": "Initial Correction"}, {"fields": [], "container": {"terminals": [{"direction": [-1, 0], "multiple": false, "name": "ABS", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 10, "left": -16}}, {"direction": [1, 0], "multiple": true, "name": "OneD", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 10, "left": 48}}], "xtype": "AutosizeImageContainer", "image": "../../static/img/SANS/circular_avg.png", "icon": "../../static/img/SANS/circular_avg_image.png"}, "name": "Circular Average"}, {"fields": [{"type": "string", "name": "ins_name", "value": "", "label": "Instrument Name (NG3,NG5,or NG7)"}, {"type": "dict", "name": "bottomLeftCoord", "value": {"Y": 0, "X": 0}, "label": "Bottom Left Coordinate"}, {"type": "dict", "name": "topRightCoord", "value": {"Y": 0, "X": 0}, "label": "Top Right Coordinate"}], "container": {"terminals": [{"direction": [-1, 0], "multiple": false, "name": "DIV", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 5, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "empty", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 25, "left": -16}}, {"direction": [-1, 0], "multiple": false, "name": "sensitivity", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data2d.sans:in", "allowedTypes": ["data2d.sans:out"]}, "offsetPosition": {"top": 40, "left": -16}}, {"direction": [1, 0], "multiple": true, "name": "ABS", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data2d.sans:out", "allowedTypes": ["data2d.sans:in"]}, "offsetPosition": {"top": 10, "left": 48}}], "xtype": "AutosizeImageContainer", "image": "../../static/img/SANS/abs_image.png", "icon": "../../static/img/SANS/Abs.png"}, "name": "Absolute Scaling"}], "languageName": "NCNR SANS INS"}

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
                term.offsetPosition[d] = (-1 * term_size);
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

