var langandr = {
  "languageName": "NCNR ANDR", 
  "modules": [
    {
      "container": {
        "height": 16, 
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
      "name": "Load"
    }, 
    {
      "container": {
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
              "left": -16, 
              "top": 1
            }, 
            "required": true
          }
        ], 
        "width": 120, 
        "xtype": "WireIt.Container"
      }, 
      "name": "Save"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/autogrid.png", 
        "image": "../../static/img/rowantests/autogrid_image.png", 
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
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Autogrid"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/sum.png", 
        "image": "../../static/img/rowantests/sum_image.png", 
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
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Combine"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/offset.png", 
        "image": "../../static/img/rowantests/offset_image.png", 
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
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Offset"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/wiggle.png", 
        "image": "../../static/img/rowantests/wiggle_image.png", 
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
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Wiggle"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/twotheta.png", 
        "image": "../../static/img/rowantests/twotheta_image.png", 
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
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Pixels to two theta"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/qxqz.png", 
        "image": "../../static/img/rowantests/qxqz_image.png", 
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
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Two theta to qxqz"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/load_he3.png", 
        "image": "../../static/img/rowantests/load_he3_image.png", 
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
              "left": 20, 
              "top": 10
            }, 
            "required": false
          }
        ], 
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Load he3"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/timestamp.png", 
        "image": "../../static/img/rowantests/timestamp_image.png", 
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
              "left": 0, 
              "top": 10
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
              "left": 20, 
              "top": 10
            }, 
            "required": false
          }
        ], 
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Timestamp"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/app_polar_matrix.png", 
        "image": "../../static/img/rowantests/app_polar_matrix_image.png", 
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
              "left": -15, 
              "top": 1
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
              "left": -10, 
              "top": 1
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
              "left": 15, 
              "top": 1
            }, 
            "required": false
          }
        ], 
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Append polarization matrix"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/sum_polar.png", 
        "image": "../../static/img/rowantests/sum_polar_image.png", 
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
              "left": -15, 
              "top": 1
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
              "left": -10, 
              "top": 1
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
              "left": 15, 
              "top": 1
            }, 
            "required": false
          }
        ], 
        "xtype": "WireIt.ImageContainer"
      }, 
      "name": "Combine polarized"
    }, 
    {
      "container": {
        "icon": "../../static/img/rowantests/polar_correct.png", 
        "image": "../../static/img/rowantests/polar_correct_image.png", 
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
              "left": 0, 
              "top": 10
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
              "left": 20, 
              "top": 10
            }, 
            "required": false
          }
        ], 
        "xtype": "WireIt.ImageContainer"
      }, 
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