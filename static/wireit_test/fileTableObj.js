function makeFileTable(fileList, moduleConfigs) {
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
    var me = this;
    this.fileList = fileList;
    this.moduleConfigs = moduleConfigs;
    this.headerList = {};
    for (var i in moduleConfigs) {
        // grab the modules that have a target (Loaders)
        if ('target_id' in moduleConfigs[i].config) {
            this.headerList[i] = moduleConfigs[i].config.target_id; 
        }
    }
    

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

    // create the main data Store
    this.store = Ext.create('Ext.data.Store', {
        // destroy the store if the grid is destroyed
        autoDestroy: true,
        model: 'Data',
        proxy: {
            type: 'localstorage',
            id: 'mainStore',
        },
//        proxy: {
//            type: 'rest',
//            url: '/files',
//            reader: {
//                type: 'json',
//                // records will have a 'Data' tag
//                record: 'Data'
//            }
//        },
        sorters: [{
            property: 'filename',
            direction:'ASC'
        }]
    });

    // set the field value of a group of records
    this.setRecords = function (record_list, field, value) {
	    for (ind in record_list) {
		    record_list[ind].set(field, value)
	    }
    }
    
    
    this.generateFileGroups = function() {
        var groups_to_run = []
	    this.store.each( function(f) {
	        var groups = f.data.group.split(',');
	        for (var g in groups) {
	            var group = parseInt(groups[g]);
	            if (!isNaN(group)) {
	                if (groups_to_run.indexOf(group) == -1 && f.data.type != 'Unassigned') { groups_to_run.push(group) }
	            }
	        }
	    });
        return groups_to_run;
    }
    
    this.getUnassociatedFiles = function(reductionInstance) {
        var unassociated_files = [];
        var associated_files = [];
        // add any file that is associated in this reduction Instance
        this.store.each( function (f) {
            var groups = f.data.group.split(',');
            var associated = false;
            for (var g in groups) {
                var group = parseInt(groups[g]);
                //if (group == reductionInstance && f.data.type != 'Unassigned') { associated_files.push(f.data.filename) }  
                if (group == reductionInstance && f.data.type != 'Unassigned') { associated = true; }
            }
            if (!associated) {
                unassociated_files.push(f.data.filename);
            } else {
                associated_files.push(f.data.filename);
            }
        });
        return unassociated_files;
    }
    
    // configuring selection Model
    var rowSelecting = Ext.create('Ext.selection.RowModel', {
	    allowDeselect: false,
    });

    // regular expression for group testing
    // group field accepts only comma separated integers as entries
    this.acceptable_entry = /^[0-9]+(, ?[0-9]+)*,?$/


    // configuring cell editing
    var cellEdit = Ext.create('Ext.grid.plugin.CellEditing', {
	    clicksToEdit: 2,
	    listeners: {
		    edit: function(cellEdit, e) {
			    if (e.field == 'group') {
				    if (! me.acceptable_entry.test(e.value)){
				       e.record.set(e.field, e.originalValue);
				       alert("Invalid entry for field 'group'. Please enter comma separated integers.");
			        }
		        }
		    },
	    },
    });

    
    // combobox options for file type editing
    this.combo = []
    for (var i in this.headerList) {
	    this.combo.push([me.headerList[i],me.headerList[i]]);
    }

    // create the grid
    this.grid = Ext.create('Ext.grid.Panel', {
        title: 'Data Files',
        store: this.store,
        sm: rowSelecting,
        columns: [
            {
               	header: 'Files',
               	dataIndex: 'filename',
               	flex: 1,
               	field: {
               	   xtype: 'textfield',
	               allowBlank: false,
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
		            allowBlank: false,
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
                me.contextMenu.showAt(e.getXY())
            },
        },
        trackMouseOver: true,
        plugins: [cellEdit],
        multiSelect: true,
        height: 350,
        width: 600,
    });


    
    this.refreshStore = function() {
        me.store.removeAll();
        //console.log('refreshing store:', me.headerList, me.fileList, me.moduleConfigs);
        // grab all the modules that are loaders (they're in the headerList)
       
        if (me.fileList.length != 0) {
	        //// PULLS IN APPROPRIATE FILE TYPES FROM CONFIGS, CAN ONLY SAVE ONE REDUCTION INSTANCE (GROUP) CURRENTLY
	        var fileNames = []
	        files = {};
	        for (var q in me.fileList) {
		        fileNames.push(me.fileList[q][1])
		        files[me.fileList[q][1]] = {'hash': me.fileList[q][0], 'type': 'Unassigned', 'group': []};
		    }
	        for (var i in me.headerList) {
	            var module = me.moduleConfigs[i];
	            for (var j in module.config) {
	                if (module.config[j].files) {
	                    for (var k in module.config[j].files) {
	                        var fn = module.config[j].files[k];
	                        if (fn in files) {
			                    files[fn].type = module.config.target_id;
			                    files[fn].group.push(j);
			                }
	                    }
	                }
	            }
	        }

            for (var fn in files) {
                var newFile = Ext.ModelManager.create({
                    filename: fn,
                    filehash: files[fn].hash,
                    filetype: files[fn].type,
                    group: String(files[fn].group),
                    },
                    'Data');
                me.store.insert(0, newFile);
            }                
        }
    }
    
    this.refreshStore();
    
    this.update = function(fileList, moduleConfigs) {
        //console.log('updating: ', headerList, fileList, moduleConfigs);
        //me.headerList = headerList;
        me.headerList = {};
        for (var i in moduleConfigs) {
            if (moduleConfigs[i].config.target_id) {
                me.headerList[i] = moduleConfigs[i].config.target_id; 
            }
        }
        //console.log('new headerlist: ', me.headerList);
        me.fileList = fileList;
        me.moduleConfigs = moduleConfigs;
        me.refreshStore();
        me.contextMenu = me.newContextMenu();
    }

    // grid display panel
    this.displayPanel = Ext.create('Ext.Panel', {
        id: 'FAT_popup_displayPanel',
        //width : (this.headerList.length)*200+8+400,
        //width: 408,
        //height : 500,
        autoHeight: true,
        autoWidth: true,
//        layout: {
//		    type: 'hbox',
//		    align: 'stretch',
//	    },
        bodyPadding: '5',
    });
    
    this.displayPanel.add(this.grid);
    
    this.submit_changes = function() {
        // alter the containers in the editor... change this to a passback of configs?
	    for (var i in me.headerList) {
	        var module = me.moduleConfigs[i];
	        var container = editor.layer.containers[i];
	        for (var n in container.tracksConfigs) {
	            if (typeof container.tracksConfigs[n] == 'object') {
	                delete container.tracksConfigs[n]['files'];
	            }
	        }
	        me.store.each( function (f) {
	            var groups = f.data.group.split(',');
	            for (var g in groups) {
	                if (!(groups[g] == '')) {
	                    var groupnum = Number(groups[g]);
	                    //console.log('groupnum:', groupnum, groups);
	                    if (!container.tracksConfigs) { container.tracksConfigs = {} }
	                    if (!container.tracksConfigs[groupnum]) { container.tracksConfigs[groupnum] = {} }
	                    if (!container.tracksConfigs[groupnum]['files']) { container.tracksConfigs[groupnum]['files'] = [] }
	                    if (f.data.filetype == me.headerList[i]) {
	                        container.tracksConfigs[groupnum].files.push(f.data.filename);
	                        //console.log('pushing ' + f.data.filename + ' to container ' + i);
	                    }
	                }
	            }
	        });    
	    }
	    editor.reductionInstances = me.generateFileGroups();
	    editor.setReductionIndex();
        Ext.getCmp('FAT_popup').close();
    };
    
    // overall display panel  
    this.mainPanel = Ext.create('Ext.Panel', {
        id: 'FAT_popup_mainPanel',
	    autoWidth: true,
	    autoHeight: true,
	    bodyPadding: '2',
	    items: [displayPanel, 
		    {
			    xtype: 'button',
			    text: 'Submit',
			    height: '30',
			    componentCls: 'big-button',
			    handler: this.submit_changes,
		    },
		    ],
	});

    this.return_handler = function(text) {
	    return function() {
		    me.setRecords(me.grid.getSelectionModel().getSelection(),'filetype',text);
	    };
    }


    // context menu for group/type editing
    this.newContextMenu = function() {
        var newMenu = new Ext.menu.Menu({
	        items: [{
	            text: 'Set Type',
	            menu: function() {
	                //console.log('menu', me);
	                var setTypeMenu = [];
	                for (var i in me.headerList) {
	                    //console.log(me, headerList[i]);
	                    var entry = { 
	                        text: me.headerList[i],  
	                        handler: me.return_handler(me.headerList[i]),
	                    }
	                    setTypeMenu.push(entry);
	                }
	                return setTypeMenu;    
                }(),
            },
	        { 
	            text: 'Clear Type',
	            handler: function() {
		            me.setRecords(me.grid.getSelectionModel().getSelection(), 'filetype', 'Unassigned')
		        },
	        },
	        {
	            text: 'Set Group',
	            handler: function() {
		            Ext.Msg.prompt('Set Group?', 'Please enter the group value:', function(btn, grpnm) {
		                if (btn == 'ok' && me.acceptable_entry.test(grpnm)){
		                    me.setRecords(me.grid.getSelectionModel().getSelection(), 'group', grpnm);
                		}
		                else if (btn == 'ok') {
			                alert("Invalid entry for field 'group'. Please enter comma separated integers.");
			            }
		            });
	            }
            }, 
            {
	            text: 'Clear Group',
	            handler: function() {
		            me.setRecords(me.grid.getSelectionModel().getSelection(), 'group', '')
	            }
	        }],
        });
    
        return newMenu;
    };
    
    this.contextMenu = this.newContextMenu();
    
    return this
}


