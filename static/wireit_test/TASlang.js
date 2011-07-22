var tas = {
	"propertiesFields" : [{
		"typeInvite" : "Enter a title",
		"type" : "string",
		"name" : "name",
		"label" : "Title"
	}, {
		"type" : "text",
		"name" : "description",
		"cols" : 30,
		"label" : "Description"
	}],
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
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
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
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
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
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : -15
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : 15
				}
			}],
			"xtype" : "WireIt.ImageContainer",
			"image" : "../../static/img/sum.png",
			"icon" : "../../static/img/sum.png"
		},
		"name" : "Join"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : true,
				"name" : "input",
				"required" : false,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
				},
				"offsetPosition" : {
					"top" : 10,
					"left" : 0
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
				},
				"offsetPosition" : {
					"top" : 10,
					"left" : 20
				}
			}],
			"xtype" : "WireIt.ImageContainer",
			"image" : "../../static/img/scale.png",
			"icon" : "../../static/img/scale.png"
		},
		"name" : "Scale"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : false,
				"name" : "input",
				"required" : true,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : -15
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : 15
				}
			}],
			"xtype" : "WireIt.ImageContainer",
			"image" : "../../static/img/sum.png",
			"icon" : "../../static/img/sum.png"
		},
		"name" : "Normalize Monitor"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : false,
				"name" : "input",
				"required" : true,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : -15
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : 15
				}
			}],
			"xtype" : "WireIt.ImageContainer",
			"image" : "../../static/img/sum.png",
			"icon" : "../../static/img/sum.png"
		},
		"name" : "Detailed Balance"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : false,
				"name" : "input",
				"required" : true,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : -15
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : 15
				}
			}],
			"xtype" : "WireIt.ImageContainer",
			"image" : "../../static/img/sum.png",
			"icon" : "../../static/img/sum.png"
		},
		"name" : "Monitor Correction"
	}, {
		"container" : {
			"terminals" : [{
				"direction" : [-1, 0],
				"multiple" : false,
				"name" : "input",
				"required" : true,
				"alwaysSrc" : false,
				"ddConfig" : {
					"type" : "data1d.tas:in",
					"allowedTypes" : ["data1d.tas:out"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : -15
				}
			}, {
				"direction" : [1, 0],
				"multiple" : true,
				"name" : "output",
				"required" : false,
				"alwaysSrc" : true,
				"ddConfig" : {
					"type" : "data1d.tas:out",
					"allowedTypes" : ["data1d.tas:in"]
				},
				"offsetPosition" : {
					"top" : 1,
					"left" : 15
				}
			}],
			"xtype" : "WireIt.ImageContainer",
			"image" : "../../static/img/sum.png",
			"icon" : "../../static/img/sum.png"
		},
		"name" : "Volume Correction"
	}],
	"languageName" : "NCNR BT7"
}