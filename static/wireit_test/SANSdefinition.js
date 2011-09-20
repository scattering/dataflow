var sans = {
	"modules" : [{
		"container" : {
			"width" : 120,
			"terminals" : [{
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.sans:out",
					"allowedTypes" : ["data1d.sans:in"]
				},
				"offsetPosition" : {
					"top" : 1,
					"right" : -16
				}
			}],
			"xtype" : "WireIt.Container",
			"height" : 16
		},
		"name" : "Load"
	}, {
		"container" : {
			"width" : 120,
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : false,
				"name" : "input",
				"required" : true,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.sans:in",
					"allowedTypes" : ["data1d.sans:out"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : -16
				}
			}],
			"xtype" : "WireIt.Container",
			"height" : 16
		},
		"name" : "Save"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : true,
				"name" : "input",
				"required" : false,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.sans:in",
					"allowedTypes" : ["data1d.sans:out"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : -16
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.sans:out",
					"allowedTypes" : ["data1d.sans:in"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : 48
				}
			}],
			"xtype" : "AutosizeImageContainer",
			"width" : "auto",
			"image" : "../../static/img/SANS/div_image.png",
			"icon" : "../../static/img/SANS/div.png"
		},
		"name" : "Correct Detector Sensitivity"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : true,
				"name" : "input",
				"required" : false,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.sans:in",
					"allowedTypes" : ["data1d.sans:out"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : -16
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.sans:out",
					"allowedTypes" : ["data1d.sans:in"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : 48
				}
			}],
			"xtype" : "AutosizeImageContainer",
			"width" : "auto",
			"image" : "../../static/img/SANS/correct_background_image.png",
			"icon" : "../../static/img/SANS/correct_background.png"
		},
		"name" : "correct_background"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : true,
				"name" : "input",
				"required" : false,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.sans:in",
					"allowedTypes" : ["data1d.sans:out"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : -16
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.sans:out",
					"allowedTypes" : ["data1d.sans:in"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : 48
				}
			}],
			"xtype" : "AutosizeImageContainer",
			"width" : "auto",
			"image" : "../../static/img/SANS/initial_correction_image.png",
			"icon" : "../../static/img/SANS/initial_correction.png"
		},
		"name" : "initial_correction"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : true,
				"name" : "input",
				"required" : false,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.sans:in",
					"allowedTypes" : ["data1d.sans:out"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : -16
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.sans:out",
					"allowedTypes" : ["data1d.sans:in"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : 48
				}
			}],
			"xtype" : "AutosizeImageContainer",
			"width" : "auto",
			"image" : "../../static/img/SANS/annular2_image.png",
			"icon" : "../../static/img/SANS/annular2.png"
		},
		"name" : "annular_av"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : true,
				"name" : "input",
				"required" : false,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.sans:in",
					"allowedTypes" : ["data1d.sans:out"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : -16
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.sans:out",
					"allowedTypes" : ["data1d.sans:in"]
				},
				"offsetPosition" : {
					"top" : 16,
					"left" : 48
				}
			}],
			"xtype" : "AutosizeImageContainer",
			"width" : "auto",
			"image" : "../../static/img/SANS/abs_image.png",
			"icon" : "../../static/img/SANS/abs.png"
		},
		"name" : "absolute_scaling"
	}],
	"propertiesFields" : [{
		"typeInvite" : "Enter a title",
		"type" : "string",
		"name" : "name",
		"label" : "Title"
	}, {
		"label" : "Description",
		"type" : "text",
		"name" : "description",
		"cols" : 30
	}],
	"languageName" : "NCNR SANS INS"
}

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
