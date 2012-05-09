/**
 * jqplot.jquerymobile plugin
 * jQuery Mobile device touch event support
 *
 * Version: 0.1
 * Revision: A
 *
 * Brian B. Maranville
 * No copyright on this plugin.
 * Based almost entirely on code from:
 * http://vetruvet.blogspot.com/2010/12/converting-single-touch-events-to-mouse.html
 *
 * jqPlot is currently available for use in all personal or commercial projects 
 * under both the MIT (http://www.opensource.org/licenses/mit-license.php) and GPL 
 * version 2.0 (http://www.gnu.org/licenses/gpl-2.0.html) licenses. This means that you can 
 * choose the license that best suits your project and use it accordingly. 
 *
 * Although not required, the author would appreciate an email letting him 
 * know of any substantial use of jqPlot.  You can reach the author at: 
 * chris at jqplot dot com or see http://www.jqplot.com/info.php .
 *
 * If you are feeling kind and generous, consider supporting the project by
 * making a donation at: http://www.jqplot.com/donate.php .
 *
 */
(function($) {
    var touchToMouse = function(event) {
        //if (event.touches.length > 1) return; //allow default multi-touch gestures to work
        var touch = event.changedTouches[0];
        touch.data = event.data;
        var type = "";
        
        switch (event.type) {
        case "touchstart": 
            type = "mousedown"; break;
        case "touchmove":  
            event.preventDefault();   
            type="mousemove";   break;
        case "touchend":
            type="mouseup";     break;
        default: 
            return;
        }
        
        // https://developer.mozilla.org/en/DOM/event.initMouseEvent for API
        var simulatedEvent = document.createEvent("MouseEvent");
        simulatedEvent.initMouseEvent(type, true, true, window, 1, 
                touch.screenX, touch.screenY, 
                touch.clientX, touch.clientY, false, 
                false, false, false, 0, null);
        
        touch.target.dispatchEvent(simulatedEvent);
        //event.preventDefault();
    };
    //element.ontouchstart = touchToMouse;
    //element.ontouchmove = touchToMouse;
    //element.ontouchend = touchToMouse;
    
    function postDraw() {
        this.eventCanvas._ctx.canvas.ontouchstart = touchToMouse;
        this.eventCanvas._ctx.canvas.ontouchmove = touchToMouse;
        this.eventCanvas._ctx.canvas.ontouchend = touchToMouse;
    }
    $.jqplot.postDrawHooks.push(postDraw);
})(jQuery);
