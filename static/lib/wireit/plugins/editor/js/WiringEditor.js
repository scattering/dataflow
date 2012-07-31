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
			this.options.layerOptions.layerMapOptions = layerOptions.layerMapOptions || {
				parentEl: 'layerMap'
			};

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
			var baseConfigFunction = function(name) {
				return (name == "Group") ? ( {
					"xtype": "WireIt.GroupFormContainer",
					"title": "Group",

					"collapsible": true,
					"fields": [ ],
					"legend": "Inner group fields",
					"getBaseConfigFunction" : baseConfigFunction
				}) : temp.modulesByName[name].container;
			};
			this.options.layerOptions.grouper = {
				"baseConfigFunction": baseConfigFunction
			};

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
				Dom.get('left').appendChild( WireIt.cn('ul', {
					id: 'modulesAccordionView'
				}) );
				var li = WireIt.cn('li');
				li.appendChild(WireIt.cn('h2',null,null,"Main"));
				var d = WireIt.cn('div');
				d.appendChild( WireIt.cn('div', {
					id: "module-category-main"
				}) );
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
				var div = WireIt.cn('div', {
					className: "WiringEditor-module"
				});

				if(module.description) {
					div.title = module.description;
				}

				if(module.container.icon) {
					div.appendChild( WireIt.cn('img', {
						src: module.container.icon
					}) );
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
			} catch(ex) {
				console.log(ex);
			}
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
				containerConfig.getGrouper = function() {
					return temp.getCurrentGrouper(temp);
				};
				containerConfig.fields = jQuery.extend(true, {}, module.fields);
				containerConfig.groups = {};
				var container = this.layer.addContainer(containerConfig);

				// Adding the category CSS class name
				var category = module.category || "main";
				Dom.addClass(container.el, "WiringEditor-module-category-"+category.replace(/ /g,'-'));

				// Adding the module CSS class name
				Dom.addClass(container.el, "WiringEditor-module-"+module.name.replace(/ /g,'-'));

			} catch(ex) {
				this.alert("Error Layer.addContainer: "+ ex.message);
				if(window.console && YAHOO.lang.isFunction(console.log)) {
					console.log(ex);
				}
			}
		},
		
		onSave: function() {
		    this.renderSavePanel();
		    this.savePanel.show();
		},
		/**
		 * @method renderSavePanel
		 */
		renderSavePanel: function() {
			if( !this.savePanel) {
				this.savePanel = new widget.Panel('WiringEditor-savePanel', {
					fixedcenter: true,
					draggable: true,
					width: '500px',
					visible: false,
					modal: true
				});
				this.savePanel.setHeader("Save current wiring");
				var body = "<input type='text' id='saveName' />";
				body += "<div><input type='button' value='Save to this Experiment' id='WiringEditor-saveNormal' /><br>";
				body += "<input type='button' value='Save as Standard Template' id='WiringEditor-saveToInstrument' /><br>";
				body += "<input type='button' value='Cancel' id='WiringEditor-saveCancel' /></div>";
				this.savePanel.setBody(body)
				//"Filter: <input type='text' id='loadFilter' /><div id='loadPanelBody'></div><div id='loadPanelButtons'></div>");
				this.savePanel.render(document.body);
                
				
				// Listen to the button press to upload a new file
				Event.onAvailable('WiringEditor-saveCancel', function() {
				    document.getElementById('WiringEditor-saveCancel').onclick = function() { editor.savePanel.hide() }
				}, this, true);
				Event.onAvailable('WiringEditor-saveNormal', function() {
				    document.getElementById('WiringEditor-saveNormal').onclick = function() { 
				        var wirename = document.getElementById('saveName').value;
				        editor.save(wirename, false);
				        editor.savePanel.hide();
				    }
				}, this, true);
				Event.onAvailable('WiringEditor-saveToInstrument', function() {
				    document.getElementById('WiringEditor-saveToInstrument').onclick = function() { 
				        var wirename = document.getElementById('saveName').value;
				        editor.save(wirename, true);
				        editor.savePanel.hide();
				    }
				}, this, true);
			}
		},
		/**
		 * save the current module
		 */
		save: function(wirename, saveToInstrument) {
		    // if this flag is set, the server will save the template to the 
		    // Instrument space instead of the current Experiment, making it
		    // available to all users (a default template)
            var saveToInstrument = saveToInstrument || false; // defaults to false
           
			var value = this.getValue();
			//var wirename;
			//this.renderSavePanel();
			//this.savePanel.show();
			//var promptname = prompt("Please set the name for this wiring template (or hit cancel to leave the name unchanged)", value.name)
			//if (promptname != null) { 
			//    wirename = promptname;
			//} else {
			//    wirename = value.name;
			//}
			
			if(wirename === "") {
				this.alert("Please choose a name");
				return;
			}
			// THIS IS WHERE THE MAGIC HAPPENS
			// getValue returns the current wiring, and the tempSavedWiring stores all the relevant info
			this.tempSavedWiring = {
				name: wirename,
				modules: value.working.modules,
				properties: value.working.properties,
				wires:value.working.wires,
				language: this.options.languageName
			};
			for (var i in this.tempSavedWiring.modules) {
				//console.log(i, this.tempSavedWiring.modules[i].config)
				
				// This saves only the most recent config...
				//this.tempSavedWiring.modules[i].config = this.tempSavedWiring.modules[i].config[this.reductionInstance];
				
			}
			var data = { saveToInstrument: saveToInstrument, 
			                 new_wiring:  this.tempSavedWiring }
			                   
			this.adapter.saveWiring(data, {
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

			this.markSaved();

			//this.alert("Saved !\n source code follows:\n" + JSON.stringify(this.tempSavedWiring));

			// TODO: call a saveModuleSuccess callback...
		},
		/**
		 * saveModule failure callback
		 * @method saveModuleFailure
		 */
		saveModuleFailure: function(errorStr, b) {
		    if (b && b.errorStr) { var errorStr = b.errorStr; }
			this.alert("Unable to save the wiring : "+errorStr);
		},
	
		    
		// added 8/10/11, Maranville
		// uploads files to server as POST
		/**
		 * @method uploadFiles
		 */
		uploadFiles: function(files) {
		    if (this.launchedFromExperimentPage) {
		        var experiment_id = this.launchedFromExperimentPage;
		        var post_data = {experiment_id: experiment_id};
		        var csrf_token = getCookie('csrftoken');
		        var uploader = new Uploader(files, "uploadFiles/", csrf_token, post_data);
		        uploader.sendAll();
		    }
		    else {
		        console.log("can't upload files unless associated with an experiment id");
		    } 
		},
		
		downloadFiles: function(files) {
		    console.log('downloading files, someday');
		},    
		

		textInputPopup: function(prompt) {
		    var textInputForm = new Ext.FormPanel( {
	            //renderTo: Ext.getBody(),
	            bodyPadding: 5,
	            width: 300,
	            autoHeight: true,
                layout: 'anchor',
	            id: 'text_input_form',
	            autodestroy: true,
	            //defaultType: 'textfield',
	            submitted: false,
	            items: [{
	                xtype: 'textfield',
                    fieldLabel: prompt,
                    name: 'text_value',
                    allowblank: false,
                }],
	            buttons: [{
	                text: 'Submit',
	                //formBind: true, //only enabled once the form is valid
	                //disabled: true,
	                handler: function() {
	                    var parent_popup = Ext.getCmp('text_input_popup');
		                parent_popup.submitted = true;
		                console.log('this inside popup_form', this);
		                parent_popup.value = this.up().items.items[0].value;
	                    parent_popup.close();
		                 
	                }
                },{
		            text: 'Cancel',
		            handler: function() {
		                Ext.getCmp('text_input_popup').submitted = false;
		                Ext.getCmp('text_input_popup').close();
		                }
	            },],
            });

		    if (!Ext.getCmp('text_input_popup')) {
		        var textPopup = new Ext.Window({
                    title: 'Text input',
                    closeable: true,
                    closeAction: 'hide',
                    id: 'text_input_popup',
                    hidden: true,
                    resizable: true,
                    //autosize: true,
                    modal: true,
                    renderTo: Ext.getBody(),
                    align: 'center',
                    submitted: false,
                    value: '',
                    });
            } else {
                var textPopup = Ext.getCmp('text_input_popup');
                if (textPopup.items.length > 0) { win.removeAll(); };
            }
            
            textPopup.add(textInputForm);
            textPopup.doLayout();
            textPopup.show();
            console.log(textPopup.submitted, textPopup.value);
        },
	        				
		// added 9/20/11, Maranville
		// sends current wiring diagram to server as POST, gets data in comma-separated-form as download
		// seems natural to combine this function with runReduction, since it's the same
		// except what you do with the result... 
		/**
		 * @method getCSV
		 */

		getCSV: function(reductionInstance, clickedOn, outfilename) {
			var value = this.getValue()
			var reductionInstance = reductionInstance ? reductionInstance : this.reductionInstance ;
            if (!outfilename) {
                var result = {
                    that: this,
                    reductionInstance: reductionInstance,
                    clickedOn: clickedOn,
                }
                
                function process_result(btn, text) {
                    if (btn == 'ok' && text != ""){
                        this.that.getCSV(this.reductionInstance, this.clickedOn, text);
                    } 
                }
                
                Ext.Msg.prompt('Name', 'Filename:', process_result, result, false, '' );
                return // getCSV ends here... will be called again by process_result if button "ok" pressed
            }
            
			this.toReduce = {
				name: value.name,
				modules: value.working.modules,
				properties: value.working.properties,
				wires: value.working.wires,
				language: value.working.language,
				clickedOn: clickedOn,
				group: reductionInstance,
				file_dict: FILE_DICT,
				outfilename: outfilename,
			};
			for (var j in this.toReduce.modules) {
			    //this.toReduce.modules[j].config = this.toReduce.modules[j].config[reductionInstance];
				//this.toReduce.modules[j].config['files'] = []
			}

			this.adapter.getCSV(this.toReduce);
		},
		
		getResult: function(result){
		    tempResult = result;
		},
		// PASSING THE WIRE OVER TO THE SERVER, SO WE SHOULD GET BACK ONLY ONE PLOTTABLE OBJECT
		// NO NEED TO CHECK THE WIRE SOURCE HERE, JUST PLOT WHATEVER YOU GET
		//downloadResult: function(result) {
		//	downloadURL = result.URL
		//	plotid = 'plot';
		//	toPlot = display
		//	plottingAPI(toPlot, plotid)

		//},
		
		// added 6/21/11, Tracer
		// sends current wiring diagram to server as POST, gets data to display/plot as a response
		/**
		 * @method runReduction
		 */

		generateReductionRecipe: function(reductionInstance, clickedOn) {
			var value = this.getValue()
			var reductionInstance = reductionInstance ? reductionInstance : this.reductionInstance ;
			var clickedOn = clickedOn ? clickedOn : this.wireClickedOn ;

			this.toReduce = {
			    returnType: 'plottable',
				name: value.name,
				modules: value.working.modules,
				properties: value.working.properties,
				wires: value.working.wires,
				language: value.working.language,
				clickedOn: clickedOn,
				group: reductionInstance,
				file_dict: FILE_DICT,
			};
			for (var j in this.toReduce.modules) {
			    //this.toReduce.modules[j].config = this.toReduce.modules[j].config[reductionInstance];
				//this.toReduce.modules[j].config['files'] = []
			}
			
			return this.toReduce;
			
        },

		// PASSING THE WIRE OVER TO THE SERVER, SO WE SHOULD GET BACK ONLY ONE PLOTTABLE OBJECT
		// NO NEED TO CHECK THE WIRE SOURCE HERE, JUST PLOT WHATEVER YOU GET
		displayResult: function(display) {
			plotid = 'plot';
			var that = this;
			function makePlotWindow() {
			    if (!that.plotWindow || !that.plotWindow.window || that.plotWindow.window.closed) {
			        that.plotWindow = window.open("/plotWindow/", "", "status=1,width=800,height=450"); }
			    else { that.plotWindow.onload(); }
			}
			
			var unfilled_data = [];
			var target_length = display.length;
			var filled_data_count = 0;
			
			for (var i=0; i<display.length; i++) {
			    if (display[i].binary_fp) { 
			        unfilled_data.push(display[i]);
			    } else {
			        filled_data_count++;
			    }
			}
			
			if (filled_data_count == target_length) { 
			    toPlot=display;
			    makePlotWindow();
			    //this.plotWindow.plottingAPI(display, plotid)  //commented out, was throwing errors; Yee 7/13/12
			};
			
			for (var i=0; i<unfilled_data.length; i++) {
			    var ud = unfilled_data[i];
			    var onFinish = function() { 
			        filled_data_count++;
			        console.log(filled_data_count);
			        if (filled_data_count == target_length) { 
			            toPlot = display;
			            makePlotWindow();
			            //that.plotWindow.plottingAPI(display, plotid); 
			        };
			    } 
			    this.adapter.getBinaryData(ud, onFinish);
			}
			
			
			//toPlot = this.fill_data(display, {success: function() {this.plotWindow.plottingAPI(toPlot, plotid)}} );
			
			
			//this.plotWindow.plottingAPI(toPlot, plotid)

		},
		runModuleFailure: function(error) {
			this.alert("Unable to run the reduction: " + error)
		},
		
		runAndPlot: function(reductionInstance) {
		    var toReduce = this.generateReductionRecipe(reductionInstance);
		    this.adapter.runReduction(toReduce, {
				success: this.displayResult,
				failure: this.runModuleFailure,
				scope: this,
			});		    
		},
		
		runAndSave: function(reductionInstance, clickedOn, dataname) {
		    if (!dataname) {
                function process_result(btn, text) {
                    if (btn == 'ok' && text != "") {
                        editor.runAndSave(reductionInstance, clickedOn, text);
                    } 
                }
                
                Ext.Msg.prompt('Name', 'Data name:', process_result, {}, false );
                return // getCSV ends here... will be called again by process_result if button "ok" pressed
            }
		    var toReduce = this.generateReductionRecipe(reductionInstance, clickedOn);
		    var tempSavedWiring = {
				name: dataname,
				modules: toReduce.modules,
				properties: toReduce.properties,
				wires: toReduce.wires,
				language: toReduce.languageName
			};
		    var datadict = { toReduce: toReduce,
		                 new_wiring:  tempSavedWiring,
		                 experiment_id: this.launchedFromExperimentPage,
		                 dataname: dataname };

            var callbacksdict = {
                success: function () {
                    $.ajax({
                        url: '/saveUpdate/',
                        type: 'GET',
                        data: { 'experiment_id': this.launchedFromExperimentPage },
                        success: function(response) {
                            //Updating METADATA, FILES, and FILES_DICT
                            var resultdict = Ext.decode(response);
                            editor.FAT.METADATA = Ext.decode(resultdict.file_metadata); //passed as string
                            var FILES = resultdict.file_keys;
                            editor.FAT.FILES = FILES;
                            var FILE_DICT = {};
                            for (var i in FILES) {
                                FILE_DICT[FILES[i][1]]=FILES[i][0];
                            }
                            editor.FAT.FILE_DICT = FILE_DICT;
                        },
                        failure: function(response) {
                            console.log('save failure: ', response);
                        }
                    });
                }, 
                failure: function(response) { console.log('failure: ', response); }
            };
		    this.adapter.saveData(datadict, callbacksdict);		    
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
		 * @method onFATButton
		 */
		onFATButton: function() {
		    if (!this.FAT) {
		        this.FAT = makeFileTable(FILES, this.getValue().working.modules);
		    } else {
		        this.FAT.update(FILES, this.getValue().working.modules);
		    }
		    
		    if (!Ext.getCmp('FAT_popup')) {
			        var win = new Ext.Window({
			            
			            title: 'File Associations Table',
			            closeable: true,
			            closeAction: 'hide',
			            id: 'FAT_popup',
			            hidden: false,
			            resizable: true,
			            //autosize: true,
			            modal: true,
			            renderTo: Ext.getBody(),
			            align: 'center',
			            });			        
			        win.alignTo(document.getElementById('WiringEditor-FATButton'), 'bl');
       		        win.add(this.FAT.mainPanel);
			} else {
			    var win = Ext.getCmp('FAT_popup');			        
			}
		    
//			    var win_el = win.el.dom;
//			    while (win_el.hasChildNodes()) {
//			        win_el.removeChild(win_el.lastChild);
//			    }
//		        var FAT = makeFileTable(this.getFATHeaders(), FILES, this.getValue().working.modules);
		        //console.log(FAT);
			win.doLayout();
			win.show();
		},		
		
		runAllReductions: function () {
		    alert("running all reductions...");
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
				var body = "Filter: <input type='text' id='loadFilter' /><input type='button' value='Upload wiring' id='WiringEditor-uploadPipe' /><div id='loadPanelBody'></div>"
				this.loadPanel.setBody(body)
				//"Filter: <input type='text' id='loadFilter' /><div id='loadPanelBody'></div><div id='loadPanelButtons'></div>");
				this.loadPanel.render(document.body);
                
				// Listen the keyup event to filter the module list
				Event.onAvailable('loadFilter', function() {
					Event.addListener('loadFilter', "keyup", this.inputFilterTimer, this, true);
				}, this, true);
				// Listen to the button press to upload a new file
				Event.onAvailable('WiringEditor-uploadPipe', function() {
				    Event.addListener('WiringEditor-uploadPipe', 'click', function(){ this.alert('not implemented yet...'); }, this, true);
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
			this.inputFilterTimeout = setTimeout( function() {
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
						list.appendChild( WireIt.cn('li',null, {
							cursor: 'pointer'
						},pipe.name) );
					}
				}
			}
			var panelBody = Dom.get('loadPanelBody');

			// Purge element (remove listeners on panelBody and childNodes recursively)
			YAHOO.util.Event.purgeElement(panelBody, true);

			panelBody.innerHTML = "";
			panelBody.appendChild(list);
			panelBody.appendChild(document.createElement('button'));

			Event.addListener(list, 'click', function(e,args) {
				this.loadPipe(Event.getTarget(e).innerHTML);
			}, this, true);
		},
		/**
		 * Start the loading of the pipes using the adapter
		 * @method load
		 */
		load: function() {
			//console.log('LOADING') //debugging
			this.adapter.listWirings({
				language: this.options.languageName,
				experiment_id: this.launchedFromExperimentPage
			}, {
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
			this.pipesByName = {};

			// Build the "pipesByName" index
			for(var i = 0 ; i < this.pipes.length ; i++) {
				this.pipesByName[ this.pipes[i].name] = this.pipes[i];
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

				var wiring = this.getPipeByName(name), i; 
				if(!wiring) {
					this.alert("The wiring '"+name+"' was not found.");
					return;
				}

				// TODO: check if current wiring is saved...
				this.layer.clear();

				//this.propertiesForm.setValue(wiring.properties, false); // the false tells inputEx to NOT fire the updatedEvt

				if(lang.isArray(wiring.modules)) {
                        
					// Containers
					for(i = 0 ; i < wiring.modules.length ; i++) {
						var m = wiring.modules[i];
						if(this.modulesByName[m.name]) {
							var baseContainerConfig = this.modulesByName[m.name].container;
							YAHOO.lang.augmentObject(m.config, baseContainerConfig);
							m.config.title = m.name;
							var container = this.layer.addContainer(m.config);
							Dom.addClass(container.el, "WiringEditor-module-"+m.name);
							container.fields = m.fields;
							container.groups = m.config.groups;
						} else {
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
				//console.log('REPLACING FAT')
				if (!this.FAT) {
				    this.FAT = makeFileTable(FILES, this.getValue().working.modules);
				} else {
				    this.FAT.update(FILES, this.getValue().working.modules);
				}
				this.reductionInstances = this.FAT.generateFileGroups();
				if (this.reductionInstances.length == 0) this.reductionInstances = [1];
				// if this.FAT.generateFileGroups returns empty group, set default to 1;
				this.setReductionIndex();
				// Call the File Association Table with appropriate headers
				//makeFileTable(this.getFATHeaders(),FILES, this.getValue().working.modules)
				///console.log(this.getFATHeaders())

			} catch(ex) {
				this.alert(ex);
				if(window.console && YAHOO.lang.isFunction(console.log)) {
					console.log(ex);
				}
			}
		},
		
		// sets the editor reduction instance to something within 
		// the reductionInstances set.
		setReductionIndex: function(index) {
		    var new_index = (index != null) ? index : this.reductionIndex;
		    if (new_index >= this.reductionInstances.length) {
			    new_index = (this.reductionInstances.length - 1);
		    }
			if (new_index < 0) {
			    new_index = 0;
			}
			this.reductionIndex = new_index;
			this.reductionInstance = this.reductionInstances[this.reductionIndex];
			document.getElementById('reductionInstance').innerHTML = String(this.reductionInstance);
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
			var obj = {
				modules: [],
				wires: [],
				properties: null
			};

			for( i = 0 ; i < this.layer.containers.length ; i++) {
				obj.modules.push({
					name: this.layer.containers[i].modulename,
					value: this.layer.containers[i].getValue(),
					config: this.layer.containers[i].getConfig()
				});
			}

			for( i = 0 ; i < this.layer.wires.length ; i++) {
				var wire = this.layer.wires[i];
				var wireObj = wire.getConfig();
				wireObj.src = {
					moduleId: WireIt.indexOf(wire.terminal1.container, this.layer.containers),
					terminal: wire.terminal1.name
				};
				wireObj.tgt = {
					moduleId: WireIt.indexOf(wire.terminal2.container, this.layer.containers),
					terminal: wire.terminal2.name
				};
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
		 * Runs through all existing wires and adds the target (Module name, terminal name) if the wire's source is Load
		 * 7/8
		 * 8/29 NOTE: this has been moved to inside the fileTable code.
		 **/
		getFATHeaders: function() {
		    // NOT USED ANYMORE: queue for deletion
		    console.log("Am I really getting FATHeaders?");
			var wiringDiagram = this.getValue().working
			var wireList = wiringDiagram.wires
			var moduleList = wiringDiagram.modules
			var headersList = [] // actual list of headers
			for (var i in moduleList) {
			    if (moduleList[i].config.target_id) {
			        headersList.push(moduleList[i].config.target_id);
			    }
			//var loadCheck = /Load/ // regex for checking if a module is a load, matches "Load"
			//for (var i=0; i < wireList.length; i++) {
			//	if (loadCheck.test(moduleList[wireList[i].src.moduleId].name)) {
			//		headersList.push(moduleList[wireList[i].tgt.moduleId].name + ' ' + wireList[i].tgt.terminal + ': ' + wireList[i].src.moduleId)
			//	}
			}
			return headersList;
		},
		/**
		 * This method gets called every time there is an updateAll() call on the FAT.
		 * Currently, it updates the number of reduction instances and the display for
		 * Instance Info
		 * 8/29/11 BBM: this is not used anymore.  Queue for deletion.
		 **/

		FATupdate: function(templateConfig) {
		    // NOT USED ANYMORE: queue for deletion
			//console.log('in Editor', templateConfig)
			setMax = 0;
			for (i in templateConfig) {
				setMax += 1
			}
			//this.maxReduction = setMax;
			this.templateConfig = templateConfig;
			this.displayCurrentReduction();
			this.extendModuleConfigs()
			this.updateFileConfigs(templateConfig)

		},
		updateFileConfigs: function(file_associations) {
		    // NOT USED ANYMORE: queue for deletion
			//console.log('ENTERING FILE CONFIGS')
			for (var l in this.layer.containers) {
				for (var j in this.layer.containers[l].tracksConfigs) {
				    if (this.layer.containers[l].tracksConfigs[j]['files']) {
				        // reset all the file configs to empty
				        this.layer.containers[l].tracksConfigs[j]['files'] = [];
				    }
				}
			}
			for (var j = 1; j <= Object.size(file_associations); j++) {
				for (var i in file_associations[j]) {
					if (typeof file_associations[j][i] == "object") {
						for (var k in file_associations[j][i]) {
							//console.log('j',j,'i',i,'k',k)
							console.log(this.layer.containers[i.split(": ").pop()].tracksConfigs[j]['files'])
							var target_container = this.layer.containers[i.split(": ").pop()];
							if (!target_container.tracksConfigs[j]['files']) {
							    target_container.tracksConfigs[j]['files'] = [];
							}
							target_container.tracksConfigs[j]['files'].push(file_associations[j][i][k]);
							if (target_container.hasOwnProperty('updateFiles')) {
							    target_container.updateFiles();
							}
						}
					} else {
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
		    this.setReductionIndex(this.reductionIndex - 1);
		},
		
		nextReductionInstance: function() {
		    this.setReductionIndex(this.reductionIndex + 1);
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
		    // I don't think this is used anymore.  Queue for deletion.
		    // 
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
			config = module.getConfig().groups[this.reductionInstance]
			//console.log(module.getConfig())
			for (i in config) {
				//console.log(i, config[i])
				if (typeof config[i] == "object") {
					HTML += '<dt>' + i +  "</dt><dd>"
					for (var j in config[i]) {
						HTML += "<p>" + j + ": " + config[i][j] + "</p>"
					}
					HTML += "</dd>"
				} else {
					HTML += '<dt>' + i + "</dt><dd>" + config[i] + '</dd>'
				}
			}
			HTML += "</dl>";
			YAHOO.util.Dom.get('instance-modules-info').innerHTML = HTML
		},
		generateConfigForm: function(moduleID) {
//			while (YAHOO.util.Dom.get("instance-modules-input").hasChildNodes()) {
//				YAHOO.util.Dom.get("instance-modules-input").removeChild(YAHOO.util.Dom.get("instance-modules-input").lastChild);
//			}
			configHeaders = [];
			//badHeaders = ["files", "position", "xtype", "width", "terminals", "height", "title", "image", "icon"]
			var container = this.layer.containers[moduleID];
			var configs = container.getConfig().groups[this.reductionInstance] || {};

			var module = this.modulesByName[container.modulename]

			// !!! EXPLICIT JQUERY DEPENDENCY HERE !!!
			configHeaders = jQuery.extend({}, module.fields, configs);
			if (!('groups' in container)) { container.groups = {}; }
			// now we link the groups object to the newly created object - so when it is
			// updated in the form, it will update directly to the object config
			container.groups[this.reductionInstance] = configHeaders;
			   
			//console.log(configHeaders, configHeaders.length)
			if (configHeaders.length != 0) {
			    //console.log('configHeaders:', configHeaders)
			    
			    if (!Ext.getCmp('module_config_popup')) {
			        var win = new Ext.Window({
			            title: 'Module configuration',
			            closeable: true,
			            closeAction: 'hide',
			            id: 'module_config_popup',
			            hidden: false,
			            resizable: false,
			            //autosize: true,
			            modal: true,
			            renderTo: Ext.getBody(),
			            });
			    } else {
			        var win = Ext.getCmp('module_config_popup');
			        if (win.items.length > 0) { win.removeAll(); };
			    }
			    
			    var cF = configForm(configHeaders, moduleID);
			    win.add(cF);
			    win.alignTo(this.layer.containers[moduleID].el, 'br');
			    win.doLayout();
			    win.show();
			        
			} else {
				alert("This module has no configurable inputs");
			}
		},
		setModuleConfigsFromForm: function(configs, moduleID, instanceNumber) {
		    // probably not going to be used anymore...
		    // queue for deletion
		    console.log("I thought this was deprecated! (setModuleConfigsFromForm)");
			if (typeof instanceNumber == "number") {
				for (var i in configs) {
					splitConfig = i.split(',')
					//console.log(splitConfig)
					if (splitConfig[0] == splitConfig[1]) {
						if ( typeof configs[i] != 'undefined') {
							this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]] = configs[i]
						}
					} else {
						if (typeof configs[i] != 'undefined') {
							//console.log(this.layer.containers[moduleID].tracksConfigs[this.reductionInstance], splitConfig[0], splitConfig[1], configs[i]);
							if (this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]]) {
							    this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]][splitConfig[1]] = configs[i]
							} else {
							    this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]] = {}; //{splitConfig[1] : configs[i]}
							    this.layer.containers[moduleID].tracksConfigs[this.reductionInstance][splitConfig[0]][splitConfig[1]] = configs[i]
							}
						}
					}
				}
			} else {
				for (var i in configs) {
					splitConfig = i.split(',')
					//console.log(splitConfig)
					if (splitConfig[0] == splitConfig[1]) {
						if ( typeof configs[i] != 'undefined') {
							for (var j = 1; j <= this.maxReduction; j++) {
								this.layer.containers[moduleID].tracksConfigs[j][splitConfig[0]] = configs[i]
							}
						}
					} else {
						if ( typeof configs[i] != 'undefined') {
							for (var j = 1; j <= this.maxReduction; j++ ) {
								this.layer.containers[moduleID].tracksConfigs[j][splitConfig[0]][splitConfig[1]] = configs[i]
							}
						}
					}
				}
			}
			//this.layer.containers[moduleID].onMouseDown()
			//console.log(this.layer.containers[moduleID].tracksConfigs)
		},
	});

	/**
	 * WiringEditor Adapters
	 * @static
	 */
	WireIt.WiringEditor.adapters = {};

})();
