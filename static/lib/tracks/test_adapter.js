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
		    url: 'getCSV/'
		},
		
		filesExist: {
		    method: 'POST', 
		    url: '/filesExist/'
		},
		
		saveData: {
		    method: 'POST', 
		    url: 'saveData/'
		}
		
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
	
	saveData: function(val, callbacks) {
	    var wiring = {};
	    var callbacks = callbacks || { 
	        success: function(o) { console.log('success', o ); },
	        failure: function(o) { console.log('failure', o ); },
	        };
	    YAHOO.lang.augmentObject(wiring, val);
	    this._sendRequest("saveData", wiring, callbacks);
	},
	
	getBinaryData: function(unfilled_data, onFinish) {
        var oReq = new XMLHttpRequest(); 
        //oReq.open("GET", "/getBinaryData/"+val, true); 
        oReq.open("POST", "/getBinaryData/", true);   
        oReq.responseType = "arraybuffer";
        //oReq.multipart = true;
        oReq.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        oReq.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        oReq.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        
        oReq.onload = function (oEvent) {
            if (oReq.status == 200) {
            var arrayBuffer = oReq.response;
            console.log('binary received');
            if (arrayBuffer) {  
                var byteArray = new Float32Array(arrayBuffer);
                unfilled_data.z_binary_array = byteArray;
                var z = [[]];
                var row;
                var width = unfilled_data.dims.xdim;
                var height = unfilled_data.dims.ydim;
                for (var r=0; r<height; r++) {
                    var row = [];
                    for (var c=0; c<width; c++) {
                        row.push(byteArray[c + r*width]);
                    }
                    z[0].push(row); 
                }
                
                unfilled_data.z = z;
                console.log('binary received and processed', byteArray.length); 
                onFinish();
                
            }  
        }
        }
        console.log('getting binary...', unfilled_data.binary_fp);
        oReq.send("binary_fp="+unfilled_data.binary_fp);
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
                var r = ""; //7/31/12, r was not being set always, causing errors. I think r="" will be ok.
                 // CHANGED (7/5/11), JSON parsing was not working
                try { r = YAHOO.lang.JSON.parse(s) }
                catch(ex) { console.log('parse error in test_adapter:', ex); }
                //r = eval('(function() { return ' + s + '; })()');
                callbacks.success.call(callbacks.scope, r);
            },
            failure: function(o) {
                var s = o.responseText;
                //         // CHANGED (7/5/11), JSON parsing was not working
                var errorStr = o.status + " " + o.statusText;
                try { 
                    r = YAHOO.lang.JSON.parse(s);
                    errorStr = r.errorStr;
                } 
                catch(ex) {}

                callbacks.failure.call(callbacks.scope, errorStr);
            }
        }, postData); 
    }
	
};
