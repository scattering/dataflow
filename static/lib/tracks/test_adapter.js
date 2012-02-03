// test adapter, JSON

function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                // remove whitespace from beginning and end: (like jQuery.trim)
                var cookie = cookies[i].replace(/(^[\s\xA0]+|[\s\xA0]+$)/g, '');
                //var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


test_adapter = {
//WireIt.WiringEditor.adapters.tracks = {
	
	/**
	 * You can configure this adapter to different schemas.
	 * url can be functions !
	 */
	config: {
		listWirings: {
			method: 'POST',
			url: 'listWirings/'
		},

		saveWiring: {
			method: 'POST',
			url: 'saveWiring/'
		},
		
		runReduction: {
			method: 'POST',
			url: 'runReduction/'
		},
		
		getCSV: {
		    method: 'POST',
		    url: 'getCSV/',
		},
		
		filesExist: {
		    method: 'POST', 
		    url: '/filesExist/',
		}, 
	},
	
	init: function() {
		YAHOO.util.Connect.setDefaultPostHeader('application/json');
	},
	
	listWirings: function(val, callbacks) {
		this._sendRequest("listWirings", val, callbacks);
	},
	
	saveWiring: function(val, callbacks) {
		//var wiring = {};
		//YAHOO.lang.augmentObject(wiring, val);	
		this._sendRequest("saveWiring", val, callbacks);
	},
	
	runReduction: function(val, callbacks) {
		var wiring = {};
		YAHOO.lang.augmentObject(wiring, val);
		this._sendRequest("runReduction", wiring, callbacks);
	},
	
	getCSV: function(val) {
		var wiring = {};
		YAHOO.lang.augmentObject(wiring, val);
		var postData = 'data=' + YAHOO.lang.JSON.stringify(val);
		var download_form = document.getElementById('getCSVForm');
		download_form.data.value = YAHOO.lang.JSON.stringify(val);
		download_form.submit()
	},
	
	filesExist: function(filehashes, callbacks) {
	    var callbacks = callbacks || { 
	        success: function(o) { console.log('success', o ); },
	        failure: function(o) { console.log('failure', o ); },
	        };
	    this._sendRequest("filesExist", {filehashes:filehashes}, callbacks);
	},	
	
	_downloadRequest: function(action, value, callbacks) {
	    var postData = 'data=' + YAHOO.lang.JSON.stringify(value);
		
		var url = "";
		if( YAHOO.lang.isFunction(this.config[action].url) ) {
			url = this.config[action].url(value);
		}
		else {
			url = this.config[action].url;
		}
		var method = "";
		if( YAHOO.lang.isFunction(this.config[action].url) ) {
			method = this.config[action].method(value);
		}
		else {
			method = this.config[action].method;
		}
		var download_form = document.getElementById('getCSVForm');
		download_form.data.value = YAHOO.lang.JSON.stringify(value);
		download_form.submit()
        //YAHOO.util.Connect.initHeader('X-CSRFToken', getCookie('csrftoken'));
		//YAHOO.util.Connect.asyncRequest(method, url, {}, postData);
	},
	
	_sendRequest: function(action, value, callbacks) {
		//value = {"hey":["++","+-"]}
		/**
		var params = [];
		for(var key in value) {
			if(value.hasOwnProperty(key)) {
				// edited 6/22, now stringifies value
				params.push(window.encodeURIComponent(key) +"="+window.encodeURIComponent(value[key]));							
			}
		}
		var postData = params.join('&');
		**/
		
		var postData = 'data=' + encodeURIComponent(YAHOO.lang.JSON.stringify(value));
		
		var url = "";
		if( YAHOO.lang.isFunction(this.config[action].url) ) {
			url = this.config[action].url(value);
		}
		else {
			url = this.config[action].url;
		}
		var method = "";
		if( YAHOO.lang.isFunction(this.config[action].url) ) {
			method = this.config[action].method(value);
		}
		else {
			method = this.config[action].method;
		}
        YAHOO.util.Connect.initHeader('X-CSRFToken', getCookie('csrftoken'));
        YAHOO.util.Connect.asyncRequest(method, url, {
			success: function(o) {
				var s = o.responseText;
				         // CHANGED (7/5/11), JSON parsing was not working
					 try { r = YAHOO.lang.JSON.parse(s) }
					 catch(ex) { console.log('parse error in test_adapter:', ex); }
					 //r = eval('(function() { return ' + s + '; })()');
			 	callbacks.success.call(callbacks.scope, r);
			},
			failure: function(o) {
			    //var s = o.responseText;
				//         // CHANGED (7/5/11), JSON parsing was not working
				//	 r = YAHOO.lang.JSON.parse(s)
				var error = o.status + " " + o.statusText;
				callbacks.failure.call(callbacks.scope, error);
			}
		}, postData); 
	}
	
};
