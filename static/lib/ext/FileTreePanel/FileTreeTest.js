Ext.require([
    'Ext.tree.*',
    'Ext.data.*',
]);

Ext.onReady(function() {

    // create the store. Sends a request to 'getNCNRdirectories', that will be handled
    // by django.
     var treeStore = Ext.create('Ext.data.TreeStore', {
        proxy: {
		type: 'ajax',
		actionMethods:'GET',
		reader: {
			type: 'json',
			root: {
				text: 'pub',
				id: 0,
				
			},
		url: 'getNCNRdirs/',
	},
    });

    // create the tree
    tree = Ext.create('Ext.tree.Panel', {
    	id: 'tree',
        hideHeaders: true,
        rootVisible: true,
        height: 350,
        width: 400,
        renderTo: 'tree-example',
        collapsible: true,
        
        //store: 'Ext.data.TreeStore',
        //initComponent: function(){
        	//treeStore.load()
        	//Ext.Ajax.request({
        	//	url: 'getNCNRdirs/',
        	//	});
        	//},
        store: treeStore,
    });
    
    treeStore.load()
});
