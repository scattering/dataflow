//Webworker that handles loading the files and metadata
//Currently set up to handle TripleAxis objects only
self.addEventListener('message', function(e){

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
            self.close() //closes webworker

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
