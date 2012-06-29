/*
 * Author: Alex Yee
 *
 * This is the frontend for the UB matrix calculator web-app.
 * 
 * Highlighting table rows helped by:
 *   http://www.sencha.com/forum/showthread.php?4909-Check-Box-Row-Selection-Model&p=25831
 */

Ext.onReady(function () {
    var conn = new Ext.data.Connection();
    var isUBcalculated = 'no';     //Tells whether UB matrix has been calculated
                                   //either: 'no', 'yes', or 'refined'
                         
// ********* START - Defining and assigning variables for the numberfield inputs  *********
    var aField = new Ext.form.NumberField({
        fieldLabel: 'a',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var bField = new Ext.form.NumberField({
        fieldLabel: 'b',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var cField = new Ext.form.NumberField({
        fieldLabel: 'c',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var alphaField = new Ext.form.NumberField({
        fieldLabel: 'α',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var betaField = new Ext.form.NumberField({
        fieldLabel: 'β',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var gammaField = new Ext.form.NumberField({
        fieldLabel: 'γ',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var wavelengthField = new Ext.form.NumberField({
        fieldLabel: 'Wavelength (λ)',
        allowBlank: true,
        decimalPrecision: 7
    });
    
    
    //scattering plane h, k, l numberfields:
    var h1Field = new Ext.form.NumberField({
        fieldLabel: 'h1',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var k1Field = new Ext.form.NumberField({
        fieldLabel: 'k1',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var l1Field = new Ext.form.NumberField({
        fieldLabel: 'l1',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var h2Field = new Ext.form.NumberField({
        fieldLabel: 'h2',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var k2Field = new Ext.form.NumberField({
        fieldLabel: 'k2',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var l2Field = new Ext.form.NumberField({
        fieldLabel: 'l2',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    
    //UB matrix numberfields:
    var UB11Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB12Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB13Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB21Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB22Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB23Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB31Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB32Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB33Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    
    //phi fixed phi field
    var phiField = new Ext.form.NumberField({
        fieldLabel: 'Fixed Phi (φ)',
        allowBlank: false,
        decimalPrecision: 7,
    });
    
    // ********* END - Defining and assigning variables for the numberfield inputs  *********  
                                   
    myUBmatrix = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]] //The variable that will hold the calculated UB matrix

    var baseData = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ];
    var baseIdealData = [
        [0.0, 0.0, 0.0, '0', '0', '0', '0', '0'],
    ];

    // create the Data Store
    var UBInputFields = [
        { name: 'h',        type: 'float'},
        { name: 'k',        type: 'float'},
        { name: 'l',        type: 'float'},
        { name: 'twotheta', type: 'float'},
        { name: 'theta',    type: 'float'},
        { name: 'chi',      type: 'float'},
        { name: 'phi',      type: 'float'},
    ] 
    var store = new Ext.data.ArrayStore({
        autodestroy     : false,
        storeId         : 'UBInputStore',
        fields          : UBInputFields,
        pruneModifiedRecords: true
    });
    store.loadData(baseData);
    
    
    var desiredFields = [
        { name: 'h'},
        { name: 'k'},
        { name: 'l'},
        { name: 'twotheta'},
        { name: 'theta'},
        { name: 'omega'},
        { name: 'chi'},
        { name: 'phi'},
    ] 
    var idealDataStore = new Ext.data.ArrayStore({
        autoDestroy     : false,
        storeId         : 'desiredStore',
        fields          : desiredFields,
        pruneModifiedRecords: true
    });
    idealDataStore.loadData(baseIdealData);
    
    
    // ********* START - Creating Column Models *********
    var numberFieldEditor = new Ext.form.NumberField({
        allowBlank: false,
        allowDecimals: true,
        decimalPrecision: 7
    });
    var textFieldEditor = new Ext.form.TextField({
        maxLength: 11,
    });
    
    //creating the checkbox selection model
    checkBoxRowSelectionModel = function(config) {
        checkBoxRowSelectionModel.superclass.constructor.call(this, config);
    }
    Ext.extend(checkBoxRowSelectionModel , Ext.grid.RowSelectionModel, {
	    initEvents : function(){
            var view = this.grid.view;
            view.on("refresh", this.onRefresh, this);
            view.on("rowupdated", this.onRowUpdated, this);
            view.on("rowremoved", this.onRemove, this);
        }	
    });

    var cm = new Ext.grid.ColumnModel({
        // specify any defaults for each column
        defaults: {
            sortable: false,
            align: 'right',
            width: 60,     
            editor: new Ext.form.NumberField({
                allowBlank: false,
                allowDecimals: true,
                decimalPrecision: 7 
            })
        },
        columns: [
            {
            header: 'h',
            dataIndex: 'h'
            },
        {
            header: 'k',
            dataIndex: 'k'
            },
        {
            header: 'l',
            dataIndex: 'l'
            },
        {
            header: '2θ',
            dataIndex: 'twotheta'
            },
        {
            header: 'θ',
            dataIndex: 'theta'
            },
        {
            header: 'χ',
            dataIndex: 'chi'
            },
        {
            header: 'φ',
            dataIndex: 'phi'
            },
        ]
    });
    
    var cm2 = new Ext.grid.ColumnModel({
        defaults: {
            sortable: false,
            align: 'right',
            width: 65
        },
        columns: [
        {
            header: "",
            dataIndex: 'mycheckbox',
            width: 25,
            renderer: renderCheckBox          
        }, {
            header: 'h',
            dataIndex: 'h',
            width: 55,
            editor: numberFieldEditor
        }, {
            header: 'k',
            dataIndex: 'k',
            width: 55,
            editor: numberFieldEditor
        }, {
            header: 'l',
            dataIndex: 'l',
            width: 55,
            editor: numberFieldEditor
        }, {
            header: '2θ',
            dataIndex: 'twotheta',
            editor: textFieldEditor
        }, {
            header: 'θ',
            dataIndex: 'theta',
            editor: textFieldEditor
        }, {
            header: 'ω',
            dataIndex: 'omega',
            editor: textFieldEditor
        }, {
            header: 'χ',
            dataIndex: 'chi',
            editor: textFieldEditor
        }, {
            header: 'φ',
            dataIndex: 'phi',
            editor: textFieldEditor
        }
        ]
    });
    
    //Setting the calculated angle values to uneditable
    cm2.setEditable(4, false);
    cm2.setEditable(5, false);
    cm2.setEditable(6, false);
    cm2.setEditable(7, false);
    cm2.setEditable(8, false);
    // ********* END - Creating Column Models *********
    
    
    // create the editor grids
    var observationGrid = new Ext.grid.EditorGridPanel({
        store: store,
        cm: cm,
        id              : 'observationEditorGrid',
        width           : 440,
        height          : 187,
        title           : 'Observations',
        frame           : true,
        clicksToEdit    : 1,
        decimalPrecision: 6, //still showing 7 decimal places...
        viewConfig: { 
            forceFit : true
        },
        bbar: [{
            text: 'Add New Row',
            handler: addRowObservation
        }, 
        '-', //Shorthand for Ext.Tollbar.Separator (the " | " between buttons)
        {
            text: 'Calculate 2θ',
            handler: calctwotheta
        },
        '-',
        {
            text: 'Calculate UB',
            handler: submitData
        },
        '-',
        {
            text: 'Refine UB',
            handler: RefineSubmitData
        },
        '-',
        {
            text: 'Evaluate Lattice',
            handler: getLattice
        }]
        
    });
    
    var grid2 = new Ext.grid.EditorGridPanel({
        store: idealDataStore,
        cm: cm2,
        selModel: new checkBoxRowSelectionModel (),
        width: 539,
        height: 200,
        title: 'Desired Results',
        frame: true,
        clicksToEdit: 1,        
        decimalPrecision: 6,
        tbar: [{
            text: 'Add New Row',
            handler: addRow
        }, 
        '-',
        {
            text: 'Remove Selected Rows',
            handler: removeRow
        }, 
        '-',    
        {
            text: '*** CALCULATE RESULTS ***',
            handler: calculateResults
        }]
    });
    
    //create a template for a checkbox 
    var tplCB = new Ext.Template( '<input name="checkbox" type="checkbox" {checked}>');
    tplCB.compile();
	
    function renderCheckBox (v, p, record) {
	    var chk = '';
	    if (grid2.selModel.isIdSelected(v))
	    {
		    chk = 'checked'; 
	    }	
	    return tplCB.applyTemplate({checked: chk});
    }
    
    grid2.on("rowclick", rowClick);

    //If row's checkbox is chcked, highlight (select) the row.
    function rowClick(grid, rowID, event){
	    var x = event.getTarget();
	    if (x.name == "checkbox"){
		    if (x.checked){
			    x.checked = true;
			    grid.selModel.selectRow(rowID, true, false);
			    return false;			
		    }
		    else
		    {
			    x.checked = false;
			    grid.selModel.deselectRow(rowID, false, false);
		    }
	    } 
	    return true;
    }
    
    
    function removeRow(button, event) {
        var i = 0;
        var removed = 0;
        
        while (i < idealDataStore.getCount()){
            
            //if 'row i' in grid2 is selected (highlighted)
            if(grid2.selModel.isSelected(i)){
                idealDataStore.removeAt(i);
                removed = removed +1; //preventing error message of no row selected
            }
            else{
                i = i +1;
            }
        }
        if (removed == 0) {
            Ext.Msg.alert('Error: No row selected');
        }
    };
    
    // ****************** START - Defining grid button functions ****************** 
    function calctwotheta (button, event) { 
        //Calculates and stores the B and UB matricies when the button 'Calculate UB Matrix' is pressed
        params = {'data': [] };
        
        params['data'].push({
            'a': aField.getValue(),
            'b': bField.getValue(),
            'c': cField.getValue(),
            'alpha': alphaField.getValue(),
            'beta': betaField.getValue(),
            'gamma': gammaField.getValue(),
            'wavelength': wavelengthField.getValue()
        });
        
        //only sends the observations that aren't (0,0,0)
        for (var i = 0; i < store.getCount(); i++) {
            var record = store.getAt(i)
            if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){   
                params['data'].push(record.data); 
            }
        };
        
        conn.request({
            url: '/WRed/files/calcTheta/',
            method: 'POST',
            params: Ext.encode(params),
            success: thetasuccess,
            failure: function () {
                Ext.Msg.alert('Error: Failed to calculate 2θ with current lattice parameters');
            }
        });

    };
    
    function thetasuccess (responseObject) {
        twothetas = Ext.decode(responseObject.responseText);

        var c = 0;
        for (var row = 0; row < store.getCount(); row++){
            var record = store.getAt(row);
            if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){   
                record.set('twotheta', twothetas[c]['twotheta']);
                c = c + 1;
            }
        }

        store.commitChanges(); //removes red mark in corner of cell that indicates an uncommited edit
    };
    
    function submitData(button, event) { 
        //Calculates and stores the B and UB matricies when the button 'Calculate UB Matrix' is pressed
        params = {'data': [] };
        
        //only sends the first two row's of observations
        for (var i = 0; i < 2; i++) {
            var record = store.getAt(i)
            params['data'].push(record.data); 
        };
        
        params['data'].push({
            'a': aField.getValue(),
            'b': bField.getValue(),
            'c': cField.getValue(),
            'alpha': alphaField.getValue(),
            'beta': betaField.getValue(),
            'gamma': gammaField.getValue()
        });

        conn.request({
            url: '/WRed/files/calcUBmatrix/',
            method: 'POST',
            params: Ext.encode(params),
            success: ubsuccess,
            failure: function () {
                isUBcalculated = 'no';
                Ext.Msg.alert('Error: Failed to calculate UB matrix');
            }
        });

    };
    
    function RefineSubmitData (button, event) { 
        //Calculates and stores the B and UB matricies when the button 'Refine UB Matrix' is pressed
        params = {'data': [] };

        params['data'].push({
            'wavelength': wavelengthField.getValue()
        });

        for (var i = 0; i < store.getCount(); i++) {
            var record = store.getAt(i)            
            //there will never be a (0,0,0) h,k,l vector so don't push that row
            if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){   
                params['data'].push(record.data); //adding table's input to data to be sent to backend
            }
        };
        
        conn.request({
            url: '/WRed/files/refineUBmatrix/',
            method: 'POST',
            params: Ext.encode(params),
            success: refineubsuccess,
            failure: function () {
                isUBcalculated = 'no';
                Ext.Msg.alert('Error: Failed to calculate UB matrix');
            }
        });
    };
    
    function ubsuccess (responseObject) {
        stringUBmatrix = responseObject.responseText; //Receives UBmatrix as a String w/ elements separated by a ', '
        theUBmatrix = stringUBmatrix.split(', '); //Makes a 1D array of the 9 UBmatrix values, each as a String
        for (i = 0; i < 3 ; i++){
            myUBmatrix[i][0] = parseFloat(theUBmatrix[3*i]); //Converts each String into a Float
            myUBmatrix[i][1] = parseFloat(theUBmatrix[3*i+1]);
            myUBmatrix[i][2] = parseFloat(theUBmatrix[3*i+2]);
        }
        
        //displaying UB matrix values
        UB11Field.setValue(myUBmatrix[0][0]);
        UB12Field.setValue(myUBmatrix[0][1]);
        UB13Field.setValue(myUBmatrix[0][2]);
        UB21Field.setValue(myUBmatrix[1][0]);
        UB22Field.setValue(myUBmatrix[1][1]);
        UB23Field.setValue(myUBmatrix[1][2]);
        UB31Field.setValue(myUBmatrix[2][0]);
        UB32Field.setValue(myUBmatrix[2][1]);
        UB33Field.setValue(myUBmatrix[2][2]);

        isUBcalculated = 'yes';
        store.commitChanges(); //removes red mark in corner of cell that indicates an uncommited edit
    };
    

    function refineubsuccess (responseObject) {
        //TODO may need to add in calculated lattice parameters
    
        stringUBmatrix = responseObject.responseText; //Receives UBmatrix as a String w/ elements separated by a ', '
        theUBmatrix = stringUBmatrix.split(', '); //Makes a 1D array of the 9 UBmatrix values, each as a String

        for (i = 0; i < 3 ; i++){
            myUBmatrix[i][0] = parseFloat(theUBmatrix[3*i]); //Converts each String into a Float
            myUBmatrix[i][1] = parseFloat(theUBmatrix[3*i+1]);
            myUBmatrix[i][2] = parseFloat(theUBmatrix[3*i+2]);
        }
        
        //displaying UB matrix values
        UB11Field.setValue(myUBmatrix[0][0]);
        UB12Field.setValue(myUBmatrix[0][1]);
        UB13Field.setValue(myUBmatrix[0][2]);
        UB21Field.setValue(myUBmatrix[1][0]);
        UB22Field.setValue(myUBmatrix[1][1]);
        UB23Field.setValue(myUBmatrix[1][2]);
        UB31Field.setValue(myUBmatrix[2][0]);
        UB32Field.setValue(myUBmatrix[2][1]);
        UB33Field.setValue(myUBmatrix[2][2]);

        isUBcalculated = 'refined';
        store.commitChanges(); 
    };
    
    
    function calculateResults(button, event) {
        //Calculates the desired angles when the button 'Calculate Results' is pressed
        params = {'data': [] };
        
        //IF the combobox is in the Bisecting Plane mode
        if (myCombo.getValue() == 'Bisecting'){

            //sending back all necessary data to calculate UB and desired angles
            params['data'].push({
                'a'         : aField.getValue(),
                'b'         : bField.getValue(),
                'c'         : cField.getValue(),
                'alpha'     : alphaField.getValue(),
                'beta'      : betaField.getValue(),
                'gamma'     : gammaField.getValue(),
                'wavelength': wavelengthField.getValue(),
                'UBmatrix'  : myUBmatrix
            }); 

            for (var j = 0; j < idealDataStore.getCount(); j++){
                //gets all the data from the Desired Data table except (0,0,0) vectors
                var record = idealDataStore.getAt(j);
                if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){
                    params['data'].push(record.data);
                }
            }  
                
            conn.request({
                url: '/WRed/files/omegaZero/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed calculation for Bisecting mode');
                }
            });
        }
 
        //ELSE IF the combobox is in the Scattering Plane mode
        else if (myCombo.getValue() == 'Scattering Plane'){
            
            //sending back all necessary data to calculate UB and desired angles
            params['data'].push({
                'a'         : aField.getValue(),
                'b'         : bField.getValue(),
                'c'         : cField.getValue(),
                'alpha'     : alphaField.getValue(),
                'beta'      : betaField.getValue(),
                'gamma'     : gammaField.getValue(),
                'h1'        : h1Field.getValue(),
                'k1'        : k1Field.getValue(),
                'l1'        : l1Field.getValue(),
                'wavelength': wavelengthField.getValue(),
                'h2'        : h2Field.getValue(),
                'k2'        : k2Field.getValue(),
                'l2'        : l2Field.getValue(),
                'UBmatrix'  : myUBmatrix
            });

            for (var j = 0; j < idealDataStore.getCount(); j++){
                var record = idealDataStore.getAt(j)
                if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){
                    params['data'].push(record.data);
                }
            }

            conn.request({
                url: '/WRed/files/scatteringPlane/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed calculation for Scattering Plane mode');
                }
            });
        }
        else if (myCombo.getValue() == 'Phi Fixed'){
            
            //sending back all necessary data to calculate UB and desired angles
            params['data'].push({
                'a'         : aField.getValue(),
                'b'         : bField.getValue(),
                'c'         : cField.getValue(),
                'alpha'     : alphaField.getValue(),
                'beta'      : betaField.getValue(),
                'gamma'     : gammaField.getValue(),
                'wavelength': wavelengthField.getValue(),
                'phi'       : phiField.getValue(),
                'UBmatrix'  : myUBmatrix
            });
            
            for (var j = 0; j < idealDataStore.getCount(); j++){
                var record = idealDataStore.getAt(j);
                if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){
                    params['data'].push(record.data);
                }
            }

            conn.request({
                url: '/WRed/files/phiFixed/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed calculation for Phi Fixed mode');
                }
            });
        }
        else {
            Ext.Msg.alert('Error: Please select a valid calculation mode');
        }
    };
    
    function successFunction(responseObject) {
        idealdata = Ext.decode(responseObject.responseText);

        //Updating desired data table
        var counter = 0;
        changes = ['twotheta', 'theta', 'omega', 'chi', 'phi'];
        for (var i = 0; i < idealDataStore.getCount(); i++){
            record = idealDataStore.getAt(i);

            if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){
                //if it's not a (0,0,0) vector, update its calculated angles
                if (idealdata[counter] === 'Error') {
                    //setting up the error message
                    record.set('twotheta', 'Invalid');
                    record.set('theta', 'Vector!');
                    record.set('omega', 'Not in');
                    record.set('chi', 'Scattering');
                    record.set('phi', 'Plane.');
                }
                else{
                    for (var c in changes) {
                        fieldName = changes[c];
                        record.set(fieldName, idealdata[counter][fieldName]);
                    }
                   
                }
                counter = counter+1;
            }
        }
        
        idealDataStore.commitChanges();
    }

    
    function addRowObservation() {
        var input = observationGrid.getStore().recordType;
        var r = new input({
            h: 0.0,
            k: 0.0,
            l: 0.0,
            twotheta: 0.0,
            theta: 0.0,
            omega: 0.0,
            chi: 0.0,
            phi: 0.0
        });
        observationGrid.stopEditing(); 
        store.add(r); //adds new row to the bottom of the table (ie the last row)
        observationGrid.startEditing(store.getCount()-1, 0); //starts editing for first cell of new row
    };
    
    function addRow() {
        var input = grid2.getStore().recordType;
        var r = new input({
            h: 0.0,
            k: 0.0,
            l: 0.0,
            twotheta: 0.0,
            theta: 0.0,
            omega: 0.0,
            chi: 0.0,
            phi: 0.0
        });
        grid2.stopEditing(); 
        idealDataStore.add(r); //adds new row to the bottom of the table (ie the last row)
        grid2.startEditing(idealDataStore.getCount()-1, 0); //starts editing for first cell of new row
    };
    
    //TODO COME HERE
    
    
    function getLattice() {
        //With a calculated UB matrix, the lattice parameters can be calculated
        
        params = {'UBmatrix': myUBmatrix};

        conn.request({
            url: '/WRed/files/latticeParameters/',
            method: 'POST',
            params: Ext.encode(params),
            success: displayLattice,
            failure: function () {
                Ext.Msg.alert('Error: Could not calculate the lattice parameters from the UB matrix');
            }
        });
    };
    
    function displayLattice (responseObject){
        lattice = Ext.decode(responseObject.responseText);
        
        aField.setValue(lattice['a']);
        bField.setValue(lattice['b']);
        cField.setValue(lattice['c']);
        alphaField.setValue(lattice['alpha']);
        betaField.setValue(lattice['beta']);
        gammaField.setValue(lattice['gamma']);
    }
    
    // ****************** END - Defining grid button functions ****************** 
   

    // ********* START - Setting up lattice constants GUI  ********* 
    var topFieldset = {
        xtype       : 'fieldset',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '115%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items   : [
                            aField
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            bField                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            cField                               
                        ]
                    }, {
                        //Buffer blank space to even out the c inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items   : [
                            alphaField
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            betaField                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            gammaField                               
                        ]
                    }, {
                        //Buffer blank space to even out the gamma inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            wavelengthField,
        ]
    };
    // ********* END - Setting up lattice constants GUI  ********* 

    
    // ********* START - Setting up scattering plane h/k/l GUI  ********* 
    var ScatteringFieldset = {
        xtype       : 'fieldset',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items   : [
                            h1Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            k1Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            l1Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the l1 inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items   : [
                            h2Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            k2Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            l2Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the l2 inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                //empty container to allow horizontal inputboxes for h,k,l
                xtype       : 'container',
                border      : false,
                width       : 230
            } 
        ]
    };
    
    // ********* END - Setting up scattering plane h/k/l GUI  ********* 
    
    // ********* START - Setting up phi fixed GUI  ********* 
    var PhiFixedFieldset = {
        xtype       : 'fieldset',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 250,
                        labelWidth  : 80,
                        items   : [
                            phiField
                        ]
                    },
                    {
                        //Buffer blank space to even out the phi inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            }
        ]
    };
    
    // ********* END - Setting up phi fixed GUI  ********* 
    
    
    // ********* START - Setting up calculated UB matrix GUI  ********* 
    var UBFieldset = {
        xtype       : 'fieldset',
        title       : 'UB Matrix',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : true,
            decimalPrecision: 7
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items   : [
                            UB11Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB12Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB13Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the first row of numberfields
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items   : [
                             UB21Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB22Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB23Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the second row of numberfields
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items   : [
                             UB31Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB32Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB33Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the third row of numberfields
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                //empty container to allow a 3x3 arrangement of numberfields for the UB matrix
                xtype       : 'container',
                border      : false,
                width       : 230
            }
        ]
    };
    
    // ********* END - Setting up calculated UB matrix GUI  ********* 
    
    // ********* START - Handling loading and saving data  ********* 
    
    var uploadPanel = new Ext.FormPanel({
        fileUpload: true,
        frame: true,
        title: 'Upload A Data File',
        autoHeight: true,
        bodyStyle: 'padding: 0 10px 5px 10px;',
        labelWidth: 30,
        items: [{
            xtype       : 'fileuploadfield',
            anchor      : '100%',
            id          : 'inputfile',
            emptyText   : 'Select a file...',
            fieldLabel  : 'File',
            name        : 'file',
            buttonText  : 'Browse...'
        }],
        buttons: [{
            text: 'Save & Download Data', //Save & Download Data button
            icon: '/media/icons/silk/disk.png', //graphic that accompanies the button
            handler: saveFunction
        }, {
            text: 'Load Data',  //Load Data button
            icon: '/media/icons/silk/add.png',
            handler: function (){
                if (uploadPanel.getForm().isValid()) {
                    uploadPanel.getForm().submit({
                        url: '/WRed/files/uploadingData/',
                        waitMsg: 'Uploading data...',
                        method: 'POST',
                        success: uploadFunction,
                        failure: function() {
                            Ext.Msg.alert('Error: Could not upload data.');
                        }
                    })
                }
                else {
                    Ext.Msg.alert('Error: Could not upload data.');
                }
            }
        }]
    });
    
    function saveFunction() {
        //Writes data to a textfile for user to download
        
        params = {'data': [] };

        params['data'].push({
            'h1'        : h1Field.getValue(), //h, k, ls are the scattering plane vectors
            'k1'        : k1Field.getValue(),
            'l1'        : l1Field.getValue(),
            'wavelength': wavelengthField.getValue(),
            'h2'        : h2Field.getValue(),
            'k2'        : k2Field.getValue(),
            'l2'        : l2Field.getValue(),        
            'a'         : aField.getValue(),
            'b'         : bField.getValue(),
            'c'         : cField.getValue(),
            'alpha'     : alphaField.getValue(),
            'beta'      : betaField.getValue(),
            'gamma'     : gammaField.getValue(),
            'mode'      : myCombo.getValue(),
            'numrows'   : store.getCount(),
            'ub'        : myUBmatrix,
            'phi'       : phiField.getValue(),
            'isUBcalculated': isUBcalculated
        });
        for (var i = 0; i < store.getCount(); i++) { //all the observation table's data 
            var record1 = store.getAt(i)
            params['data'].push(record1.data); 
        }; 
        for (var j = 0; j < idealDataStore.getCount(); j++){ //all the desired results table's data
            var record2 = idealDataStore.getAt(j)
            params['data'].push(record2.data);
        }  
            
        conn.request({
            url: '/WRed/files/savingData/',
            method: 'POST', 
            params: Ext.encode(params),
            success: function (){
                window.open('/WRed/files/downloadingData/'); //opens dialogue box window
            },
            failure: function () {
                Ext.Msg.alert('Error: Could not save');
            }
        });
        
    };
    
    
    
    function uploadFunction (formPanel, uploadObject) {
        responseJSON = Ext.decode(uploadObject.response.responseText);
        data = responseJSON['data']['array'];
        
        if (data[0] == null){
            Ext.Msg.alert('Error: Please select a file.');
        }
        else{
            //uploading lattice constants data
            aField.setValue(data[0]['a']);
            bField.setValue(data[0]['b']);
            cField.setValue(data[0]['c']);
            alphaField.setValue(data[0]['alpha']);
            betaField.setValue(data[0]['beta']);
            gammaField.setValue(data[0]['gamma']);
            wavelengthField.setValue(data[0]['wavelength']);
            
            //uploading comboBox (mode) information
            myCombo.setValue(data[0]['mode']);
            valueObject = {'data': {'mode': data[0]['mode']}};
            comboFunction(myCombo, valueObject);
            
            //uploading scattering plane vectors
            h1Field.setValue(data[0]['h1']);
            k1Field.setValue(data[0]['k1']);
            l1Field.setValue(data[0]['l1']);
            h2Field.setValue(data[0]['h2']);
            k2Field.setValue(data[0]['k2']);
            l2Field.setValue(data[0]['l2']);
            
            //uploading fixed phi value
            phiField.setValue(data[0]['phi']);
            
            //uploading observation data and ideal data
            newData = [];
            newIdealData = [];
            for (i = 1; i < data.length; i++){
                if (data[i]['omega'] == null){ //omega = null if it's observation data
                    tempData = [data[i]['h'], data[i]['k'], data[i]['l'], data[i]['twotheta'], data[i]['theta'], data[i]['chi'], data[i]['phi']];
                    
                    newData.push(tempData);
                }
                else {
                    tempIdealData = [data[i]['h'], data[i]['k'], data[i]['l'], data[i]['twotheta'], data[i]['theta'], data[i]['omega'], data[i]['chi'], data[i]['phi']];
                    
                    newIdealData.push(tempIdealData);
                }
            }
                
            store.loadData(newData);
            idealDataStore.loadData(newIdealData);
            
            isUBcalculated = data[0]['isUBcalculated'];
            theUBmatrix = data[0]['UBmatrix'];
            for (i = 0; i < 3 ; i++){
                myUBmatrix[i][0] = parseFloat(theUBmatrix[3*i]); //Converts each String into a Float
                myUBmatrix[i][1] = parseFloat(theUBmatrix[3*i+1]);
                myUBmatrix[i][2] = parseFloat(theUBmatrix[3*i+2]);
            }
            
            //displaying UB matrix values
            UB11Field.setValue(myUBmatrix[0][0]);
            UB12Field.setValue(myUBmatrix[0][1]);
            UB13Field.setValue(myUBmatrix[0][2]);
            UB21Field.setValue(myUBmatrix[1][0]);
            UB22Field.setValue(myUBmatrix[1][1]);
            UB23Field.setValue(myUBmatrix[1][2]);
            UB31Field.setValue(myUBmatrix[2][0]);
            UB32Field.setValue(myUBmatrix[2][1]);
            UB33Field.setValue(myUBmatrix[2][2]);
                
        }
    };


    // ********* END - Handling loading and saving data  *********  
    
    // ************** Setting up the ComboBox ************** 
    var myComboStore = new Ext.data.ArrayStore({
        data: [[1, 'Bisecting'], [2, 'Scattering Plane'], [3, 'Phi Fixed']],
        fields: ['id', 'mode'],
        idIndex: 0
    });
    
    var myCombo = new Ext.form.ComboBox ({
        fieldLabel  : 'Select a Mode',
        store       : myComboStore,
        
        displayField: 'mode',
        typeAhead   : true,
        mode        : 'local',
        
        triggerAction:  'all', //Lets you see all drop down options when arrow is clicked
        selectOnFocus:  true,
        value        : 'Bisecting',
        
        listeners: {
            select: {
                fn: comboFunction
            }
        }
    });
    
    function comboFunction (combo, value) {
        //The comboBox gave a nasty object for value, hence the value['data']['mode']
        if (value['data']['mode'] == 'Bisecting'){
            //If switching to 'Bisecting' mode, removes special input boxes from other modes
            
            southPanel.removeAll(false); //sets auto-Destroy to false
            southPanel.setHeight(0);
            southPanel.add(ScatteringFieldset);

            southPanel.setTitle('No Mode-specific Inputs for Bisecting Mode');
            southPanel.doLayout(); //for already rendered panels, refreshes the layout
            
            innerRightTopPanel.doLayout();
        }
        else if (value['data']['mode'] == 'Scattering Plane'){
            //If switching to 'Scattering Plane' mode, removes other special input boxes from modes
            //and adds the scattering plane vectors input boxes
            
            southPanel.removeAll(false);
            southPanel.setHeight(91);
            southPanel.add(ScatteringFieldset);

            southPanel.setTitle('Scattering Plane Vectors');
            southPanel.doLayout();
            
            innerRightTopPanel.doLayout();
        }
        else if (value['data']['mode'] == 'Phi Fixed'){
            //If switching to 'Phi Fixed' mode, removes other special input boxes from modes
            //and adds the phi fixed value input box
            
            southPanel.removeAll(false);
            southPanel.setHeight(70);
            southPanel.add(PhiFixedFieldset);

            southPanel.setTitle('Fixed Phi Value');
            southPanel.doLayout();
            
            innerRightTopPanel.doLayout();
        }
        else{
            //Does nothing...
            //Ext.Msg.alert('Error: Could not save');
        }
    };

    
    //Setting up and rendering Panels 
    var southPanel = new Ext.Panel ({
        title   : 'No Mode-specific Inputs for Bisecting Mode',
        region  : 'south',
        margins : '0 5 0 0',
        height  : 0,
        id      : 'south-container'
    });
    
    var northPanel = new Ext.Panel ({
        region      : 'north',
        height      : 100,
        items       : [uploadPanel]
    });
    
    var innerLeftTopPanel = new Ext.Panel({
        layout: 'border',
        width: 440,
        height: 290, 
        items: [{
            region: 'center',
            items: [observationGrid]
        }, 
            northPanel,
        ]
    });

    var innerRightTopPanel = new Ext.Panel({
        layout: 'border',
        width: 350,
        height: 290,
        border: true,
        items: [{
            title   : 'Lattice Parameters',
            region  : 'center',
            id      : 'center-component',
            layout  : 'fit',
            margins : '0 5 0 0', //small margins to the east of box
            items   : [topFieldset]
        }, {
            title   : 'Choose the Mode',
            region  : 'north',
            height  : 50,
            margins : '0 5 0 0',
            items   : [myCombo]
        }, 
        southPanel
        ]
    });  

    var TopPanel = new Ext.Panel({
        layout: 'table',
        width: 790,
        layoutConfig: {
            columns: 2
        },
        items: [innerLeftTopPanel, innerRightTopPanel]
    });

    var BottomPanel = new Ext.Panel({
        layout: 'table',
        width: 790,
        layoutConfig: {
            columns: 2
        },
        items: [UBFieldset, grid2]
    });
    
// ************************** START - Setting up the tabs  **************************

    var myTabs = new Ext.TabPanel({
        resizeTabs: true, // turn on tab resizing
        minTabWidth: 115,
        tabWidth: 135,
        enableTabScroll: true,
        width: 793,
        height: 524,
        activeItem: 'calcTab', //Making the calculator tab selected first
        defaults: {autoScroll:true},
        items: [
            {
                title: 'UB Calculator',
                id: 'calcTab',
                iconCls: '/media/icons/silk/calculator.png',
                items: [TopPanel, BottomPanel]
            }, {
                title: 'Help Manual',
                id: 'helpManualTab',
                padding: 5,
                iconCls: '/media/icons/silk/help.png',    
                html: '<br/><h1>' +
                    'UB Matrix Calculator for 3- and 4-circle Neutron and X-ray Diffractometers' + '</h1> <br/><br/> <h3>' +
                    'Performing Calculations' + '</h3> <br/> <P>' +
                    '&nbsp; **Note: if you need an additional row for a table, click on its "Add New Row" button.' + '<br/><br/>' + 
                    '1) Enter in your observed reflections in the Observations table. For help observing reflections:' + '<br/>' +
                    '&nbsp;&nbsp; a) Input the lattice parameters' + '<br/>' +
                    '&nbsp;&nbsp; b) Input the (h, k, l) indices in the Observations table' + '<br/>' +
                    '&nbsp;&nbsp; c) Click on "Calculate 2θ" to compute the 2θ values for those indices' + '<br/><br/>' +
                    '2) If you only have two observations:' + '<br/>' +
                    '&nbsp;&nbsp; a) Input the lattice parameters (if not already entered)' + '<br/>' +
                    '&nbsp;&nbsp; b) Click the "Calculate UB" to calculate the UB matrix' + '<br/><br/>' +
                    '3) If you have more than two observations:' + '<br/>' +
                    '&nbsp;&nbsp; a) Click on "Refine UB" to calculate the refined UB matrix' + '<br/>' +
                    '&nbsp;&nbsp; b) Click on "Evaluate Lattice" to compute the lattice parameters' + '<br/><br/>' +
                    '4) Input the (h, k, l) indices of the reflections that you want calculated in Desired Results table' + '<br/>' +
                    '5) Select the mode for your calculation from the drop-down menu. To obtain a solution, one of the following must be selected:' + '<br/>' + 
                    '&nbsp;&nbsp; a) Bisecting (Omega=0)' + '<br/>' + 
                    '&nbsp;&nbsp; b) Phi Fixed' + '<br/>' +
                    '&nbsp;&nbsp; c) Scattering Plane' + '<br/><br/>' +
                    '6) Depending on your mode selection, additional input may be required' + '<br/>' +
                    '7) If you selected Phi Fixed mode, input the fixed phi value' + '<br/>' +
                    '8) If you selected Scattering Plane mode, enter the (h, k, l) indices for the two vectors that define the Scattering Plane' + '<br/>' +
                    '9) Click on the "*** Calculate Results ***" button to calculate the angles for the desired indices' + '<br/>' +
                    '10) You may change values and repeat the calculations as frequently as desired' + '<br/><br/><br/> </P> <h3>' +
                    
                    'Saving Data' + '</h3> <br/> <P>' +
                    'To save your data, you must download a textfile of your data by clicking the "Save & Download Data" button. This file will be downloaded to your designated download directory, or will prompt you for a download location, depending on browser settings.' + '<br/><br/>' +
                    'WARNING: Editing the saved file may result in a loss of data or failure to upload. See "Alternate Saving/Loading Usage" for more details.' + '<br/><br/><br/> </P> <h3>' +
                    
                    'Loading Data' + '</h3> <br/> <P>' +
                    '1) Click the "Browse" button' + '<br/>' +
                    '2) Select your data textfile' + '<br/>' + 
                    '3) Click the "Load Data" button' + '<br/><br/><br/></P> <h3>' +
                    
                    'Alternate Saving/Loading Usage' + '</h3> <br/> <P>' +
                    'Due to the nature of the loading and saving mechanisms, data may be entered by directly editing a textfile and loading it into the program (loading instructions above). There are 9 essential lines of text that must be located within your file for it to load. 7 are data headers, telling the order to put the data in, which are immediately followed by the appropriate data, separated by commas, on the following line(s). If you have no data for a specific header, leave the subsequent line blank. These headers are (without the quotes):' + '<br/>' + 
                    '&nbsp;&nbsp; "#Mode"' + '<br/>' + 
                    '&nbsp;&nbsp; "#a b c alpha beta gamma wavelength"' + '<br/>' + 
                    '&nbsp;&nbsp; "#Observations h k l twotheta theta chi phi"' + '<br/>' + 
                    '&nbsp;&nbsp; "#Scattering Plane Vectors h k l"' + '<br/>' + 
                    '&nbsp;&nbsp; "#Fixed Phi Value"' + '<br/>' + 
                    '&nbsp;&nbsp; "#Desired h k l twotheta theta omega chi phi"' + '<br/>' + 
                    '&nbsp;&nbsp; "#UBmatrix"' + '<br/><br/>' + 
                    'Uniquely, the line following "#UBmatrix" should be one of three options:' + '<br/>' +
                    '&nbsp;&nbsp; "no" --------- UBmatrix is not calculated.' + '<br/>' + 
                    '&nbsp;&nbsp; "yes" -------- UB matrix is calculated. Its 9 values should be on the next line.' + '<br/>' + 
                    '&nbsp;&nbsp; "refined" -- UB matrix is refined. Its 9 values should be on the next line.' + '<br/><br/>' + 
                    'Furthermore, there is no limit to the amount of observaitons or desired results data. Consequently, they require an ending statement that immediately follows the last line of observations or desired results. These final 2 essential lines are:' + '<br/>' +  
                    '&nbsp;&nbsp; "#End observations"' + '<br/>' + 
                    '&nbsp;&nbsp; "#End desired"' + '<br/><br/>' +
                    'For example, a data textfile may look like this (shown in blue below). Note that header ordering and spaces are optional:' + '<br/><br/> </P> <P style="color:blue">' +
                    //START OF FILE  
                    '#Mode' + '<br/>' + 
                    'Scattering Plane' + '<br/><br/>' + 
                     
                    '#a b c alpha beta gamma wavelength' + '<br/>' + 
                    '3.9091056,3.9091018,3.9091019,89.9999575,90.0001171,90.0000603,2.35916' + '<br/><br/>' + 
                     
                    '#Observations h k l twotheta theta chi phi' + '<br/>' + 
                    '1,1,0,50.522,25.261,88.1065,78.428' + '<br/>' + 
                    '0,0,1,35.1257,17.5628,-178.8505,-48.94' + '<br/>' + 
                    '0,1,0,35.1257,17.5628,43.4843,42.1502' + '<br/>' + 
                    '1,0,0,35.1257,17.5628,133.5075,39.8488' + '<br/>' + 
                    '1,1,1,63.0205,31.5102,126.441,-51.0087' + '<br/>' + 
                    '2,1,1,95.3162,47.658,120.124,-16.956' + '<br/>' + 
                    '#End observations' + '<br/><br/>' + 
                     
                    '#UBmatrix' + '<br/>' + 
                    'refined ' + '<br/>' + 
                    '-0.135209723313,0.13760748667,-0.16799695155,-0.112847227161,0.124557757337,0.192849947079,0.18553738062,0.176039655796,-0.00513161157565'+ '<br/><br/>' + 
                     
                    '#Scattering Plane Vectors h k l' + '<br/>' + 
                    '1,0,0' + '<br/>' + 
                    '0,1,1' + '<br/><br/>' + 
                     
                    '#Fixed Phi Value' + '<br/>' + 
                    '236' + '<br/><br/>' + 
                     
                    '#Desired h k l twotheta theta omega chi phi' + '<br/>' + 
                    '1,1,-1,Invalid,Vector!,Not in,Scattering,Plane.' + '<br/>' + 
                    '1,1,1,63.0204001841,53.1674731954,21.6572731033,120.051971519,-12.5966659616' + '<br/>' + 
                    '1,1,2,0,0,0,0,0' + '<br/>' + 
                    '#End desired' + '<br/><br/></P>' +
                    //END OF FILE
                    'In terms of usability, the desired h,k,l may be input with 0 for their angle values (as shown in the last line of the desired input). These angles can then be computed by loading in your data file and using the calculator.' 
                            
            }
        ]
    });

// ************************** END - Setting up the tabs  **************************
    
    myTabs.render('tabs');
    
});
