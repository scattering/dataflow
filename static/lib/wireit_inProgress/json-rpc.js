/**
 * JsonRpc Adapter (using ajax)
 * @class WireIt.WiringEditor.adapters.JsonRpc
 * @static 
 */
WireIt.WiringEditor.adapters.JsonRpc = {
	
	config: {
		url: '../../backend/php/WiringEditor.php'
	},
	
	init: function() {
		YAHOO.util.Connect.setDefaultPostHeader('application/json');
	},
	
	saveWiring: function(val, callbacks) {
		
		// Make a copy of the object
		var wiring = {};
		YAHOO.lang.augmentObject(wiring, val);
		
		// Encode the working field as a JSON string
		wiring.working = YAHOO.lang.JSON.stringify(wiring.working);
		
		this._sendJsonRpcRequest("saveWiring", wiring, callbacks);
	},
	
	deleteWiring: function(val, callbacks) {
		this._sendJsonRpcRequest("deleteWiring", val, callbacks);
	},
	
	listWirings: function(val, callbacks) {
		this._sendJsonRpcRequest("listWirings", val, callbacks);
	},
	
	// private method to send a json-rpc request using ajax
	_sendJsonRpcRequest: function(method, value, callbacks) {
		var postData = YAHOO.lang.JSON.stringify({"id":(this._requestId++),"method":method,"params":value,"version":"json-rpc-2.0"});

	console.log('listWirings');
                rstring={"wires": [{"src": {"terminal": "output", "moduleId": 0}, "tgt": {"terminal": "input", "moduleId": 1}}, {"src": {"terminal": "output", "moduleId": 1}, "tgt": {"terminal": "input", "moduleId": 2}}, {"src": {"terminal": "output", "moduleId": 2}, "tgt": {"terminal": "input", "moduleId": 3}}], "modules": [{"terminals": "", "config": {"position": [5, 20], "xtype": "WireIt.Container"}, "name": "Load", "value": {}}, {"terminals": {"input": [-15, 1, -1, 0], "output": [15, 1, 1, 0]}, "config": {"position": [160, 20], "xtype": "WireIt.ImageContainer"}, "name": "Join", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [280, 40], "xtype": "WireIt.ImageContainer"}, "name": "Scale", "value": {}}, {"terminals": "", "config": {"position": [340, 40], "xtype": "WireIt.Container"}, "name": "Save", "value": {}}], "properties": {"name": "test tas", "description": "example TAS diagram"}};
                rjason=YAHOO.lang.JSON.stringify(rstring);
                rjason=YAHOO.lang.JSON.parse(rjason);
                callbacks.success.call(callbacks.scope,[rjason]);
/*
		YAHOO.util.Connect.asyncRequest('POST', this.config.url, {
			success: function(o) {
				var s = o.responseText,
					 r = YAHOO.lang.JSON.parse(s);
					
				var wirings = r.result;
				
				for(var i = 0 ; i < wirings.length ; i++) {
					wirings[i].working = YAHOO.lang.JSON.parse(wirings[i].working);
				}
					
			 	callbacks.success.call(callbacks.scope, r.result);
			},
			failure: function() {
				callbacks.failure.call(callbacks.scope, r);
			}
		},postData);*/
	},
	_requestId: 1
};
