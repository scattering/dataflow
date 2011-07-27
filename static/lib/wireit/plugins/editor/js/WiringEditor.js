(function() {
    var util = YAHOO.util,lang = YAHOO.lang;
    var Event = util.Event, Dom = util.Dom, Connect = util.Connect,widget = YAHOO.widget;

/**
 * The WiringEditor class provides a full page interface 
 * @class WiringEditor
 * @extends WireIt.BaseEditor
 * @constructor
 * @param {Object} options
 */
WireIt.WiringEditor = function(options) {

	 /**
	  * Hash object to reference module definitions by their name
	  * @property modulesByName
	  * @type {Object}
	  */
   this.modulesByName = {};
	WireIt.WiringEditor.superclass.constructor.call(this, options);

	 // LoadWirings
	 if( this.adapter.init && YAHOO.lang.isFunction(this.adapter.init) ) {
			this.adapter.init();
 	 }
 	 // Commented out the initial load. Now must click load to bring up the loading screen
	 //this.load();
};

lang.extend(WireIt.WiringEditor, WireIt.BaseEditor, {

	 /**
	  * @method setOptions
	  * @param {Object} options
	  */
	 setOptions: function(options) {
    
		WireIt.WiringEditor.superclass.setOptions.call(this, options);
    
	    // Load the modules from options
	    this.modules = options.modules || [];
	    for(var i = 0 ; i < this.modules.length ; i++) {
	       var m = this.modules[i];
	       this.modulesByName[m.name] = m;
	    }

		this.adapter = options.adapter || WireIt.WiringEditor.adapters.JsonRpc;
     
	    this.options.languageName = options.languageName || 'anonymousLanguage';
     
	    this.options.layerOptions = {};
	    var layerOptions = options.layerOptions || {};


	    this.options.layerOptions.parentEl = layerOptions.parentEl ? layerOptions.parentEl : Dom.get('center');
	    this.options.layerOptions.layerMap = YAHOO.lang.isUndefined(layerOptions.layerMap) ? true : layerOptions.layerMap;
	    this.options.layerOptions.layerMapOptions = layerOptions.layerMapOptions || { parentEl: 'layerMap' };

	 	 this.options.modulesAccordionViewParams = YAHOO.lang.merge({
														collapsible: true, 
														expandable: true, // remove this parameter to open only one panel at a time
														width: 'auto', 
														expandItem: 0, 
														animationSpeed: '0.3', 
														animate: true, 
														effect: YAHOO.util.Easing.easeBothStrong
													},options.modulesAccordionViewParams || {});

		 // Grouping options
	    var temp = this;
	    var baseConfigFunction = function(name)  { 
				return (name == "Group") ? ({
			    "xtype": "WireIt.GroupFormContainer",
			    "title": "Group",    

			    "collapsible": true,
			    "fields": [ ],
			    "legend": "Inner group fields",
			    "getBaseConfigFunction" : baseConfigFunction
				}) : temp.modulesByName[name].container;
		};

	    this.options.layerOptions.grouper = {"baseConfigFunction": baseConfigFunction };

	 },


	/**
	 * Add the rendering of the layer
	 */
  	render: function() {

		WireIt.WiringEditor.superclass.render.call(this);

	    /**
	     * @property layer
	     * @type {WireIt.Layer}
	     */
	    this.layer = new WireIt.Layer(this.options.layerOptions);
		this.layer.eventChanged.subscribe(this.onLayerChanged, this, true);

		// Left Accordion
		this.renderModulesAccordion();

	    // Render module list
	    this.buildModulesList();
  	},

	/**
	 * render the modules accordion in the left panel
	 */
	renderModulesAccordion: function() {

		// Create the modules accordion DOM if not found
		if(!Dom.get('modulesAccordionView')) {
			Dom.get('left').appendChild( WireIt.cn('ul', {id: 'modulesAccordionView'}) );
			var li = WireIt.cn('li');
			li.appendChild(WireIt.cn('h2',null,null,"Main"));
			var d = WireIt.cn('div');
			d.appendChild( WireIt.cn('div', {id: "module-category-main"}) );
			li.appendChild(d);
			Dom.get('modulesAccordionView').appendChild(li);
		}

		this.modulesAccordionView = new YAHOO.widget.AccordionView('modulesAccordionView', this.options.modulesAccordionViewParams);

		// Open all panels
		for(var l = 1, n = this.modulesAccordionView.getPanels().length; l < n ; l++) {
			this.modulesAccordionView.openPanel(l);
		}
	},

 
 	/**
  	 * Build the left menu on the left
  	 * @method buildModulesList
  	 */
 	buildModulesList: function() {

     	var modules = this.modules;
     	for(var i = 0 ; i < modules.length ; i++) {
		  	this.addModuleToList(modules[i]);
     	}

     	// Make the layer a drag drop target
     	if(!this.ddTarget) {
       	this.ddTarget = new YAHOO.util.DDTarget(this.layer.el, "module");
       	this.ddTarget._layer = this.layer;
     	}
 	},

 	/**
  	 * Add a module definition to the left list
  	 */
 	addModuleToList: function(module) {
	try {
		var div = WireIt.cn('div', {className: "WiringEditor-module"});

		if(module.description) {
			div.title = module.description;
		}

      if(module.container.icon) {
         div.appendChild( WireIt.cn('img',{src: module.container.icon}) );
      }
      div.appendChild( WireIt.cn('span', null, null, module.name) );

      var ddProxy = new WireIt.ModuleProxy(div, this);
      ddProxy._module = module;

		// Get the category element in the accordion or create a new one
		var category = module.category || "main";
		var el = Dom.get("module-category-"+category);
		if( !el ) {
			this.modulesAccordionView.addPanel({
				label: category,
				content: "<div id='module-category-"+category+"'></div>"
			});
			this.modulesAccordionView.openPanel(this.modulesAccordionView._panels.length-1);
			el = Dom.get("module-category-"+category);
		}

		el.appendChild(div);
	}catch(ex){ console.log(ex);}
 	},
 
 
	getCurrentGrouper: function(editor) {
     	return editor.currentGrouper;
 	},
 
 	/**
  	 * add a module at the given pos
  	 */
	addModule: function(module, pos) {
	    try {
	       var containerConfig = module.container;
	       containerConfig.position = pos;
	       containerConfig.title = module.name;
	       var temp = this;
	       containerConfig.getGrouper = function() { return temp.getCurrentGrouper(temp); };
	       var container = this.layer.addContainer(containerConfig);

			 // Adding the category CSS class name
			 var category = module.category || "main";
			 Dom.addClass(container.el, "WiringEditor-module-category-"+category.replace(/ /g,'-'));

			 // Adding the module CSS class name
	       Dom.addClass(container.el, "WiringEditor-module-"+module.name.replace(/ /g,'-'));

	    }
	    catch(ex) {
	       this.alert("Error Layer.addContainer: "+ ex.message);
			 if(window.console && YAHOO.lang.isFunction(console.log)) {
				console.log(ex);
			}
	    }    
	},

 	/**
  	 * save the current module
  	 */
 	save: function() {
  
    	var value = this.getValue();
    	var wirename = prompt("Please set the name for this wiring template (or hit cancel to leave the name unchanged)", value.name)
    	if(wirename === "") {
       	this.alert("Please choose a name");
       	return;
    	}
		// THIS IS WHERE THE MAGIC HAPPENS
		// getValue returns the current wiring, and the tempSavedWiring stores all the relevant info
		this.tempSavedWiring = {name: wirename, modules: value.working.modules, properties: value.working.properties, wires:value.working.wires, language: this.options.languageName };
	for (var i in this.tempSavedWiring.modules) {
		//console.log(i, this.tempSavedWiring.modules[i].config)
		this.tempSavedWiring.modules[i].config = this.tempSavedWiring.modules[i].config[this.reductionInstance]
		}
	this.tempSavedWiring.properties.name = wirename
    	this.adapter.saveWiring(this.tempSavedWiring, {
       	success: this.saveModuleSuccess,
       	failure: this.saveModuleFailure,
       	scope: this
    	});
 	},

	 /**
	  * saveModule success callback
	  * @method saveModuleSuccess
	  */
	 saveModuleSuccess: function(o) {

		//this.markSaved();

	   //this.alert("Saved !\n source code follows:\n" + JSON.stringify(this.tempSavedWiring));

		// TODO: call a saveModuleSuccess callback...
	 },

	 /**
	  * saveModule failure callback
	  * @method saveModuleFailure
	  */
	 saveModuleFailure: function(errorStr) {
	    this.alert("Unable to save the wiring : "+errorStr);
	 },

// added 6/21/11, Tracer
// sends current wiring diagram to server as POST, gets data to display/plot as a response
	/**
	* @method runReduction
	*/

	runReduction: function(file_associations) {
	    var value = this.getValue()

	    //console.log(value)
	    if(value.name === "") {
       		this.alert("Please choose a name");
           	return;
	    }
	    this.toReduce = {
	        name: value.name,
	        modules: value.working.modules,
	        properties: value.working.properties,
	        wires: value.working.wires,
	        language: value.working.language,
	        clickedOn: this.wireClickedOn
        };
        for (var j in this.toReduce.modules) {
        	this.toReduce.modules[j].config = this.toReduce.modules[j].config[this.reductionInstance]
        	this.toReduce.modules[j].config['files'] = []
        	}
        for (var i in file_associations) {
        	if (typeof file_associations[i] == "object") {
        		for (var k in file_associations[i]) {
        	   		this.toReduce.modules[i.split(": ").pop()].config['files'].push(FILE_DICT[file_associations[i][k]])
        	   	}
        	}
        	else {
		    // not entering in a 'files' config if the module is not a loader        		
        	}
        }
        //console.log(this.toReduce)
	    this.adapter.runReduction(this.toReduce, {
           	success: this.runModuleSuccess,
           	failure: this.runModuleFailure,
           	scope: this,
	    });	    
 	},
	
	// PASSING THE WIRE OVER TO THE SERVER, SO WE SHOULD GET BACK ONLY ONE PLOTTABLE OBJECT
	// NO NEED TO CHECK THE WIRE SOURCE HERE, JUST PLOT WHATEVER YOU GET
	runModuleSuccess: function(display) {
		plotid = 'plot';
		toPlot = display
		//console.log(toPlot)
		//console.log(display)
		//var toPlot = display[this.wireClickSource].output[0], zipped = [];
		//if (this.wireClickSource) {
		//	toPlot = display[this.wireClickSource].output
		//	}
		//else {
		//	toPlot = display[0].output
		//}
		//console.log(toPlot)
		plottingAPI(toPlot, plotid)

	},

	runModuleFailture: function(error) {
		this.alert("Unable to run the reduction: " + error)
	},


	 /**
	  * @method onNew
	  */
	onNew: function() {

		if(!this.isSaved()) {
			if( !confirm("Warning: Your work is not saved yet ! Press ok to continue anyway.") ) {
				return;
			}
		}

		this.preventLayerChangedEvent = true;

	    this.layer.clear(); 

	    this.propertiesForm.clear(false); // false to tell inputEx to NOT send the updatedEvt

		this.markSaved();

		this.preventLayerChangedEvent = false;
	},

	 /**
	  * @method onDelete
	  */
	onDelete: function() {
	    if( confirm("Are you sure you want to delete this wiring ?") ) {
		this.layer.clear()
		console.log('DELETED')
		/*       
	      var value = this.getValue();
	 		this.adapter.deleteWiring({name: value.name, language: this.options.languageName},{
	 			success: function(result) {
					this.onNew();
	 				this.alert("Deleted !");
	 			},
				failure: function(errorStr) {
					this.alert("Unable to delete wiring: "+errorStr);
				},
				scope: this
	 		});
       		*/
	    }
	},

	 /**
	  * @method renderLoadPanel
	  */
	renderLoadPanel: function() {
	    if( !this.loadPanel) {
	        this.loadPanel = new widget.Panel('WiringEditor-loadPanel', {
	          fixedcenter: true,
	          draggable: true,
	          width: '500px',
	          visible: false,
	          modal: true
	        });
	        this.loadPanel.setHeader("Select the wiring to load");
	        this.loadPanel.setBody("Filter: <input type='text' id='loadFilter' /><div id='loadPanelBody'></div>");
	        this.loadPanel.render(document.body);

			// Listen the keyup event to filter the module list
			Event.onAvailable('loadFilter', function() {
				Event.addListener('loadFilter', "keyup", this.inputFilterTimer, this, true);
			}, this, true);

	    }
	 },

	/**
	 * Method called from each keyup on the search filter in load panel.
	 * The real filtering occurs only after 500ms so that the filter process isn't called too often
	 */
	inputFilterTimer: function() {
		if(this.inputFilterTimeout) {
			clearTimeout(this.inputFilterTimeout);
			this.inputFilterTimeout = null;
		}
		var that = this;
		this.inputFilterTimeout = setTimeout(function() {
				that.updateLoadPanelList(Dom.get('loadFilter').value);
		}, 500);
	},


	 /**
	  * @method updateLoadPanelList
	  */
	updateLoadPanelList: function(filter) {

		this.renderLoadPanel();

	    var list = WireIt.cn("ul");
	    if(lang.isArray(this.pipes)) {
	        for(var i = 0 ; i < this.pipes.length ; i++) {
	            var pipe = this.pipes[i];
	            if(!filter || filter === "" || pipe.name.match(new RegExp(filter,"i")) ) {
		            list.appendChild( WireIt.cn('li',null,{cursor: 'pointer'},pipe.name) );
				}
	        }
	    }
	    var panelBody = Dom.get('loadPanelBody');

		 // Purge element (remove listeners on panelBody and childNodes recursively)
	    YAHOO.util.Event.purgeElement(panelBody, true);

	    panelBody.innerHTML = "";
	    panelBody.appendChild(list);

	    Event.addListener(list, 'click', function(e,args) {
	    	this.loadPipe(Event.getTarget(e).innerHTML);
	    }, this, true);

	},

	 /**
	  * Start the loading of the pipes using the adapter
	  * @method load
	  */
	load: function() {
    	console.log('LOADING') //debugging
	    this.adapter.listWirings({language: this.options.languageName, experiment_id: this.launchedFromExperimentPage},{
			success: function(result) {
				this.onLoadSuccess(result);
			},
			failure: function(errorStr) {
				this.alert("Unable to load the wirings: "+errorStr);
			},
			scope: this
		});

	},

	 /**
	  * @method onLoadSuccess
	  */
	onLoadSuccess: function(wirings) {

		// Reset the internal structure
		this.pipes = wirings;
		console.log('wiring length: ' + this.pipes.length)
		this.pipesByName = {};

		// Build the "pipesByName" index
		for(var i = 0 ; i < this.pipes.length ; i++) {
            this.pipesByName[ this.pipes[i].name] = this.pipes[i];
	        console.log('adding ' + this.pipes[i].name + ' to pipesByName')
		}

    	this.updateLoadPanelList();

		// Check for autoload param and display the loadPanel otherwise
		if(!this.checkAutoLoad()) { 
    			this.loadPanel.show();
		}
		
	},

	/**
	 * checkAutoLoad looks for the "autoload" URL parameter and open the pipe.
	 * returns true if it loads a Pipe
	 * @method checkAutoLoad
	 */
	checkAutoLoad: function() {
		if(!this.checkAutoLoadOnce) {
			var p = window.location.search.substr(1).split('&');
			var oP = {};
			for(var i = 0 ; i < p.length ; i++) {
				var v = p[i].split('=');
				oP[v[0]]=window.decodeURIComponent(v[1]);
			}
			this.checkAutoLoadOnce = true;
			if(oP.autoload) {
				this.loadPipe(oP.autoload);
				return true;
			}
		}
		return false;
	},

	/**
	 * @method getPipeByName
	 * @param {String} name Pipe's name
	 * @return {Object} return the pipe configuration
	 */
	getPipeByName: function(name) {
	   var n = this.pipes.length,ret;
	   for(var i = 0 ; i < n ; i++) {
	      if(this.pipes[i].name == name) {
			return this.pipes[i] //.working; Changed as part of changes to listWirings
	      }
	   }
	   return null;
	},

	/**
	 * @method loadPipe
	 * @param {String} name Pipe name
	 */
	loadPipe: function(name) {

		if(!this.isSaved()) {
			if( !confirm("Warning: Your work is not saved yet ! Press ok to continue anyway.") ) {
				return;
			}
		}

		try {

			this.preventLayerChangedEvent = true;
			this.loadPanel.hide();

			var wiring = this.getPipeByName(name), i; // getPipeByName has TASWires, but looking at
								  // getPipeByName, we need TASWires.working
								  // Changed getPipeByName such that it returns the
								  // wiring rather than the .working
			console.log('Getting wiring: ' + name)

			if(!wiring) {
				this.alert("The wiring '"+name+"' was not found.");
				return;
		 	}

		   // TODO: check if current wiring is saved...
		   this.layer.clear();

		   this.propertiesForm.setValue(wiring.properties, false); // the false tells inputEx to NOT fire the updatedEvt

		   if(lang.isArray(wiring.modules)) {
  
		      // Containers
		      for(i = 0 ; i < wiring.modules.length ; i++) {
		         var m = wiring.modules[i];
		         if(this.modulesByName[m.name]) {
		            var baseContainerConfig = this.modulesByName[m.name].container;
		            YAHOO.lang.augmentObject(m.config, baseContainerConfig); 
		            m.config.title = m.name;
		            //console.log('pre', m) // continue working on this (pulling module config from dumped template)
		            var container = this.layer.addContainer(m.config);
		            //console.log('post',container)
		            Dom.addClass(container.el, "WiringEditor-module-"+m.name);
		            container.setValue(m.value);
		            container.tracksConfigs = {1: m.config}
		            //console.log(container)
		         }
		         else {
		            throw new Error("WiringEditor: module '"+m.name+"' not found !");
		         }
		      }
   
		      // Wires
		      if(lang.isArray(wiring.wires)) {
		          for(i = 0 ; i < wiring.wires.length ; i++) {
		             // On doit chercher dans la liste des terminaux de chacun des modules l'index des terminaux...
		             this.layer.addWire(wiring.wires[i]);
		          }
		      }
		  }
  
		  this.markSaved();

		  
		  this.preventLayerChangedEvent = false;
		  // removes existing FAT
		  console.log('REPLACING FAT')
		  while (YAHOO.util.Dom.get('FAT').hasChildNodes()) {
    			YAHOO.util.Dom.get('FAT').removeChild(YAHOO.util.Dom.get('FAT').lastChild);
			}
		  // Call the File Association Table with appropriate headers
		  makeFileTable(this.getFATHeaders(),FILES, this.getValue().working.modules)
		  ///console.log(this.getFATHeaders())

 		}
 		catch(ex) {
    		this.alert(ex);
			if(window.console && YAHOO.lang.isFunction(console.log)) {
				console.log(ex);
			}
 		}
	},


	onLayerChanged: function() {
		if(!this.preventLayerChangedEvent) {
			this.markUnsaved();
		}
	},

 
	/**
	 * This method return a wiring within the given vocabulary described by the modules list
	 * @method getValue
	 */
	getValue: function() {
  
	  var i;
	  var obj = {modules: [], wires: [], properties: null};

	  for( i = 0 ; i < this.layer.containers.length ; i++) {
	     obj.modules.push( {name: this.layer.containers[i].title, value: this.layer.containers[i].getValue(), config: this.layer.containers[i].getConfig()});
	  }

	  for( i = 0 ; i < this.layer.wires.length ; i++) {
	     var wire = this.layer.wires[i];
		var wireObj = wire.getConfig();
		wireObj.src = {moduleId: WireIt.indexOf(wire.terminal1.container, this.layer.containers), terminal: wire.terminal1.name };
		wireObj.tgt = {moduleId: WireIt.indexOf(wire.terminal2.container, this.layer.containers), terminal: wire.terminal2.name };
	     obj.wires.push(wireObj);
	  }
 
	  obj.properties = this.propertiesForm.getValue();
  	  obj['language'] = CHOSEN_LANG_NAME
	  return {
	     name: obj.properties.name,
	     working: obj
	  };
	},

	/**
	* This method returns a list of strings for the column headers in the FAT.
	* Currently, it simply runs through all existing wires and adds the target (Module name, terminal name)
	* if the wire's source is Load
	* 7/8
	**/
	getFATHeaders: function() {
		var wiringDiagram = this.getValue().working
		var wireList = wiringDiagram.wires
		var moduleList = wiringDiagram.modules
		var hitModules = [] // at some point to check which modules have already been touched
		var headersList = [] // actual list of headers
		var loadCheck = /Load/ // regex for checking if a module is a load, matches "Load"
		for (var i=0; i < wireList.length; i++) {
			//console.log(i)
			if (loadCheck.test(moduleList[wireList[i].src.moduleId].name)) {
			
				headersList.push(moduleList[wireList[i].tgt.moduleId].name + ' ' + wireList[i].tgt.terminal + ': ' + wireList[i].src.moduleId)
				//console.log(moduleList[wireList[i].src.moduleId].name)
				}
			}
		return headersList;	
		},
		
	/**
	* This method gets called every time there is an updateAll() call on the FAT. 
	* Currently, it updates the number of reduction instances and the display for 
	* Instance Info
	**/
	
	FATupdate: function(templateConfig) {
		//console.log('in Editor', templateConfig)
		setMax = 0;
		for (i in templateConfig) {
			setMax += 1
			}
		this.maxReduction = setMax;
		this.templateConfig = templateConfig;
		this.displayCurrentReduction();
		this.extendModuleConfigs()
		this.updateFileConfigs(templateConfig)
	
	},
	
	updateFileConfigs: function(file_associations) {
	//console.log('ENTERING FILE CONFIGS')
	for (var l in this.layer.containers) {
		for (var j in this.layer.containers[l].tracksConfigs) {
			this.layer.containers[l].tracksConfigs[j]['files'] = []
			}
		}
	for (var j = 1; j <= Object.size(file_associations); j++) {
	        for (var i in file_associations[j]) {
        		if (typeof file_associations[j][i] == "object") {
        			for (var k in file_associations[j][i]) {
        				//console.log('j',j,'i',i,'k',k)
        				//console.log(this.layer.containers[i.split(": ").pop()].tracksConfigs[j]['files'])
        	   			this.layer.containers[i.split(": ").pop()].tracksConfigs[j]['files'].push([file_associations[j][i][k]])
        	   	}
        		}
        
        	else {
		    // not entering in a 'files' config if the module is not a loader        		
        	}
        }
        }
        //console.log('LEAVING FILE CONFIGS')
	},
		
	/**
	* These following methods are for paging through the reduction template instances
	*
	* prevReductionInstance and nextReductionInstance update the button display, set the value editor.reductionInstance and call displayCurrentReduction()
	**/	
	prevReductionInstance: function() {
		if (this.reductionInstance>1) {
			this.reductionInstance -= 1
			YAHOO.util.Dom.get('reductionInstance').innerHTML = String(this.reductionInstance)
			this.displayCurrentReduction()
			//this.setModuleConfigs()
			}
	
	},
		
		
	nextReductionInstance: function() {
		if (this.reductionInstance < this.maxReduction) {
			this.reductionInstance += 1
			YAHOO.util.Dom.get('reductionInstance').innerHTML = this.reductionInstance
			this.displayCurrentReduction()
			//this.setModuleConfigs()
			}
	},
	
	displayCurrentReduction: function() {
		//console.log('In DISPLAY')
		
		// changes the reduction number
		HTML = '<dl class ="instance-info-display">'
		for (var i in this.templateConfig[this.reductionInstance]) {
			HTML += '<dt>' + i + "</dt><dd>" + this.templateConfig[this.reductionInstance][i] + '</dd>'
			}
		HTML += "</dl>";
		YAHOO.util.Dom.get('instance-files-info').innerHTML = HTML
		
		// updates the module info display
		if (this.clickedModuleID) {
			this.layer.containers[this.clickedModuleID].onMouseDown()
		}
	},
	
	/**
	* This method makes sure that each module has a config list for every reduction instance
	**/
	
	extendModuleConfigs: function() {
		console.log('In ExtendModuleConfig')
		containers = this.layer.containers
		for (var i=0; i < containers.length; i++) {
			size = Object.size(containers[i].tracksConfigs)
			diff = this.maxReduction - size
			tempConfig = containers[i].tracksConfigs[1]
			//console.log('diff',diff)
			//console.log(tempConfig)
			if (diff>0) {
				//console.log('there is a diff')
				for (var j = 1; j <= diff; j ++ ) {
					containers[i].tracksConfigs[size+j] = {}
					for (var k in tempConfig) {
						containers[i].tracksConfigs[size+j][k] = tempConfig[k]
						}
					}
				}
			}
	},
	
	displayClickedModuleConfig: function(module) {
		//console.log('in display module config!')
		HTML = '<dl class ="instance-info-display">'
		config = module.getConfig()[this.reductionInstance]
		//console.log(module.getConfig())
		for (i in config) {
			//console.log(i, config[i])
			if (typeof config[i] == "object") {
				HTML += '<dt>' + i +  "</dt><dd>"
				for (var j in config[i]) {
					HTML += "<p>" + j + ": " + config[i][j] + "</p>"
					}
				HTML += "</dd>"
				}
			else {
				HTML += '<dt>' + i + "</dt><dd>" + config[i] + '</dd>'
			}
		}
		HTML += "</dl>";
		YAHOO.util.Dom.get('instance-modules-info').innerHTML = HTML	
	},

	generateConfigForm: function(moduleID) {
		console.log('generating form')
		while (YAHOO.util.Dom.get("instance-modules-input").hasChildNodes()) {
	    			YAHOO.util.Dom.get("instance-modules-input").removeChild(YAHOO.util.Dom.get("instance-modules-input").lastChild);
				}
		configHeaders = []
		badHeaders = ["files", "position", "xtype", "width", "terminals", "height", "title", "image", "icon"]
		configs = this.layer.containers[moduleID].getConfig()[this.reductionInstance]
		//console.log(configs)
		for (var j in configs) {
			if (badHeaders.indexOf(j) == -1) {
				//console.log(configs[j], typeof configs[j])
				if (typeof configs[j] == 'string' || typeof configs[j] == 'number' || typeof configs[j] == 'undefined'){
					configHeaders.push([j,[j]])
					}
				if (typeof configs[j] == "object") {
					fieldNames = []
					for (var k in configs[j]) {
						fieldNames.push(k)
						}
					configHeaders.push([j,fieldNames])
					}
			}
		}
		//console.log(configHeaders, configHeaders.length)
		if (configHeaders.length != 0) {
			configForm(configHeaders, moduleID)
			}
		else {YAHOO.util.Dom.get("instance-modules-input").innerHTML = "THIS MODULE HAS NO CONFIGURABLE INPUTS"}
	},
	
	setModuleConfigsFromForm: function(configs, moduleID, instanceNumber) {
		if (typeof instanceNumber == "number") {
			for (var i in configs) {
				splitConfig = i.split(',')
				//console.log(splitConfig)
				if (splitConfig[0] == splitConfig[1]) {
					this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]] = configs[i]
					}
				else {
					this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]][splitConfig[1]] = configs[i]
				}
				}
			}
		else {
			for (var i in configs) {
				splitConfig = i.split(',')
				//console.log(splitConfig)
				if (splitConfig[0] == splitConfig[1]) {
					for (var j = 1; j <= this.maxReduction; j++) {
						this.layer.containers[moduleID].tracksConfigs[j][splitConfig[0]] = configs[i]
						}
					}
				else {
					for (var j = 1; j <= this.maxReduction; j++ ) {
						this.layer.containers[moduleID].tracksConfigs[j][splitConfig[0]][splitConfig[1]] = configs[i]
					}
				}
				}
			}
		this.layer.containers[moduleID].onMouseDown()
		//console.log(this.layer.containers[moduleID].tracksConfigs)
		},


});


/**
 * WiringEditor Adapters
 * @static
 */
WireIt.WiringEditor.adapters = {};


})();

