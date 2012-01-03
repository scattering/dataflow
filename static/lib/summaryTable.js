Ext.onReady(function() {
/* FILE ASSOCIATIONS TABLE, Andrew Tracer, 6/8/2011

Field:
	-filename, the name of the file
		- accepts any string
	-filetype, the type of file (e.g., measurement or background)
		- combobox options MEA or BAC
	-group, associating a bunch of files (e.g., measurement and 
		background from one experiment)
		- accepts lone integers and comma separated integers

Editing:
	-Double-click on a cell to edit an individual record's field values.
	-Shift + right-click will allow you to edit the filetype and group of all selected rows.		
	-the group field will accept a single integer or a list of integers.
		The latter option is to allow association of a single file 
		with multiple groups

*/
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
        if (range != 0 && low != NaN && high != NaN) {return '<div class="woot"><div style="margin-right:' + roffset + '%; margin-left:' + loffset + '%;"></div></div>';}
        else {return '<div class="woot empty"></div>';}
    }
    var storeFields = [];
    var dataArray = [];
	
	
// defines data model 'Data'
   Ext.define('Data', {
	extend: 'Ext.data.Model',
	   fields: [
		{name: 'filename', type: 'string'},
		{name: 'filetype'},
		{name: 'group', type: 'string'},
		]
	});

// set the field value of a group of records
   function setRecords(record_list, field, value) {
	for (ind in record_list) {
		record_list[ind].set(field, value)
		}
	}

// updates the stores of the target grids (measurement/background) 
// based on filetype values and refreshes all grid views
   function UpdateAll() {
	measureStore.removeAll()
	backStore.removeAll()
	myGrid.getView().refresh()
	for (var i = 0; i < myGrid.getStore().count(); i++) {
           rec = myGrid.getStore().getAt(i)
	   if (rec.get('filetype') == 'MEA') {
		for (var j in rec.get('group').split(',')) {
			var newFile = Ext.ModelManager.create({
			   filename: rec.get('filename'),
			   filetype: rec.get('filetype'),
			   group: rec.get('group').split(',')[j]},
			   'Data')
			measureStore.insert(0,newFile)
			}
		}
	   if (rec.get('filetype') == 'BAC') {
		for (var k in rec.get('group').split(',')) {
			var newFile = Ext.ModelManager.create({
			   filename: rec.get('filename'),
			   filetype: rec.get('filetype'),
			   group: rec.get('group').split(',')[k]},
			   'Data')
			backStore.insert(0,newFile)
			}
		}	
		}
	measureStore.sort()
	backStore.sort()
	measureGrid.getView().refresh()
	backGrid.getView().refresh()
};


// stores previous selection in order to (try to) deal with contextmenu issue
	// not working
   var prev_sel = [];

// configuring selection Model
   var rowSelecting = Ext.create('Ext.selection.RowModel', {
	allowDeselect: false,
	});

// regular expression for group testing
	// group field accepts only comma separated integers as entries
   var acceptable_entry = /^[0-9]+(, ?[0-9]+)*,?$/


// configuring cell editing
   var cellEdit = Ext.create('Ext.grid.plugin.CellEditing', {
	clicksToEdit: 2,
	listeners: {
	   edit: function(cellEdit, e) {
		if (e.field == 'group') {
			if (! acceptable_entry.test(e.value)){
				e.record.set(e.field, e.originalValue)
				console.log("Invalid entry for field 'group'. Please enter comma separated integers.")
				}
}
	UpdateAll()
},	
	},
});	   


// create the main data Store
    var store = Ext.create('Ext.data.Store', {
        // destroy the store if the grid is destroyed
        autoDestroy: true,
        model: 'Data',
        proxy: {
            type: 'rest',
	    url: '/files',
            reader: {
                type: 'json',
                // records will have a 'Data' tag
                record: 'Data'
            }
        },
        sorters: [{
            property: 'filename',
            direction:'ASC'
        }]
    });

// insert 20 records into the store to play around with
for (var i = 0; i < 20; i ++) {
	fname = 'new_file' + i
	var newFile = Ext.ModelManager.create({
		filename: fname,
		filetype: 'N',}, 
		'Data');
		store.insert(0, newFile);
	}
	

// create the grid
var myGrid = Ext.create('Ext.grid.Panel', {
   title: 'Data Files',
   store: store,
   sm: rowSelecting,
   columns: [
	{
	   header: 'Files', 
	   dataIndex: 'filename', 
	   flex: 1,
	   field: {
		xtype: 'textfield',
		allowBlank: false
	},
},
{
	   header: 'Type', 
	   dataIndex: 'filetype', 
	   flex: 1,
           field: {
                xtype: 'combobox',
                typeAhead: true,
                triggerAction: 'all',
                selectOnTab: true,
                store: [
                    ['MEA','MEA'],
                    ['BAC','BAC'],
                ],
                lazyRender: true,
                listClass: 'x-combo-list-small'
            }
},
	{
	   header: 'Group', 
	   dataIndex: 'group', 
	   flex: 1,
	   field: {
		xtype: 'textfield',
		allowBlank: false
	},
},
     ],
  
// selection-related events and configs
   listeners: {
		render: function() {
                       //disable the default browser context menu
                       Ext.getBody().on("contextmenu", Ext.emptyFn, null, {preventDefault: true});
               },
		select: function() {
			//console.log('select')
			},
		selectionchange: function() {
			//console.log('change')
			},
		beforeselect: function() {
			//console.log('beforeselection')
			},
		beforedeselect: function() {
			//console.log('beforedeselect')
},
		itemcontextmenu: function(a,b,c,d,e) {
			contextMenu.showAt(e.getXY())
		},
},
   trackMouseOver: true,
   plugins: [cellEdit],
   multiSelect: true,
   height: 250,
   width: 250,
});



// Setting up grids and stores for drop targets

    //measurement store
    var measureStore = Ext.create('Ext.data.Store', {
        autoDestroy: true,
        model: 'Data',
	groupField: 'group',
        proxy: {
            type: 'rest',
	    url: '/files',
            reader: {
                type: 'json',
                // records will have a 'Data' tag
                record: 'measureData'
            }
        },
        sorters: [{
            property: 'group',
            direction:'ASC'
        }]
    });

    // background store
    var backStore = Ext.create('Ext.data.Store', {
        autoDestroy: true,
        model: 'Data',
	groupField: 'group',
        proxy: {
            type: 'rest',
	    url: '/files',
            reader: {
                type: 'json',
                // records will have a 'Data' tag
                record: 'backData'
            }
        },
        sorters: [{
            property: 'group',
            direction:'ASC'
        }]
    });

   // measurement Grid
   var measureGrid = Ext.create('Ext.grid.Panel', {
	title: 'Measurement Files',
	store: measureStore,	
	features: [{ftype: 'grouping'}],
	columns: [
	{
	   header: 'Files', 
	   dataIndex: 'filename', 
	   flex: 1,
	   field: {
		xtype: 'textfield',
		allowBlank: false
	},
}
	],
	height: 250,
	width: 250,
});

   // background grid
   var backGrid = Ext.create('Ext.grid.Panel', {
	title: 'Background Files',
	store: backStore,
	features: [{ftype: 'grouping'}],
	columns: [
	{
	   header: 'Files', 
	   dataIndex: 'filename', 
	   flex: 1,
	   field: {
		xtype: 'textfield',
		allowBlank: false
	},
}
	],
	height: 250,
	width: 250,
});
	
    // overall display
    var displayPanel = Ext.create('Ext.Panel', {
        width    : 762,
        height   : 500,
        layout: {
		type: 'hbox',
		align: 'stretch',
		},
        bodyPadding: '5',
	renderTo: 'gridtest',
        items    : [
            myGrid,
	    measureGrid,
	    backGrid,
        ],
    });

   // context menu for group/type editing
   contextMenu = new Ext.menu.Menu({
	items: [{ 
	text: 'Set Type',
	menu: [{
		text: 'MEA',
		handler: function() {
		   	setRecords(myGrid.getSelectionModel().getSelection(), 'filetype', 'MEA')
			UpdateAll()
			}
		},
		{
		text: 'BAC',
		handler: function() {
			setRecords(myGrid.getSelectionModel().getSelection(),'filetype','BAC')	
			UpdateAll()		
		}
	}
	],

},
{
	text: 'Set Group',
	handler: function() {
	 	Ext.Msg.prompt('Set Group?', 'Please enter the group value:', function(btn, grpnm) {
		if (btn == 'ok' && acceptable_entry.test(grpnm)){
			setRecords(myGrid.getSelectionModel().getSelection(), 'group', grpnm)
			UpdateAll()
		} 	
		else if (btn == 'ok') {
			console.log("Invalid entry for field 'group'. Please enter comma separated integers.")}
	    }
	)}
}, {
	text: 'Clear Group',
	handler: function() {
		setRecords(myGrid.getSelectionModel().getSelection(), 'group', '')
		UpdateAll()	
	}
}],
});



});