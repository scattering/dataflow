Ext.require([
    'Ext.tree.*',
    'Ext.data.*',
]);

Ext.onReady(function() {

    // create the store. Sends a request to 'getNCNRdirectories', that will be handled
    // by django.
     treeStore = Ext.create('Ext.data.TreeStore', {
        proxy: {
		type: 'ajax',
		actionMethods:'GET',
		reader: {
			type: 'json',
			//root: 'pub'
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
        rootVisible: false,
        
        //store: 'Ext.data.TreeStore',
        //initComponent: function(){
        	//treeStore.load()
        	//Ext.Ajax.request({
        	//	url: 'getNCNRdirs/',
        	//	});
        	//},
        store: treeStore,
        listeners: {
        	beforeexpand: function() {
        		console.log('PANEL HAS BEEN EXPANDED')
        		},
        	beforecontainermouseover: function() {
        		console.log('MOUSEOVER!')
        		},
        	beforeitemexpand: function() {
        		console.log('TREE ITEM HAS BEEN EXPANDED')
        		},
        		
        	},
        
    });
    
    treeStore.load()
});
