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
			"xtype" : "WireIt.ImageContainer",
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
			"xtype" : "WireIt.ImageContainer",
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
			"xtype" : "WireIt.ImageContainer",
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
			"xtype" : "WireIt.ImageContainer",
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
			"xtype" : "WireIt.ImageContainer",
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