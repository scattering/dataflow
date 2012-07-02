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

    Ext.regModel('fileModel', {
	fields: [
	    {name: 'file name', type: 'string'},
	    'database id',
	    {name:'sha1',type:'string'}
	]
    });

    var store = Ext.create('Ext.data.Store', { model: 'fileModel'});
	
//	var store = new Ext.data.Store({
//        proxy: new Ext.data.proxy.Memory(dataArray),
//        reader: new Ext.data.ArrayReader({},storeFields),
//        remoteSort: true,
//    });
    var gridColumns = [];
	
    gridColumns.push({header: 'file name', width: 150, sortable: true, dataIndex: 'filename'});
    //storeFields.push({name: fieldData[0]});
    gridColumns.push({header: 'database id', width: 150,hidden:true, sortable: true, dataIndex: 'database_id'});
    //storeFields.push({name: fieldData[1]});
    gridColumns.push({header: 'sha1', width: 150,hidden:true, sortable: true, dataIndex: 'sha1'});
    //storeFields.push({name: fieldData[2]});	
	
	/*GridPanel that displays the data*/
    var grid = new Ext.grid.GridPanel({
        store: store,
        columns: gridColumns,
        stripeRows: true,
        height: 500,
        autoWidth: true,
        title: 'Available files',
        bbar: [],
    });
	
    grid.render('gridtest');


	
/*After data is retrieved from server, we have to reinitiallize the Store reconfigure the ArrayGrid
so that the new data is displayed on the page*/
    function reload_data(){
	var fieldData = dataArray[0]; //First row is the parameters of the data file (e.g. ['X', 'Y', 'Z', 'Temp'])
	maxvals = dataArray[1];       //Second row is the max values of the parameters over all files (used for rendering ranges)
	minvals = dataArray[2];       //Third row is min values of parameters
	dataArray.splice(0, 3);        //The rest is the actual data
	var gridColumns = [];
	storeFields = [];
    /*The first three parameters (File Name, database ID, and md5 sum) aren't renedered using the
    standard renderer and the ID and md5 sum aren't displayed at all, they are only used for server
    requests later, so we add them to the Store differently*/
	gridColumns.push({header: fieldData[0], width: 150, sortable: true, dataIndex: fieldData[0]});
	storeFields.push({name: fieldData[0]});
	gridColumns.push({header: fieldData[1], width: 150,hidden:true, sortable: true, dataIndex: fieldData[1]});
	storeFields.push({name: fieldData[1]});
	gridColumns.push({header: fieldData[2], width: 150,hidden:true, sortable: true, dataIndex: fieldData[2]});
	storeFields.push({name: fieldData[2]});
	for (var i = 3; i < fieldData.length; ++i) {
	    gridColumns.push({header: fieldData[i], width: 100, renderer: vrange, sortable: true, dataIndex: fieldData[i]});
	    storeFields.push({name: fieldData[i]});
	}
	//store = new Ext.data.Store({
	//    proxy: new Ext.data.proxy.Memory(dataArray),
	//    reader: new Ext.data.ArrayReader({},storeFields),
	//    remoteSort: true,
	//});
	    
	Ext.regModel('fileModel', {
	    fields: storeFields
	});
	var store = Ext.create('Ext.data.Store', { model: 'fileModel'});
	grid.columns=gridColumns;
	
	//add all files to the store..
	var filerecs=[];
	for (var j = 0; j < dataArray.length; ++j) {
	    var filerec={}
	    for (var i = 0; i < fieldData.length; ++i) {
		filerec[fieldData[i]]=dataArray[j][i];
	    }
	    filerecs.push(filerec);
	}
	store.loadData(filerecs);
	//colModel = new Ext.grid.ColumnModel({columns: gridColumns});
	//store.load({params:{start:0, limit:10}});
	//grid.getBottomToolbar().removeAll();
	//grid.getBottomToolbar().add(new Ext.PagingToolbar({
	//        store:store,
	//        pageSize: 10,
	//        displayInfo: false,
	//        displayMsg: 'Displaying topics {0} - {1} of {2}',
	//        emptyMsg: "No topics to display",
	//    }))
	//grid.getBottomToolbar().doLayout();
	grid.reconfigure(store, gridColumns);
    
    };



/*Retrieve data in json format via a GET request to the server. This is used
anytime there is new data, and initially to populate the table.*/
    function update() {
	//dataArray=[['file name','database id','sha1','x','y','z'],[NaN,NaN,NaN,10,10,10],[NaN,NaN,NaN,-10,-10,-10],['file1','1','sh1','1,9','2,3','3,4'],['file2','1','sh2','4,5','2,3','5,5']];	
    var conn = new Ext.data.Connection();
        conn.request({
            url: '/json/',
            method: 'GET',
            params: {},
            success: function(responseObject) {
                dataArray = Ext.decode(responseObject.responseText);//decodes the response
                reload_data();                                      //resets the store and grids
            },
            failure: function() {
            }
        });
	//reload_data();
    }
    update();
	




});