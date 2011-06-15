/**
 * JsonRpc Adapter (using ajax)
 * @static 
 */
WireIt.WiringEditor.adapters.JsonRpc = {
	
	config: {
		url: 'WiringEditor.php'
	},
	
	init: function() {
		YAHOO.util.Connect.setDefaultPostHeader('application/json');
	},
	
	saveWiring: function(val, callbacks) {
		this._sendJsonRpcRequest("saveWiring", val, callbacks);
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
		/* This request causes an error. We need a server.*/
		YAHOO.util.Connect.asyncRequest('POST', this.config.url, {
			success: function(o) {
				var s = o.responseText,
					 r = YAHOO.lang.JSON.parse(s);
			 	callbacks.success.call(callbacks.scope, r.result);
			},
			failure: function(o) {
				var error = o.status + " " + o.statusText;
				callbacks.failure.call(callbacks.scope, error);
				console.log('Fail')
			}
		},postData);
	},
	_requestId: 1
};
