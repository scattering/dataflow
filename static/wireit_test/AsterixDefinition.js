var asterix = {
  "languageName": "LANSCE ASTERIX", 
  "modules": [
        {"container": {
        "height": 16, 
        "image": "", 
        "terminals": [
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "right": -16, 
              "top": 1
            }, 
            "required": false
          }
        ], 
        "width": 120, 
        "xtype": "WireIt.Container"
      }, 
      "fields": [
        {
          "label": "Files", 
          "name": "files", 
          "type": "[file]", 
          "value": []
        }, 
//        {
//          "label": "Center Pixel", 
//          "name": "center_pixel", 
//          "type": "float", 
//          "value": 145.0,
//        }, 
//        {
//          "label": "Wavelength over Time-of-Flight", 
//          "name": "wl_over_tof", 
//          "type": "scientific", 
//          "value": 1.9050372144288577e-5,
//        }, 
//        {
//          "label": "Pixel width/distance (to sample)", 
//          "name": "pixel_width_over_dist", 
//          "type": "float", 
//          "value":  0.00034113856493630764,
//        },
      ], 
      "name": "LoadAsterix"
    },
    {"container": {
        "height": 16, 
        "image": "", 
        "terminals": [
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": false, 
            "name": "output", 
            "offsetPosition": {
              "right": -16, 
              "top": 1
            }, 
            "required": false
          }
        ], 
        "width": 120, 
        "xtype": "WireIt.Container"
      }, 
      "fields": [
        {
          "label": "Files", 
          "name": "files", 
          "type": "[file]", 
          "value": []
        }, 
      ], 
      "name": "LoadAsterixSpectrum"
    },
    {
      "container": {
        "height": 16, 
        "image": "../../static/img/offspecular/save_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -16, 
              "top": 1
            }, 
            "required": true
          }
        ], 
        "width": 120, 
        "xtype": "SaveContainer"
      }, 
      "fields": [
        {
          "label": "Intent", 
          "name": "intent", 
          "type": "string", 
          "value": ""
        }, 
        {
          "label": "Save extension", 
          "name": "ext", 
          "type": "[string]", 
          "value": ""
        }
      ], 
      "name": "Save"
    },
    {
      "container": { 
        "height": 16, 
        "terminals": [
        {  "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -16, 
              "top": 1
            }, 
            "required": true
          }
        ], 
        "width": 120, 
        "xtype": "SliceContainer"
      }, 
      "fields": [
        {
          "label": "Intent", 
          "name": "intent", 
          "type": "string", 
          "value": ""
        }
      ], 
      "name": "Slice Data"
    },
    {
      "container": {
        "icon": "../../static/img/offspecular/correct_spectrum_icon.png", 
        "image": "../../static/img/offspecular/correct_spectrum_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 4
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": true, 
            "name": "spectrum", 
            "offsetPosition": {
              "left": -12, 
              "top": 40
            }, 
            "required": false
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [], 
      "name": "Correct Spectrum"
    },
    {
      "container": {
        "icon": "../../static/img/offspecular/tof_lambda_icon.png", 
        "image": "../../static/img/offspecular/tof_lambda_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [
        {
          "label": "Wavelength over Time-of-Flight", 
          "name": "wl_over_tof", 
          "type": "scientific", 
          "value": 1.9050372144288577e-5,
        }, 
      ], 
      "name": "TOF to Wavelength"
    },
    {
      "container": {
        "icon": "../../static/img/offspecular/shift_icon.png", 
        "image": "../../static/img/offspecular/shift_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [
        {
          "label": "Edge Bin", 
          "name": "edge_bin", 
          "type": "int", 
          "value": 180,
        },
        {
          "label": "Axis",
          "name": "axis",
          "type": "int",
          "value": 0,
        },
      ], 
      "name": "Shift Data"
    },
    {
      "container": {
        "icon": "../../static/img/offspecular/qxqz.png", 
        "image": "../../static/img/offspecular/twothetalambda_qxqz_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 4
            }, 
            "required": true
          },  
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      },
      "fields": [
        {
          "label": "Sample angle (theta)", 
          "name": "theta", 
          "type": "string", 
          "value": ""
        },
        {
          "label": "Qx min", 
          "name": "qxmin", 
          "type": "float", 
          "value": -0.0030000000000000001
        }, 
        {
          "label": "Qx max", 
          "name": "qxmax", 
          "type": "float", 
          "value": 0.0030000000000000001
        }, 
        {
          "label": "Qx bins", 
          "name": "qxbins", 
          "type": "int", 
          "value": 201
        }, 
        {
          "label": "Qz min", 
          "name": "qzmin", 
          "type": "float", 
          "value": 0.0
        }, 
        {
          "label": "Qz max", 
          "name": "qzmax", 
          "type": "float", 
          "value": 0.10000000000000001
        }, 
        {
          "label": "Qz bins", 
          "name": "qzbins", 
          "type": "int", 
          "value": 201
        }
      ], 
      "name": "Two theta lambda to qxqz"
    },
    {
      "container": {
        "icon": "../../static/img/offspecular/autogrid.png", 
        "image": "../../static/img/offspecular/mask_image.png", 
        "height": 16, 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "right": -12, 
              "top": 16
            }, 
            "required": false
          }
        ],  
        "width": 80, 
        "xtype": "AutosizeImageContainer",
      }, 
      "fields": [
        {
          "label": "xmin pixel", 
          "name": "xmin", 
          "type": "string", 
          "value": "0"
        }, 
        {
          "label": "xmax pixel", 
          "name": "xmax", 
          "type": "string", 
          "value": ""
        }, 
        {
          "label": "ymin pixel", 
          "name": "ymin", 
          "type": "string", 
          "value": "0"
        }, 
        {
          "label": "ymax pixel", 
          "name": "ymax", 
          "type": "string", 
          "value": ""
        }, 
      ], 
      "name": "Mask Data"
    }, 
    
    {
      "container": {
        "icon": "../../static/img/offspecular/sum.png", 
        "image": "../../static/img/offspecular/sum_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input_data", 
            "offsetPosition": {
              "left": -12, 
              "top": 4
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": true, 
            "name": "input_grid", 
            "offsetPosition": {
              "left": -12, 
              "top": 40
            }, 
            "required": false
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [], 
      "name": "Combine"
    }, 
    {
      "container": {
        "icon": "../../static/img/offspecular/offset.png", 
        "image": "../../static/img/offspecular/offset_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "right": -16, 
              "top": 16
            }, 
            "required": false
          }
        ],
        "width": 120,
        "xtype": "OffsetContainer"
      }, 
      "fields": [
        {
          "label": "Offset amount", 
          "name": "offsets", 
          "type": "dict:str:float", 
          "value": {
            "theta": 0.0, 
            "xpixel": 0.0
          }
        }
      ],
      "name": "Offset"
    },
    
    {
      "container": {
        "icon": "../../static/img/offspecular/twotheta.png", 
        "image": "../../static/img/offspecular/twotheta_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [
        {
          "label": "pixel width over d", 
          "name": "pw_over_d", 
          "type": "float", 
          "value": 0.0003411385649,
        }, 
        {
          "label": "qzero pixel", 
          "name": "qzero_pixel", 
          "type": "float", 
          "value": 145.0,
        }, 
        {
          "label": "twotheta offset", 
          "name": "twotheta_offset", 
          "type": "float", 
          "value": 0.0,
        }
      ], 
      "name": "Asterix Pixels to two theta"
    },
//    {
//      "container": {
//        "icon": "../../static/img/offspecular/autogrid.png", 
//        "image": "../../static/img/offspecular/slice_image.png", 
//        "terminals": [
//          { "alwaysSrc": false, 
//            "ddConfig": {
//              "allowedTypes": ["data2d.ospec:out" ], 
//              "type": "data2d.ospec:in"
//            }, 
//            "direction": [-1,0], 
//            "multiple": false, 
//            "name": "input", 
//            //"offsetPosition": {"left": -12, "top": 16}, 
//            "required": true
//          }, 
//          {
//            "alwaysSrc": true, 
//            "ddConfig": {
//              "allowedTypes": ["data2d.ospec:in"], 
//              "type": "data2d.ospec:out"
//            }, 
//            "direction": [0,1], 
//            "multiple": true, 
//            "name": "output_x", 
//            //"offsetPosition": {"right": -16,"top": 4}, 
//            "required": false
//          }, 
//          {
//            "alwaysSrc": true, 
//            "ddConfig": {
//              "allowedTypes": ["data2d.ospec:in"], 
//              "type": "data2d.ospec:out"
//            }, 
//            "direction": [1,0], 
//            "multiple": true, 
//            "name": "output_y", 
//            //"offsetPosition": {"right": -16, "top": 40}, 
//            "required": false
//          }
//        ], 
//        "xtype": "AutosizeImageContainer"
//      }, 
//      "fields": [], 
//      "name": "Slice Data"
//    },
    {
      "container": {
        "icon": "../../static/img/offspecular/autogrid.png", 
        "image": "../../static/img/offspecular/autogrid_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [
        {
          "label": "extra grid point", 
          "name": "extra_grid_point", 
          "type": "bool", 
          "value": true
        }, 
        {
          "label": "minimum step", 
          "name": "min_step", 
          "type": "float", 
          "value": 1e-10
        }
      ], 
      "name": "Autogrid"
    },
    {"container": {
        "icon": "../../static/img/offspecular/normalize_icon.png",
        "image": "../../static/img/offspecular/normalize_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          },
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": false, 
            "name": "output", 
            "offsetPosition": {
              "right": -16, 
              "top": 1
            }, 
            "required": false
          }
        ], 
        "width": 120, 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [], 
      "name": "Normalize to Monitor"
    },  
    {
      "container": {
        "icon": "../../static/img/offspecular/polar_correct.png", 
        "image": "../../static/img/offspecular/polar_correct_image.png", 
        "terminals": [
          {
            "alwaysSrc": false, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
              ], 
              "type": "data2d.ospec:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "input", 
            "offsetPosition": {
              "left": -12, 
              "top": 16
            }, 
            "required": true
          }, 
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:in"
              ], 
              "type": "data2d.ospec:out"
            }, 
            "direction": [
              1, 
              0
            ], 
            "multiple": true, 
            "name": "output", 
            "offsetPosition": {
              "left": 48, 
              "top": 16
            }, 
            "required": false
          }
        ], 
        "xtype": "AutosizeImageContainer"
      }, 
      "fields": [
        {
          "label": "Polarization assumptions", 
          "name": "assumptions", 
          "type": "int", 
          "value": 0
        }, 
        {
          "label": "Auto assumptions", 
          "name": "auto_assumptions", 
          "type": "bool", 
          "value": true
        }
      ], 
      "name": "Polarization correction"
    }
  ], 
  "propertiesFields": [
    {
      "label": "Title", 
      "name": "name", 
      "type": "string", 
      "typeInvite": "Enter a title"
    }, 
    {
      "cols": 30, 
      "label": "Description", 
      "name": "description", 
      "type": "text"
    }
  ]
};

OffsetContainer = function(opts, layer) {
    OffsetContainer.superclass.constructor.call(this, opts, layer);
    var content = document.createElement('div');
    content.innerHTML = '';
    //var saveButton = document.createElement('img');
    var getAxisInfoButton = document.createElement('button');
    getAxisInfoButton.value = 'getaxisinfo';
    getAxisInfoButton.innerHTML = 'Get axis info';
    //saveButton.src = this.image;
    content.appendChild(getAxisInfoButton);
    this.axisDescription = document.createElement('div');
    console.log(this.axisDescription);
    this.axisDescription.innerHTML = '';
    console.log(this.axisDescription, this);
    content.appendChild(this.axisDescription)
    
    this.setBody(content);
    YAHOO.util.Event.addListener(getAxisInfoButton, 'click', this.getAxisInfo, this, true);
};

YAHOO.lang.extend(OffsetContainer, WireIt.Container, {
    getAxisInfo: function(e, f) {
        var reductionInstance = editor.reductionInstance;
        var wires = f.wires;
        if (wires.length == 0) {
            alert('no data to get (no wires in)');
            return
        } else {
            var wire_in = f.wires[0];
            clickedOn = {'source': wire_in.src,'target': wire_in.tgt};
        }
        //editor.getPlottable(reductionInstance, clickedOn);
		var toReduce = editor.generateReductionRecipe(reductionInstance, clickedOn);
        //if (this.terminals[0].wires.length < 1) { alert('no wires'); return }
		editor.adapter.runReduction(toReduce, {
		    success: this.updateAxes,
		    failure: editor.runModuleFailure,
		    scope: this,
		});		    		    
	},
    updateAxes: function(plottable_data) {
        console.log('updating Axes');
        if (Object.prototype.toString.call(plottable_data) === "[object Array]") {
            var plottable_data = plottable_data[0];
        }
        if (plottable_data.type == "2d") {
            var axes_labels = [plottable_data.xlabel, plottable_data.ylabel];
        }
        else if (plottable_data.typ == "nd") {
            var axes_labels = [plottable_data.orderx[0].label];
        }
        var displayText = "";
        for (var i in axes_labels) {
            displayText += axes_labels[i] + '<br>';
        }
        var module = null;
        //var CHOSEN_LANG = andr2;
        for (var index in CHOSEN_LANG.modules) {
		    if(CHOSEN_LANG.modules[index].name == this.title) {
		        module = CHOSEN_LANG.modules[index];
				break;
			}
		}
        console.log(plottable_data, this, "displayText:", displayText, "fields:", module.fields);
        this.axisDescription.innerHTML = displayText;
        module.fields[0].value = {}
        for (var i in axes_labels) {
            module.fields[0].value[axes_labels[i]] = 0.0;
        }
    },
});

SaveContainer = function(opts, layer) {
    SaveContainer.superclass.constructor.call(this, opts, layer);
    
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    var content = document.createElement('div');
    content.innerHTML = '';
    //var saveButton = document.createElement('img');
    var saveButton = document.createElement('button');
    saveButton.value = 'save';
    saveButton.innerHTML = 'Save';
    //saveButton.src = this.image;
    content.appendChild(saveButton); 
    
//    var getCSVForm = document.createElement('form');
//    getCSVForm.method = "post";
//    getCSVForm.action="getCSV/";
//    getCSVForm.id = 'narf';
//    var csrf_div = document.createElement('div');
//    csrf_div.style = "display:none";
//    var csrf_input = document.createElement('input');
//    csrf_input.type = "hidden";
//    csrf_input.name = "csrfmiddlewaretoken";
//    csrf_input.value = getCookie('csrftoken');
//    csrf_div.appendChild(csrf_input);
//    getCSVForm.appendChild(csrf_div);
//    var data_input = document.createElement('input');
//    data_input.type = 'hidden';
//    data_input.id = 'data';
//    data_input.name = 'data';
//    getCSVForm.appendChild(data_input);
//    var outfilename = document.createElement('input');
//    outfilename.type='text';
//    outfilename.id = 'outfilename';
//    outfilename.value = 'data.csv';
//    getCSVForm.appendChild(outfilename);
    
    var getCSVButton = document.createElement('button');
    //getCSVButton.type = 'submit';
    getCSVButton.value = 'getCSV';
    getCSVButton.innerHTML = 'download CSV';
    //saveButton.src = this.image;
    //getCSVForm.appendChild(getCSVButton); 
    //content.appendChild(getCSVForm);
    content.appendChild(getCSVButton);
      
    this.setBody(content);
    this.CSVForm = getCSVForm;

    YAHOO.util.Event.addListener(saveButton, 'click', this.Save, this, true);
    YAHOO.util.Event.addListener(getCSVButton, 'click', this.getCSV, this, true);
};

YAHOO.lang.extend(SaveContainer, WireIt.Container, {
    xtype: 'SaveContainer',
    Save: function(e) {
        console.log('save click:', e);
        alert('save to server not yet implemented.  Try downloading CSV version of data');
    },
    getCSV: function(e, f) {
        var reductionInstance = editor.reductionInstance;
        var wires = f.wires;
        if (wires.length == 0) {
            alert('no data to get (no wires in)');
            return
        } else {
            var wire_in = f.wires[0];
            clickedOn = {'source': wire_in.src,'target': wire_in.tgt};
        }
        editor.getCSV(reductionInstance, clickedOn);
    }
});

SliceContainer = function(opts, layer) {
    SliceContainer.superclass.constructor.call(this, opts, layer);
    var content = document.createElement('div');
    content.innerHTML = '';
    //var saveButton = document.createElement('img');
    var sliceButton = document.createElement('button');
    sliceButton.value = 'slice';
    sliceButton.innerHTML = 'Slice';
    //saveButton.src = this.image;
    content.appendChild(sliceButton);
    this.setBody(content);
    YAHOO.util.Event.addListener(sliceButton, 'click', this.openSliceWindow, this, true);
};

YAHOO.lang.extend(SliceContainer, WireIt.Container, {
    xtype: 'SliceContainer',
    openSliceWindow: function(e) {
        //console.log('save click:', e);
        //alert('save to server not yet implemented.  Try downloading CSV version of data');
        this.sliceWindow = window.open("/plotWindow/", "", "status=1,width=650,height=500");
        this.sliceWindow.update_plot(editor.toPlots);
    }
});


