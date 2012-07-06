//function makeFileSelector(files) {
//     var selector = new Ext.form.ComboBox({
//         xtype: 'combobox',
//         name: 'countries',
//        // Stop users being able to type in the combobox
//         editable: false,
//        // Even though the user cant type any more
//        // once they select one option it'll remove any
//        // others that don't start with the same letters
//        // unless we turn off filtering
//         disableKeyFilter: true,
//        // Only allow users to pick an option that exists
//        // in the list of options (not one of their own)
//         forceSelection: true,
//        // This isn't entirely necessary but the combox
//        // will start off blank otherwise
//         emptyText: '--select one--',
//        // This one's vital: when the user clicks on the
//        // drop-down show ALL options
//         triggerAction: 'all',
//        // By default it retrieves remote data,
//        // we're using local data
//         mode: 'local',
//        // ComboBox will only accept data from a Store
//        // so we have to create a basic one
//         store: new Ext.data.SimpleStore({
//          id: 0,
//          fields: ['value', 'text'],
//          data : [['1', 'UK'], ['2', 'US']]
//         }),
//        // Specify which fields in the store hold
//        // the value and the display text
//         valueField: 'value',
//         displayField: 'text',
//        // Important: by default the POST/GET data
//        // for this item will contain the display text
//        // not the value. This option creates a hidden field
//        // with the same name as the dropdown containing the
//        // selected value so it is that which gets returned
//         hiddenName: 'countries',
//         multiple: true,
//         size: 4,
//    });
//    return selector;
//}

/*
function sortedKeys(array, sortkey) {
    var sortkey = sortkey || 'sortOrder';
    var keys = [];
    for (var i in array) {
        var el = array[i].value;
        if (typeof el == 'object') { 
            keys.push(sortedKeys(el, sortkey));
        } else {
            keys.push(i);
        }
    }
    function comparator(a,b) {
        
        if (typeof array[a] == 'object' sortkey in array[a] && sortkey in b) {
            return a[sortkey] - b[sortkey];
        }
        else if (sortkey in a && !(sortkey in b)) {
            // by default, put sorted values first
            return 1;
        }
        else if (sortkey in b && !(sortkey in a)) {
            // see above
            return -1;
        }
        // now we only have items without sortkeys
        else { return 0 }
    }
    return keys.sort(comparator);
}
*/

function makeFileMultiSelect(src_files, selected_files, form_id, fieldLabel) {

//    var src_files = []
//    for (var i in FILES) {
//        src_files.push(FILES[i][1]);
//    }
    var fieldLabel = fieldLabel || 'files'; // can override
    
    var form_id = form_id || 0;
    src_files.sort()

    var source_files_selector = {
		xtype: 'multiselect',
		name              :  'multiselect',
		fieldLabel        :  'Multiselect',
		store: src_files,
		height: 390,
	};
	
	var dest_files_selector = {
		xtype: 'multiselect',
		name              :  'multiselect',
		fieldLabel        :  'Multiselect',
		store: [],          
		allowBlank        :  true,
		height: 390,
	}
	
	var itemselector = {
	    xtype: 'itemselector',
	    fieldLabel: fieldLabel,
	    multiselects: [source_files_selector, dest_files_selector],
	    store: src_files,
	    value: selected_files,
	    width: 400,
	    height: 400,
	    reverse_lookup_id: form_id
	}
	
	var item = {
	    xtype: 'fieldset',
	    title: fieldLabel,
	    fieldLabel: fieldLabel,
	    //labelWidth: 0,
	    collapsible: true,
	    layout: 'fit',
//	    width: 600,
//	    defaults: {
//		    anchor: '100%'
//	    },
	    items: itemselector
    }
	return item;
}


//******************************************************************************

function makeFileSummarySelect(experiment_id, form_id, fieldLabel) {
    var fieldLabel = fieldLabel || 'files'; // can override
    var form_id = form_id || 0;
    var table_is_created = false;

    var maxvals = [];
    var minvals = [];
    // Generates the "range graphic" in the cells of the file gridpanel
    function vrange(val, meta, record, rI, cI, store) {
        var range = maxvals[cI] - minvals[cI];
        var spl = val.split(',');
        var low = parseFloat(spl[0]);
        var high = parseFloat(spl[1]);
        var roffset = 0;
        var loffset = 0;
        if (range != 0) {
            loffset = ((low - minvals[cI]) / range) * 100 - 1;
            roffset = ((maxvals[cI] - high) / range) * 100 - 1;
        }
        var ret = high + low;
        if (range != 0 && low != NaN && high != NaN) {
            return '<div class="woot"><div style="margin-right:' + roffset + '%; margin-left:' + loffset + '%;"></div></div>';
        } else {
            return '<div class="woot empty"></div>';
        }
    }

    Ext.regModel('fileModel', {
        fields: storeFields
    });
    var storeFields = [];
    var store = Ext.create('Ext.data.Store', { model: 'fileModel'});
    var dataObject = [];
    var gridColumns = [];

    var myCheckboxModel = new Ext.selection.CheckboxModel({
        //checkOnly: true,
        listeners: {
            selectionchange: function (selectionModel, selected, options) {
                // Must refresh the view after every selection
                selectionModel.view.refresh();
            }
        }
    });


    /* GridPanel that displays the data. Filled with empty columns since they are populated with update() */
    var filesummarygrid = new Ext.grid.GridPanel({
        store: store,
        selModel: new Ext.selection.CheckboxModel(),
        columns: gridColumns,
        stripeRows: true,
        height: 250,
        autoWidth: true,
        title: 'Select the files to run reductions on:',
        bbar: [],
    });
    


    /* After data is retrieved from server, we have to reinitiallize the Store reconfigure the grid
    so that the new data is displayed on the page */
    function reload_data(){
        var fieldData = dataObject[0]; //First row is the parameters of the data file (e.g. ['X', 'Y', 'Z', 'Temp'])    
        maxvals = dataObject[1];       //Second row is the max values of the parameters over all files (used for rendering ranges)
        minvals = dataObject[2];       //Third row is min values of parameters
        dataObject.splice(0, 3);       //Remove first three rows; the rest is the actual data

        //add all files to the store..
        var filerecs=[];
	    for (var j = 0; j < dataObject.length; ++j) {
	        var filerec={}
	        for (var i = 0; i < fieldData.length; ++i) {
		        filerec[fieldData[i]] = dataObject[j][i];
	        }
	        filerecs.push(filerec);
	    }

        if (!table_is_created) {
            storeFields = [];
            var gridColumns = [];

            // the first two columns of checkboxes and "Available Files" are not
            // rendered using the standard renderer
            gridColumns.push({header: fieldData[0], width: 100, sortable: true, dataIndex: fieldData[0]});
            storeFields.push({name: fieldData[0]});

            for (var i = 1; i < fieldData.length; ++i) {
                gridColumns.push({header: fieldData[i], width: 100, renderer: vrange, sortable: true, dataIndex: fieldData[i]});
                storeFields.push({name: fieldData[i]});
            }

            Ext.regModel('fileModel', {
                fields: storeFields
            });
            var store = Ext.create('Ext.data.Store', { model: 'fileModel'});
            filesummarygrid.columns = gridColumns;
            
            store.loadData(filerecs);
            filesummarygrid.store = store;

            table_is_created = true;
	    } else {
            filesummarygrid.store.loadData(filerecs);
            filesummarygrid.getView().refresh();
        }
        
    };



    /*Retrieve data in json format via a GET request to the server. This is used
    anytime there is new data, and initially to populate the table.*/
    function update() {
        var conn = new Ext.data.Connection();
        conn.request({
            url: '/metadatajson/',
            method: 'GET',
            params: {'experiment_id': experiment_id},
            success: function(responseObject) {
                dataObject = Ext.decode(responseObject.responseText); //decodes the response
                reload_data();                                        //resets the store and grids
            },
            failure: function() {
                alert("failure with GET!");
            }
        });
	    
    }
    
    update();
	return filesummarygrid;
}

function stripHeadersObject(headers) {
    // reduce headers to name:value pairs (removing label)
    var new_config = {};
    for (var i in headers) {
        var header = headers[i];
        var type = header.type;
        if (type == 'Object') {
            new_config[i] = stripHeadersObject(header);
        } else { // it's just a value
            new_config[i] = header.value;
        }
    }
    return new_config;
}

function configForm(headerList, moduleID) {

	// **DEPRECATED**: headerList should contain a list of [fieldset title ("theta"), [list field names ["x","y"] (dict will have multiple, list and float only one) ]
	// headerlist now should contain list [{'name': name, 'value': val, 'label': label, 'type': type}], {'name': name2, 'value': val2...}, ...]?? not really

	items = [];
	var reverse_lookup_id = 0;
	reverse_lookup = {};
	
    function createItem(header, fieldname) {
        // convert config fields into ExtJS form fields
        var item;
        if (header.type == 'files') {
	        /*
            editor.FAT.update(FILES, editor.getValue().working.modules);
            var unassociated_files = editor.FAT.getUnassociatedFiles(editor.reductionInstance);
            var module_files = header.value;
            var total_files = [];
            for (var i in unassociated_files) { total_files.push(unassociated_files[i]); }
            for (var i in module_files) { total_files.push(module_files[i]); }
            item = makeFileMultiSelect(total_files, module_files, reverse_lookup_id, header.label);
            reverse_lookup[reverse_lookup_id] = header; // pointer back to the original object
            reverse_lookup_id += 1;
            */

            experiment_id = editor.launchedFromExperimentPage
            item = makeFileSummarySelect(experiment_id, reverse_lookup_id, header.label);
            //item = makeFileSummarySelect(total_files, module_files, reverse_lookup_id, header.label);

            reverse_lookup[reverse_lookup_id] = header; // pointer back to the original object
            reverse_lookup_id += 1;
            
        } 
        /*
        else if (header.type == 'files_with_summary') {
            editor.FAT.update(FILES, editor.getValue().working.modules);
            var total_files = header.value;

            extractMetadata(total_files);

            item = makeFileSummarySelect(total_files, reverse_lookup_id, header.label);
            reverse_lookup[reverse_lookup_id] = header; // pointer back to the original object
            reverse_lookup_id += 1;
	    }
        */

        else if (header.type == "Array" || header.type == "Object") { // allow for nested lists of parameters
            var itemlist = [];

            for (var j in header.value) { // nested list... is inner element
                itemlist.push(createItem(header.value[j]));
            }
            item = {
                xtype: 'fieldset',
                title: header.label,
                collapsible: true,
                //defaultType: header.type,
                decimalPrecision : 12,
                layout: 'anchor',
                anchor: '100%',
                autoHeight: true,
                items: itemlist,
            }
        }
        
        else if (header.type == "List") {
            item = 12;
            
            var data = [];
            for (var i in header.choices) {
                data.push({'value':header.choices[i]});
            }
            
            // The data store containing the list of states
            var choices = Ext.create('Ext.data.Store', {
                fields: ['value'],
                data : data
            });

            // Create the combo box, attached to the states data store
            item =  {
                xtype: 'combo', 
                fieldLabel: header.label,
                store: choices,
                queryMode: 'local',
                displayField: 'value',
                valueField: 'value',
                reverse_lookup_id: reverse_lookup_id,
                allowBlank: false,
                editable: false,
                triggerAction: 'all',
                typeAhead: false,
                mode: 'local',
                //renderTo: Ext.getBody()
            }
            
            if (header.choices.indexOf(header.value) != -1) { 
                item.value = header.value; 
            } else {
                item.value = data[0].value;
            }
            
            if ('label' in header) { 
                item.fieldLabel = header.label;
            } else {
                item.fieldLabel = fieldname;
            }
            reverse_lookup[reverse_lookup_id] = header;
            reverse_lookup_id += 1;

        }
        
        else {
            var defaultType; type = header.type || 'undefined';
            if(type == 'string' || type == 'undefined') {
                defaultType = 'textfield';
	    } else if(type == 'number' || type == 'float') {
		defaultType = 'numberfield';
	    } else if(type == 'boolean') {
	        defaultType = 'checkbox';
	    }
            item = {
	        fieldLabel: header.label,
	        xtype: defaultType,
	        name: fieldname,
	        decimalPrecision: 14,
	        value: header.value,
	        anchor: "-20", 
	        allowblank: false,
	        width: 100,
	        autoHeight: true, 
	        reverse_lookup_id: reverse_lookup_id
            }
	    if (defaultType == 'checkbox') { item.checked = header.value; }
		reverse_lookup[reverse_lookup_id] = header;
		reverse_lookup_id += 1;
            }
            return item
        }
    
        for (var i in headerList) {
            // walk through the headerList and create the form items
            items.push(createItem(headerList[i], i));
        }
            
    
        var formPanel = new Ext.FormPanel( {
        
		//renderTo: Ext.getBody(),
		reverse_lookup: reverse_lookup,
		bodyPadding: 5,
		width: 600,
        layout: 'anchor',
		id: 'module_config_form',
		autodestroy: true,
		//defaultType: 'textfield',
		items: items,
		buttons: [{
			text: 'Reset',
			handler: function() {
				this.up('form').getForm().reset();
			}
		},{
			text: 'Submit',
			formBind: true, //only enabled once the form is valid
			disabled: true,
			handler: function() {
				var moduleConfigs = {}
				var form = this.up('form').getForm();

				if (form.isValid()) {
				    for (var j in form._fields.items) {
				        var item = form._fields.items[j];
				        if ("reverse_lookup_id" in item) {
				            reverse_lookup[item.reverse_lookup_id].value = item.getValue();
				        }
				    }
				    Ext.getCmp('module_config_popup').close();
				}
				else { editor.alert('form not valid!'); }
			}
		},{
			text: 'Show Source',
			formBind: true,
			disabled: true,
			handler: function() {
			    var container = editor.layer.containers[moduleID];
			    var module = editor.modules.filter(function(el) { return el.name == container.modulename })[0]; 
			    sourcewin = window.open("/static/lib/sourcewindow.html", "_blank");
			    sourcewin.modname = module.name;
			    sourcewin.source = module.source;
			    sourcewin.onload = function() {
			        this.document.title = "Source: " + module.name;
			        //this.document.getElementById('modname').innerHTML = "<h2>" + this.modname + "</h2>";
			        this.document.getElementById('code').innerHTML = this.source;
			    }
			}
		}
		/*{
			text: 'Submit for all instances',
			formBind: true,
			disabled: true,
			handler: function() {
				var moduleConfigs = {}
				var form = this.up('form').getForm();
				if (form.isValid()) {
					for (var k in form._fields.items) {
						moduleConfigs[headerList[k]] = form._fields.items[k].getValue();
					}
					//console.log('CONFIGS IN FORM', moduleConfigs);
					editor.setModuleConfigsFromForm(moduleConfigs, moduleID, 'all');
					Ext.getCmp('module_config_popup').close();
				}
			}
		} */
		],
	});
	myFormPanel = formPanel;
	return formPanel;
}
