function configForm(headerList, moduleID) {

	// headerList should contain a list of [fieldset title ("theta"), [list field names ["x","y"] (dict will have multiple, list and float only one) ]
	items = []

	console.log(headerList)
	for (var i in headerList) {
		items2 = []
		for (var j in headerList[i][1]) {
			item2 = {
				fieldLabel: headerList[i][1][j],
				name: headerList[i][1][j],
			},
			//console.log('i', i, 'j', j)
			//console.log('adding item: ', item2)
			items2.push(item2)
		}
		defaultType = headerList[i][2];
		if(defaultType == 'string' || defaultType == 'undefined'){
			defaultType = 'textfield';
		} else if(defaultType == 'number'){
			defaultType = 'numberfield';
		} else if(defaultType == 'boolean'){
			defaultType = 'checkbox';
		}
		item = {
			xtype: 'fieldset',
			title: headerList[i][0],
			collapsible: true,
			defaultType: defaultType,
			layout: 'anchor',
			defaults: {
				anchor: '100%'
			},
			items: items2,
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

	Ext.create('Ext.form.Panel', {
		renderTo: "instance-modules-input",
		bodyPadding: 5,
		width: 400,
		layout: 'anchor',
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
					//console.log("FORM FIELDS", form.getFields())
					//console.log('FORM VALUES', form.getFieldValues())
					console.log('FORM FIELD ITEMS', form._fields.items)
					for (var j in form._fields.items) {
						key = form._fields.items[j].ownerCt.title + ',' + form._fields.items[j].fieldLabel
						moduleConfigs[key] = form._fields.items[j].lastValue
					}
					console.log('CONFIGS IN FORM', moduleConfigs);
					editor.setModuleConfigsFromForm(moduleConfigs, moduleID, editor.reductionInstance)
				}
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
						moduleConfigs[headerList[k]] = form._fields.items[k].lastValue
					}
					console.log('CONFIGS IN FORM', moduleConfigs)
					editor.setModuleConfigsFromForm(moduleConfigs, moduleID, 'all')
				}
			}
		},],
	});
}