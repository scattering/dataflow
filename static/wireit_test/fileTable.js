function makeFileTable(headerList) {
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

// list for holding the stores for each file type
storeList = []
gridList = []

// defines data model 'Data'
// may need to add a 'hidden' field hash to keep track of actual file identity
   Ext.define('Data', {
	extend: 'Ext.data.Model',
	fields: [
		{name: 'filename', type: 'string'},
		{name: 'filehash', type: 'string'},
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
	for (var i in headerList) {
    	    storeList[i].removeAll()
    }
//measureStore.removeAll()
//backStore.removeAll()
	myGrid.getView().refresh()
	for (var i = 0; i < myGrid.getStore().count(); i++) {
       		rec = myGrid.getStore().getAt(i)
           	for (var k in headerList) {
            		if (rec.get('filetype') == headerList[k]) {
            		    for (var j in rec.get('group').split(',')) {
            		    var newFile = Ext.ModelManager.create({
				filename: rec.get('filename'),
				filetype: rec.get('filetype'),
				group: rec.get('group').split(',')[j]},
'Data')
				storeList[k].insert(0,newFile)
			   }
			}
		}

/**
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
**/
}
//measureStore.sort()
//backStore.sort()
//measureGrid.getView().refresh()
//backGrid.getView().refresh()
	for (var i in headerList) {
		storeList[i].sort()
		gridList[i].getView().refresh()
	}
	generate_FileGroups()
	editor.FATupdate(template_configs)
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
if (fileList) {
	for i in fileList {
		var newFile = Ext.ModelManager.create({
			filename: i[1],
			filehash: i[0],
			filetype: 'N',
			},
			'Data');
		store.insert(0, newFile);
		}
	}
// insert records into the store to play around with if a file list has not been passed into the Wiring Editor
if !(fileList) {
	for (var j = 0; j < 3; j++) {
		for (var i = 0; i < 20; i ++) {
			fname = 'new_file' + i
			var newFile = Ext.ModelManager.create({
				filename: fname,
				filehash: '0',
				filetype: 'N',
				group: j,},
		'Data');
				store.insert(0, newFile);
		}
	}
}

// combobox options for file type editing
combo = []
for (var i in headerList) {
	combo.push([headerList[i],headerList[i]])
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
                store: combo,
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

// tbar button for running reduction
/**
   tbar: [
   	{
   	text: 'Run Reduction',
   	handler: function() {
		console.log('RUNNING REDUCTION!')
		}
	},
   ],
   **/
// selection-related events and configs
   listeners: {
	render: function() {
                       //disable the default browser context menu
                       Ext.getBody().on("contextmenu", Ext.emptyFn, null, 	{preventDefault: true});
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



// Setting up grids and stores for all file types

for (var i in headerList) {
	storeList.push(Ext.create('Ext.data.Store', {
		autoDestroy: true,
		model: 'Data',
		groupField: 'group',
		proxy: {
			type: 'rest',
			urls: '/files',
			reader: {
				type: 'json',
				record: headerList[i],
			}
		},
		sorters: [{
		property: 'group',
		direction: 'ASC',
	}]
	})
)
    }
/**
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
**/

for (var i in headerList) {
	gridList.push( Ext.create('Ext.grid.Panel', {
		title: headerList[i],
		store: storeList[i],
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
		//tbar: [{text: ''}],
		height: 250,
		width: 200,
	})
	)
    }
/**
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
**/

//console.log(headerList)
//console.log(storeList)
//console.log(gridList)

  // setting up grid array to give panel
panelItems = [myGrid].concat(gridList) //gridList]
//console.log(panelItems)

    // grid display panel
    var displayPanel = Ext.create('Ext.Panel', {
        width : (headerList.length)*200+8+250,
        height : 500,
        layout: {
		type: 'hbox',
		align: 'stretch',
	},
        bodyPadding: '5',
	//renderTo: 'FAT',
        items : panelItems //+ gridList
    });

   // overall display panel  
var panelTwo = Ext.create('Ext.Panel', {
	width : (headerList.length)*200+8+250+10,
	height: 530,
	layout: {
		type: 'vbox',
		align: 'stretch',
		},
	bodyPadding: '2',
	items: [displayPanel, 
		{
			xtype: 'button',
			text: 'Run Reduction',
			height: '30',
			handler: run_reduction,
		},
		],
	renderTo: 'FAT',
	});

////////
// Run Reduction
// need to add method for checking whether or not the groups selected exit
//      one idea: check to see the result of send_to_Wireit, and disallow NOFILE

send_to_Wireit = {}
template_configs = {}

// cleans up the store.getGroups objects into a list of strings
function handleResult(identifier, result) {
	if (result) {
		for (var i in result.children) {
			//console.log(send_to_Wireit[identifier])
			if (!send_to_Wireit[identifier]) {
				//console.log("IN UNDEFINED")
				send_to_Wireit[identifier] = [result.children[i].data.filename]
				}
			else {
			send_to_Wireit[identifier] = send_to_Wireit[identifier].concat(result.children[i].data.filename)
			}
		}
		}
	else {
		send_to_Wireit[identifier]='NO FILE'
	   }
	};
		
	
// run reduction handler
// perhaps change it to run reduction for all groups. And the run reduction on the WE will run the current group 
// selection
function generate_FileGroups() {
	groups_to_run = []
	template_configs = {}
	for (var k in storeList) {
		for (var j in storeList[k].getGroups()){
			groups_to_run = groups_to_run.concat(storeList[k].getGroups()[j].name)
			}
		}
	groups_to_run = makeUnique(groups_to_run) // makes the array unique
	index = groups_to_run.indexOf('') // removes the default group ' '
	if (index != -1) {
		groups_to_run.splice(groups_to_run.indexOf(''),1)
		}
	console.log(groups_to_run)
	for (var i in groups_to_run) {
		send_to_Wireit = {}
		for (var j in storeList) {
			//console.log(groups_to_run[i],headerList[j])
			var result = storeList[j].getGroups(groups_to_run[i])
			handleResult(headerList[j], result)
			// pick out the files in store j that are
			// in group i
			template_configs[groups_to_run[i]] = send_to_Wireit
			}
		}
		
    }

function run_reduction() {
	Ext.Msg.prompt('Choose Group?', 'Please enter the groups to be run through reduction:', function(btn, grps) {
		if (btn == 'ok' && acceptable_entry.test(grps)){
			groups_to_run = grps.split(',')
			for (var i in groups_to_run) {
				send_to_Wireit = {}
				for (var j in storeList) {
					//console.log(groups_to_run[i],headerList[j])
					var result = storeList[j].getGroups(groups_to_run[i])
					handleResult(headerList[j], result)
					// pick out the files in store j that are
					// in group i
					}
				}
			console.log(send_to_Wireit)
			window.editor.runReduction(send_to_Wireit)
			}
		else if (btn == 'ok') {
			console.log("Invalid entry for field 'group'. Please enter comma separated integers.")}
			}
    )}

// setting up menu items for context menu
setTypeMenu = []

function return_handler(text) {
	return function() {
		setRecords(myGrid.getSelectionModel().getSelection(),
'filetype', text);
		UpdateAll();
	};
}

for (var i in headerList) {
	entry = {
		text: headerList[i],
		handler: return_handler(headerList[i]),
	}
setTypeMenu.push(entry)
}
//console.log(setTypeMenu)

   // context menu for group/type editing
contextMenu = new Ext.menu.Menu({
	items: [{
	text: 'Set Type',
	menu: setTypeMenu,
	},
	{ 
	text: 'Clear Type',
	handler: function() {
		setRecords(myGrid.getSelectionModel().getSelection(), 'filetype', 'N')
		UpdateAll()
		},
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
}, 
{
	text: 'Clear Group',
	handler: function() {
		setRecords(myGrid.getSelectionModel().getSelection(), 'group', '')
		UpdateAll()
	}
	}],
});
}


