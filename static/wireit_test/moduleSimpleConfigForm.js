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


function makeFileMultiSelect(src_files, selected_files) {

//    var src_files = []
//    for (var i in FILES) {
//        src_files.push(FILES[i][1]);
//    }

    src_files.sort()
    console.log('src_files', src_files);
    console.log('dest_files', files);
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
	    fieldLabel: 'files',
	    multiselects: [source_files_selector, dest_files_selector],
	    store: src_files,
	    value: selected_files,
	    width: 400,
	    height: 400,
	}
	
	var item = {
	    xtype: 'fieldset',
	    title: 'files',
	    fieldLabel: 'files',
	    //labelWidth: 0,
	    collapsible: true,
	    layout: 'fit',
//	    width: 600,
//	    defaults: {
//		    anchor: '100%'
//	    },
	    items: itemselector,
    }
	return item;
}

function configForm(headerList, moduleID) {

	// headerList should contain a list of [fieldset title ("theta"), [list field names ["x","y"] (dict will have multiple, list and float only one) ]
	items = []

	console.log(headerList)
	for (var i in headerList) {
	    var header = headerList[i];
	    if (header[0] == 'files') {
	        editor.FAT.update(FILES, editor.getValue().working.modules);
	        var unassociated_files = editor.FAT.getUnassociatedFiles(editor.reductionInstance);
	        var module_files = header[2];
	        var total_files = [];
	        for (var i in unassociated_files) { total_files.push(unassociated_files[i]); }
	        for (var i in module_files) { total_files.push(module_files[i]); }
	        item = makeFileMultiSelect(total_files, module_files);
	    } else {
		    items2 = []
		    for (var j in headerList[i][1]) {
			    item2 = {
				    fieldLabel: headerList[i][1][j],
				    name: headerList[i][1][j],
				    decimalPrecision: 14,
				    value: headerList[i][2][j],
				    anchor: "-20", 
				    allowblank: false,
				    width: 100,
				    autoHeight: true,
				    //height: 50,
			    },
			    //console.log('i', i, 'j', j)
			    //console.log('adding item: ', item2)
			    items2.push(item2)
		    }
		    defaultType = typeof headerList[i][2][0];
		    if(defaultType == 'string' || defaultType == 'undefined') {
			    defaultType = 'textfield';
		    } else if(defaultType == 'number') {
			    defaultType = 'numberfield';
		    } else if(defaultType == 'boolean') {
			    defaultType = 'checkbox';
		    }
		    item = {
			    xtype: 'fieldset',
			    title: headerList[i][0],
			    collapsible: true,
			    defaultType: defaultType,
			    decimalPrecision : 12,
			    layout: 'anchor',
			    anchor: '100%',
			    autoHeight: true,
			    items: items2,
		    }
		}
		items.push(item)
	}

	/**
	 for (var i in headerList) {
	 item = {
	 fieldLabel: headerList[i],
	 name: headerList[i],
	 allowBlank: false,
	 }
	 items.push(item)
	 }
	 **/
    
    var formPanel = new Ext.FormPanel( {
		//renderTo: Ext.getBody(),
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
				console.log("submitting")
				if (form.isValid()) {
					console.log("valid")
					//console.log("FORM FIELDS", form.getFields())
					//console.log('FORM VALUES', form.getFieldValues())
					//console.log('FORM FIELD ITEMS', form._fields.items)
					var allStringsBlank = true;
					for (var j in form._fields.items) {
						key = form._fields.items[j].ownerCt.title + ',' + form._fields.items[j].fieldLabel
						moduleConfigs[key] = form._fields.items[j].getValue();
						if(form._fields.items[j].id.split("-")[0] == 'numberfield' && typeof moduleConfigs[key] == "string")
							moduleConfigs[key] = Number(moduleConfigs[key]);
						if(allStringsBlank && form._fields.items[j].id.split("-")[0] == 'textfield'){
							if(form._fields.items[j].getValue() != undefined){
								allStringsBlank = false;
							}
						}
					}
					//console.log('CONFIGS IN FORM', moduleConfigs);
					editor.setModuleConfigsFromForm(moduleConfigs, moduleID, editor.reductionInstance)
					//console.log("setModuleConfigsFromForm", moduleConfigs, moduleID, editor.reductionInstance);
					
					//console.log("All strings blank? ",allStringsBlank);
					if(allStringsBlank){
						for(var j in form._fields.items){
							if(form._fields.items[j].id.split("-")[0] == 'textfield'){
								key = form._fields.items[j].ownerCt.title + ',' + form._fields.items[j].fieldLabel
								moduleConfigs[key] = "" // blank should be reset
							}
						}
						//console.log("RESETING ALL EMPTY STRING FIELDS");
						editor.setModuleConfigsFromForm(moduleConfigs, moduleID, editor.reductionInstance);
						//console.log("setModuleConfigsFromForm", moduleConfigs, moduleID, editor.reductionInstance);
					}
				    Ext.getCmp('module_config_popup').close();
				}; 
			}
		},{
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
		},],
	});
	console.log('formPanel:', formPanel);
	return formPanel;
}
