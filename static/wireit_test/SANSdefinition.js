var sans_lang = {"propertiesFields": [{"typeInvite": "Enter a title", "type": "string", "name": "name", "label": "Title"}, {"type": "text", "name": "description", "cols": 30, "label": "Description"}], "modules": [{"container": {"width": 120, "terminals": [{"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 1, "right": -16}}], "xtype": "WireIt.Container", "height": 16}, "name": "Load"}, {"container": {"width": 120, "terminals": [{"direction": [-1, 0], "multiple": false, "name": "input", "required": true, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 1, "left": -16}}], "xtype": "WireIt.Container", "height": 16}, "name": "Save"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/convertq.png", "icon": "../../static/img/rowantests/convertq.png"}, "name": "Convertq"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/correct_detector_efficiency.png", "icon": "../../static/img/rowantests/correct_detector_efficiency.png"}, "name": "correct_detector_efficiency"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/monitor_normalize.png", "icon": "../../static/img/rowantests/monitor_normalize.png"}, "name": "monitor_normalize"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/correct_background.png", "icon": "../../static/img/rowantests/correct_background.png"}, "name": "correct_background"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/generate_transmission.png", "icon": "../../static/img/rowantests/generate_transmission.png"}, "name": "generate_transmission"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/initial_correction.png", "icon": "../../static/img/rowantests/initial_correction.png"}, "name": "initial_correction"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/correct_solid_angle.png", "icon": "../../static/img/rowantests/correct_solid_angle.png"}, "name": "correct_solid_angle"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/convert_qxqy.png", "icon": "../../static/img/rowantests/convert_qxqy.png"}, "name": "convert_qxqy"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/annular_av.png", "icon": "../../static/img/rowantests/annular_av.png"}, "name": "annular_av"}, {"container": {"terminals": [{"direction": [-1, 0], "multiple": true, "name": "input", "required": false, "alwaysSrc": false, "ddConfig": {"type": "data1d.sans:in", "allowedTypes": ["data1d.sans:out"]}, "offsetPosition": {"top": 10, "left": 0}}, {"direction": [1, 0], "multiple": true, "name": "output", "required": false, "alwaysSrc": true, "ddConfig": {"type": "data1d.sans:out", "allowedTypes": ["data1d.sans:in"]}, "offsetPosition": {"top": 10, "left": 20}}], "xtype": "WireIt.ImageContainer", "image": "../../static/img/rowantests/absolute_scaling.png", "icon": "../../static/img/rowantests/absolute_scaling.png"}, "name": "absolute_scaling"}], "languageName": "NCNR SANS INS"}

