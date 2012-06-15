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

// Given a bundle of TripleAxis objects, 
function makeDataSummary(source_objects, selected_objects, form_id, fieldLabel) {

//    var src_files = []
//    for (var i in FILES) {
//        src_files.push(FILES[i][1]);
//    }
    var fieldLabel = fieldLabel || 'data_summary'; // can override
    
    var form_id = form_id || 0;
    //src_files.sort()

    var source_objects_selector = {
		xtype: 'multiselect',
		name              :  'multiselect',
		fieldLabel        :  'Multiselect',
		store: source_objects,
		height: 390,
	};
	
	var dest_objects_selector = {
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
	    multiselects: [source_objects_selector, dest_objects_selector],
	    store: src_objects,
	    value: selected_objects,
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
	        editor.FAT.update(FILES, editor.getValue().working.modules);
	        var unassociated_files = editor.FAT.getUnassociatedFiles(editor.reductionInstance);
	        var module_files = header.value;
	        var total_files = [];
	        for (var i in unassociated_files) { total_files.push(unassociated_files[i]); }
	        for (var i in module_files) { total_files.push(module_files[i]); }
	        item = makeFileMultiSelect(total_files, module_files, reverse_lookup_id, header.label);
	        reverse_lookup[reverse_lookup_id] = header; // pointer back to the original object
	        reverse_lookup_id += 1;
	        
        } 

        else if (header.type == 'data_summary') {
                //editor.FAT.update(FILES, editor.getValue().working.modules);
	        var unassociated_files = editor.FAT.getUnassociatedFiles(editor.reductionInstance);
	        var module_files = header.value;
	        var total_files = [];
	        for (var i in unassociated_files) { total_files.push(unassociated_files[i]); }
	        for (var i in module_files) { total_files.push(module_files[i]); }
	        item = makeDataSummary(total_files, module_files, reverse_lookup_id, header.label);
	        reverse_lookup[reverse_lookup_id] = header; // pointer back to the original object
	        reverse_lookup_id += 1;

      }

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
