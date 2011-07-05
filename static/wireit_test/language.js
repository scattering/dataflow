var testLanguage = 
{
    "propertiesFields": [
        {
            "typeInvite": "Enter a title",
            "type": "string",
            "name": "name",
            "label": "Title"
        },
        {
            "type": "text",
            "name": "description",
            "cols": 30,
            "label": "Description"
        }
    ],
    "modules": [
        {
            "container": {
                "terminals": [
                    {
                        "direction": [1, 0],
                        "multiple": true,
                        "name": "output",
                        "required": false,
                        "alwaysSrc": true,
                        "ddConfig": {
                            "type": "data1d.tas:out",
                            "allowedTypes": [
                                "data1d.tas:in"
                            ]
                        },
                        "offsetPosition": {
                            "top": 1,
                            "right": -16
                        }
                    }
                ],
                "xtype": "WireIt.Container",
                "height": 16,
                "width": 120,
            },
            "name": "Load"
        },
        {
            "container": {
                "terminals": [
                    {
                        "direction": [-1, 0],
                        "multiple": false,
                        "name": "input",
                        "required": false,
                        "alwaysSrc": false,
                        "ddConfig": {
                            "type": "data1d.tas:in",
                            "allowedTypes": [
                                "data1d.tas:out"
                            ]
                        },
                        "offsetPosition": {
                            "top": 1,
                            "left": -16,
                        }
                    }
                ],
                "xtype": "WireIt.Container",
                "height": 16,
                "width": 120,
            },
            "name": "Save"
        },
        {
            "container": {
                "terminals": [
                    {
                        "direction": [
                            -1,
                            0
                        ],
                        "multiple": true,
                        "name": "input",
                        "required": false,
                        "alwaysSrc": false,
                        "ddConfig": {
                            "type": "data1d.tas:in",
                            "allowedTypes": [
                                "data1d.tas:out"
                            ]
                        },
                        "offsetPosition": {
                            "top": 10,
                            "left": -16,
                        }
                    },
                    {
                        "direction": [1, 0],
                        "multiple": true,
                        "name": "output",
                        "required": false,
                        "alwaysSrc": true,
                        "ddConfig": {
                            "type": "data1d.tas:out",
                            "allowedTypes": [
                                "data1d.tas:in"
                            ]
                        },
                        "offsetPosition": {
                            "top": 10,
                            "left": 48,
                        }
                    }
                ],
                "xtype": "WireIt.Container",
                "image": "../../static/img/silk/add.png",
                "icon": "../../static/img/silk/add.png",
                "width": 60,
            },
            "name": "Join"
        },
        {
            "container": {
                "terminals": [
                    {
                        "direction": [
                            -1,
                            0
                        ],
                        "multiple": true,
                        "name": "input",
                        "required": false,
                        "alwaysSrc": false,
                        "ddConfig": {
                            "type": "data1d.tas:in",
                            "allowedTypes": [
                                "data1d.tas:out"
                            ]
                        },
                        "offsetPosition": {
                            "top": 10,
                            "left": -16,
                        }
                    },
                    {
                        "direction": [
                            1,
                            0
                        ],
                        "multiple": true,
                        "name": "output",
                        "required": false,
                        "alwaysSrc": true,
                        "ddConfig": {
                            "type": "data1d.tas:out",
                            "allowedTypes": [
                                "data1d.tas:in"
                            ]
                        },
                        "offsetPosition": {
                            "top": 10,
                            "left": 48,
                        }
                    }
                ],
                "xtype": "WireIt.Container",
                "image": "../../static/img/fugue/balance.png",
                "icon": "../../static/img/fugue/balance.png",
                "width": 60,
            },
            "name": "Scale"
        }
    ],
    "languageName": "NCNR BT7"
};
