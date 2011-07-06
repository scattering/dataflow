function MakeFileUpload() {
Ext.create('Ext.form.Panel', {
    title: 'Upload a File',
    width: 400,
    bodyPadding: 10,
    frame: true,
    renderTo: Ext.getBody(),    
    items: [{
        xtype: 'filefield',
        name: 'file',
        fieldLabel: 'File',
        labelWidth: 50,
        msgTarget: 'side',
        allowBlank: false,
        anchor: '100%',
        buttonText: 'Select File...'
    }],

    buttons: [{
        text: 'Upload',
        handler: function() {
            var form = this.up('form').getForm();
            if(form.isValid()){
                form.submit({
                    url: 'UploadNCNRFile',
                    waitMsg: 'Uploading your file...',
                    success: function(fp, o) {
                        Ext.Msg.alert('Success', 'Your photo "' + o.result.file + '" has been uploaded.');
                    }
                });
            }
        }
    }]
});
};

Ext.onReady(MakeFileUpload)
