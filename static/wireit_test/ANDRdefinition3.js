var andr2 = {
  "languageName": "NCNR ANDR", 
  "modules": [
    {
      "container": {
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
        "xtype": "WireIt.Container",
        //"xtype": "LoadContainer",
      }, 
      "fields": [
        {
          "label": "Files", 
          "name": "files", 
          "type": "[file]", 
          "value": []
        }, 
        {
          "label": "Intent", 
          "name": "intent", 
          "type": "string", 
          "value": ""
        }, 
        {
          "label": "Auto-polstate", 
          "name": "auto_PolState", 
          "type": "boolean", 
          "value": false
        }, 
        {
          "label": "PolStates", 
          "name": "PolStates", 
          "type": "dict:string:string", 
          "value": {}
        }
      ], 
      "name": "Load"
    }, 
    {
      "container": {
        "height": 16, 
        "image": "", 
        "terminals": [
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec.he3:in"
              ], 
              "type": "data2d.ospec.he3:out"
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
          "type": "list:str", 
          "value": []
        }
      ], 
      "name": "Load he3"
    }, 
    {
      "container": {
        "height": 16, 
        "image": "", 
        "terminals": [
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec.timestamp:in"
              ], 
              "type": "data2d.ospec.timestamp:out"
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
          "type": "list:str", 
          "value": []
        }
      ], 
      "name": "Load stamps"
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
        "icon": "../../static/img/offspecular/wiggle.png", 
        "image": "../../static/img/offspecular/wiggle_image.png", 
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
          "label": "amplitude", 
          "name": "scale", 
          "type": "float", 
          "value": 0.14000000000000001
        }
      ], 
      "name": "Wiggle"
    }, 
        {
      "container": {
        "icon": "../../static/img/offspecular/wiggle.png", 
        "image": "../../static/img/offspecular/wiggle_image.png", 
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
        "xtype": "WireIt.Container"
      }, 
      "fields": [
        {
          "label": "0: hanning, 1: hamming\n2:boxcar", 
          "name": "window", 
          "type": "integer", 
          "value": 0
        }
      ], 
      "name": "Smooth"
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
          "label": "pixels per degree", 
          "name": "pixels_per_degree", 
          "type": "float", 
          "value": 80.0
        }, 
        {
          "label": "qzero pixel", 
          "name": "qzero_pixel", 
          "type": "int", 
          "value": 309
        }, 
        {
          "label": "instrument resolution", 
          "name": "instr_resolution", 
          "type": "float", 
          "value": 9.9999999999999995e-07
        }
      ], 
      "name": "Pixels to two theta"
    }, 
    {
      "container": {
        "icon": "../../static/img/offspecular/qxqz.png", 
        "image": "../../static/img/offspecular/qxqz_image.png", 
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
            "multiple": false, 
            "name": "output_grid", 
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
      "fields": [
        {
          "label": "wavelength", 
          "name": "wavelength", 
          "type": "float", 
          "value": 5.0
        }
      ], 
      "name": "Two theta to qxqz"
    }, 
    {
      "container": {
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
        "width": 150, 
        "xtype": "WireIt.Container"
      }, 
      "fields": [
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
      "name": "Empty QxQz grid"
    }, 
    {
      "container": {
        "icon": "../../static/img/offspecular/timestamp.png", 
        "image": "../../static/img/offspecular/timestamp_image.png", 
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
                "data2d.ospec.timestamp:out"
              ], 
              "type": "data2d.ospec.timestamp:in"
            }, 
            "direction": [
              -1, 
              0
            ], 
            "multiple": false, 
            "name": "stamps", 
            "offsetPosition": {
              "left": -12, 
              "top": 40
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
          "label": "Override existing?", 
          "name": "override_existing", 
          "type": "bool", 
          "value": false
        }
      ], 
      "name": "Timestamp"
    }, 
    {
      "container": {
        "icon": "../../static/img/offspecular/app_polar_matrix.png", 
        "image": "../../static/img/offspecular/app_polar_matrix_image.png", 
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
            "multiple": false, 
            "name": "he3cell", 
            "offsetPosition": {
              "left": -12, 
              "top": 40
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
      "fields": [], 
      "name": "Append polarization matrix",
    }, 
    {
      "container": {
        "icon": "../../static/img/offspecular/sum_polar.png", 
        "image": "../../static/img/offspecular/sum_polar_image.png", 
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
            "multiple": false, 
            "name": "grid", 
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
      "name": "Combine polarized"
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
    },
    
    //
        {
      "container": {
        "height": 100,
        "width": 100,  
        "terminals": [
          {
            "alwaysSrc": true, 
            "ddConfig": {
              "allowedTypes": [
                "data2d.ospec:out"
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
            "required": true
          }
        ], 
        "width": 100,
        "height": 100, 
        "xtype": "LoadDropBox"
      }, 
      "fields": [
        {
          "label": "Intent", 
          "name": "intent", 
          "type": "string", 
          "value": ""
        }, 
        {
          "label": "LoadDropBox extension", 
          "name": "ext", 
          "type": "[string]", 
          "value": ""
        }
      ], 
      "name": "LoadDropBox"
    },
    
      { "container": { "height": 100, "width": 100, "terminals": [
          { "alwaysSrc": true, "ddConfig": { "allowedTypes": [ "data2d.ospec:out" ], "type": "data2d.ospec:out" }, 
            "direction": [ 1, 0 ], "multiple": false, "name": "output", "offsetPosition": { "right": -16, "top": 1 }, "required": true } ], 
            "width": 100, "height": 100, "xtype": "LoadFormBox" }, 
        "fields": [ {"label": "Intent", "name": "intent", "type": "string", "value": "" }, 
                    {"label": "LoadFormBox extension", "name": "ext", "type": "[string]", "value": ""} ], 
        "name": "LoadFormBox" },
        
      	   {
	      "name": "LoadContainer",
	      "fields": [   {"label": "Intent", "name": "intent", "type": "string", "value": "" }, 
                        {"label": "LoadContainer extension", "name": "ext", "type": "[string]", "value": "" } ],
			"category": "form",
	        "container": {
	   		"xtype": "LoadContainer",
	   		"width": 250,
	   		"terminals": [{"alwaysSrc": true, "ddConfig": {"allowedTypes": ["data2d.ospec:in"],"type": "data2d.ospec:out"}, "direction": [1,0],"multiple": true, 
            "name": "output", "offsetPosition": {"right": -16, "top": 1}, "required": false}], 
	   		"title": "Files",    
	   		"icon": "",

	   		"collapsible": true,
	   		//"fields": [ 
	   		//	{"type": "select", "label": "Files", "name": "files", "selectValues": [] },
	   		//	{"type":"file", "label":"upload more files", "size": 25}
	   		//],
	   		"legend": "Associated files"
	   	}
	   },
        
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


LoadContainer = function(opts, layer) {
    LoadContainer.superclass.constructor.call(this, opts, layer);
    this.body = document.createElement('div');
    this.form_files = document.createElement('select');
    this.form_files.setAttribute('multiple', 'true');
    this.body.appendChild(this.form_files);
    this.setBody(this.form_files);
    
    //this.form.inputs[0].el.multiple = true;
//    for (var i in FILES) {
//        this.form.inputs[0].addChoice(FILES[i][1])
//    }
    
    this.updateFiles = function() {
        
        this.form_files.innerHTML = "";
        for (var i in FILES) {
            // then fill up with files from FILES
            var newchoice = document.createElement('option');
            newchoice.setAttribute('value', FILES[i][1]);
            newchoice.innerText = FILES[i][1];
            newchoice.selected = false;
            this.form_files.appendChild(newchoice);
        }
        for (var j in this.tracksConfigs) {
            var tracks_files = this.tracksConfigs[j]['files'];
            for (var f in tracks_files) {
                var filename = tracks_files[f][0];
                var options = this.form_files.getElementsByTagName('option');
                for (var o in options) {
                    if (options[o].value == filename) { options[o].selected = true; }
                }
            }
        }
    }
    
//    this.updateFiles = function() {
//        var form_files = this.form.getFieldByName('files');
//        var num_choices = form_files.choicesList.length;
//        for (var i=0; i < num_choices; i++) {
//            // clear out all the choices
//            //var choice = form_files.choicesList[i];
//            form_files.removeChoice(form_files.choicesList[0]);
//        }
//        console.log('form_files length: ', form_files.choicesList.length);
//        for (var i in FILES) {
//            // then fill up with files from FILES
//            form_files.addChoice({"value": FILES[i][1], "selected": false}); 
//        }
//        for (var j in this.tracksConfigs) {
//            var tracks_files = this.tracksConfigs[j]['files'];
//            for (var f in tracks_files) {
//                var filename = tracks_files[f][0];
//                form_files.choicesList[form_files.getChoicePosition({'value': filename})].node.selected = true;                
//            }
//        }
//    }

    //this.form.inputs.push(inputEx.Field({type: "file", name:"newfile"}));
};

YAHOO.lang.extend(LoadContainer, WireIt.Container, {
    xtype: 'LoadContainer',
});

SaveContainer = function(opts, layer) {
    SaveContainer.superclass.constructor.call(this, opts, layer);
    var content = document.createElement('div')
    var name_input = document.createElement('input');
    name_input.type = "text";
    var save_button = document.createElement('button');
    save_button.textContent = "save";
    //content.appendChild(name_input);
    content.appendChild(save_button);
    //content.innerHTML = 'Click here to save:';
    //var saveButton = document.createElement('img');
    //saveButton.src = this.image;
    //content.appendChild(saveButton);    
    this.setBody(content);
    this.name_input = name_input;

    YAHOO.util.Event.addListener(save_button, 'click', this.Save, this, true);
};

YAHOO.lang.extend(SaveContainer, WireIt.Container, {
    xtype: 'SaveContainer',
    Save: function(e) {
        var newname = prompt("Save file to:", "");
        if (!newname || newname == "") {return;}
        var locInFiles = -1;
        for (var i in FILES) {
            if (newname == FILES[i][1]) { locInFiles = i; }
        }
        console.log('locInFiles', locInFiles);
        if (locInFiles >= 0) {
            confirm('file ' + newname + ' exists.  Overwrite?')
        } else {
            alert('I am saving to ' + newname);
        }
    }
});

LoadDropBox = function(opts, layer) {
    LoadDropBox.superclass.constructor.call(this, opts, layer);
    var dropbox = document.createElement('div');
    //dropbox.id = "dropbox";
    var droplabel = document.createElement('span');
    droplabel.innerHTML = "Drop file here...";
    var progressbar = document.createElement('div');
    progressbar.id = 'progressbar';
    this.progressbar = progressbar;
    var newimg = document.createElement('img');
    
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
    
    var uploadForm = document.createElement('form');
    uploadForm.method = "post";
    uploadForm.enctype="multipart/form-data";
    uploadForm.action="#";
    uploadForm.name = "uploadForm";
    uploadForm.id="uploadForm";
    var csrf_div = document.createElement('div');
    csrf_div.style = "display:none";
    var csrf_input = document.createElement('input');
    csrf_input.type = "hidden";
    csrf_input.name = "csrfmiddlewaretoken";
    csrf_input.value = getCookie('csrftoken');
    csrf_div.appendChild(csrf_input);
    var file_input = document.createElement('input');
    file_input.type = "file";
    file_input.multiple = "true";
    file_input.onchange = function() { uploadForm.submit() };
    uploadForm.appendChild(csrf_div);
    uploadForm.appendChild(file_input);
    
//    var formframe = document.createElement('iframe');
//    formframe.id = "upload_form_frame"
//    formframe.width = "100%";
//    formframe.height = "100%";
//    formframe.marginwidth = "0";
//    formframe.marginheight = "0";
//    formframe.vspace = "0";
//    formframe.hspace = "0";
//    formframe.frameborder = "1";
//    formframe.scrolling = "no";
//    formframe.src = "uploadFiles/?experiment_id="+ launchedFromExperimentPage;

//    dropbox.innerHTML =  "<iframe src='uploadFiles/?experiment_id="+ launchedFromExperimentPage +"' width=56 height=50>";
//    dropbox.id = 'dropbox';
//    dropbox.innerHTML =  "<iframe src='uploadFiles/?experiment_id="+ launchedFromExperimentPage +"' width=56 height=50 frameborder=0 scrolling=no>";
    dropbox.appendChild(droplabel);
    dropbox.appendChild(progressbar);
    dropbox.appendChild(newimg);
//    dropbox.appendChild(uploadForm);
    var that = this;
	
	this.setBody(dropbox);
	
	function handleReaderLoadEnd (evt) {
	    $(progressbar).progressbar({ value: 100 });

	    //var img = document.getElementById("preview");
	    //newimg.src = evt.target.result;
        if (evt.target.readyState == FileReader.DONE) { // DONE == 2
            //document.getElementById('byte_content').textContent = evt.target.result;
            //document.getElementById('byte_range').textContent = 
            //['Read bytes: ', start + 1, ' - ', stop + 1,
            // ' of ', file.size, ' byte file'].join('');
            console.log("done.  I am module #:", editor.layer.containers.indexOf(that))
            //editor.uploadFiles(evt.target.result)
        }

	    //makeFileTable(editor.getFATHeaders(),FILES, editor.getValue().working.modules
	    //console.log("done.  I am module #:", editor.layer.containers.indexOf(that))
    }
    
	function handleReaderProgress(evt) {
	    if (evt.lengthComputable) {
		    var loaded = (evt.loaded / evt.total);

		    $(progressbar).progressbar({ value: loaded * 100 });
	    }
    }
    
	function handleFiles(files) {
	    editor.uploadFiles(files)
	    console.log('files: ', files);
	    var file = files[0];
	    //if (files.length > 0) {
	    //    handleFiles(files)
	    //}
        droplabel.innerHTML = "Processing " + file.name;

	    var reader = new FileReader();

	    // init the reader event handlers
	    reader.onprogress = handleReaderProgress;
	    reader.onloadend = handleReaderLoadEnd;

	    // begin the read operation
	    //reader.readAsDataUrl(file);
	    reader.readAsBinaryString(file);
    }

	
	function click(evt) {
	    alert("You shouldn't click me.");
	}
	
	function dragEnter(evt) {
	    evt.stopPropagation();
	    evt.preventDefault();
    }

    function dragExit(evt) {
	    evt.stopPropagation();
	    evt.preventDefault();
    }

    function dragOver(evt) {
	    evt.stopPropagation();
	    evt.preventDefault();
    }

    function drop(evt) {
	    evt.stopPropagation();
	    evt.preventDefault();

	    var files = evt.dataTransfer.files;
	    var count = files.length;

	    // Only call the handler if 1 or more files was dropped.
	    if (count > 0)
		    handleFiles(files);
    }
    
    // init event handlers
	dropbox.addEventListener("dragenter", dragEnter, false);
	dropbox.addEventListener("dragexit", dragExit, false);
	dropbox.addEventListener("dragover", dragOver, false);
	dropbox.addEventListener("drop", drop, false);
	dropbox.addEventListener("click", click, false);
}

YAHOO.lang.extend(LoadDropBox, WireIt.Container, {
    xtype: 'LoadDropBox',
});	
   
//div.fileinputs {
//	position: relative;
//}

//div.fakefile {
//	position: absolute;
//	top: 0px;
//	left: 0px;
//	z-index: 1;
//}

//input.file {
//	position: relative;
//	text-align: right;
//	-moz-opacity:0 ;
//	filter:alpha(opacity: 0);
//	opacity: 0;
//	z-index: 2;
//}

//<div class="fileinputs">
//	<input type="file" class="file" />
//	<div class="fakefile">
//		<input />
//		<img src="search.gif" />
//	</div>
//</div>

LoadFormBox = function(opts, layer) {
    LoadFormBox.superclass.constructor.call(this, opts, layer);
    // create elements
    var body = document.createElement('div');
    var selector = document.createElement('select');
    
            var formdiv = document.createElement('div');
            var input = formdiv.appendChild(document.createElement("input"));
//                input_overlay = formdiv.appendChild(document.createElement("div")),
//                fake_input = input_overlay.appendChild(document.createElement("input")),
//                input_img = input_overlay.appendChild(document.createElement("img"));
            
            formdiv.style.setProperty("position", "relative");
            // set input type as file
            input.setAttribute("type", "file");
            
            // enable multiple selection (note: it does not work with direct input.multiple = true assignment)
            input.setAttribute("multiple", "true");
            
//            // make it invisible, but sitting on top:
//            input.style.setProperty("position", "relative");
//            input.style.setProperty("text-align", "right");
//	        input.style.setProperty("-moz-opacity", "0");
//	        input.style.setProperty("filter", "alpha(opacity: 0)");
//	        input.style.setProperty("opacity", 0);
//	        input.style.setProperty("z-index", 2);
//	        
//	        // add the image overlay
//	        input_overlay.style.setProperty("position", "absolute");
//	        input_overlay.style.setProperty("top", "0px");
//	        input_overlay.style.setProperty("left", "0px");
//	        input_overlay.style.setProperty("z-index", 1);
//	        //var img_actual = new Image();
//	        
//	        input_img.src = "/static/img/upload_files.png";
            
            // auto upload on files change
            input.addEventListener("change", function(){
                editor.uploadFiles(input.files)
                }, false);
            
	
	this.setBody(formdiv);
}

YAHOO.lang.extend(LoadFormBox, WireIt.Container, {
    xtype: 'LoadFormBox',
});	
