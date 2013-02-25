//Webworker that handles loading the files and metadata
//Currently set up to handle TripleAxis objects only
self.addEventListener('message', function(e){
    var input = document.getElementById('new_files');
    input.disabled = false;
    var progress_div = document.getElementById('progress_div');
    
    check_existence = function(files) {
        var filehashes = [];
        var hash_lookup = {};
        num_files = files.length;
        function add_filehash(filename, result, filehashes, num_files) {
            var filehash = SHA1(result);
            hash_lookup[filename] = filehash;
            var new_length = filehashes.push(filehash);
            
            self.postMessage(filehashes, hash_lookup);
            //console.log(filehashes, hash_lookup);
           
         if (new_length >= num_files) {
                test_adapter.filesExist(filehashes);
            }
            return
        }
            
        for (var i=0; i<files.length; i++) {
            var reader = new FileReader();
            reader.onload = (function(theFile) {
                return function(e) {
                    add_filehash(theFile.name, e.target.result, filehashes, num_files)
                };
            })(files[i]);
            reader.readAsBinaryString(files[i]);
        }
    };
    
    checkAll = function(formname, checked) {
        if (checked == undefined) var checked = true;
        items = document.getElementsByName(formname);
        for (var i in items) {
            items[i].checked = checked;
        };
    };
    
    input.addEventListener("change", function(){
        
        // disable the input
        input.setAttribute("disabled", "true");
        
        progress_div.innerHTML="";
        progress_bars = {};
        for (var i=0; i<input.files.length; i++) {
            var new_div = progress_div.appendChild(document.createElement("div"));
            new_div.textContent = input.files[i].name;
            var new_bar = new_div.appendChild(document.createElement("progress"));
            new_bar.value = 0;
            new_bar.max = input.files[i].size;
            progress_bars[input.files[i].name] = new_bar;
        }
        
        sendMultipleFiles({
            url: '/uploadFiles/',
            // list of files to upload
            files:input.files,
            
            extra_data: {"experiment_id": experiment_id},
            
            csrf_token: getCookie('csrftoken'),
            
            // clear the container 
            onloadstart:function(){
            },
            
            // do something during upload ...
            onprogress:function(rpe, xhr){
                var fn = this.file.name;
                progress_bars[fn].value = rpe.loaded;
            },
            
            // fired when last file has been uploaded
            onload:function(rpe, xhr){
                // enable the input again
                input.removeAttribute("disabled");
                // reload the page without reposting any data:
                window.location.href = window.location.pathname;
                
                // this would reload the window, but includes last POST data:
                //window.location.reload();
            },
            
            // if something is wrong ... (from native instance or because of size)
            onerror:function(){
                var fn = this.file.name;
                progress_bars[fn].textContent = "The file " + fn + " is too big [" + size(this.file.size) + "]";
                
                // enable the input again
                input.removeAttribute("disabled");
            }
        });
    }, false);

    self.postMessage('end of loadwebworker.js code');

        /*
    var conn = new Ext.data.Connection();
        conn.request({
            url: '/loadwebworker/',
            method: 'GET',
            params: {},
            success: function(responseObject) {
                dataArray = Ext.decode(responseObject.responseText);//decodes the response
            },
            failure: function() {
            }
        });

    }
    self.postMessage('TODO msg from worker');
    */
}, false);
