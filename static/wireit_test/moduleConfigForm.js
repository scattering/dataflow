function configForm(headerList, moduleID) {
	items = []
	for (var i in headerList) {
		item = {
			fieldLabel: headerList[i],
			name: headerList[i],
			allowBlank: false,
			}
		items.push(item)
	}
			
		
	Ext.create('Ext.form.Panel', {
		renderTo: "instance-modules-input",
		bodyPadding: 5,
		width: 400,
		layout: 'anchor',
		defaultType: 'textfield',
		items: items,
		buttons: [{
			text: 'Reset',
			handler: function() {
			    this.up('form').getForm().reset();
			}
		    }, {
			text: 'Submit',
			formBind: true, //only enabled once the form is valid
			disabled: true,
			handler: function() {
			    var moduleConfigs = {}
			    var form = this.up('form').getForm();
			    if (form.isValid()) {
			    	for (var j in form._fields.items) {
			    		//console.log('FORM ', form)
			    		moduleConfigs[headerList[j]] = form._fields.items[j].lastValue
			    		}
				//console.log(moduleConfigs);
				editor.setModuleConfigsFromForm(moduleConfigs, moduleID, editor.reductionInstance)
			    }
			}
		    },
		    {
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
		    		editor.setModuleConfigsFromForm(moduleConfigs, moduleID, 'all')
		    		}
		    	}
		    	},],
	});
}
			
	
	
